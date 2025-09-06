"""Example AutoGen agent with Docker code execution."""

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import CancellationToken
import asyncio

def create_docker_agent():
    """Create an AutoGen agent with Docker code execution capabilities."""
    model_client = OpenAIChatCompletionClient(model="gpt-4o")
    
    agent = AssistantAgent(
        name="docker_agent",
        system_message="You are a helpful assistant that can execute code in a Docker environment.",
        model_client=model_client
    )
    
    return agent

async def main():
    """Example usage of the Docker agent."""
    agent = create_docker_agent()
    
    # Example interaction
    task = "Write a Python script to analyze data using pandas and matplotlib"
    
    async for response in agent.run_stream(task=task, cancellation_token=CancellationToken()):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
