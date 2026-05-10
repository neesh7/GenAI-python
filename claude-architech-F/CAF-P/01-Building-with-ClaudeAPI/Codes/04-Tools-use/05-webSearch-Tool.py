# ===== IMPORTS =====
from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import Message
import json

# ===== INITIALIZATION =====
"""
WEB SEARCH TOOL OVERVIEW:

Like the text editor tool, Claude has a BUILT-IN web search tool.
This is a pre-built tool provided by Anthropic that allows Claude to:
- Search the web for current information
- Access real-time data beyond Claude's training cutoff
- Filter results by domain for safety/relevance

KEY DIFFERENCE from text_editor_tool:
- Text editor: We implement the tool functions (view, create, str_replace)
- Web search: Claude and Anthropic handle the implementation
  We only need to provide the schema configuration

WHEN WOULD YOU USE THIS?
- Questions about current events or real-time data
- Information that changes frequently (weather, stock prices, news)
- Specific websites you want to prioritize (e.g., only medical journals)
- Research tasks that require up-to-date information
"""

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"


# ===== HELPER FUNCTIONS =====
def add_user_message(messages, message):
    """Add a user message to conversation history."""
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(user_message)


def add_assistant_message(messages, message):
    """Add an assistant message to conversation history."""
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(assistant_message)


def chat(messages, system=None, temperature=1.0, stop_sequences=[], tools=None):
    """Call Claude API with optional tools."""
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message


def text_from_message(message):
    """Extract all text blocks from a message."""
    return "\n".join([block.text for block in message.content if block.type == "text"])


# ===== WEB SEARCH TOOL SCHEMA =====
"""
WEB SEARCH TOOL SCHEMA EXPLAINED:

The web_search_schema tells Claude:
1. What version of the web search tool to use
2. Max number of searches allowed per conversation
3. Which domains are allowed (for filtering/safety)

CONFIG FIELDS:

"type": "web_search_20250305"
  - Schema version for current API (may change over time)
  - Different versions may have different capabilities
  - Check Anthropic docs for latest version

"name": "web_search"
  - Name Claude uses to request this tool
  - When Claude wants to search: "I'll use web_search"
  - When you receive tool_use block: tool_use.name == "web_search"

"max_uses": 5
  - Maximum number of web searches Claude can perform in this conversation
  - Prevents excessive API calls and costs
  - Claude can choose to use fewer searches if not needed

"allowed_domains": ["nih.gov"]
  - SECURITY FEATURE: Only return results from specified domains
  - Prevents Claude from accessing arbitrary websites
  - Useful when you want results from trusted sources only
  - Example: For medical questions, only allow .nih.gov (NIH official)
  - Empty list or omitted = allow any domain

WHY DOMAIN FILTERING?
- Safety: Prevent results from unreliable sources
- Relevance: Focus on authoritative sources for your use case
- Cost: Fewer irrelevant results to process
- Trust: Medical = .nih.gov, Legal = .law.gov, etc.

EXAMPLE CONFIGURATIONS:

# Medical research - only official NIH
{
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 10,
    "allowed_domains": ["nih.gov", "pubmed.ncbi.nlm.nih.gov"]
}

# News articles - only reputable news sites
{
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 5,
    "allowed_domains": ["bbc.com", "reuters.com", "apnews.com"]
}

# Academic research - only academic sources
{
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 8,
    "allowed_domains": ["arxiv.org", "scholar.google.com", "jstor.org"]
}

# No restrictions - search anywhere
{
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 5,
    "allowed_domains": []  # Empty = no domain restrictions
}
"""

web_search_schema = {
    "type": "web_search_20250305",      # Schema version for web search tool
    "name": "web_search",                # Tool name Claude uses to call it
    "max_uses": 5,                       # Maximum searches per conversation
    "allowed_domains": ["nih.gov"],      # Only NIH.gov results (medical authority)
}


# ===== TOOL EXECUTION AND PROCESSING =====
"""
HOW THE WEB SEARCH TOOL WORKS IN A CONVERSATION:

1. USER ASKS A QUESTION:
   "What's the best exercise for gaining leg muscle?"

2. CLAUDE ANALYZES THE REQUEST:
   "I need current fitness information to give accurate advice"
   "I'll use web_search to find the latest fitness research"

3. CLAUDE CALLS THE WEB SEARCH TOOL:
   - Generates a search query (e.g., "best leg exercises muscle building")
   - Requests: tool_use(name="web_search", input={"query": "..."})
   - stop_reason = "tool_use" (Claude is waiting for search results)

4. ANTHROPIC API SEARCHES THE WEB:
   - Searches Google or other search engines
   - Filters results by allowed_domains (only .nih.gov in this case)
   - Returns: search results with titles, snippets, URLs
   - Respects max_uses limit

5. WE PROCESS THE RESULTS:
   - Extract search_results from tool_use response
   - Format as tool_result block
   - Add back to message history
   - send_to_claude with results

6. CLAUDE READS THE RESULTS:
   - Sees: "Search returned 3 results from nih.gov"
   - Reads: Titles, snippets, URLs
   - Synthesizes: Information into helpful answer
   - Responds: "Based on the NIH research, the best leg exercises are..."

7. CONVERSATION ENDS:
   - stop_reason != "tool_use"
   - Claude has answered the question
"""


