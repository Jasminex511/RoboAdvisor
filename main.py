import openai
import streamlit as st
from streamlit_chat import message
import os
from dotenv import load_dotenv

openai.api_key = 'yourAPIkey'


def generate_response(prompt):
    completion=openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.6,
    )
    message=completion.choices[0].text
    return message


# Function to initialize session state
def initialize_session_state():
    if not hasattr(st.session_state, 'generated'):
        st.session_state.generated = []
    if not hasattr(st.session_state, 'past'):
        st.session_state.past = []


# Initialize session state
initialize_session_state()

st.title("AI Chatbot")

user_input = st.text_input("You:", key='input')

if user_input:
    output = generate_response(user_input)

    # Store the output and user input in session state
    st.session_state.generated.append(output)
    st.session_state.past.append(user_input)

if hasattr(st.session_state, 'generated') and st.session_state.generated:
    for i in range(len(st.session_state.generated) - 1, -1, -1):
        st.write(st.session_state.generated[i])
        st.write(st.session_state.past[i])