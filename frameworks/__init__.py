from core.registry import register_agent

from .echo.agent import EchoAgent
from .openai_sdk.agent import OpenAISDKAgent

register_agent("echo", lambda: EchoAgent(prefix="Echo: "))
register_agent("openai_sdk", OpenAISDKAgent)
