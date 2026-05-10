import dotenv
from anthropic import Anthropic
import requests
from anthropic.types import ToolParam

# Load env variables, setting up client
dotenv.load_dotenv()
client = Anthropic()

# users_query = input("Please ask any weather related query ? -> ")
users_query = "what is weather of Delhi, India?"

# Weather API Call - TOOL
def get_weather(location: str):
    if not location or location.strip() == "":
        raise ValueError("Location cannot be empty")

    # Using format=j1 to get JSON response instead of plain text
    url = f"https://wttr.in/{location}?format=j1"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    # Extract current weather from JSON response
    data = response.json()
    current = data['current_condition'][0]
    return {
        "location": location,
        "condition": current['weatherDesc'][0]['value'],
        "temperature": f"{current['temp_C']}°C",
        "humidity": f"{current['humidity']}%",
        "feels_like": f"{current['FeelsLikeC']}°C"
    }


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

# user-messege
message = []
message.append(  {
            "role": "user",
            "content": users_query
        })

# Create method to make AI Call
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=500,
    system="You are Helpful AI which responds to users weather related queries and you do not entertain any other queries!",
    messages=message,
    tools=[get_weather_tool_schema]
)

# Check if Claude actually called a tool or responded with text
if response.stop_reason == "tool_use" and response.content[0].type == "tool_use":
    # Safe to extract tool information
    print("\n✓ Tool Call Detected:")
    print(f"  Tool ID: {response.content[0].id}")
    print(f"  Tool Name: {response.content[0].name}")
    print(f"  Tool Input: {response.content[0].input}")

    # Add assistant response to message history
    message.append({
        "role": "assistant",
        "content": response.content
    })

    # Execute the tool and get weather data
    try:
        weather_report = get_weather(**response.content[0].input)
        print(f"\n✓ Weather Data Retrieved: {weather_report}")

        # Add tool result back to message history
        message.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": response.content[0].id,
                    "content": str(weather_report)
                }
            ]
        })

        # Send tool result back to Claude for final response
        final_response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            system="You are Helpful AI which responds to users weather related queries and you do not entertain any other queries!",
            messages=message,
            tools=[get_weather_tool_schema]
        )

        # Extract final text response safely
        if final_response.content and final_response.content[0].type == "text":
            print("\n✓ Final Response from Claude:")
            print(final_response.content[0].text)
        else:
            print("\n✗ Unexpected response type from Claude")

    except Exception as e:
        print(f"\n✗ Error executing tool: {str(e)}")

elif response.content[0].type == "text":
    # Claude responded with text instead of tool call
    print("\n✓ Claude's Response (No Tool Call):")
    print(response.content[0].text)

else:
    # Unexpected response type
    print(f"\n✗ Unexpected response: {response.content[0].type}")
    print(f"Stop Reason: {response.stop_reason}")