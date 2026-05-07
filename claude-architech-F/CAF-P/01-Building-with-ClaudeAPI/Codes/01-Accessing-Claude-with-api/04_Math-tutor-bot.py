from anthropic import Anthropic
import dotenv

# Load the env
dotenv.load_dotenv()

# Setup the Client
client = Anthropic()
model = "claude-haiku-4-5-20251001"
# Helper Functions
def add_user_messege(messages, text):
    user_messege = {"role": "user", "content": text}
    messages.append(user_messege)

def add_assistant_messege(messages, text):
    assistant_messege = {"role": "assistant", "content": text}
    messages.append(assistant_messege)

def chat(messages, system_prompt=None, temperature=0.5):
    # Note temp close to 0 is deterministic and close to 1 is creative use case
    params = {
        "model": model,
        "max_tokens": 500,
        "messages": messages,
        "temperature": temperature
    }
    if system_prompt:
        params["system"] = system_prompt

    message = client.messages.create(**params)
    return message.content[0].text

# declare an message list to maintain conversation history
messages = []

system = """you are a helpful and calm math tutor.
            Do not directly answer the students instead guide them step by step
"""

# Take User Input
user_input = input("Tell me your Query: ")
add_user_messege(messages, user_input) # this is basically history logging

# AI Call
# ai_response = chat(messages)
# ai_response = chat(messages, system)
ai_response = chat(messages, system, temperature=1.0)

# Append AI Response in message history
add_assistant_messege(messages, ai_response)
print(ai_response)
