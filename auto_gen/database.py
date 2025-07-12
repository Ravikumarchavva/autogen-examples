import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
from autogen_agentchat.messages import TextMessage
import os
from dotenv import load_dotenv
from logger import event_logger
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def main() -> None:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
    params = StdioServerParams(
        command="./toolbox",
        args=[
            "--stdio",
            "--tools-file",
            "tools.yaml"
        ],
        env={
            "DATABASE_URL": "postgresql://postgres:postgres@localhost:5432/postgres",
        },
        read_timeout_seconds= 60
    )
    async with McpWorkbench(server_params=params) as workbench:
        agent = AssistantAgent(
            name="assistant",
            model_client=OpenAIChatCompletionClient(
                model="gpt-4o",
                api_key=OPENAI_API_KEY,
            ),
            description="A GPT-powered assistant agent for database tasks.",
            system_message="You are a helpful assistant powered by GPT. Reply with TERMINATE when you are done.",
            memory=None,
            handoffs=None,
            workbench=workbench,
            reflect_on_tool_use=True,
        )

        print("Starting the GPT-powered assistant agent...")
        result = await agent.run(
            task="Give me the balance of all accounts for customer ID '1'.",
        )
        event_logger.info("Agent has completed the task.")
        output_message = result.messages[-1]
        if not isinstance(output_message, TextMessage):
            raise TypeError("Expected the last message to be a TextMessage.")
        print(output_message.content)

        result = await agent.run(
            task="Now tell me the phone number of this customer",
        )
        output_message = result.messages[-1]
        if not isinstance(output_message, TextMessage):
            raise TypeError("Expected the last message to be a TextMessage.")
        print(output_message.content)

if __name__ == "__main__":
    asyncio.run(main())
