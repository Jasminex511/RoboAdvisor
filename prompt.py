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
            Do you want to have any savings or funds for emergency? How much? \
            What is your comfort level with investment risk? (very low,low, medium, high,very high) \
            What is your expected rate of return for your investments? \
            Which kind of investment period you are looking for?(1-3 years,3-5 years, over 5 years) \
            Is your investment plan short-term, medium-term, or long-term? \
            Which of the following industries and markets do you have a preference for, such as :Healthcare, Finance, Real Estate, Consumer Discretionary, Consumer Staples, 
            Energy, Industrials, Materials, Communication Services, Utilities, International Markets, Emerging Markets, ESG, AI & Technology, Biotech.
            And what is the preference level for that interest? You can answer: not interested, a little interested, moderately interested, very interested, extremely interested. \
            When you believe you asked all the questions you need, wrap it up with a response starting with 'Thank you for providing all the necessary information.'.\
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
            "Money Budget", "Investment For", "Investment Plan", 
            "Risk Tolerance" ,"Investment Period" , "Preferred Industry" , "Industry Preference" ,"Emergency Money", "Expected Return" as the keys.\
            If the information isn't present, use "unknown" as the value.\
            
            For the "Risk Tolerance":Transform the outcome "very low" to "5% volatility",
                                     Transform the outcome "low" to "10% volatility",
                                     Transform the outcome "medium" to "15% volatility",
                                     Transform the outcome "high" to "20% volatility",
                                     Transform the outcome "very high" to "25% volatility",\
            
            For the "Investment Period":  Transform the outcome "1-3 years" to "1-3 years with Volatility Adjustment Factor is 0.7",
                                          Transform the outcome "3-5 years" to "3-5 years with Volatility Adjustment Factor is 1.0",
                                          Transform the outcome "over 5 years" to "over 5 years with Volatility Adjustment Factor is 1.3",\
            
            For the "Industry Preference": Transform the outcome "not interested" to "0% weight",
                                           Transform the outcome "a little interested" to "1%-10% weight",
                                           Transform the outcome "moderately interested" to "11%-30% weight",
                                           Transform the outcome "very interested" to "31%-50% weight",
                                           Transform the outcome "extremely interested" to "51%-100% weight",\
            
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
