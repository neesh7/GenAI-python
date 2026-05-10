# Claude Tool Use with Streaming Guide

## Overview

This code implements a **multi-turn conversational AI agent** that uses Claude's tool-calling capabilities with **real-time streaming**. The agent can fetch weather and air quality information for any location and provide comprehensive responses.

### Key Features
- ✅ **Real-time streaming output** - See Claude's response as it's generated
- ✅ **Tool argument streaming** - Watch tool arguments appear in real-time
- ✅ **Multi-tool support** - Execute multiple tools in a single turn
- ✅ **Error handling** - Gracefully handles API failures and invalid data
- ✅ **Two streaming modes** - Standard (validated) and Fine-grained (immediate)
- ✅ **Multi-turn conversation** - Claude can request tools and process results

---

## Architecture Overview

```
User Query
    ↓
Claude API (with streaming)
    ├─ Streams text response
    ├─ Streams tool arguments
    └─ Returns final message
    ↓
Tool Execution Loop
    ├─ Extract tool requests
    ├─ Execute each tool
    └─ Collect results
    ↓
Send Tool Results to Claude
    ├─ Claude processes results
    ├─ Streams new response
    └─ May request more tools
    ↓
Repeat until Claude stops using tools
    ↓
Final Response to User
```

---

## Core Concepts: Standard vs Fine-Grained Streaming

### **Standard Mode** (Default: `fine_grained=False`)

The API **validates and buffers** tool argument JSON at top-level key-value boundaries.

```
Generation Timeline:
Claude generates: {"location": "D
                                e
                                l
                                h
                                i"...}
                  ↓
                  API waits for complete "location" value
                  ↓
                  Validation: ✓ Valid
                  ↓
                  Send chunk burst with complete key-value pair
                  
Chunks received:  {"location": "Delhi"}
json.loads()      ✓ Always succeeds
```

**Characteristics:**
- ✅ JSON validation **ENABLED** on API side
- ✅ `snapshot` is always valid and parseable
- ✅ Chunks arrive in validated batches (may see delays)
- ✅ Safe to call `json.loads(snapshot)` without error handling
- 📍 Best for: Reliability, guaranteed valid JSON, typical use cases

---

### **Fine-Grained Mode** (Beta: `fine_grained=True`)

The API **disables validation** and sends chunks **immediately** as they're generated.

```
Generation Timeline:
Claude generates: {"location": "D
                                e
                                l
                                h
                                i"...}
                  ↓
                  API sends chunk immediately (no buffering)
                  ↓
                  Sends next chunk immediately
                  
Chunks received:  { (incomplete)
                   "location": "De (incomplete)
                   "location": "Delhi (incomplete)
                   "location": "Delhi" (incomplete)
json.loads()      ✗ May fail on incomplete JSON
```

**Characteristics:**
- ❌ JSON validation **DISABLED** on API side
- ⚡ Chunks arrive as fast as Claude generates them
- ⚠️ `snapshot` may contain incomplete/invalid JSON: `{"key": unde` or `{"a": 1`
- 🛡️ **MUST** wrap `json.loads(snapshot)` in `try/except`
- 📍 Best for: Real-time UX, immediate feedback, responsive applications

**When to use Fine-Grained:**
- You need live progress updates on tool argument generation
- Buffering delays negatively impact user experience
- You're showing a progress indicator or streaming UI
- You can handle JSON parsing errors gracefully

---

## Code Structure

### 1. **Tool Definition Functions**

#### `get_weather(location: str)` — Lines 65-90

Fetches current weather for a location using the **wttr.in API**.

```python
get_weather("Delhi, India")
# Returns:
{
    "location": "Delhi, India",
    "condition": "Haze",
    "temperature": "30°C",
    "humidity": "55%",
    "feels_like": "29°C"
}
```

**Flow:**
1. Validate location is not empty
2. Build API URL: `https://wttr.in/{location}?format=j1`
3. Make HTTP request with 10-second timeout
4. Parse JSON response and extract current conditions
5. Return structured dictionary

---

#### `get_air_quality(location: str)` — Lines 95-132

