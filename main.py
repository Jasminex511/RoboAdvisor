import openai
import streamlit as st
import pandas as pd
import json
import time
import openpyxl
from openai.error import RateLimitError
from init import initialize_session_state
from prompt import generate_cont_response, get_completion_from_messages, context, prompt

openai.api_key = "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"


def chatbot_app():

    initialize_session_state()

    st.title("AI Chatbot")

    user_input = st.text_input("You:")

    if user_input and not st.session_state.completed:
        retries = 0
        max_retries = 60
        while retries < max_retries:
            try:
                output = generate_cont_response(user_input, 'user', context)
                if output:
                    # gpt will use this sentence as part of the output when all questions are asked.
                    if "Thank you for providing all the necessary information." in output:
                        st.session_state.completed = True
                    context.append({'role': 'assistant', 'content': output})
                    st.session_state.generated.append(output)
                    st.session_state.past.append(user_input)
                    break
            except RateLimitError:
                # wait 20s and try again
                time.sleep(20)
                retries += 1
        if retries >= max_retries:
            st.error("Failed to get a response after several attempts. Please try again later.")

    # when all questions are asked, transform chat-history to structured input
    if st.session_state.completed:
        prompt[0]['content'] += "Review text: " + " ".join([f"{c['role']}: {c['content']}" for c in context[1:]])
        response = get_completion_from_messages(prompt)

        # convert response into a xlsx file
        dict_data = json.loads(response)
        dict_data_list = {i: [dict_data[i]] for i in dict_data.keys()}
        df = pd.DataFrame.from_dict(dict_data_list)
        df.to_excel("user_information.xlsx", index=False)

    if hasattr(st.session_state, 'generated') and st.session_state.generated:
        for i in range(len(st.session_state.generated) - 1, -1, -1):
            st.write(st.session_state.generated[i])
            st.write(st.session_state.past[i])


if __name__ == "__main__":
    chatbot_app()
