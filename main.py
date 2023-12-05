import openai
import streamlit as st
import pandas as pd
import os
import json
import time
from PIL import Image
import openpyxl
from openai.error import RateLimitError
from init import initialize_session_state
from prompt import generate_cont_response, get_completion_from_messages, context, prompt, result_prompt

openai.api_key = "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"


def chatbot_app():

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
                        st.write(output)
                        print("conversation end")
                    else:
                        context.append({'role': 'assistant', 'content': output})
                        st.session_state.generated.append(output)
                        st.session_state.past.append(user_input)
                    break
            except RateLimitError:
                # wait 20s and try again
                print("rate limit reached")
                time.sleep(20)
                retries += 1
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break
        if retries >= max_retries:
            st.error("Failed to get a response after several attempts. Please try again later.")

    # when all questions are asked, transform chat-history to structured input
    if st.session_state.completed:
        prompt[0]['content'] += "Review text: " + " ".join([f"{c['role']}: {c['content']}" for c in context[1:]])

        while True:
            try:
                response = get_completion_from_messages(prompt)
                break
            except RateLimitError:
                print("rate limit reached")
                time.sleep(20)

        # convert response into a xlsx file
        dict_data = json.loads(response)
        dict_data_list = {i: [dict_data[i].lower()] for i in dict_data.keys()}
        df = pd.DataFrame.from_dict(dict_data_list)
        df.to_excel("user_information.xlsx", index=False)
        print("input ready")

        while True:
            if os.path.exists("OUTPUT_1_bestStrategyMetrics.csv") and os.path.exists("OUTPUT_3_weightsTable.csv"):
                df_best = pd.read_csv("OUTPUT_1_bestStrategyMetrics.csv")
                print("output 1 read")
                image_strategy_plot = Image.open("OUTPUT_2_StrategyPlot.png")
                print("output 2 read")
                df_weight = pd.read_csv("OUTPUT_3_weightsTable.csv")
                print("output 3 read")
                image_asset_plot = Image.open("OUTPUT_4_assetAreaPlot.png")
                print("output 4 read")
                break
            else:
                print("files not generated yet")
                time.sleep(20)

        results = {"return": {}, "weights": {}}
        for i, row in df_best.iterrows():
            results["return"][row[0]] = row[1]
        for i, row in df_weight.iterrows():
            etf = row[2]
            weights = row[3]
            results["weights"][etf] = weights
        print(results)

        result_prompt[0]['content'] += "Review text: " + json.dumps(results)

        while True:
            try:
                response_result = get_completion_from_messages(result_prompt)
                break
            except RateLimitError:
                print("rate limit reached")
                time.sleep(20)

        print(response_result)
        st.write(response_result)
        st.image(image_strategy_plot, caption='Strategy')
        st.image(image_asset_plot, caption='Asset Area')

        os.remove("user_information.xlsx")
        for f in os.listdir():
            if f.startswith("OUTPUT"):
                os.remove(f)

    if hasattr(st.session_state, 'generated') and st.session_state.generated:
        for i in range(len(st.session_state.generated) - 1, -1, -1):
            st.write(st.session_state.generated[i])
            st.write(st.session_state.past[i])


if __name__ == "__main__":
    initialize_session_state()
    chatbot_app()

