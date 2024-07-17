import streamlit as st
import vertexai
from google.cloud import aiplatform as vertexai
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig, ChatSession, Content, Part

# Set up your Google Cloud project
project = "gemini-explorer-429518"
vertexai.init(project=project)

config = GenerationConfig(
    temperature=0.4
)
model = GenerativeModel(
    "gemini-pro",
    generation_config=config
)
chat = model.start_chat()

# Define the initial message function
def initial_message_function(chat: ChatSession):
    initial_message = "Hello! How can I assist you today?"
    response = chat.send_message(initial_message)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )

def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text
    
    with st.chat_message("model"):
        st.markdown(output)
    
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )
    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )

    # Update the chat history with the user and model messages
    user_content = Content(role="user", parts=[Part.from_text(query)])
    model_content = Content(role="model", parts=[Part.from_text(output)])
    chat.history.append(user_content)
    chat.history.append(model_content)

# Set Up Streamlit Interface
st.title("Gemini Explorer")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display and Load Chat History
for index, message in enumerate(st.session_state.messages):
    content = Content(
        role=message["role"],
        parts=[Part.from_text(message["content"])]
    )
    if index != 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    chat.history.append(content)

# For initial message startup
if len(st.session_state.messages) == 0:
    # Invoke initial message
    initial_prompt = "Introduce yourself as Rex, a virtual assistant. You use emojis to be interactive"
    llm_function(chat, initial_prompt) 

# Capture and Process User Query
query = st.chat_input("Gemini Explorer")
if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)

