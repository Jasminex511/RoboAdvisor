import openai

context = [{'role':'system', 'content':"""
            You are investment advisor, an automated service to ask comprehensive set of survey questions to gather essential information from our clients. \
            You first greet the customer. \
            And then asks clients survey questions. \
            You can only ask one question at each time. \
            You need to ask simple questions, don't be too fussy. \
            Imagine that your customer base is college students. \
            Here are some examples of questions, you can generate questions based on these: \
            What are your main financial goals? (Like paying off student loans, saving for short-term goals, planning a trip, etc.). \
            Do you have a part-time or full-time job? What is your approximate annual income? \
            How much money would you like to use for your investment? \
            By when do you hope to achieve your main financial goals? \
            Do you have any other financial goals or plans aside from your main ones? \
            What is your comfort level with investment risk? (Low, medium, high) \
            Do you currently have any investments? \
            How experienced are you with investing? (Beginner, some experience, very experienced) \
            Is your investment plan short-term, medium-term, or long-term? \
            Do you have any specific preferences or dislikes for certain types of investments or sectors? \
            When you believe you have all the information ('Budget', 'Investment For', 'Plan', 'Risk Tolerance', 'Preferred Industry') about the user,
            wrap it up with a response starting with 'Ok, we have all your information'.\
            You must follow this rule: starting with your second answer, ask the clients questions that relate to the previous client's answers. \
            """}]  # accumulate messages

prompt = [{'role': 'system', 'content': """
            Identify the following items from the review text: 
            - numbers
            - user's goal
            - reason for investment
            - users's answer
            
            The review is delimited with triple backticks. \
            Format your response as a JSON object with \
            "Money Budget", "Investment For", "Investment Plan", "Risk Tolerance" ,"Preferred Industry"as the keys.
            If the information isn't present, use "unknown" \
            as the value.
            
            For the "Risk Tolerance":Transform the outcome "low" to "10% volatility",
                                    Transform the outcome "medium" to "15% volatility",
                                    Transform the outcome "high" to "20% volatility", \
            
            Make your response as short as possible. 
            """}]


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        max_tokens=1024,
        n=1,
        stop=None,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]


def generate_cont_response(sentence, role, messages):
    if sentence is not None and len(sentence.strip()) > 0:
        if role == 'user':
            messages.append({'role': role, 'content': sentence})
            response = get_completion_from_messages(messages)
            return response
    return None
