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

openai.api_key = "YOUR-API-KEY"


def chatbot_app():
    st.title("AI Chatbot")
    user_input = st.text_input("You:")

    # placeholder for the final responses
    result_placeholder = st.empty()
    image1_placeholder = st.empty()
    image2_placeholder = st.empty()

    if user_input and not st.session_state.completed:
        while True:
            try:
                # call llm with the first prompt
                output = generate_cont_response(user_input, 'user', context)
                if output:
                    # gpt will use this sentence as part of the output when all questions are asked
                    if "Thank you for providing all the necessary information." in output:
                        st.session_state.completed = True
                        print("conversation end")
                    # appending the chat to keep track of what has been asked
                    context.append({'role': 'assistant', 'content': output})
                    st.session_state.generated.append(output)
                    st.session_state.past.append(user_input)
                    break
            except RateLimitError:
                # wait 20s and try again
                print("rate limit reached")
                time.sleep(20)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break

    # show the chat history which reads from the bottom to the top
    if hasattr(st.session_state, 'generated') and st.session_state.generated:
        for i in range(len(st.session_state.generated) - 1, -1, -1):
            st.write(st.session_state.generated[i])
            st.write(st.session_state.past[i])

    # when all questions are asked, transform chat-history to structured input
    if st.session_state.completed:
        # appending the chat history to the second prompt for the llm to review
        prompt[0]['content'] += "Review text: " + " ".join([f"{c['role']}: {c['content']}" for c in context[1:]])

        while True:
            try:
                # call llm with the second prompt
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
            # wait for the MATLAB script to run, output 4 is the last one to be generated, when it is ready read all outputs
            if os.path.exists("OUTPUT_4_assetAreaPlot.png"):
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
                # if the files are not generated yet, wait for 20s and try again
                print("files not generated yet")
                time.sleep(20)

        # transform the csv files to dictionary
        results = {"return": {}, "weights": {}}
        for i, row in df_best.iterrows():
            results["return"][row[0]] = row[1]
        for i, row in df_weight.iterrows():
            etf = row[2]
            weights = row[3]
            results["weights"][etf] = weights
        print(results)

        # convert the results to JSON and append it to the third prompt for llm to review
        result_prompt[0]['content'] += "Review text: " + json.dumps(results)

        while True:
            try:
                # call the llm with the third prompt
                response_result = get_completion_from_messages(result_prompt)
                break
            except RateLimitError:
                print("rate limit reached")
                time.sleep(20)

        # add the final results to the placeholder saved before, show the final responses and the images
        print(response_result)
        result_placeholder.write(response_result)
        image1_placeholder.image(image_strategy_plot, caption='Strategy')
        image2_placeholder.image(image_asset_plot, caption='Asset Area')

        # remove all outputs
        os.remove("user_information.xlsx")
        for f in os.listdir():
            if f.startswith("OUTPUT"):
                os.remove(f)


if __name__ == "__main__":
    initialize_session_state()
    chatbot_app()
