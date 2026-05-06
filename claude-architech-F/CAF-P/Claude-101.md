# Claude 101: Complete Learning Guide

A comprehensive guide to understanding Claude, the Claude API, and best practices for building AI applications.

---

## Table of Contents

1. [What is Claude?](#what-is-claude)
2. [Claude Models](#claude-models)
3. [Claude Code vs Claude API](#claude-code-vs-claude-api)
4. [Getting Started](#getting-started)
5. [Prompt Engineering](#prompt-engineering)
6. [Tool Use & Function Calling](#tool-use--function-calling)
7. [Advanced Features](#advanced-features)
8. [Best Practices](#best-practices)
9. [Real-World Examples](#real-world-examples)

---

## What is Claude?

Claude is Anthropic's AI assistant - a large language model (LLM) trained with **Constitutional AI** to be helpful, harmless, and honest.

### Key Characteristics:

- **Context Window**: 200k tokens (all models)
- **Training Data**: Up to April 2024
- **Strengths**:
  - Long-form text analysis & generation
  - Code understanding & generation
  - Reasoning & problem-solving
  - Safety & responsible AI
  - Multi-turn conversations

### Constitutional AI:
Claude is trained using Constitutional AI, which means it's guided by a set of principles to:
- Be helpful and honest
- Decline harmful requests
- Admit uncertainty
- Consider multiple perspectives

---

## Claude Models

### Current Model Lineup (May 2026)

| Model | Release | Speed | Intelligence | Cost | Use Case |
|---|---|---|---|---|---|
| **Claude Opus 4.7** | Latest | Slower | Highest | Highest | Complex reasoning, research, strategic tasks |
| **Claude Sonnet 4.6** | Mid-tier | Medium | High | Medium | **Default choice** - best balance |
| **Claude Haiku 4.5** | Fast | Fastest | Good | Lowest | Streaming, real-time, cost-sensitive tasks |

### Choosing the Right Model:

```
Complex reasoning task? → Use Opus 4.7
Balanced need? → Use Sonnet 4.6 (recommended)
Speed critical? → Use Haiku 4.5
```

### Key Model Properties:

- **Context Window**: All models = 200k tokens
- **Streaming**: Supported on all models
- **Tool Use**: Supported on all models
- **Caching**: Supported on all models

---

## Claude Code vs Claude API

### Claude Code (CLI)

**Best for**: Interactive development, quick prototyping, debugging

```bash
claude                    # Start interactive session
claude -p "your prompt"  # Headless one-shot
```

**Features**:
- Full IDE integration (VSCode, JetBrains)
- File system access
- Git integration
- Built-in tools (bash, file editing)
- Memory & session management
- Auto-accept mode (`Shift+Tab`)

### Claude API

**Best for**: Production apps, integrations, programmatic access

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**Features**:
- REST API or SDKs (Python, JS, etc.)
- Tool use / function calling
- Prompt caching
- Batch API
- Fine-tuning (coming soon)
- Message history management
- Custom system prompts

### When to Use Which?

| Use Case | Claude Code | Claude API |
|---|---|---|
| Development & debugging | ✅ | ❌ |
| Production applications | ❌ | ✅ |
| One-off analysis | ✅ | ❌ |
| Integrations with existing apps | ❌ | ✅ |
| Real-time chat UI | ❌ | ✅ |
| File editing workflows | ✅ | ❌ |

---

## Getting Started

### Installation

#### Claude Code (CLI)

```powershell
# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex

# macOS/Linux
curl -fsSL https://claude.ai/install.sh | sh
```

```bash
# Verify installation
claude --version
claude auth status
```

#### Claude API

```bash
# Install Python SDK
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."  # Linux/macOS
$env:ANTHROPIC_API_KEY="sk-ant-..."   # PowerShell
```

### Your First Interaction

#### Claude Code

```bash
claude
# Type: Hello! Tell me about yourself.
# Interact naturally...
```

#### Claude API

```python
from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello! Tell me about yourself."}
    ]
)

print(response.content[0].text)
```

---

## Prompt Engineering

Prompt engineering is the art of structuring requests to get better responses from Claude.

### Principle 1: Clarity & Specificity

**❌ Bad:**
```
Write code for a calculator.
```

**✅ Good:**
```
Create a Python function that implements a simple calculator.
It should accept two numbers and an operator (+, -, *, /).
Return the result or raise a ValueError for invalid operators.
Include docstring and type hints.
```

### Principle 2: Role & Context

**❌ Bad:**
```
Explain machine learning.
```

**✅ Good:**
```
You are a senior data scientist explaining ML to a junior developer
who has basic Python knowledge but no ML experience.
Explain the concept of supervised learning using a simple analogy.
Keep it to 2-3 paragraphs.
```

### Principle 3: Examples (Few-Shot Prompting)

```
Convert these function names to snake_case:

Example:
Input: calculateTotal
Output: calculate_total

Now convert:
Input: getUserById
Output: ?
```

### Principle 4: Step-by-Step Reasoning (Chain of Thought)

```
Let's think step by step:
1. First, identify the key requirements
2. Then, sketch the architecture
3. Next, implement each component
4. Finally, add error handling and tests

Problem: [Your problem here]
```

### Principle 5: System Prompts

System prompts define Claude's behavior for the entire conversation.

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="You are a helpful coding assistant. Always provide working code examples.",
    messages=[
        {"role": "user", "content": "How do I read a file in Python?"}
    ]
)
```

### Principle 6: Output Formatting

**Request specific format:**

```
Respond in JSON format with the following structure:
{
  "summary": "one line summary",
  "key_points": ["point1", "point2", ...],
  "code_example": "python code here"
}
```

### Prompt Template Formula

```
[ROLE/CONTEXT]
You are [specific role]. [Relevant background].

[TASK]
Your task is to [specific action].

[CONSTRAINTS]
- [Constraint 1]
- [Constraint 2]
- [Output format: JSON]

[EXAMPLES]
Example input: [example]
Example output: [example]

[ACTUAL REQUEST]
[Your actual request]
```

---

## Tool Use & Function Calling

Tool use allows Claude to interact with external systems (APIs, databases, file systems, etc.).

### What is Tool Use?

- Claude can request to call functions
- You define what functions are available
- Claude decides when to use them
- You execute and return results
- Claude processes results and responds

### Simple Tool Use Example

```python
import anthropic
import json

client = anthropic.Anthropic()

# Define tools available to Claude
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name"
                }
            },
            "required": ["location"]
        }
    }
]

# Initial request
messages = [
    {"role": "user", "content": "What's the weather in Paris?"}
]

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

# Handle tool use
while response.stop_reason == "tool_use":
    # Claude wants to call a tool
    for block in response.content:
        if block.type == "tool_use":
            tool_name = block.name
            tool_input = block.input
            
            # Execute the tool (mock implementation)
            if tool_name == "get_weather":
                result = f"Weather in {tool_input['location']}: 20°C, Sunny"
            
            # Add tool result to conversation
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    }
                ]
            })
    
    # Get Claude's next response
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