Fetches air quality index (AQI) and pollution data using **waqi.info API**.

```python
get_air_quality("Delhi")
# Returns:
{
    "location": "Delhi",
    "aqi": 287,
    "level": "Very Unhealthy",
    "dominant_pollutant": "pm25",
    "pm25": 192,
    "pm10": 342,
    "o3": 28
}
```

**Flow:**
1. Validate location is not empty
2. Use demo API key (replace with your own from waqi.info)
3. Build API URL and make request
4. Extract AQI data from response
5. Convert numeric AQI to human-readable level
6. Return structured dictionary with pollutant details

---

#### `get_aqi_level(aqi_value)` — Lines 135-146

Converts numeric AQI value to human-readable health level.

```
AQI Range       → Health Level
0-50            → Good
51-100          → Moderate
101-150         → Unhealthy for Sensitive Groups
151-200         → Unhealthy
201-300         → Very Unhealthy
300+            → Hazardous
```

---

### 2. **Tool Schema Definition**

Tool schemas tell Claude **what tools are available** and **what parameters they accept**.

#### Weather Tool Schema (Lines 154-167)

```python
get_weather_tool_schema = ToolParam({
    "name": "get_weather",
    "description": "Retrieves current weather information...",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name or location..."
            }
        },
        "required": ["location"]
    }
})
```

**What this does:**
- Tells Claude the tool is called `"get_weather"`
- Explains what it does (description)
- Specifies it needs a `location` parameter (string, required)
- Claude uses this to generate valid tool calls

---

### 3. **Helper Functions**

#### `add_user_message(messages, content)` — Lines 192-198

Adds a user message to the conversation history.

```python
add_user_message(messages, "What's the weather in Delhi?")
# messages becomes:
[{"role": "user", "content": "What's the weather in Delhi?"}]
```

**Why it matters:** Conversation history is essential for multi-turn conversations. Claude needs to see the full context.

---

#### `add_assistant_message(messages, content)` — Lines 200-206

Adds an assistant (Claude) message to the conversation history.

```python
messages.append({"role": "assistant", "content": response.content})
```

---

#### `chat_stream(...)` — Lines 208-257

**Creates a streaming connection to Claude's API.**

```python
with chat_stream(
    messages,
    system=system_prompt,
    tools=[get_weather_tool_schema, get_air_quality_tool_schema],
    fine_grained=False  # Use standard mode
) as stream:
    for chunk in stream:
        # Process streaming chunks
```

**Key Parameters:**
- `messages` - Conversation history
- `system` - System prompt guiding Claude's behavior
- `tools` - Available tools Claude can use
- `tool_choice` - Force specific tool or auto-select
- `fine_grained` - Enable fine-grained streaming mode

**With `fine_grained=True`:**
- Adds beta header: `["fine-grained-tool-streaming-2025-05-14"]`
- JSON validation disabled
- Chunks arrive immediately without buffering

**With `fine_grained=False` (default):**
- API validates chunks at key-value boundaries
- Only sends validated batches
- Safer but higher latency

---

#### `text_from_message(message)` — Lines 259-261

Extracts all text content from a message response.

```python
text = text_from_message(response)
# Joins all text blocks into single string
```

---

#### `run_tool(tool_name, tool_input)` — Lines 263-271

**Router function** that executes the correct tool based on its name.

```python
if tool_name == "get_weather":
    return get_weather(**tool_input)
elif tool_name == "get_air_quality":
    return get_air_quality(**tool_input)
```

This pattern makes it easy to add new tools without changing the streaming logic.

---

#### `run_tools(message)` — Lines 273-305

**Extracts all tool calls from Claude's response and executes them.**

**Key steps:**

1. **Extract tool requests** from response content blocks
```python
tool_requests = [
    block for block in message.content
    if block.type == "tool_use"
]
```

2. **Move tool_id extraction above try block** (prevents NameError)
```python
if hasattr(tool_request, 'id'):
    tool_id = tool_request.id
elif isinstance(tool_request, dict):
    tool_id = tool_request.get('id', 'unknown')
```