def process_tool_response(response):
    """
    Process Claude's response and execute any tool calls.

    When Claude requests web_search:
    1. Extract search query from tool_use block
    2. The API automatically performs the search
    3. Results are returned in the response
    4. We format them as tool_result for Claude

    Important: With web_search, the API handles the actual searching.
    We don't need to implement search ourselves (unlike text_editor_tool).
    We just pass the tool request through and let Anthropic handle it.

    Returns:
        tool_results: List of tool_result blocks to send back to Claude
    """
    tool_requests = [block for block in response.content if block.type == "tool_use"]
    tool_result_blocks = []

    for tool_request in tool_requests:
        # For web_search, the tool_use.input contains the search query
        if tool_request.name == "web_search":
            # In a real implementation, Anthropic's API handles the actual search
            # and returns results in the response
            # We format it as a tool_result for Claude to process

            # Extract search results if available
            # (In production, this would come from the API response)
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": "Search executed successfully",  # Placeholder
                "is_error": False,
            }
        else:
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": f"Unknown tool: {tool_request.name}",
                "is_error": True,
            }

        tool_result_blocks.append(tool_result_block)

    return tool_result_blocks


# ===== MULTI-TURN CONVERSATION WITH WEB SEARCH =====
"""
MULTI-TURN CONVERSATION FLOW WITH WEB SEARCH:

Turn 1 - Claude Decides to Search:
  User: "What's the best exercise for gaining leg muscle?"
  Claude: "I need current fitness information"
  Claude: Uses web_search to find "best leg exercises"
  stop_reason = "tool_use" (waiting for search results)

Turn 2 - Process Search Results:
  We: "Here are the search results from nih.gov"
  Add: Results to message history
  Claude: Reads results and formulates response

Turn 3 - Claude Responds:
  Claude: "Based on the latest research, squats and deadlifts..."
  stop_reason = "end_turn" (conversation complete)

KEY DIFFERENCES FROM TEXT EDITOR TOOL:
- Text editor: We implement the functions (view, create, str_replace)
- Web search: API implements the search, we just request it
- Text editor: Results come from file system
- Web search: Results come from the web/search engines
"""


def run_conversation(messages, system_prompt=None):
    """
    Run multi-turn conversation with web search support.

    Orchestrates the conversation loop:
    1. Send user query with web_search tool enabled
    2. Claude may respond with text OR request web_search
    3. If web_search requested, process and send results back
    4. Repeat until Claude finishes (no more tool requests)

    Args:
        messages: Conversation history list
        system_prompt: Optional system prompt to guide Claude

    Returns:
        Updated messages list with full conversation history

    Note: This demonstrates how Claude can autonomously search the web
    to find current information and incorporate it into responses.
    """
    system_prompt = system_prompt or "You are a helpful assistant with access to web search."

    iteration = 0
    max_iterations = 10  # Prevent infinite loops

    while iteration < max_iterations:
        iteration += 1

        # Step 1: Send messages + web_search tool to Claude
        print(f"\n--- Iteration {iteration} ---")
        response = chat(
            messages,
            system=system_prompt,
            tools=[web_search_schema],  # Enable web search
        )

        # Step 2: Add Claude's response to history
        add_assistant_message(messages, response)

        # Step 3: Display Claude's text response
        text = text_from_message(response)
        if text:
            print(f"Claude: {text}")

        # Step 4: Check if Claude called a tool or finished
        if response.stop_reason != "tool_use":
            print("\n--- Conversation Complete ---")
            break

        # Step 5: Process tool calls (web_search requests)
        print(f"Claude requested web search...")
        tool_results = process_tool_response(response)

        # Step 6: Add tool results and continue loop
        add_user_message(messages, tool_results)

    return messages


# ===== MAIN EXECUTION =====
if __name__ == "__main__":
    """
    EXAMPLE USAGE:

    This example asks Claude about exercises for building leg muscle.
    Claude will use web search to find current fitness research from NIH.gov.

    The conversation flow:
    1. User asks question
    2. Claude decides to search for current information
    3. Web search finds results from allowed domains (nih.gov)
    4. Claude synthesizes results into helpful answer
    5. Conversation ends with informed response
    """

    messages = []

    # Add user's question
    add_user_message(
        messages,
        "What's the best exercise for gaining leg muscle?",
    )

    # Run conversation with web search enabled
    run_conversation(messages)
