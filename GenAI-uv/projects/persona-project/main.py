from dotenv import load_dotenv
from openai import OpenAI
import prompts as myprompts

load_dotenv()

client = OpenAI()

# Zero-shot Prompting: The model is given a direct question or task

SYSTEM_PROMPT = myprompts.getPrompts()
user_prompt = input('ask your query !')
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": user_prompt},
        
    ]
)
print(response)
if response.status_code == 200:

    print(response.choices[0].message.content)