import openai
import streamlit as st
from prompt import generate_cont_response, get_completion_from_messages, context, prompt

openai.api_key = "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"


# Function to initialize session state
def initialize_session_state():
    if not hasattr(st.session_state, 'generated'):
        st.session_state.generated = []
    if not hasattr(st.session_state, 'past'):
        st.session_state.past = []
    if not hasattr(st.session_state, 'completed'):
        st.session_state.completed = False


# Initialize session state
def chatbot_app():
    # Initialize session state
    initialize_session_state()

    st.title("AI Chatbot")

    user_input = st.text_input("You:")

    if user_input and not st.session_state.completed:
        output = generate_cont_response(user_input, 'user', context)
        if output:
            context.append({'role': 'assistant', 'content': output})
            # Store the output and user input in session state
            st.session_state.generated.append(output)
            st.session_state.past.append(user_input)
        if output.startswith("Ok, we have all your information"):
            st.session_state.completed = True

    if st.session_state.completed:
        prompt[0]['content'] += "Review text: " + "\\".join([f"{c['role']}: {c['content']}" for c in context[1:]])
        print(prompt)

        response = get_completion_from_messages(prompt)
        print(response)

        #result = optimization_model(response, ...other inputs?)

    if hasattr(st.session_state, 'generated') and st.session_state.generated:
        for i in range(len(st.session_state.generated) - 1, -1, -1):
            st.write(st.session_state.generated[i])
            st.write(st.session_state.past[i])


if __name__ == "__main__":
    chatbot_app()
