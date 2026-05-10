# Complete Guide to Tool Use with Claude

## Table of Contents
1. [Tool Use Fundamentals](#tool-use-fundamentals)
2. [Types of Tools](#types-of-tools)
3. [Tool Use Patterns](#tool-use-patterns)
4. [Streaming with Tools](#streaming-with-tools)
5. [Batch Processing](#batch-processing)
6. [Real-World Tool Examples](#real-world-tool-examples)
7. [Best Practices](#best-practices)
8. [Comparison Table](#comparison-table)

---

## Tool Use Fundamentals

### What Are Tools?

Tools are **functions that Claude can call to perform actions** beyond just generating text. They extend Claude's capabilities by enabling:
- File system operations (read, write, edit)
- Web searches for current information
- API calls to external services
- Database queries
- Custom business logic

### How Tool Use Works

```
User: "Create a Python file with hello world"
    ↓
Claude: "I'll create that file for you"
Claude requests: tool_use(name="create_file", input={...})
    ↓
Your code: Executes text_editor_tool.create(...)
    ↓
You return: "File created successfully"
    ↓
Claude: Reads result, says "I've created the file"
```

### Key Concept: Schema vs Implementation

| Aspect | Schema | Implementation |
|---|---|---|
| **What it is** | JSON definition of tool interface | Actual Python function |
| **Who provides** | You (custom) or Claude (built-in) | You always |
| **Purpose** | Tells Claude what tool exists | Executes when Claude calls it |
| **Example** | `{"name": "get_weather", "input_schema": {...}}` | `def get_weather(location): ...` |

---

## Types of Tools

### 1. Custom Tools (You Implement Everything)

**When:** You need specialized functionality for your application

**You provide:**
- JSON schema (interface)
- Python implementation (function)
- Error handling
- Validation

```python
# Schema (tell Claude about tool)
weather_schema = ToolParam({
    "name": "get_weather",
    "description": "Get weather for a location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string"}
        },
        "required": ["location"]
    }
})

# Implementation (actual function)
def get_weather(location: str):
    response = requests.get(f"https://wttr.in/{location}?format=j1")
    return response.json()

# Router (direct Claude requests to function)
def run_tool(tool_name, tool_input):
    if tool_name == "get_weather":
        return get_weather(**tool_input)
```

**Examples:**
- Weather API tool
- Air quality tool
- Custom database queries
- Business logic functions

---

### 2. Built-in Tools (Claude/Anthropic Provides Implementation)

**When:** Anthropic has already built the tool for you

**You provide:**
- Schema configuration (small stub)
- Tool execution routing (pass-through)

**Anthropic provides:**
- Full implementation
- API integration
- Error handling

#### A. Text Editor Tool

```python
# You only provide this small schema stub
text_editor_schema = {
    "type": "text_editor_20250728",  # Version for your model
    "name": "str_replace_based_edit_tool"
}

# API automatically:
# - Views files
# - Creates files  
# - Replaces text
# - Inserts lines
# - Undoes edits
```

**Capabilities:**
- `view`: Display file/directory contents
- `create`: Create new file
- `str_replace`: Replace exact text (exactly once)
- `insert`: Insert at line number
- `undo_edit`: Restore from backup

**Best For:**
- File manipulation
- Code generation
- Content creation
- Local file operations

---

#### B. Web Search Tool

```python
# You only provide schema configuration
web_search_schema = {
    "type": "web_search_20250305",     # Latest version
    "name": "web_search",
    "max_uses": 5,                     # Rate limit
    "allowed_domains": ["nih.gov"]     # Domain filtering
}

# API automatically:
# - Searches the web
# - Filters by domain
# - Returns relevant results
# - Respects rate limits
```

**Configuration Options:**
- `type`: Schema version (changes with API updates)
- `name`: Tool identifier Claude uses
- `max_uses`: Maximum searches per conversation
- `allowed_domains`: Safety - only return from trusted sources

**Domain Filtering Examples:**
```python
# Medical research
"allowed_domains": ["nih.gov", "pubmed.ncbi.nlm.nih.gov"]

# News articles
"allowed_domains": ["bbc.com", "reuters.com", "apnews.com"]

# Academic papers
"allowed_domains": ["arxiv.org", "scholar.google.com"]

# No restrictions
"allowed_domains": []  # Empty = search anywhere
```

**Best For:**
- Current events
- Real-time information
- Beyond training cutoff data
- Authoritative sources

---

## Tool Use Patterns

### Pattern 1: Single-Turn Tool Use

**Flow:** User question → Claude uses tool → Response

```python
def single_turn_tool_use():
    messages = []
    
    # Step 1: Add user query
    messages.append({
        "role": "user",
        "content": "What's the weather in London?"
    })
    
    # Step 2: Call Claude with tools available
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=messages,
        tools=[weather_tool_schema]
    )
    
    # Step 3: If tool was called, execute it
    if response.stop_reason == "tool_use":
        tool_call = response.content[0]  # Get first tool call
        result = run_tool(tool_call.name, tool_call.input)
        
        # Add result and ask Claude for final response
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": json.dumps(result)
            }]
        })
        
        # Get final response
        final = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            messages=messages
        )
        
        print(final.content[0].text)
```

**When to Use:**
- Simple queries requiring one tool call
- Quick information lookups
- No complex decision-making needed

---

### Pattern 2: Multi-Turn Tool Use (Agent Loop)

**Flow:** User → Claude → Tool → Claude → Tool → ... → Response

```python
def multi_turn_tool_use():
    messages = []
    system_prompt = "You are a helpful assistant with access to weather and air quality tools."
    
    # Initial user query
    messages.append({"role": "user", "content": "Tell me about Delhi's weather and air quality"})
    
    # Loop until Claude doesn't need tools
    while True:
        # Call Claude with available tools
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            messages=messages,
            system=system_prompt,
            tools=[weather_schema, air_quality_schema]
        )
        
        # Add Claude's response
        messages.append({"role": "assistant", "content": response.content})
        
        # Print any text
        for block in response.content:
            if block.type == "text":
                print(block.text)
        
        # Check if Claude finished (no more tool requests)
        if response.stop_reason != "tool_use":
            break
        
        # Execute all tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                try:
                    output = run_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(output),
                        "is_error": False
                    })
                except Exception as e:
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(e),
                        "is_error": True
                    })
        
        # Add tool results and loop
        messages.append({"role": "user", "content": tool_results})
    
    return messages
```

**When to Use:**
- Complex queries requiring multiple steps
- Tools depend on results from other tools
- Agent-like behavior needed
- Interactive problem-solving

---

## Streaming with Tools

### What is Streaming with Tools?

Streaming allows you to see **real-time progress** on tool argument generation and text generation, including:
- Text as Claude types it
- Tool arguments as they're generated
- Tool names immediately when called

### Two Streaming Modes

#### Mode 1: Standard Streaming (Default)

```python
def standard_streaming_with_tools():
    messages = []
    messages.append({"role": "user", "content": "Get weather for Delhi and New York"})
    
    # Stream with standard mode (default)
    with client.messages.stream(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=messages,
        tools=[weather_schema]
    ) as stream:
        for chunk in stream:
            # Handle text streaming
            if chunk.type == "content_block_delta":
                if hasattr(chunk.delta, 'text'):
                    print(chunk.delta.text, end="", flush=True)
            
            # Detect tool calls
            if chunk.type == "content_block_start":
                if chunk.content_block.type == "tool_use":
                    print(f"\n>>> Calling: {chunk.content_block.name}")
            
            # Handle tool arguments
            if chunk.type == "input_json":
                print(f" args: {chunk.partial_json}", end="", flush=True)
        
        # Get final message after streaming
        response = stream.get_final_message()
        
        # Execute any tools
        if response.stop_reason == "tool_use":
            # Process tools...
```

**Characteristics:**
- ✅ API validates JSON at key-value pair boundaries
- ✅ `snapshot` always contains valid JSON
- ✅ Safe to call `json.loads(snapshot)`
- ⚠️ May see delays between key-value pairs (buffering)

**Output Example:**
```
Getting weather information...
>>> Calling: get_weather args: {"location": "Delhi, India"}
>>> Calling: get_weather args: {"location": "New York"}

Temperature in Delhi is 30°C...
```

---

#### Mode 2: Fine-Grained Streaming

```python
def fine_grained_streaming_with_tools():
    messages = []
    messages.append({"role": "user", "content": "Get weather for Delhi"})
    
    # Stream with fine-grained mode enabled
    with client.messages.stream(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=messages,
        tools=[weather_schema],
        betas=["fine-grained-tool-streaming-2025-05-14"]  # Enable fine-grained
    ) as stream:
        for chunk in stream:
            # Text handling same as standard
            if chunk.type == "content_block_delta":
                if hasattr(chunk.delta, 'text'):
                    print(chunk.delta.text, end="", flush=True)
            
            # Tool calls same
            if chunk.type == "content_block_start":
                if chunk.content_block.type == "tool_use":
                    print(f"\n>>> Tool: {chunk.content_block.name} args: ", end="", flush=True)
            
            # IMPORTANT: In fine-grained mode, JSON may be incomplete
            if chunk.type == "input_json":
                print(chunk.partial_json, end="", flush=True)
                
                # Must handle invalid JSON in fine-grained mode
                try:
                    parsed = json.loads(chunk.snapshot)
                except json.JSONDecodeError:
                    pass  # Incomplete JSON, keep accumulating
        
        response = stream.get_final_message()
```

**Characteristics:**
- ❌ API validation **DISABLED**
- ⚡ Chunks arrive **immediately** (no buffering)
- ⚠️ `snapshot` may be incomplete/invalid JSON
- 🛡️ **MUST** wrap `json.loads()` in try/except
- ✅ Final message always has valid JSON

**Key Difference Visualization:**

```
Standard Mode:
{... → validate → send burst
↑                    ↑
Wait for complete   Send when valid

Fine-grained Mode:
{... → send immediately
↑
No validation, immediate chunks
```

---

### Streaming Implementation Comparison

| Aspect | Standard | Fine-Grained |
|---|---|---|
| **JSON Validation** | ✅ Enabled | ❌ Disabled |
| **Chunk Timing** | Batched (after validation) | Immediate |
| **Latency** | Higher | Lower |
| **JSON Safety** | Always valid | May be invalid |
| **Error Handling** | Not needed | try/except required |
| **Use Case** | Reliability | Real-time responsiveness |
| **Display** | Clean batches | Partial streams |

---

## Batch Processing

### What is Batch Processing?

Batch processing allows you to submit **multiple requests at once** and retrieve results asynchronously, optimized for cost and throughput.

### Single Request vs Batch

**Single Request Pattern:**
```python
# Request 1 → Response 1
# Request 2 → Response 2  
# Request 3 → Response 3
# Total: 3 API calls, 3 round-trips

for user_query in user_queries:
    response = client.messages.create(...)  # Individual call
```

**Batch Processing Pattern:**
```python
# [Request 1, Request 2, Request 3] → Batch submit
# API processes asynchronously
# [Response 1, Response 2, Response 3] → Retrieve
# Total: 1 API call, 1 batch + 1 retrieve

batch_requests = [
    {"custom_id": "req-1", "params": {...}},
    {"custom_id": "req-2", "params": {...}},
    {"custom_id": "req-3", "params": {...}}
]
batch = client.messages.batches.create(requests=batch_requests)
```

---

### Batch Processing Implementation

```python
def batch_processing_example():
    """
    Process multiple requests efficiently using batches.
    
    Use case: Analyze 100 customer feedback texts
    Without batch: 100 API calls
    With batch: 1 batch submission + 1 retrieval
    """
    
    # Step 1: Prepare multiple requests
    requests = []
    
    feedback_texts = [
        "Product works great!",
        "Terrible quality",
        "Average experience",
        # ... 97 more
    ]
    
    for i, feedback in enumerate(feedback_texts):
        requests.append({
            "custom_id": f"feedback-{i}",
            "params": {
                "model": "claude-sonnet-4-5",
                "max_tokens": 100,
                "messages": [
                    {
                        "role": "user",
                        "content": f"Analyze sentiment: {feedback}"
                    }
                ]
            }
        })
    
    # Step 2: Submit batch
    print(f"Submitting {len(requests)} requests in batch...")
    batch = client.messages.batches.create(requests=requests)
    batch_id = batch.id
    
    print(f"Batch ID: {batch_id}")
    print(f"Status: {batch.processing_status}")
    
    # Step 3: Poll for completion (or set up webhook)
    import time
    max_retries = 60
    retry_count = 0
    
    while retry_count < max_retries:
        batch_status = client.messages.batches.retrieve(batch_id)
        
        if batch_status.processing_status == "succeeded":
            print("Batch completed!")
            break
        elif batch_status.processing_status == "failed":
            print("Batch failed!")
            return None
        
        print(f"Status: {batch_status.processing_status}")
        time.sleep(5)
        retry_count += 1
    
    # Step 4: Retrieve results
    results = []
    with client.messages.batches.results(batch_id) as results_iter:
        for result in results_iter:
            results.append({
                "id": result.custom_id,
                "response": result.message
            })
    
    return results
```

---

### When to Use Batching

**✅ Good Use Cases:**
- Processing 10+ requests
- Bulk content generation
- Batch analysis tasks
- Cost optimization important
- Speed not critical (asynchronous OK)
- Scheduled jobs

**❌ NOT Good For:**
- Real-time chat
- Interactive conversations
- Single requests
- Speed critical
- Multi-turn loops with dependencies

---

### Cost Comparison

```
Individual Requests (100 queries):
- 100 API calls
- Full price per request
- Example: 100 × $0.01 = $1.00

Batch Processing (100 queries):
- 1 batch submission + 1 retrieval
- 50% discount on requests
- Example: 100 × $0.01 × 0.5 = $0.50

Savings: 50% cost reduction
```

---

## Real-World Tool Examples

### Example 1: Weather and Air Quality Agent

**Goal:** Provide comprehensive location information

**Tools Used:**
1. Custom: `get_weather` (wttr.in API)
2. Custom: `get_air_quality` (waqi.info API)

**Code Pattern:**
```python
def weather_quality_agent():
    messages = []
    system = "Provide weather and air quality for locations"
    
    messages.append({
        "role": "user",
        "content": "What's the weather and air quality in Delhi?"
    })
    
    # Multi-turn loop
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            messages=messages,
            system=system,
            tools=[get_weather_schema, get_air_quality_schema]
        )
        
        messages.append({"role": "assistant", "content": response.content})
        print(text_from_message(response))
        
        if response.stop_reason != "tool_use":
            break
        
        # Execute tools
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                if block.name == "get_weather":
                    result = get_weather(block.input["location"])
                elif block.name == "get_air_quality":
                    result = get_air_quality(block.input["location"])
                
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                    "is_error": False
                })
        
        messages.append({"role": "user", "content": tool_results})
```

**Output:**
```
>>> Tool Call: "get_weather" args: {"location": "Delhi, India"}
>>> Tool Call: "get_air_quality" args: {"location": "Delhi, India"}

Weather in Delhi is 30°C with haze. Air quality is unhealthy...
```

---

### Example 2: Text Editor for Code Generation

**Goal:** Claude generates and creates code files

**Tools Used:**
1. Built-in: `str_replace_based_edit_tool`

**Code Pattern:**
```python
def code_generation_agent():
    messages = []
    system = "You are a Python expert. Create files as requested."
    
    messages.append({
        "role": "user",
        "content": "Create a Python file that calculates fibonacci numbers"
    })
    
    # Conversation with text editor tool
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            messages=messages,
            system=system,
            tools=[get_text_edit_schema("claude-sonnet-4-5")]
        )
        
        messages.append({"role": "assistant", "content": response.content})
        print(text_from_message(response))
        
        if response.stop_reason != "tool_use":
            break
        
        # Process tool calls (API handles implementation)
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                # In real implementation, Anthropic API executes this
                # We just pass it through
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": "Tool executed successfully",
                    "is_error": False
                })
        
        messages.append({"role": "user", "content": tool_results})
```

**Output:**
```
>>> Tool Call: "str_replace_based_edit_tool" command: create
  path: "fibonacci.py"
  
I've created a fibonacci.py file with...
```

---

### Example 3: Research with Web Search

**Goal:** Find current information and synthesize it

**Tools Used:**
1. Built-in: `web_search`

**Code Pattern:**
```python
def research_agent():
    messages = []
    system = "Search the web for current information when needed"
    
    messages.append({
        "role": "user",
        "content": "What are the latest AI developments in 2025?"
    })
    
    # Multi-turn with web search
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            messages=messages,
            system=system,
            tools=[{
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 5,
                "allowed_domains": ["arxiv.org", "techcrunch.com", "openai.com"]
            }]
        )
        
        messages.append({"role": "assistant", "content": response.content})
        print(text_from_message(response))
        
        if response.stop_reason != "tool_use":
            break
        
        # Web search results handled by API
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                # API searches and returns results
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": "Search results retrieved",
                    "is_error": False
                })
        
        messages.append({"role": "user", "content": tool_results})
```

**Output:**
```
Claude requested web search...
Searching for: "latest AI developments 2025"
Found results from arxiv.org, techcrunch.com...

Based on the latest research, key AI developments include...
```

---

## Best Practices

### 1. Error Handling

```python
def robust_tool_execution(tool_name, tool_input):
    """Execute tool with comprehensive error handling."""
    try:
        if tool_name == "get_weather":
            if not tool_input.get("location"):
                raise ValueError("Location is required")
            return get_weather(tool_input["location"])
        
        elif tool_name == "get_air_quality":
            location = tool_input.get("location")
            if not location:
                raise ValueError("Location is required")
            return get_air_quality(location)
        
        else:
            raise Exception(f"Unknown tool: {tool_name}")
    
    except ValueError as e:
        return {"error": f"Validation error: {str(e)}"}
    except ConnectionError as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
```

---

### 2. Input Validation

```python
def validate_tool_input(tool_name, tool_input):
    """Validate tool input before execution."""
    
    if tool_name == "get_weather":
        required = ["location"]
        for field in required:
            if field not in tool_input:
                raise ValueError(f"Missing required field: {field}")
        
        location = tool_input["location"]
        if not isinstance(location, str) or len(location) == 0:
            raise ValueError("Location must be non-empty string")
    
    return True
```

---

### 3. Tool Result Formatting

```python
def format_tool_result(tool_use_id, result, is_error=False):
    """Properly format tool result for Claude."""
    return {
        "type": "tool_result",
        "tool_use_id": tool_use_id,
        "content": json.dumps(result) if not isinstance(result, str) else result,
        "is_error": is_error
    }
```

---

### 4. Preventing Infinite Loops

```python
def safe_multi_turn_tool_use(messages, max_iterations=10):
    """Multi-turn tool use with safety limits."""
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            messages=messages,
            tools=[tool_schema]
        )
        
        messages.append({"role": "assistant", "content": response.content})
        
        if response.stop_reason != "tool_use":
            break
        
        # Process tools...
    
    if iteration >= max_iterations:
        print("Warning: Max iterations reached")
    
    return messages
```

---

### 5. Streaming Best Practices

```python
def streaming_with_tool_tracking():
    """Track streaming progress and tool calls."""
    tool_calls = []
    current_tool = None
    
    with client.messages.stream(...) as stream:
        for chunk in stream:
            # Track tool calls
            if chunk.type == "content_block_start":
                if chunk.content_block.type == "tool_use":
                    current_tool = {
                        "id": chunk.content_block.id,
                        "name": chunk.content_block.name,
                        "input": ""
                    }
                    print(f"\n📞 Calling: {chunk.content_block.name}")
            
            # Stream tool arguments
            if chunk.type == "input_json" and current_tool:
                current_tool["input"] += chunk.partial_json
                print(chunk.partial_json, end="", flush=True)
            
            # Stream text
            if chunk.type == "content_block_delta":
                if hasattr(chunk.delta, 'text'):
                    print(chunk.delta.text, end="", flush=True)
            
            # Finalize tool call
            if chunk.type == "content_block_stop" and current_tool:
                tool_calls.append(current_tool)
                current_tool = None
        
        response = stream.get_final_message()
    
    return response, tool_calls
```

---

## Comparison Table

### Tool Characteristics

| Feature | Custom Tools | Text Editor | Web Search |
|---|---|---|---|
| **Implementation** | You write | Anthropic | Anthropic |
| **Schema** | Full schema | Stub only | Stub only |
| **Setup Complexity** | Complex | Simple | Simple |
| **Examples** | Weather, API | Files | Research |
| **Data Source** | External APIs | File system | Web |
| **Real-time** | Depends | Yes | Yes |
| **Cost** | Included | Included | Included |

---

### Execution Patterns

| Pattern | Single-Turn | Multi-Turn | Streaming | Batch |
|---|---|---|---|---|
| **Complexity** | Simple | Complex | Moderate | Moderate |
| **Speed** | Slow (1+ calls) | Slow (many calls) | Fast | Slow (async) |
| **Cost** | Normal | Normal | Normal | 50% off |
| **Use Case** | Simple Q&A | Agent loops | Real-time | Bulk |
| **Interactive** | No | Yes | Yes | No |
| **Tool Use** | Yes | Yes | Yes | Yes |

---

### Streaming Modes

| Mode | Standard | Fine-Grained |
|---|---|---|
| **JSON Valid** | Always | Sometimes |
| **Buffering** | Yes | No |
| **Error Handling** | Not needed | Required |
| **Responsiveness** | Moderate | High |
| **Setup** | Default | Beta flag |
| **Best For** | Reliability | Real-time UX |

---

## Quick Reference

### Single Tool Call
```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=messages,
    tools=[tool_schema]
)
```

### Multi-Turn Tool Loop
```python
while response.stop_reason == "tool_use":
    tool_results = run_tools(response)
    messages.append({"role": "user", "content": tool_results})
    response = client.messages.create(...)
```

### Streaming with Tools
```python
with client.messages.stream(tools=[...]) as stream:
    for chunk in stream:
        # Process chunks
    response = stream.get_final_message()
```

### Batch Processing
```python
batch = client.messages.batches.create(requests=batch_requests)
# Wait for completion
batch_status = client.messages.batches.retrieve(batch.id)
# Get results
results = client.messages.batches.results(batch.id)
```

---

## Summary

**Tool Use enables Claude to:**
- ✅ Perform actions beyond text generation
- ✅ Access real-time information
- ✅ Work with files and systems
- ✅ Integrate with your applications
- ✅ Build autonomous agents

**Choose your pattern:**
- **Single-turn:** Quick, simple queries
- **Multi-turn:** Complex, multi-step tasks
- **Streaming:** Real-time responsiveness
- **Batch:** Cost optimization for bulk processing

**Combine for maximum power:**
- Multi-turn + streaming = Interactive agent with real-time feedback
- Multi-turn + tools = Autonomous problem-solving
- Batch + tools = Scalable bulk processing
- Streaming + web search = Real-time research agent
