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

def chat(messages, query_count, query_limit):
    remaining = query_limit - query_count
    system_prompt = f"You are a helpful chatbot. Current conversation: Query {query_count} of {query_limit} (You have {remaining} {'query' if remaining == 1 else 'queries'} left)."

    if remaining <= 0:
        system_prompt += " This is the last query. After answering this, say goodbye with a friendly farewell message starting with [END_CONVERSATION]"

    message = client.messages.create(
        model=model,
        max_tokens=500,
        system=system_prompt,
        messages= messages
    )
    return message.content[0].text

# declare an message list to maintain conversation history
messages = []

query_count = 0
query_limit = 5
while True:
    query_count +=1
    # Take User Input
    user_input = input("Tell me your Query: ")
    add_user_messege(messages, user_input) # this is basically history logging

    # AI Call
    ai_response = chat(messages, query_count, query_limit)

    # Append AI Response in message history
    add_assistant_messege(messages, ai_response)
    print(ai_response)

    # Check if AI detected end of conversation
    if "[END_CONVERSATION]" in ai_response or query_count > query_limit:
        break