**Why this matters:** If tool extraction fails, `except` block needs `tool_id` to reference. Moving it above prevents `NameError`.

3. **Execute each tool**
```python
tool_output = run_tool(tool_name, tool_input)
```

4. **Format results for Claude**
```python
tool_result_block = {
    "type": "tool_result",
    "tool_use_id": tool_id,      # Links result to request
    "content": json.dumps(tool_output),
    "is_error": False
}
```

5. **Handle errors gracefully**
```python
except Exception as e:
    tool_result_block = {
        "type": "tool_result",
        "tool_use_id": tool_id,
        "content": f"Error {e}",
        "is_error": True
    }
```

---

### 4. **Main Conversation Loop**

#### `run_conversation(messages, fine_grained=False)` — Lines 307-400

**This is the heart of the agent.** It implements the multi-turn conversation loop.

**The Flow:**

```python
while True:
    # Step 1: Stream response from Claude
    with chat_stream(..., fine_grained=fine_grained) as stream:
        
        # Step 2: Process chunks in real-time
        for chunk in stream:
            if chunk.type == "content_block_delta":
                if hasattr(chunk.delta, 'text'):
                    print(chunk.delta.text, end="", flush=True)
            
            if chunk.type == "content_block_start":
                if chunk.content_block.type == "tool_use":
                    print(f'\n>>> Tool Call: "{chunk.content_block.name}" args: ', end="", flush=True)
            
            if chunk.type == "input_json":
                # Print tool arguments as they stream
                print(chunk.partial_json, end="", flush=True)
                
                if fine_grained:
                    # In fine-grained mode, JSON may be incomplete
                    try:
                        current_args = json.loads(chunk.snapshot)
                    except json.JSONDecodeError:
                        pass  # Incomplete fragment, keep accumulating
        
        # Step 3: Get final message after streaming completes
        response = stream.get_final_message()
    
    # Step 4: Add response to history
    messages.append({"role": "assistant", "content": response.content})
    
    # Step 5: Check if Claude is done
    if response.stop_reason != "tool_use":
        print()
        break
    
    # Step 6: Execute tools
    tool_results = run_tools(response)
    
    # Step 7: Add tool results and loop again
    messages.append({
        "role": "user",
        "content": tool_results
    })
```

---

## Streaming Chunk Types

When iterating through `stream`, you may receive different chunk types:

| Chunk Type | Purpose | Has |
|---|---|---|
| `message_start` | Initial response metadata | `message.stop_reason` |
| `content_block_start` | Beginning of text/tool block | `content_block.type`, `content_block.name` |
| `content_block_delta` | Streaming text or tool input | `delta.text` or `delta.input` |
| `content_block_stop` | End of a content block | — |
| `input_json` | Tool argument JSON | `partial_json`, `snapshot` |
| `message_delta` | Final message metadata | `delta.stop_reason` |
| `message_stop` | End of response | — |

---

## Example Output

### Standard Mode (`fine_grained=False`)

```
>>> Tool Call: "get_weather" args: {"location": "Delhi, India"}
>>> Tool Call: "get_air_quality" args: {"location": "Delhi, India"}

The weather in Delhi, India is currently:

**Temperature:** 30°C
**Condition:** Haze
**Humidity:** 55%
**Feels Like:** 29°C

Unfortunately, the air quality data could not be retrieved...
```

**Notice:** Tool arguments appear after they're fully validated.

---

### Fine-Grained Mode (`fine_grained=True`)

```
>>> Tool Call: "get_weather" args: {"location {"location": "Delhi", India"}
>>> Tool Call: "get_air_quality" args: {"location": "Delhi"...

The weather in Delhi, India is currently...
```

**Notice:** You see partial/incomplete JSON as it streams (`"{"location": "Delhi", India"}`), but by the final message they're complete and valid.

---

## Error Handling

### Fine-Grained JSON Parsing Error

```python
if chunk.type == "input_json":
    if fine_grained:
        try:
            current_args = json.loads(chunk.snapshot)
        except json.JSONDecodeError:
            # snapshot is incomplete: {"key": unde
            pass  # Silently continue, next chunk will complete it
```

