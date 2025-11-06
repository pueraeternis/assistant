import asyncio
import logging

import click

import frameworks  # noqa: F401 # pylint: disable=unused-import
from core.logging import get_logger, setup_logging
from core.memory import InMemoryMemory
from core.registry import AGENT_REGISTRY, get_agent

# configure logging
setup_logging()
logger = get_logger(__name__)

available_agents = list(AGENT_REGISTRY.keys())


@click.group()
def cli() -> None:
    """Assistant CLI entrypoint."""


@cli.command()
@click.option("--agent", default="openai_sdk", type=click.Choice(available_agents), help="Agent to use")
@click.option("--dialog-id", default="default", help="Dialog/session id")
def chat(agent: str, dialog_id: str) -> None:
    """Start interactive chat loop with the selected agent."""
    logging.getLogger().setLevel(logging.WARNING)
    asyncio.run(_chat_loop(agent_name=agent, dialog_id=dialog_id))


async def _chat_loop(agent_name: str, dialog_id: str) -> None:
    """Interactive loop. Type exit/quit to finish."""
    try:
        agent_obj = get_agent(agent_name)
    except KeyError as exc:
        logger.error("Agent not found: %s", exc)
        raise SystemExit(1) from exc

    memory = InMemoryMemory()
    print(f"Interactive chat with agent='{agent_name}', dialog_id='{dialog_id}'. Type 'exit' to quit.")

    while True:
        user_prompt = click.style("User> ", fg="blue", bold=True)
        user_text = input(user_prompt).strip()
        if not user_text:
            continue
        if user_text.lower() in {"exit", "quit"}:
            print("Bye!")
            break

        await memory.append(dialog_id, role="user", text=user_text)
        response = await agent_obj.chat(user_text, dialog_id=dialog_id)
        await memory.append(dialog_id, role="assistant", text=response)

        assistant_prompt = click.style("Assistant> ", fg="green", bold=True)
        print(f"{assistant_prompt}{response}")


if __name__ == "__main__":
    cli()
