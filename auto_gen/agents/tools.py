import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools


async def main() -> None:
    # Get the fetch tool from mcp-server-fetch.
    fetch_mcp_server = StdioServerParams(command="uvx", args=["mcp-server-fetch"])
    tools = await mcp_server_tools(fetch_mcp_server)

    # Create an agent that can use the fetch tool.
    model_client = OpenAIChatCompletionClient(model="gpt-4o")
    agent = AssistantAgent(name="fetcher", model_client=model_client, tools=tools, reflect_on_tool_use=True)  # type: ignore

    # Let the agent fetch the content of a URL and summarize it.
    result = await agent.run(task="Summarize the content of https://en.wikipedia.org/wiki/Seattle")
    print(result.messages[-1].content)


asyncio.run(main())