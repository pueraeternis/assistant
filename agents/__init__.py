# agents/__init__.py

from typing import List, Optional

from config.settings import settings
from core.base_agent import BaseAgent
from core.base_tool import BaseTool
from core.memory import RedisMemory
from core.registry import register_agent

from .echo.agent import EchoAgent
from .openai.agent import OpenAIAgent


def openai_factory(
    tools: Optional[List[BaseTool]] = None,
    system_prompt: Optional[str] = None,
) -> OpenAIAgent:
    """Factory for creating OpenAIAgent with custom tools and system prompt."""
    memory = RedisMemory(redis_url=settings.REDIS_URL)
    agent_instance = OpenAIAgent(memory=memory, tools=tools)
    if system_prompt:
        agent_instance.system_prompt = system_prompt

    return agent_instance


# Simple agent for test
register_agent("echo", lambda: EchoAgent(prefix="Echo: "))


def assistant_factory(**kwargs) -> BaseAgent:
    """Factory for creating a fully featured OpenAI agent with optional tools."""
    return openai_factory(tools=kwargs.get("tools"))


register_agent("assistant", assistant_factory)


def researcher_factory(**kwargs) -> BaseAgent:
    """Factory for creating a researcher agent that uses only internet search tools."""
    researcher_prompt = """You are a specialized researcher agent. Your ONLY function is to find information on the internet.

    Follow this algorithm strictly:
    1.  When you receive a user query, your FIRST and ONLY initial action MUST BE to use the "InternetSearch" tool. Do not answer from your internal knowledge.
    2.  Analyze the search results. If the snippets provide enough information, formulate the final answer based ONLY on them.
    3.  If the snippets are insufficient but contain promising URLs, your NEXT action MUST BE to use the "BrowseWebpage" tool on the most relevant URL.
    4.  Formulate the final answer based ONLY on the information you have gathered from the tools.
    5.  You are FORBIDDEN from answering from memory. If you cannot find an answer using your tools, you must state that you were unable to find the information.

    **To use a tool, you MUST respond in the following JSON format inside <tool_call> tags:**
    <tool_call>
    {
    "tool_name": "NameOfTheTool",
    "arg_name": "value"
    }
    </tool_call>
    """

    # Filter tools, keeping only those relevant for this role
    available_tools = kwargs.get("tools", [])
    researcher_tools = [t for t in available_tools if t.name in ("InternetSearch", "BrowseWebpage")]
    return openai_factory(tools=researcher_tools, system_prompt=researcher_prompt)


register_agent("researcher", researcher_factory)
