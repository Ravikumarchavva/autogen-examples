from logger import trace_logger, event_logger
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main() -> None:
    model_client = OpenAIChatCompletionClient(model="gpt-4o")
    agent = AssistantAgent("assistant", model_client=model_client)
    trace_logger.info(await agent.run(task="Say 'Hello World!'"))
    event_logger.info("Agent has completed the task.")
    await model_client.close()

asyncio.run(main())
