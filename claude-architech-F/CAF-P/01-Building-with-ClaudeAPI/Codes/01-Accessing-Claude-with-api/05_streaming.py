from anthropic import Anthropic
import dotenv

# Load env variables, Setup Client and declare Model
dotenv.load_dotenv()
client = Anthropic()
model = "claude-haiku-4-5-20251001"

# Helper Functions
def add_user_messege(messages, text):
    user_messege = {"role": "user", "content": text}
    messages.append(user_messege)

def add_assistant_messege(messages, text):
    assistant_messege = {"role": "assistant", "content": text}
    messages.append(assistant_messege)

# declare an message list to maintain conversation history
messages = []
add_user_messege(messages, "Write one sentence description of fake databases")

# # Way 1 to stream but not very much helpful or reliable
# stream = client.messages.create(
#     model=model,
#     max_tokens=500,
#     messages=messages,
#     stream=True
# )

# for event in stream:
#     print(event)

# Way 2 to stream using anthropic sdk
with client.messages.stream(
    model = model,
    max_tokens=500,
    messages=messages
) as stream:
    for text in stream.text_stream:
        print(text, end="")

# if you want to store it inside any database
# stream.get_final_message()