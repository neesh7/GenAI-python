from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import subprocess
import threading
import sys

# Load API key from .env
load_dotenv()
client = OpenAI()

# Tool: Run shell command
def run_shell(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "returncode": result.returncode
    }

# Tool: Read file
def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"


def write_file(path, content):
    try:
        with open(path, 'w') as f:
            f.write(content)
        return f"✅ File '{path}' updated successfully."
    except Exception as e:
        return f"❌ Error writing file: {e}"

def parse_npm_error(log_text):
    # Very basic pattern matching
    if "peer dependency" in log_text:
        return "Detected peer dependency conflict."
    elif "missing" in log_text or "not found" in log_text:
        return "Detected missing package error."
    else:
        return "No known error pattern detected."

def suggest_fix(issue_type, package=None, required_version=None):
    if issue_type == "peer dependency":
        return f"Try installing {package}@{required_version} or use --legacy-peer-deps."
    elif issue_type == "missing":
        return f"Run 'npm install {package}' to resolve missing dependency."
    else:
        return "No suggestion available."

def confirm_fix(message):
    response = input(f"⚠️ {message} Proceed? (y/n): ")
    return response.lower() == 'y'
def modify_package_json():
    try:
        with open("package.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        return f"❌ Failed to read package.json: {e}"

    if "scripts" not in data:
        data["scripts"] = {}

    data["scripts"]["start"] = "node server.js"

    try:
        with open("package.json", "w") as f:
            json.dump(data, f, indent=2)
        return "✅ package.json updated with start script."
    except Exception as e:
        return f"❌ Failed to write package.json: {e}"

# Timeout handler -  To prevent agent getting into infinite loop
def timeout_handler():
    print("\n⏰ Timeout reached. Agent loop terminated.")
    sys.exit(1)  # Or raise an exception if you want to catch it

# Tool dispatcher
def dispatch(tool_name, input_data):
    if tool_name == "run_shell":
        return run_shell(input_data)
    elif tool_name == "read_file":
        return read_file(input_data)
    elif tool_name == "write_file":
        path = input_data.get("path")
        content = input_data.get("content")
        if path and content:
            return write_file(path, content)
        else:
            return f"❌ Missing 'path' or 'content' in input: {input_data}"
    elif tool_name == "parse_npm_error":
        return parse_npm_error(input_data)
    elif tool_name == "suggest_fix":
        return suggest_fix(**input_data)
    elif tool_name == "confirm_fix":
        return confirm_fix(input_data)
    elif tool_name == "modify_package_json":
        return modify_package_json()
    else:
        return f"Tool '{tool_name}' not implemented."


AVAILABLE_TOOLS = {
    "run_shell": "Execute shell commands",
    "read_file": "Read file contents",
    "write_file": "Write to files",
    "parse_npm_error": "Analyze npm error logs",
    "suggest_fix": "Recommend fixes",
    "confirm_fix": "Ask user for confirmation",
    "modify_package_json": "Inject start script into package.json"
}

tool_descriptions = "\n".join([f'{name} — {desc}' for name, desc in AVAILABLE_TOOLS.items()])

SYSTEM_PROMPT = f'''
You are a local AI agent designed to diagnose and fix npm dependency issues in JavaScript/Node.js projects.

You operate in a CLI-native environment and can execute shell commands directly. Your reasoning follows a structured loop: plan → act → observe → reflect → output.

Your mission is to:
- Identify dependency issues (e.g., version conflicts, peer mismatches, missing packages)
- Suggest and optionally apply fixes using shell commands
- Maintain transparency and safety in all operations

Capabilities:
You can use the following tools:
{tool_descriptions}

Tool Invocation Protocol:
When you decide to use a tool, respond with a JSON object containing:
- step: "act"
- function: tool name (from Available Tools)
- input: input required by the tool

Tool results will be returned to you as a JSON object with step: "observe". Use this to reflect and decide next steps.

Behavior Guidelines:
- Always reason before acting. Never run destructive commands without user confirmation.
- Never run commands that modify or delete files (e.g., rm, write_file) without explicit user confirmation via the "confirm_fix" tool.
- Output responses in structured JSON format for easy parsing.
- Be concise, technical, and focused. Use humor only when appropriate.
- If uncertain, ask for clarification or suggest safe defaults.

Output Format:
{{
  "step": "string",               // One of: plan, act, observe, reflect, output
  "content": "string",            // Reasoning or explanation
  "function": "string",           // Tool name (if step is act)
  "input": "string or object"     // Input for the tool
}}
'''



# # Agent loop
# def agent_loop(user_query):
#     messages = [
#     {"role": "system", "content": SYSTEM_PROMPT},
#     {"role": "user", "content": user_query}
#     ]

#     while True:
#         response = client.chat.completions.create(
#             model="gpt-4",
#             messages=messages,
#             temperature=0.3
#         )

#         reply = response.choices[0].message.content
#         print("\n🤖 Agent Response:")
#         print(reply)

#         try:
#             parsed = json.loads(reply)
#         except json.JSONDecodeError:
#             print("⚠️ Could not parse JSON. Agent output:")
#             print(reply)
#             break

#         step = parsed.get("step")
#         content = parsed.get("content")
#         function = parsed.get("function")
#         input_data = parsed.get("input")

#         if step == "output":
#             print(f"\n✅ Final Output: {content}")
#             break
#         elif step == "act":
#             print(f"\n🔧 Executing tool: {function}")
#             result = dispatch(function, input_data)
#             messages.append({"role": "assistant", "content": reply})
#             messages.append({"role": "user", "content": f"Tool result:\n{result}"})
#         else:
#             messages.append({"role": "assistant", "content": reply})

def agent_loop():

    # Start timeout watchdog (e.g., 300 seconds = 5 minutes) -- To Prevent the agent getting into infinite loop
    timer = threading.Timer(300, timeout_handler)
    timer.start()
    #####
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print("🧑‍💻 Agent session started. Describe your npm issue to begin.")
    user_input = input("\n🧑‍💻 Your instruction: ")
    messages.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.3
        )

        reply = response.choices[0].message.content
        print("\n🤖 Agent Response:")
        print(reply)

        try:
            parsed = json.loads(reply)
        except json.JSONDecodeError:
            print("⚠️ Could not parse JSON. Agent output:")
            print(reply)
            continue

        step = parsed.get("step")
        content = parsed.get("content")
        function = parsed.get("function")
        input_data = parsed.get("input")

        if step == "output":
            if any(phrase in content.lower() for phrase in ["thank you", "i'm done", "exit"]):
                print(f"\n👋 Agent session ended: {content}")
                break
            else:
                print(f"\n✅ Final Output: {content}")
                user_input = input("\n🧑‍💻 What would you like to do next?: ")
                messages.append({"role": "user", "content": user_input})
        elif step == "act":
            print(f"\n🔧 Executing tool: {function}")
            result = dispatch(function, input_data)
            messages.append({"role": "assistant", "content": reply})
            messages.append({
                "role": "user",
                "content": json.dumps({
                    "step": "observe",
                    "output": result
                })
            })
        else:
            messages.append({"role": "assistant", "content": reply})

# Run the agent
if __name__ == "__main__":
    # query = input("🧑‍💻 Describe your npm issue: ")
    # agent_loop(query)  incase if you use first function
    agent_loop() # if you are using second functions
