import asyncio
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage, ModelClientStreamingChunkEvent
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

# Load environment variables
load_dotenv()

# Initialize Rich Console
console = Console()

def get_assistant_agent():
    """Initializes and returns the assistant agent."""
    # Note: Caching is not used here as it is a Streamlit feature.
    # A new agent will be created for each session.
    return AssistantAgent(
        name="assistant",
        system_message="You are a helpful assistant.",
        model_client=OpenAIChatCompletionClient(model="gpt-4o"),
        model_client_stream=True
    )

async def main():
    """Main function to run the terminal-based chat application."""
    console.print("[bold green]AutoGen Terminal Chat[/bold green]")
    console.print("Type 'exit' or 'quit' to end the conversation.")
    
    assistant_agent = get_assistant_agent()
    
    while True:
        prompt = Prompt.ask("[bold yellow]You[/bold yellow]")
        
        if prompt.lower() in ["exit", "quit"]:
            console.print("[bold red]Ending chat session.[/bold red]")
            break
            
        console.print(f"[bold blue]Assistant:[/bold blue] ", end="")
        
        try:
            # Stream the response from the agent
            async for response in assistant_agent.run_stream(task=prompt, cancellation_token=CancellationToken()):
                if isinstance(response, ModelClientStreamingChunkEvent) and response.content:
                    # Print each chunk of the response as it arrives
                    console.print(response.content, end="")
            
            # Print a newline after the full response is received
            console.print()

        except Exception as e:
            console.print(f"\n[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red]Chat terminated by user.[/bold red]")
