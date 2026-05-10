# ===== IMPORTS =====
import dotenv
from anthropic import Anthropic
import requests
from anthropic.types import ToolParam
from anthropic.types import Message
import json


# ===== INITIALIZATION =====
# Load environment variables (API keys) from .env file
dotenv.load_dotenv()

# Create Anthropic client instance for API communication
client = Anthropic()

# Specify Claude model to use (Haiku for speed and cost efficiency)
model = "claude-haiku-4-5-20251001"

# Initialize empty message list to store conversation history
message = []

# User query - can be changed to input() for interactive use
users_query = "what is weather of Delhi, India?"


# Tool definition

# ===== TOOL 1: WEATHER =====
# Weather API Call - Fetches weather data from wttr.in
def get_weather(location: str):
    """Fetch current weather data for a location using wttr.in API."""
    # Validate input: location cannot be empty or null
    if not location or location.strip() == "":
        raise ValueError("Location cannot be empty")

    # Build API URL with JSON format (j1) for structured data
    # Using format=j1 to get JSON response instead of plain text
    url = f"https://wttr.in/{location}?format=j1"

    # Make HTTP request to weather API with 10 second timeout
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise exception if request fails

    # Parse JSON response and extract current weather conditions
    data = response.json()
    current = data['current_condition'][0]  # Get first (current) condition entry

    # Return structured weather data as dictionary
    return {
        "location": location,
        "condition": current['weatherDesc'][0]['value'],
        "temperature": f"{current['temp_C']}°C",
        "humidity": f"{current['humidity']}%",
        "feels_like": f"{current['FeelsLikeC']}°C"
    }


# ===== TOOL 2: AIR QUALITY =====
# Air Quality Index API Call - Fetches AQI data from waqi.info
def get_air_quality(location: str):
    """Fetch air quality index (AQI) and pollution data for a location using waqi.info API."""
    # Validate input: location cannot be empty or null
    if not location or location.strip() == "":
        raise ValueError("Location cannot be empty")

    # Set up API credentials (using demo key - replace with your own from waqi.info)
    # Get free API key at: https://waqi.info/
    api_key = "demo"  # Replace with your actual API key from waqi.info
    url = f"https://api.waqi.info/feed/{location}/?token={api_key}"

    try:
        # Make API request with timeout to prevent hanging
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Check if API returned successfully (status = 'ok')
        if data['status'] == 'ok':
            # Extract AQI data from response
            aqi_data = data['data']

            # Return structured air quality data with multiple pollutant levels
            return {
                "location": location,
                "aqi": aqi_data.get('aqi', 'N/A'),  # Overall Air Quality Index
                "level": get_aqi_level(aqi_data.get('aqi')),  # Convert to health level
                "dominant_pollutant": aqi_data.get('dominentpol', 'N/A'),  # Main pollutant
                "pm25": aqi_data.get('iaqi', {}).get('pm25', {}).get('v', 'N/A'),  # PM2.5 level
                "pm10": aqi_data.get('iaqi', {}).get('pm10', {}).get('v', 'N/A'),  # PM10 level
                "o3": aqi_data.get('iaqi', {}).get('o3', {}).get('v', 'N/A')  # Ozone level
            }
        else:
            # API returned error response
            raise Exception(f"API Error: {data.get('message', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        # Network or request error occurred
        raise Exception(f"Failed to fetch air quality data: {str(e)}")


def get_aqi_level(aqi_value):
    """Convert numeric AQI value to human-readable health level (e.g., Good, Moderate, Unhealthy)."""
    if aqi_value is None or aqi_value == 'N/A':
        return "Unknown"
    if aqi_value <= 50:
        return "Good"
    elif aqi_value <= 100:
        return "Moderate"
    elif aqi_value <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi_value <= 200:
        return "Unhealthy"
    elif aqi_value <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"


# Tool Schema Definition
# JSON Schema defines the exact structure and types of inputs Claude must provide when calling this tool, ensuring type safety and validation
get_weather_tool_schema = ToolParam({  # ToolParam wraps the schema and provides type hints to ensure the tool definition matches Anthropic's expected format
    "name": "get_weather",
    "description": "Retrieves current weather information for a specified location. Returns weather condition and temperature.",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name or location for which to retrieve weather information. Examples: 'London', 'New York', 'Paris'. Cannot be empty."
            }
        },
        "required": ["location"]
    }
})