This is **required in fine-grained mode** because `snapshot` may contain incomplete JSON like:
- `{"key": unde` (incomplete string value)
- `{"a": 1` (incomplete object)
- `[1, 2,` (incomplete array)

The final message from `stream.get_final_message()` is always valid JSON regardless.

---

### Tool Execution Error

```python
except Exception as e:
    tool_result_block = {
        "type": "tool_result",
        "tool_use_id": tool_id,
        "content": f"Error {e}",
        "is_error": True
    }
```

If a tool fails (network error, invalid location, etc.), we:
1. Catch the exception
2. Format it as a tool result
3. Send it back to Claude
4. Claude can retry, use different parameters, or inform the user

---

## Configuration Guide

### Enable Fine-Grained Mode

```python
# At the bottom of the file, change:
run_conversation(messages)

# To:
run_conversation(messages, fine_grained=True)
```

**Pros:**
- ⚡ Real-time progress on tool arguments
- 📊 More responsive for UI applications
- 🔍 See partial data immediately

**Cons:**
- ⚠️ Need JSON error handling
- 📝 More complex logic
- 🐌 Still need final message for authoritative data

---

### Add Your Own Tool

1. **Write the tool function:**
```python
def get_stock_price(symbol: str):
    """Fetch stock price for a symbol."""
    # Implementation
    return {
        "symbol": symbol,
        "price": 150.25
    }
```

2. **Create tool schema:**
```python
get_stock_tool_schema = ToolParam({
    "name": "get_stock_price",
    "description": "Fetches the current stock price for a given symbol",
    "input_schema": {
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "Stock ticker symbol (e.g., 'AAPL', 'GOOGL')"
            }
        },
        "required": ["symbol"]
    }
})
```

3. **Add to tool router:**
```python
def run_tool(tool_name, tool_input):
    if tool_name == "get_weather":
        return get_weather(**tool_input)
    elif tool_name == "get_stock_price":
        return get_stock_price(**tool_input)
```

4. **Add to conversation:**
```python
with chat_stream(
    messages,
    system=system_prompt,
    tools=[
        get_weather_tool_schema,
        get_air_quality_tool_schema,
        get_stock_tool_schema  # ← Add here
    ]
) as stream:
```

---

## Key Takeaways

| Concept | Key Point |
|---|---|
| **Standard Mode** | Safe, validated JSON, good for reliability |
| **Fine-Grained Mode** | Fast, immediate chunks, requires error handling |
| **Tool Schema** | Tells Claude what tools exist and what they expect |
| **Streaming Chunks** | Different types: text, tool calls, JSON args |
| **Multi-Turn** | Tool results are added as user message, Claude responds again |
| **Error Handling** | Always use try/except in fine-grained mode for JSON |
| **Final Message** | `stream.get_final_message()` is always valid regardless of mode |

---

## Running the Code

```bash
# Install dependencies
pip install anthropic python-dotenv requests

# Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Run
python 03-Toolcall-and-streaming.py
```

**Expected Output:**
```
>>> Tool Call: "get_weather" args: {"location": "Delhi, India"}
>>> Tool Call: "get_air_quality" args: {"location": "Delhi, India"}
[Weather data and response from Claude]
```

---

## Troubleshooting

| Issue | Solution |
|---|---|
| `ModuleNotFoundError: anthropic` | Run `pip install anthropic` |
| `api_key not found` | Set `ANTHROPIC_API_KEY` environment variable |
| `connection timeout` | Check internet connection, increase timeout |
| `JSONDecodeError in fine-grained` | Expected! Wrap `json.loads()` in try/except |
| `Tool not found` | Add tool to `run_tool()` router function |
| `Invalid location error` | Tools validate input; Claude will retry with corrections |

---

## References

- [Anthropic Claude API Documentation](https://docs.anthropic.com)
- [Tool Use Guide](https://docs.anthropic.com/en/docs/build-a-system-with-claude/tool-use)
- [Streaming Documentation](https://docs.anthropic.com/en/docs/guides/streaming)
- [wttr.in Weather API](https://wttr.in)
- [WAQI Air Quality API](https://waqi.info)
