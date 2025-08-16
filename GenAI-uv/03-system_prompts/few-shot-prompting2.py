from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() # Activated environment and load the API Key Stored from there

client = OpenAI() # Setup client using API Key

# Few-shot Prompting: The model is provided with a few examples before asking it to generate a response.

SYSTEM_PROMPT = """
    You are an AI expert in Coding. You only know Python and nothing else.
    You help users in solving there python doubts only and nothing else.
    If user tried to ask something else apart from Python you can just roast them.

    Examples:
    User: How to make a Tea?
    Assistant: please ask a chef i don't know.

    Examples:
    User: How to write a function in python
    Assistant: def fn_name(x: int) -> int:
                    pass # Logic of the function
"""
user_query = input("Please ask your query ! : \n")
response = client.chat.completions.create(
    model="gpt-4.1-mini", # Which Model you want to use
    # Chat ML prompt format in messege list to build context for AI
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hey, My name is Neesh"},
        { "role": "assistant", "content": "Hey Neesh! If you have any Python questions or need help with code, feel free to ask!"},
        { "role": "user", "content": "Why 75 attendence is imp for colleges?"},
        {"role": "assistant", "content": "Because it is atleast required to learn the concepts right way"},
        {"role": "user", "content": user_query}
       
    ]
)

print(response.choices[0].message.content)