# Air Quality Tool Schema Definition
get_air_quality_tool_schema = ToolParam({
    "name": "get_air_quality",
    "description": "Retrieves air quality index (AQI) and pollution information for a specified location. Returns AQI value, health level, and dominant pollutants.",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name or location for which to retrieve air quality information. Examples: 'Delhi', 'New York', 'Beijing'. Cannot be empty."
            }
        },
        "required": ["location"]
    }
})


# ===== HELPER FUNCTIONS =====
# Message management functions for building conversation history

def add_user_message(messages, content):
    """Add a user message to the conversation history."""
    # Create user message with role and content
    # Handle both string content and Message object from API
    user_message = {"role": "user",
                     "content": content.content if isinstance(content, Message) else content}
    # Append to conversation history
    messages.append(user_message)

def add_assistant_message(messages, content):
    """Add an assistant message to the conversation history."""
    # Create assistant message with role and content
    # Handle both string content and Message object from API
    assistant_message = {"role": "assistant",
                          "content": content.content if isinstance(content, Message) else content}
    # Append to conversation history
    messages.append(assistant_message)

def chat(messages, system=None, temperature=0.5, stop_sequences=[], tools=None):
    """Call Claude API with messages, optional system prompt, and available tools."""
    # Build API request parameters
    params = {
        "model": model,  # Claude model to use
        "max_tokens": 500,  # Limit response length
        "messages": messages,  # Conversation history
        "temperature": temperature,  # Control randomness (0=deterministic, 1=creative)
        "stop_sequences": stop_sequences  # When to stop generating
    }

    # Add optional system prompt if provided
    # System prompt guides Claude's behavior and role
    if system:
        params["system"] = system

    # Add available tools if provided
    # Tools enable Claude to request actions (function calls)
    if tools:
        params["tools"] = tools

    # Make API call and get response
    message = client.messages.create(**params)
    return message

def chat_stream(messages, system=None, temperature=0.5, stop_sequences=[], tools=None, tool_choice=None, fine_grained=False):
    """Stream Claude API response with real-time token output and tool call detection."""
    # Build API request parameters for streaming
    params = {
        "model": model,  # Claude model to use
        "max_tokens": 500,  # Limit response length
        "messages": messages,  # Conversation history
        "temperature": temperature,  # Control randomness
        "stop_sequences": stop_sequences  # When to stop generating
    }

    # Add optional system prompt if provided
    if system:
        params["system"] = system

    # Add available tools if provided
    if tools:
        params["tools"] = tools

    # Add tool choice strategy if provided
    # Controls how Claude selects tools (e.g., force specific tool, auto)
    if tool_choice:
        params["tool_choice"] = tool_choice

    # Add fine-grained streaming beta feature if enabled
    # Provides more granular control over streaming events
    if fine_grained:
        params["betas"] = ["fine-grained-tool-streaming-2025-05-14"]

    # Return streaming context manager for token-by-token processing
    return client.messages.stream(**params)

def text_from_message(message):
    """Extract text content from a message response object."""
    return "\n".join([block.text for block in message.content if block.type == "text"])

def run_tool(tool_name, tool_input):
    """Execute a tool by name with given input parameters."""
    # Router function: maps tool name to actual function call
    if tool_name == "get_weather":
        # Execute weather tool with provided location
        return get_weather(**tool_input)
    elif tool_name == "get_air_quality":
        # Execute air quality tool with provided location
        return get_air_quality(**tool_input)
    else:
        # Error if requested tool doesn't exist
        raise ValueError(f"Unknown tool: {tool_name}")

