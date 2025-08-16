from dotenv import load_dotenv
from openai import OpenAI

# Load the API Key and feed it to client
load_dotenv()
client = OpenAI()

# Read and write system prompt function
def read_prompt_from_file(filePath):
    try:
        with open(filePath,'r', encoding='utf-8') as file:
            content =file.read()
            # print(content)
    except FileNotFoundError:
        print('System prompt file not found')
        content = ""
    return content

def write_prompt_into_file(filePath,context):
    with open(filePath,'a', encoding='utf-8') as file: # updated encoding to utf-8 to handle emoji writing also
        file.write(context)
        print('File is writen into context')

def parse_conversation_history(raw_text):
    lines = raw_text.splitlines()
    messages = []
    for line in lines:
        if line.startswith("User:"):
            messages.append({"role": "user", "content": line.replace("User: ", "").strip()})
        elif line.startswith("AI Neesh:"):
            messages.append({"role": "assistant", "content": line.replace("AI Neesh: ", "").strip()})
    return messages

# Passing filepath and declaring system prompt
file = 'GenAI-uv/03-system_prompts/prompt_practice01.txt'
raw_prompt  = read_prompt_from_file(file)
# print(SYSTEM_PROMPT)

# Split system prompt from conversation history
split_marker = "Conversation history:"
if split_marker in raw_prompt:
    system_prompt, history_text = raw_prompt.split(split_marker, 1)
else:
    system_prompt = raw_prompt
    history_text = ""

# ✅ Parse conversation history into structured messages
conversation_history = parse_conversation_history(history_text)

while True:
        
    USER_INPUT = input(">: ")
    if USER_INPUT.casefold() == 'done':
        break
    # Build full message list
    messages = [{"role": "system", "content": system_prompt.strip()}] + conversation_history + [{"role": "user", "content": USER_INPUT}]
    # API Call
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    ai_reply = response.choices[0].message.content
    print(ai_reply)

    # Update conversation history
    user_data = f"User: {USER_INPUT}\n"
    ai_data = f"AI Neesh: {ai_reply}\n"
    write_prompt_into_file(file, user_data + ai_data)

    # Also update in-memory history for next loop
    conversation_history.append({"role": "user", "content": USER_INPUT})
    conversation_history.append({"role": "assistant", "content": ai_reply})

    print()