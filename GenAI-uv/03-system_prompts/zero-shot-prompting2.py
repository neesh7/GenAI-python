# flake8: noqa

from dotenv import load_dotenv
from openai import OpenAI
# from langfuse.openai import OpenAI

load_dotenv() # Activates and loads the environment so the api key is available to the client

client = OpenAI() #Initializes the OpenAI client using your environment’s API key

# Zero-shot Prompting: The model is given a direct question or task

SYSTEM_PROMPT = """
    You are an AI expert in Astrology.
    You help users in by telling them their probable future by checking their horscope with today's day.
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    # In OpenAI’s Chat API, the messages list is a conversation history. Each message has a role.
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey, My name is Neesh and you are Poo !"},
        {"role": "assistant", "content": "Hey Neesh! Thanks for the nice name what's you horscope!"},
        {"role": "user", "content": "I am Superman"},
        {"role": "assistant", "content": "Hey Neesh, Stop Joking i asked for horscope"},
        {"role": "user", "content": "My horscope is saggitarius"},
    ]
)

# why not send a single prompt instead of messege list ?
# Because context matters. The model doesn’t have memory between API calls, so you have to rebuild the conversation every time. This multi-turn setup lets you:

# Simulate a natural dialogue

# Control tone and behavior

# Test how the model handles off-topic questions

# Guide the model toward a specific kind of response
print(response.choices[0].message.content)