def run_tools(message):
    """Extract and execute all tool calls from Claude's response, returning results in proper format."""
    # Step 1: Extract all tool_use blocks from Claude's response
    # Claude can request multiple tools in one response
    tool_requests = [
        block for block in message.content
        if (hasattr(block, 'type') and block.type == "tool_use") or (isinstance(block, dict) and block.get('type') == "tool_use")
    ]

    # Step 2: Initialize list to store formatted results
    tool_result_blocks = []

    # Step 3: Process each tool request
    for tool_request in tool_requests:
        # Extract tool_id before try block so except clause can always reference it
        # Use fallback 'unknown' if id attribute is missing or inaccessible
        if hasattr(tool_request, 'id'):
            tool_id = tool_request.id
        elif isinstance(tool_request, dict):
            tool_id = tool_request.get('id', 'unknown')
        else:
            tool_id = 'unknown'

        try:
            # Get tool name and input from either object or dict
            tool_name = tool_request.name if hasattr(tool_request, 'name') else tool_request['name']
            tool_input = tool_request.input if hasattr(tool_request, 'input') else tool_request['input']

            # Execute the requested tool with its input parameters
            tool_output = run_tool(tool_name, tool_input)

            # Format the successful result for Claude
            # Must include: type, tool_use_id (to link result to request), content, error flag
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_id,  # Links result back to tool call
                "content": json.dumps(tool_output),  # Convert result to JSON string
                "is_error": False
            }
        except Exception as e:
            # Format error result if tool execution fails
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_id,  # Links error back to tool call (always defined now)
                "content": f"Error {e}",  # Error message
                "is_error": True  # Flag as error
            }

        # Add formatted result to list
        tool_result_blocks.append(tool_result_block)

    # Step 4: Return all results for sending back to Claude
    return tool_result_blocks

def run_conversation(messages, tools=[], tool_choice=None, fine_grained= False):
    """Run the multi-turn conversation loop with streaming: get Claude response → execute tools if needed → repeat until final answer."""
    # System prompt: guides Claude's behavior and role for this conversation
    system_prompt = "You are a helpful assistant that provides comprehensive information about locations. When a user asks about a location, provide both weather and air quality information if available."

    # Main conversation loop
    while True:
        # Step 1: Stream Claude response with current message history and available tools
        with chat_stream(
            messages,
            system=system_prompt,
            tools=[get_weather_tool_schema, get_air_quality_tool_schema],
            tool_choice=tool_choice,
            fine_grained=fine_grained
        ) as stream:
            # Step 2: Process each chunk to display real-time output
            for chunk in stream:
                # Handle text delta - partial text streaming in real-time
                if chunk.type == "content_block_delta":
                    if hasattr(chunk.delta, 'text'):
                        print(chunk.delta.text, end="", flush=True)

                # Handle tool call detection - print tool name when block opens
                if chunk.type == "content_block_start":
                    if chunk.content_block.type == "tool_use":
                        print(f'\n>>> Tool Call: "{chunk.content_block.name}" args: ', end="", flush=True)

                # Handle streaming tool argument JSON
                if chunk.type == "input_json":
                    # Print the new fragment inline so argument JSON streams
                    # visually alongside the tool call header on one line
                    print(chunk.partial_json, end="", flush=True)

                    if fine_grained:
                        # Fine-grained mode: SDK does not pre-validate chunks,
                        # so snapshot may be incomplete mid-key-value-pair.
                        # Validate that chunks parse as JSON; store for potential use in debugging or analysis.
                        # The final authoritative tool inputs come from stream.get_final_message().
                        try:
                            current_args = json.loads(chunk.snapshot)  # For debugging/validation only
                        except json.JSONDecodeError:
                            pass  # Incomplete JSON fragment — keep accumulating

            # Step 3: Get the final message object from the stream
            response = stream.get_final_message()

        # Step 4: Add Claude's response to conversation history
        messages.append({"role": "assistant", "content": response.content})

        # Step 5: Check if Claude is done or wants to use tools
        # If stop_reason is "tool_use", Claude called a tool and needs results
        # If stop_reason is anything else (like "end_turn"), conversation is complete
        if response.stop_reason != "tool_use":
            # Claude finished the conversation - exit loop
            print()  # Add newline after streaming output
            break

        # Step 6: Execute all tools Claude requested
        tool_results = run_tools(response)

        # Step 7: Add tool results back to conversation history as user message
        # This closes the loop: Claude sees tool results and can respond accordingly
        messages.append({
            "role": "user",
            "content": tool_results
        })
        # Loop continues - Claude gets another turn with tool results

    # Return final conversation history with all exchanges
    return messages


# ===== MAIN EXECUTION =====
# Start with empty conversation history
messages = []

# Add initial user query to start the conversation
add_user_message(messages, "Tell me about the weather and air quality in Delhi, India. I want to know both the temperature and the air pollution levels.")

# Run the multi-turn conversation loop
# This orchestrates: user query → Claude response → tool execution → Claude final answer
run_conversation(messages)