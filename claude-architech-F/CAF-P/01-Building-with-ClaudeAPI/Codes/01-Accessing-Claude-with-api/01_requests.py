from anthropic import Anthropic
import dotenv


# Load env variables
dotenv.load_dotenv()

# Create an API Client
client = Anthropic()
model= "claude-sonnet-4-6"

# Create Function - Generates text by making a request to client/ Make a request
message = client.messages.create(
    model=model,
    max_tokens=500,
    messages=[
        {
            "role": "user",
            "content": "what is quantam computing? Answer in one sentence"

        },
    ]
)
# message = client.messages.create(
#     model=model,
#     max_tokens=500,
#     messages=[
#         {
#             "role": "user",
#             "content": "Hello, My name is Neesh and my query is what is quantam computing? Answer in one sentence"

#         },
#         {
#             "role": "assistant",
#             "content": "Quantum computing is a type of computing that uses quantum mechanical phenomena, such as **superposition** and **entanglement**, to process information in ways that can solve certain complex problems much faster than classical computers."
#         },
#         {
#             "role": "user",
#             "content": "What coding language is vastly used in quantam computing, What is my name?"
#         }
#     ]
# )
print(message.content[0].text)