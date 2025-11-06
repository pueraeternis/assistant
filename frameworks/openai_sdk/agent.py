from typing import Any, Dict, List, Optional, cast

from openai import APIError, AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from config.settings import settings
from core.base_agent import BaseAgent
from core.logging import get_logger
from core.memory import BaseMemory

logger = get_logger(__name__)


class OpenAISDKAgent(BaseAgent):
    """
    Agent implemented using the standard asynchronous OpenAI SDK
    and conforming to the BaseAgent interface.
    """

    def __init__(self, memory: BaseMemory):

        # Use AsyncOpenAI for async calls
        self.client = AsyncOpenAI(
            base_url=settings.OPENAI_API_URL,
            api_key=settings.OPENAI_API_KEY,
        )
        self.memory = memory
        self.model: str = settings.LLM_MODEL_NAME
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.system_prompt = settings.SYSTEM_PROMPT
        logger.info("🤖 OpenAISDKAgent initialized for model: %s", self.model)

    async def chat(self, message: str, dialog_id: Optional[str] = None) -> str:
        """
        Sends a request to the LLM and returns the response asynchronously.
        """
        if not dialog_id:
            dialog_id = "default"

        logger.info("OpenAISDKAgent.chat called for dialog_id=%s with message: '%s'", dialog_id, message)
        history = await self.memory.get_history(dialog_id)
        messages_for_llm: List[Dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt},
            *history,
            {"role": "user", "content": message},
        ]
        try:
            logger.debug("🧠 Calling LLM...")

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=cast(List[ChatCompletionMessageParam], messages_for_llm),
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            content = response.choices[0].message.content
            if content is None:
                logger.warning("Received no content from LLM for dialog_id=%s", dialog_id)
                return "Error: Received no content from LLM."

            content = content.strip()

            await self.memory.append(dialog_id, "user", message)
            await self.memory.append(dialog_id, "assistant", content)

            return content

        except APIError as e:
            # Handle OpenAI API errors (connection, authentication, rate limits, etc.)
            logger.error("OpenAI API error during LLM call for dialog_id=%s: %s", dialog_id, e)
            return f"An error occurred: {e}"
