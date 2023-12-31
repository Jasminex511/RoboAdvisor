import streamlit as st


# Function to initialize session state
def initialize_session_state():
    if not hasattr(st.session_state, 'generated'):
        st.session_state.generated = []
    if not hasattr(st.session_state, 'past'):
        st.session_state.past = []
    # when llm believes all questions are asked, this will be set to True
    if not hasattr(st.session_state, 'completed'):
        st.session_state.completed = False
