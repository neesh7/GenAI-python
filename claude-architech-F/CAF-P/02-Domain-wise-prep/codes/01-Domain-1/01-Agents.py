"""
Simple Agentic Loop Exploration
================================
Demonstrates:
- stop_reason == "end_turn" (Claude is done, break loop)
- stop_reason == "tool_use" (Claude wants to call a tool, continue loop)
- Complete agentic loop pattern
"""

import anthropic
import json

# ============================================================================
# 1. DEFINE TOOLS
# ============================================================================

tools = [
    {
        "name": "calculator",
        "description": "Perform basic arithmetic operations",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The operation to perform"
                },
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            },
            "required": ["operation", "a", "b"]
        }
    },
    {
        "name": "weather",
        "description": "Get weather for a city",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name"
                }
            },
            "required": ["city"]
        }
    }
]

# ============================================================================
# 2. TOOL IMPLEMENTATIONS
# ============================================================================

def execute_calculator(operation: str, a: float, b: float) -> str:
    """Execute basic math operations"""
    results = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else "Error: Division by zero"
    }
    result = results.get(operation, "Unknown operation")
    return json.dumps({"operation": operation, "a": a, "b": b, "result": result})

def execute_weather(city: str) -> str:
    """Simulate weather lookup"""
    weather_data = {
        "New York": "Sunny, 75°F",
        "London": "Cloudy, 60°F",
        "Tokyo": "Rainy, 68°F",
        "Paris": "Clear, 72°F"
    }
    result = weather_data.get(city, f"Weather data not found for {city}")
    return json.dumps({"city": city, "weather": result})

def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Route tool calls to implementations"""
    print(f"\n🔧 Executing tool: {tool_name}")
    print(f"   Input: {json.dumps(tool_input, indent=2)}")

    if tool_name == "calculator":
        result = execute_calculator(
            tool_input["operation"],
            tool_input["a"],
            tool_input["b"]
        )
    elif tool_name == "weather":
        result = execute_weather(tool_input["city"])
    else:
        result = json.dumps({"error": f"Unknown tool: {tool_name}"})

    print(f"   Result: {result}")
    return result

# ============================================================================
# 3. AGENTIC LOOP
# ============================================================================

def run_agent(user_input: str):
    """Run the agentic loop"""
    client = anthropic.Anthropic()

    # Initialize conversation
    messages = [
        {"role": "user", "content": user_input}
    ]

    print(f"\n{'='*70}")
    print(f"User: {user_input}")
    print(f"{'='*70}")

    iteration = 0

    # ========== THE AGENTIC LOOP ==========
    while True:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")

        # Call Claude with tools available
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        print(f"stop_reason: {response.stop_reason}")

        # ========== KEY DECISION: Check stop_reason ==========

        if response.stop_reason == "end_turn":
            # Claude is DONE - extract final answer and break
            print("\n✅ STOP_REASON = 'end_turn' → Claude is done, BREAK loop")

            # Extract text response
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"\n🤖 Claude's Final Answer:\n{block.text}")
            break

        elif response.stop_reason == "tool_use":
            # Claude wants to CALL A TOOL - continue loop
            print("\n🔄 STOP_REASON = 'tool_use' → Claude wants to call a tool, CONTINUE loop")

            # Find the tool use block
            tool_use_block = None
            assistant_message_content = []

            for block in response.content:
                assistant_message_content.append(block)
                if block.type == "tool_use":
                    tool_use_block = block
                    print(f"   Tool requested: {block.name}")

            if not tool_use_block:
                print("ERROR: stop_reason is 'tool_use' but no tool block found!")
                break

            # Execute the tool
            tool_result = execute_tool(tool_use_block.name, tool_use_block.input)

            # Add assistant response to messages
            messages.append({
                "role": "assistant",
                "content": assistant_message_content
            })

            # Add tool result back to messages
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": tool_result
                    }
                ]
            })

            print("   → Tool result added to conversation, loop continues...")

        else:
            # Unexpected stop_reason
            print(f"\n⚠️ UNEXPECTED STOP_REASON: {response.stop_reason}")
            break

# ============================================================================
# 4. TEST CASES
# ============================================================================

if __name__ == "__main__":
    print("AGENTIC LOOP EXPLORATION - stop_reason & tool_use\n")

    # Test Case 1: Calculation (will use tool_use)
    print("\n" + "="*70)
    print("TEST 1: Calculation (expects tool_use → end_turn)")
    print("="*70)
    run_agent("What is 42 + 58? Then tell me what the weather is in Paris.")

    # Test Case 2: Simple question (might just end_turn)
    print("\n" + "="*70)
    print("TEST 2: Simple Question (might skip tools)")
    print("="*70)
    run_agent("What's the capital of France?")

    # Test Case 3: Multi-step (will use tools multiple times)
    print("\n" + "="*70)
    print("TEST 3: Multi-Step (multiple tool_use → end_turn)")
    print("="*70)
    run_agent("Calculate 100 * 5, then get weather for London, then tell me the sum of those two numbers.")