# Final response
print(response.content[0].text)
```

### Tool Use Best Practices

1. **Clear Descriptions**: Make tool purposes obvious
2. **Specific Input Schemas**: Use JSON Schema to define precise inputs
3. **Error Handling**: Return meaningful error messages
4. **Limit Tools**: Only expose necessary tools
5. **Rate Limiting**: Monitor and limit tool calls
6. **Logging**: Track which tools are called and when

---

## Advanced Features

### 1. Prompt Caching

**What it does**: Caches large context to reduce latency and cost

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are a code reviewer. Be thorough but constructive."
        },
        {
            "type": "text",
            "text": large_documentation,
            "cache_control": {"type": "ephemeral"}  # Cache this
        }
    ],
    messages=[
        {"role": "user", "content": "Review this code: [code]"}
    ]
)
```

**Benefits**:
- 90% cheaper on cached tokens
- Lower latency on subsequent requests
- Perfect for large system prompts or documents

### 2. Extended Thinking (Coming Soon)

Enables Claude to "think" through complex problems before answering.

```python
# Format (when available):
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # How long to "think"
    },
    messages=[...]
)
```

### 3. Batch API

Process multiple requests efficiently in production.

```python
# Create batch job
batch = client.beta.messages.batches.create(
    requests=[
        {
            "custom_id": "task-1",
            "params": {
                "model": "claude-sonnet-4-6",
                "max_tokens": 100,
                "messages": [{"role": "user", "content": "..."}]
            }
        },
        # More requests...
    ]
)

# Check status
status = client.beta.messages.batches.retrieve(batch.id)

# Get results when ready
results = client.beta.messages.batches.results(batch.id)
```

### 4. Vision (Image Understanding)

Claude can analyze images and diagrams.

```python
import base64

with open("image.jpg", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": "What's in this image?"
                }
            ]
        }
    ]
)
```

### 5. Files API

Work with files in conversations without re-uploading.

```python
# Upload a file
file = client.beta.files.upload(
    file=open("document.pdf", "rb"),
)

# Reference in messages
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": file.id
                    }
                },
                {
                    "type": "text",
                    "text": "Summarize this document"
                }
            ]
        }
    ]
)
```

---

## Best Practices

### 1. System Prompt Design

