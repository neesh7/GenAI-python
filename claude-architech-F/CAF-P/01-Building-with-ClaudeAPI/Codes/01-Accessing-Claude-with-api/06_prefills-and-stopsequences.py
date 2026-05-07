from anthropic import Anthropic
import dotenv

# Load environment variables (API key)
dotenv.load_dotenv()

# Initialize the Anthropic client
client = Anthropic()
model = "claude-haiku-4-5-20251001"

# ============================================================================
# PREFILLS AND STOP SEQUENCES EXPLANATION
# ============================================================================
#
# PREFILLS:
# - A prefill is text that you pre-populate in the assistant's response
# - Useful for guiding the AI to respond in a specific format
# - Example: If you want JSON output, start with "{"
# - Example: If you want a numbered list, start with "1. "
# - The AI will continue from where the prefill ends
#
# STOP SEQUENCES:
# - Stop sequences are strings that signal the AI to stop generating
# - Useful for controlling response length or format
# - Example: Stop at newline to get single-line responses
# - Example: Stop at "---" to end structured responses
# - Multiple stop sequences can be provided
#
# ============================================================================


# Example 1: PREFILL - JSON FORMAT RESPONSE
# ============================================================================
# Use case: You want the AI to respond in JSON format
# Solution: Start with "{" to guide the AI toward JSON structure

def example_prefill_json():
    print("\n" + "="*60)
    print("EXAMPLE 1: PREFILL - JSON FORMAT")
    print("="*60)

    messages = [
        {
            "role": "user",
            "content": "List 3 fruits in JSON format with their colors"
        }
    ]

    # The key here is the 'content' parameter starting with "{"
    # This prefill guides Claude to output JSON
    response = client.messages.create(
        model=model,
        max_tokens=200,
        messages=messages,
        system="You are a helpful assistant that responds in JSON format.",
        # Prefill: Start the assistant's response with "{"
        # This is optional - we can add more to guide further
    )

    # In Anthropic SDK, prefill can be set via the first assistant message
    # Let's use a different approach with the actual prefill

    # Actually, to use prefill properly in Anthropic API:
    response = client.messages.create(
        model=model,
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": "List 3 fruits in JSON format with their colors"
            },
            {
                "role": "assistant",
                "content": "{"  # This is the prefill - start the response with "{"
            }
        ],
        system="You are a helpful assistant that responds in JSON format."
    )

    print("User: List 3 fruits in JSON format with their colors")
    print(f"Assistant (with prefill '{{'): {response.content[0].text}")


# Example 2: STOP SEQUENCES - SINGLE LINE RESPONSE
# ============================================================================
# Use case: You want short, single-line responses
# Solution: Use "\n" as stop sequence to stop at first newline

def example_stop_sequence_single_line():
    print("\n" + "="*60)
    print("EXAMPLE 2: STOP SEQUENCE - SINGLE LINE")
    print("="*60)

    messages = [
        {
            "role": "user",
            "content": "What is the capital of France? Explain in detail."
        }
    ]

    response = client.messages.create(
        model=model,
        max_tokens=200,
        messages=messages,
        stop_sequences=["\n"]  # Stop at the first newline
    )

    print("User: What is the capital of France? Explain in detail.")
    print(f"Assistant (stops at first \\n): {response.content[0].text}")


# Example 3: STOP SEQUENCES - CUSTOM DELIMITER
# ============================================================================
# Use case: Stop response at a specific delimiter for structured data
# Solution: Use a custom separator like "---" or "END"

def example_stop_sequence_custom():
    print("\n" + "="*60)
    print("EXAMPLE 3: STOP SEQUENCE - CUSTOM DELIMITER")
    print("="*60)

    messages = [
        {
            "role": "user",
            "content": "Provide a recipe for pasta. Format: Title | Ingredients | Instructions | Cooking Time"
        }
    ]

    response = client.messages.create(
        model=model,
        max_tokens=300,
        messages=messages,
        stop_sequences=["---", "END"]  # Multiple stop sequences
    )

    print("User: Provide a recipe for pasta. Format: Title | Ingredients | Instructions | Cooking Time")
    print(f"Assistant (stops at '---' or 'END'): {response.content[0].text}")


# Example 4: PREFILL + STOP SEQUENCE COMBINED
# ============================================================================
# Use case: Guide format with prefill AND limit length with stop sequence
# Solution: Combine both for precise control

def example_prefill_and_stop():
    print("\n" + "="*60)
    print("EXAMPLE 4: PREFILL + STOP SEQUENCE COMBINED")
    print("="*60)

    # Start with a prefill that includes the format we want
    prefill_content = """Answer in this format:
Decision: [YES/NO]
Reason: """

    messages = [
        {
            "role": "user",
            "content": "Should I buy this phone? Specs: 120Hz display, 12GB RAM, $500 price"
        },
        {
            "role": "assistant",
            "content": prefill_content  # Guide the response format
        }
    ]

    response = client.messages.create(
        model=model,
        max_tokens=200,
        messages=messages,
        stop_sequences=["\n---"]  # Stop at specific marker
    )

    print("User: Should I buy this phone? Specs: 120Hz display, 12GB RAM, $500 price")
    print(f"Assistant (prefill + stop): \n{prefill_content}{response.content[0].text}")


# Example 5: PREFILL - CODE GENERATION
# ============================================================================
# Use case: Generate code by prefilling with language/function start
# Solution: Start with language-specific syntax

def example_prefill_code():
    print("\n" + "="*60)
    print("EXAMPLE 5: PREFILL - CODE GENERATION")
    print("="*60)

    messages = [
        {
            "role": "user",
            "content": "Write a Python function that checks if a number is prime"
        },
        {
            "role": "assistant",
            "content": "```python\ndef is_prime(n):"  # Prefill to guide code generation
        }
    ]

    response = client.messages.create(
        model=model,
        max_tokens=300,
        messages=messages,
        system="You are a coding assistant."
    )

    print("User: Write a Python function that checks if a number is prime")
    print(f"Assistant (prefill for code):\n```python\ndef is_prime(n):{response.content[0].text}")


# Example 6: STOP SEQUENCES - MULTIPLE DELIMITERS
# ============================================================================
# Use case: Stop at multiple possible endpoints
# Solution: Provide array of stop sequences

def example_multiple_stop_sequences():
    print("\n" + "="*60)
    print("EXAMPLE 6: MULTIPLE STOP SEQUENCES")
    print("="*60)

    messages = [
        {
            "role": "user",
            "content": "List 5 programming languages with brief descriptions"
        }
    ]

    response = client.messages.create(
        model=model,
        max_tokens=200,
        messages=messages,
        # Stop at multiple possible markers
        stop_sequences=["6.", "7.", "\n\n\n"]
    )

    print("User: List 5 programming languages with brief descriptions")
    print(f"Assistant (stops at '6.', '7.', or 3 newlines): {response.content[0].text}")


# ============================================================================
# RUN ALL EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("\n" + "🚀 PREFILLS AND STOP SEQUENCES EXAMPLES 🚀".center(60))

    try:
        example_prefill_json()
        example_stop_sequence_single_line()
        example_stop_sequence_custom()
        example_prefill_and_stop()
        example_prefill_code()
        example_multiple_stop_sequences()

        print("\n" + "="*60)
        print("✅ ALL EXAMPLES COMPLETED")
        print("="*60)

    except Exception as e:
        print(f"❌ Error: {e}")
