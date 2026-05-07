from anthropic import Anthropic
import dotenv


# Load env variables
dotenv.load_dotenv()

# Create an API Client
client = Anthropic()
model= "claude-sonnet-4-6"

# Whatever conversation we do with AI No history is maintained anywhere so we need to maintain the history it's on us
# So after first api call whenever we make second API Call we will Send the full conversation history and by that way our context will grow.

def add_user_messege(messages, text):
    user_messege = {"role": "user", "content": text}
    messages.append(user_messege)

def add_assistant_messege(messages, text):
    assistant_messege = {"role": "assistant", "content": text}
    messages.append(assistant_messege)

# Create Function - Generates text by making a request to client/ Make a request

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=500,
        messages= messages
    )
    return message.content[0].text

# Make a Starting list of messages
messages = []

# Add in the initial user question of "Define quantum computing in one sentence"
add_user_messege(messages, "Hello I'm Neesh and i want you to Define quantum computing in one sentence")

# Pass the list of messages into 'chat' to get an answer - first call
answer = chat(messages)
print(answer)

# Take the answer and add it as an assistant messege into our list / history - saving response in conversation history
add_assistant_messege(messages, answer)

# Add in the user's follow-up question
add_user_messege(messages, "\nwrite another sentence on it and what is my name ?")

# Call chat again with the list of messages to get a final answer - second call
answer = chat(messages)
print(answer)