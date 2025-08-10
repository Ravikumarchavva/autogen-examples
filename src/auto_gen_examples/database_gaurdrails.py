import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
from autogen_agentchat.messages import TextMessage
from autogen_core.models import ModelFamily, ModelInfo
import os
from dotenv import load_dotenv
from logger import event_logger
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

model_info = ModelInfo(
    vision=False,
    function_calling=True,
    json_output=False,
    family=ModelFamily.GEMINI_2_5_FLASH,
    structured_output=False,
)

async def main() -> None:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
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
                        model="gemini-2.5-flash",
                api_key=GEMINI_API_KEY,
            model_info=model_info,
            max_tokens=4096,
            ),
            description="A Gemini-powered assistant agent for database tasks.",
            system_message="You are a helpful assistant powered by Gemini. Reply with TERMINATE when you are done.",
            memory=None,
            handoffs=None,
            workbench=workbench,
            reflect_on_tool_use=True,
            
        )

        print("Starting the Gemini-powered assistant agent...")
        result = await agent.run(
            task="Give me all customers in the bankl schema.",
        )
        event_logger.info("Agent has completed the task.")
        output_message = result.messages[-1]
        if not isinstance(output_message, TextMessage):
            raise TypeError("Expected the last message to be a TextMessage.")
        print(output_message.content)

if __name__ == "__main__":
    asyncio.run(main())