```python
system_prompt = """
You are an expert Python developer.
Your role is to provide clear, production-ready code.

Guidelines:
- Always include error handling
- Write comments for complex logic
- Follow PEP 8 style guide
- Provide explanations
- Suggest alternatives when appropriate
"""
```

### 2. Message History Management

```python
messages = []

# Add user message
messages.append({
    "role": "user",
    "content": "What's 2+2?"
})

# Get response
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=100,
    messages=messages
)

# Add assistant response to history
messages.append({
    "role": "assistant",
    "content": response.content[0].text
})

# Keep conversation going with history
messages.append({
    "role": "user",
    "content": "Add 5 to that result"
})

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=100,
    messages=messages
)
```

### 3. Error Handling

```python
import anthropic

client = anthropic.Anthropic()

try:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
except anthropic.APIError as e:
    print(f"API Error: {e}")
except anthropic.AuthenticationError:
    print("Invalid API key")
except anthropic.RateLimitError:
    print("Rate limited - wait before retrying")
```

### 4. Cost Optimization

- Use **Haiku** for simple tasks
- Enable **prompt caching** for repeated requests
- Use **batch API** for non-urgent bulk work
- Monitor usage with `/stats` / `/cost`

### 5. Safety & Responsible Use

- Never ask Claude to help with:
  - Illegal activities
  - Deception or fraud
  - Abuse or harassment
  - Weapons development
- Be transparent about Claude's limitations
- Review Claude's outputs before using
- Don't rely on Claude for critical decisions

### 6. Testing

```python
def test_claude_response():
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=100,
        messages=[{"role": "user", "content": "2+2=?"}]
    )
    
    assert "4" in response.content[0].text
    assert response.stop_reason == "end_turn"
```

---

## Real-World Examples

### Example 1: Code Review Bot

```python
def review_code(code: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system="""You are a senior code reviewer.
        Provide constructive feedback on:
        - Code quality and readability
        - Performance issues
        - Security concerns
        - Best practices
        Keep feedback concise but thorough.""",
        messages=[
            {
                "role": "user",
                "content": f"Please review this code:\n\n{code}"
            }
        ]
    )
    return response.content[0].text
```

### Example 2: Multi-Turn Conversation

```python
def interactive_conversation():
    messages = []
    
    while True:
        user_input = input("You: ")
        
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system="You are a helpful assistant.",
            messages=messages
        )
        
        assistant_message = response.content[0].text
        messages.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        print(f"\nAssistant: {assistant_message}\n")
```

### Example 3: Data Analysis with Claude

```python
def analyze_data(csv_data: str) -> dict:
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"""Analyze this CSV data and provide:
                1. Summary statistics
                2. Trends and patterns
                3. Anomalies
                4. Recommendations
                
                CSV Data:
                {csv_data}
                
                Respond in JSON format."""
            }
        ]
    )
    
    import json
    return json.loads(response.content[0].text)
```

### Example 4: API Integration with Tool Use

```python
def customer_support_agent():
    tools = [
        {
            "name": "lookup_order",
            "description": "Look up customer order details",
            "input_schema": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Customer order ID"
                    }
                },
                "required": ["order_id"]
            }
        },
        {
            "name": "refund_order",
            "description": "Process a refund for an order",
            "input_schema": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order ID to refund"
                    }
                },
                "required": ["order_id"]
            }
        }
    ]
    
    messages = [
        {"role": "user", "content": "I want to return order #12345"}
    ]
    
    # Continue until Claude doesn't need tools
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        if response.stop_reason != "tool_use":
            return response.content[0].text
        
        # Process tool calls
        for block in response.content:
            if block.type == "tool_use":
                if block.name == "lookup_order":
                    result = f"Order found: Status=Shipped, Amount=$50"
                elif block.name == "refund_order":
                    result = "Refund processed successfully"
                
                messages.append({"role": "assistant", "content": response.content})
                messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    }]
                })
                break
```

---

## Key Takeaways

1. **Claude is powerful but not perfect** - Always review outputs
2. **Prompt quality matters** - Spend time on clear prompts
3. **Tool use extends capabilities** - Integrate with your systems
4. **Context window is generous** - Use it for providing context
5. **Cost optimization is possible** - Choose right model and features
6. **Security is paramount** - Never expose API keys
7. **Multi-turn conversations work well** - Keep context for better results

---

## Resources

- [Anthropic Documentation](https://docs.anthropic.com)
- [Claude API Reference](https://docs.anthropic.com/en/api)
- [Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [JavaScript SDK](https://github.com/anthropics/anthropic-sdk-js)

---

*Last Updated: May 2026*
*For latest information, visit docs.anthropic.com*
