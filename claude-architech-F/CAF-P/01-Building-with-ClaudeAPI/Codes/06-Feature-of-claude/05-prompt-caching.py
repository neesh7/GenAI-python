# Prompt Caching Demo: Cache tools and system prompts
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import Message, ToolParam

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"


# Helper functions
def add_user_message(messages, message):
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(user_message)


def add_assistant_message(messages, message):
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(assistant_message)


def chat(messages, system=None, temperature=1.0, stop_sequences=[], tools=None):
    params = {
        "model": model,
        "max_tokens": 4000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if tools:
        tools_clone = tools.copy()
        last_tool = tools_clone[-1].copy()
        last_tool["cache_control"] = {"type": "ephemeral"}
        tools_clone[-1] = last_tool
        params["tools"] = tools_clone

    if system:
        params["system"] = [
            {
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral"}
            }
        ]

    message = client.messages.create(**params)
    return message


def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])


# Long system prompt (~6k tokens) - demonstrates caching benefits
system_prompt = """# Javascript Code Generator for Document Analysis Flow

You are an expert Javascript code generator. Your specialty is creating code for a document analysis flow builder application. The code you generate will run in a sandboxed Javascript environment (QuickJS) and will use a predefined set of UI components to construct user interfaces.

Your Goal: Generate functional Typescript code that defines both the logic and user interface for a document analysis workflow, based on the user's prompt. The generated code must be ready to execute directly within the sandbox environment.

Think of this as writing code for a very specific, constrained platform. Standard web development practices and libraries (like React, typical Javascript DOM manipulation, etc.) are not available.

## Key Functions:
- `getInitialState()`: Returns initial application state
- `render()`: Defines UI based on current state (can be async)
- Helper functions to organize code

## State Management:
- Use `await getState()` to retrieve current state
- Use `await setState(partialState)` to update state
- setState triggers re-render automatically

## LLM Interaction:
- Use `callLLM()` with schemas for structured responses
- Schemas guide LLM output and improve reliability
- Use `onProgress` callback for streaming updates

## Schema Builder Functions:
- str(description): String property
- num(description): Number property
- bool(description): Boolean property
- obj(properties, description): Object property
- arr(items, description): Array property

## Critical Guidelines:
1. Multi-screen flows should use Route components for navigation
2. Document editing applies changes automatically in track-changes mode
3. Use formatAssistantMessages for rendering message schemas
4. Include document content in systemPrompt, not user message
5. Do NOT add comments to generated code
6. Do NOT use import/export statements

## Component List:
Available components include: Chat, Button, Link, Header, H2, Panel, DocumentPicker, Route, etc. These are globally available - no imports needed.

You must strictly follow these constraints when generating code."""

# Tool schemas (~1.7k tokens) - demonstrates tool caching
tools = [
    ToolParam(
        {
            "name": "add_duration_to_datetime",
            "description": "Add a specified duration to a datetime string and returns the resulting datetime in a detailed format.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "datetime_str": {
                        "type": "string",
                        "description": "The input datetime string (format: YYYY-MM-DD)",
                    },
                    "duration": {
                        "type": "number",
                        "description": "The amount of time to add (default: 0)",
                    },
                    "unit": {
                        "type": "string",
                        "description": "The unit: 'seconds', 'minutes', 'hours', 'days', 'weeks', 'months', or 'years'",
                    },
                },
                "required": ["datetime_str"],
            },
        }
    ),
    ToolParam(
        {
            "name": "set_reminder",
            "description": "Creates a timed reminder that will notify the user at the specified time with the provided content.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The message text for the reminder notification",
                    },
                    "timestamp": {
                        "type": "string",
                        "description": "The exact date and time (ISO 8601 format: YYYY-MM-DDTHH:MM:SS)",
                    },
                },
                "required": ["content", "timestamp"],
            },
        }
    ),
    ToolParam(
        {
            "name": "get_current_datetime",
            "description": "Returns the current date and time formatted according to the specified format string.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "date_format": {
                        "type": "string",
                        "description": "Format string using strftime codes (default: '%Y-%m-%d %H:%M:%S')",
                    }
                },
                "required": [],
            },
        }
    ),
    ToolParam(
        {
            "name": "db_query",
            "description": "Executes SQL queries against a SQLite database and returns the results.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The SQL query to execute",
                    },
                    "database_path": {
                        "type": "string",
                        "description": "The path to the SQLite database file",
                    },
                    "params": {
                        "type": "object",
                        "description": "Parameters to bind to the query",
                    },
                    "result_format": {
                        "type": "string",
                        "description": "Format: 'dict', 'list', or 'table' (default: 'dict')",
                    },
                },
                "required": ["query"],
            },
        }
    ),
]


