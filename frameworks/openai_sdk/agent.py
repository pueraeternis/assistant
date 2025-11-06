from typing import Optional

from openai import APIError, AsyncOpenAI

from config.settings import settings
from core.base_agent import BaseAgent
from core.logging import get_logger

logger = get_logger(__name__)


class OpenAISDKAgent(BaseAgent):
    """
    Agent implemented using the standard asynchronous OpenAI SDK
    and conforming to the BaseAgent interface.
    """

    def __init__(self):
        # Validate required settings
        if not settings.OPENAI_API_URL:
            raise ValueError("OPENAI_API_URL must be set in settings")
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set in settings")
        if not settings.LLM_MODEL_NAME:
            raise ValueError("LLM_MODEL_NAME must be set in settings")

        # Type narrowing: after validation, these are guaranteed to be str
        assert settings.OPENAI_API_URL is not None
        assert settings.OPENAI_API_KEY is not None
        assert settings.LLM_MODEL_NAME is not None

        # Use AsyncOpenAI for async calls
        self.client = AsyncOpenAI(
            base_url=settings.OPENAI_API_URL,
            api_key=settings.OPENAI_API_KEY,
        )
        self.model: str = settings.LLM_MODEL_NAME
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.system_prompt = settings.SYSTEM_PROMPT
        logger.info("🤖 OpenAISDKAgent initialized for model: %s", self.model)

    async def chat(self, message: str, dialog_id: Optional[str] = None) -> str:
        """
        Sends a request to the LLM and returns the response asynchronously.
        """
        logger.info("OpenAISDKAgent.chat called for dialog_id=%s with message: '%s'", dialog_id, message)
        try:
            logger.debug("🧠 Calling LLM...")
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": message},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            content = response.choices[0].message.content
            if content is None:
                logger.warning("Received no content from LLM for dialog_id=%s", dialog_id)
                return "Error: Received no content from LLM."

            return content.strip()

        except APIError as e:
            # Handle OpenAI API errors (connection, authentication, rate limits, etc.)
            logger.error("OpenAI API error during LLM call for dialog_id=%s: %s", dialog_id, e)
            return f"An error occurred: {e}"
