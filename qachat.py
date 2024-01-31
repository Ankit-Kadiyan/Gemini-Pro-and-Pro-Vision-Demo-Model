from dotenv import load_dotenv
load_dotenv()   # Loading environment variables
import streamlit as st
import os
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to start Gemini chat
def start_gemini_chat():
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])
    return chat

# Function to get Gemini response
def get_gemini_response(chat, question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Chat Demo")
st.header("Gemini Chat Application")

# Initialize session state for chat history if it doesn't exist
if 'chat' not in st.session_state:
    st.session_state['chat'] = start_gemini_chat()

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input for user question
input_text = st.text_input("Input: ", key="input")

# Button to submit the question
submit = st.button("Ask the Question")

# If the user submits a question
if submit and input_text:
    # Get Gemini response
    response = get_gemini_response(st.session_state['chat'], input_text)

    # Display response
    st.subheader("The Response is")
    bot_response = ""
    for chunk in response:
        bot_response += chunk.text + " "
    
    st.write(bot_response)
    
    # Add user query and response to session chat history
    st.session_state["chat_history"].append(("You", input_text))
    st.session_state["chat_history"].append(("Bot", bot_response))

# Display chat history
st.subheader("Chat History is")
for role, text in st.session_state["chat_history"]:
    st.write(f"{role}: {text}")
