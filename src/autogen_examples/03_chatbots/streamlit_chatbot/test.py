import streamlit as st
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from dotenv import load_dotenv
load_dotenv()
import asyncio
import nest_asyncio
nest_asyncio.apply()

model_client = OpenAIChatCompletionClient(model="gpt-4o")

@st.cache_resource
def get_assistant_agent():
    return AssistantAgent(name="assistant", 
                          system_message="You are a helpful assistant.", 
                          model_client=model_client)

assistant_agent = get_assistant_agent()

# Streamlit app
st.title("AutoGen Assistant Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history (do not include current turn)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter your message:"):
    # Display user message in chat message container (not in history yet)
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        placeholder = st.empty()
        async def stream_and_accumulate():
            full_response = ""
            async for response in assistant_agent.run_stream(task=prompt, cancellation_token=CancellationToken()):
                if isinstance(response, TextMessage) and response.content:
                    full_response += response.content
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            return full_response
        response = asyncio.run(stream_and_accumulate())

    # After streaming, append both user and assistant messages to chat history, then rerun to show updated history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()