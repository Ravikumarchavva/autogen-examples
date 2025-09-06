from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models._model_client import ModelFamily, ModelInfo
from autogen_agentchat.messages import TextMessage

import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

model_info = ModelInfo(
    vision=False,
    function_calling=False,
    json_output=False,
    family=ModelFamily.GEMINI_2_0_FLASH,
    structured_output=True,
)
agent = AssistantAgent(
    name="assistant",
    model_client=OpenAIChatCompletionClient(
        model="gemini-2.5-flash",
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        model_info=model_info,
    ),
    description="A Gemini-powered assistant agent for various tasks.",
    system_message="You are a helpful assistant powered by Gemini. Reply with TERMINATE when you are done.",
    memory=None,
    handoffs=None,
    tools=None,
)

async def main():
    print("Starting the Gemini-powered assistant agent...")
    result = await agent.run(task="What is the capital of France?")
    output_message = result.messages[-1]
    if isinstance(output_message, TextMessage):
        print("\033[1mAssistant's response:\033[0m", output_message.content.split("\n")[0])
    else:
        print("Assistant's response is not a text message.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