def demonstrate_caching():
    """Demonstrate prompt caching benefits with multiple requests."""

    print("=" * 70)
    print("PROMPT CACHING DEMO")
    print("=" * 70)
    print("\nNote: First request writes to cache, follow-up requests read from cache")
    print("Cache is valid for 1 hour and requires >=1024 tokens of content\n")

    # Request 1: Initial request with system prompt + tools (writes to cache)
    print("REQUEST 1: Initial request (writing to cache)")
    print("-" * 70)
    messages = []
    add_user_message(messages, "What time is it?")

    response1 = chat(messages, system=system_prompt, tools=tools)
    print(f"Stop reason: {response1.stop_reason}")
    print(f"Cache creation tokens: {response1.usage.cache_creation_input_tokens}")
    print(f"Cache read tokens: {response1.usage.cache_read_input_tokens}")
    print(f"Input tokens: {response1.usage.input_tokens}")
    print(f"Output tokens: {response1.usage.output_tokens}")
    print(f"\nResponse: {text_from_message(response1)}\n")

    add_assistant_message(messages, response1)

    # Request 2: Follow-up with identical content (reads from cache)
    print("REQUEST 2: Follow-up request (reading from cache)")
    print("-" * 70)
    add_user_message(messages, "Add 1 day to 2025-04-15")

    response2 = chat(messages, system=system_prompt, tools=tools)
    print(f"Stop reason: {response2.stop_reason}")
    print(f"Cache creation tokens: {response2.usage.cache_creation_input_tokens}")
    print(f"Cache read tokens: {response2.usage.cache_read_input_tokens}")
    print(f"Input tokens: {response2.usage.input_tokens}")
    print(f"Output tokens: {response2.usage.output_tokens}")
    print(f"\nResponse: {text_from_message(response2)}\n")

    add_assistant_message(messages, response2)

    # Request 3: Another follow-up (cache still valid)
    print("REQUEST 3: Third request (cache still valid)")
    print("-" * 70)
    add_user_message(messages, "What tools do I have available?")

    response3 = chat(messages, system=system_prompt, tools=tools)
    print(f"Stop reason: {response3.stop_reason}")
    print(f"Cache creation tokens: {response3.usage.cache_creation_input_tokens}")
    print(f"Cache read tokens: {response3.usage.cache_read_input_tokens}")
    print(f"Input tokens: {response3.usage.input_tokens}")
    print(f"Output tokens: {response3.usage.output_tokens}")
    print(f"\nResponse: {text_from_message(response3)}\n")

    # Cache Statistics
    print("=" * 70)
    print("CACHE STATISTICS")
    print("=" * 70)

    total_cache_creation = (
        response1.usage.cache_creation_input_tokens +
        response2.usage.cache_creation_input_tokens +
        response3.usage.cache_creation_input_tokens
    )

    total_cache_read = (
        response1.usage.cache_read_input_tokens +
        response2.usage.cache_read_input_tokens +
        response3.usage.cache_read_input_tokens
    )

    total_regular_input = (
        response1.usage.input_tokens +
        response2.usage.input_tokens +
        response3.usage.input_tokens
    )

    print(f"Total cache creation (first write): {total_cache_creation} tokens")
    print(f"Total cache reads (follow-ups): {total_cache_read} tokens")
    print(f"Total regular input tokens: {total_regular_input} tokens")
    print(f"\nKey insights:")
    print(f"- Request 1 spent tokens writing system + tools to cache")
    print(f"- Requests 2-3 reused that cached content (instant access)")
    print(f"- Cache content cost 90% less per token than regular input")
    print(f"- If using 10 requests: savings would be much larger")


if __name__ == "__main__":
    demonstrate_caching()
