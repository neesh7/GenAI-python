# Model Context Protocol (MCP)

## What is MCP?

MCP is a **communication standard** that lets Claude access tools, prompts, and resources from external servers without you having to build and maintain all the integration code yourself.

Think of it as a **plug-and-play interface** for tools: someone else writes and maintains the tool definitions, you just connect to their MCP server and use them.

```
Your App (MCP Client)
        ↓ (connects via MCP)
    MCP Server A (GitHub tools)
    MCP Server B (Database tools)
    MCP Server C (API integrations)
        ↓ (provides)
    Pre-built Tools + Schemas
```

---

## The Problem MCP Solves

### Without MCP: You Write Everything

Say you want to build a ChatBot that answers questions about GitHub. Users ask: *"What are my open pull requests?"*

To answer this, Claude needs GitHub tools. **Without MCP**, you must:
1. Write a tool schema for each GitHub action (get repos, list PRs, get issues, etc.)
2. Implement the function logic for each tool
3. Handle authentication and API calls
4. Maintain all this code as GitHub's API changes

**Result:** 50+ tools × (schema + implementation + maintenance) = massive code burden

### With MCP: Pre-Built Tools

**With MCP**, a GitHub MCP server already has:
- ✅ All GitHub tool schemas defined
- ✅ All tool functions implemented
- ✅ Authentication handled
- ✅ Updated when GitHub API changes

**You just:** Connect to the MCP server and use the tools.

---

## MCP Architecture

```
┌─────────────────────────────────────────────────┐
│              Your Application                   │
│         (MCP Client / Your Server)              │
│                                                  │
│  • Receives user requests                       │
│  • Sends to Claude                              │
│  • Claude uses tools from MCP servers           │
│  • Returns responses to users                   │
└──────┬──────────────────────────┬───────────────┘
       │                          │
   MCP Protocol                MCP Protocol
       │                          │
┌──────▼───────────┐      ┌──────▼───────────┐
│   MCP Server A   │      │   MCP Server B   │
│   (GitHub)       │      │  (Database)      │
│                  │      │                  │
│ • Tool Schemas   │      │ • Tool Schemas   │
│ • Functions      │      │ • Functions      │
│ • Auth/Config    │      │ • Auth/Config    │
└──────────────────┘      └──────────────────┘
```

---

## MCP vs Tool Use: Key Differences

| Aspect | Tool Use | MCP |
|--------|----------|-----|
| **Who writes tools?** | You (in your code) | External MCP server |
| **Tool schemas** | You define them | Already defined |
| **Tool functions** | You implement them | Server implements them |
| **Maintenance** | Your responsibility | Server maintainer's responsibility |
| **Use case** | Custom, simple tools | Complex, external services (GitHub, AWS, databases) |
| **Code burden** | Higher | Lower |

**Key insight:** MCP is not a replacement for tool use—it's a pattern that *uses* tool use. MCP servers provide pre-built tools that Claude then calls.

---

## Who Authors MCP Servers?

### Official Servers
- **Service providers** (AWS, GitHub, Stripe, etc.) create official MCP servers for their own APIs
- Example: AWS releases an official MCP server with tools for EC2, S3, Lambda, etc.

### Community Servers
- Developers create MCP servers for popular services
- Published and shared in the MCP ecosystem

### Custom Servers
- You can build MCP servers for your own internal tools or services

---

## Real-World Example: GitHub Chatbot

### Setup
```
User: "What are my open pull requests?"
    ↓
Your App (MCP Client)
    ↓
Claude (receives question)
    ↓
MCP Server: GitHub (provides tools)
    ├─ github.list_repos()
    ├─ github.list_pull_requests()
    ├─ github.get_pr_details()
    └─ ... (50+ more tools)
    ↓
Claude calls: github.list_pull_requests()
    ↓
Result: [PR1, PR2, PR3...]
    ↓
Claude: "You have 3 open PRs: ..."
    ↓
User gets answer
```

### Without MCP
- You write 50+ tool schemas and functions
- You handle GitHub authentication
- You maintain API compatibility
- Cost: ~2000+ lines of code, ongoing maintenance

### With MCP
- Connect to official GitHub MCP server
- Use pre-built tools
- Server maintainer handles updates
- Cost: ~10 lines of connection code

---

## Direct API vs MCP

| Approach | Pros | Cons |
|----------|------|------|
| **Direct API calls** | Simple for 1-2 APIs | Schema + function per tool |
| | | Maintenance burden |
| | | Doesn't scale to many APIs |
| **Tool Use (inline)** | Full control | Write all schemas/functions |
| | Custom logic | Tight coupling to your app |
| **MCP Servers** | Pre-built, maintained ✨ | Requires MCP setup |
| | Scales to many services | Less custom control |
| | Decoupled, reusable | |

---

## When to Use MCP

### ✅ Good Fit
- Integrating with large, complex external services (GitHub, AWS, Stripe)
- Need 10+ tools from one service
- Service updates frequently
- Want to share integration with other apps

### ❌ Not Necessary
- Simple 1-2 API calls
- Internal-only tools
- Highly custom logic
- Lightweight integrations

---

## Core Concepts

### MCP Client
Your application that connects to MCP servers. Sends requests to Claude and receives tool calls from Claude, which it executes via MCP servers.

### MCP Server
A separate service that provides:
- **Tools** — Functions Claude can call
- **Prompts** — Pre-defined prompt templates
- **Resources** — Files, data, or external services

### Tool Schemas
Already-defined tool specifications in the MCP server. Claude reads these schemas and knows what tools are available and how to call them.

### Tool Functions
The actual code that executes when Claude calls a tool. Hosted and maintained by the MCP server, not your code.

---

## MCP Workflow

```
1. START
   ├─ Your app connects to MCP servers
   ├─ MCP servers provide tool schemas
   └─ Claude learns available tools

2. USER REQUEST
   ├─ User asks question
   └─ Your app sends to Claude with MCP tool context

3. CLAUDE RESPONDS
   ├─ Claude decides which tools to call
   └─ Claude generates tool call requests

4. YOUR APP EXECUTES
   ├─ Your app sees tool call
   ├─ Forwards to appropriate MCP server
   └─ MCP server executes the function

5. RESULT BACK TO CLAUDE
   ├─ Tool result returned to your app
   ├─ Your app sends result back to Claude
   └─ Claude uses result to answer user

6. FINAL RESPONSE
   └─ Claude gives final answer to user
```

---

## Quick Summary

| Question | Answer |
|----------|--------|
| **What is MCP?** | A protocol for connecting Claude to pre-built tool servers |
| **Why use it?** | Avoid writing and maintaining complex integrations |
| **Who writes tools?** | MCP server maintainers (often the service provider) |
| **How many tools?** | As many as the MCP server provides (50+, 100+, etc.) |
| **Cost vs direct API?** | Lower cost, less code, easier maintenance |
| **Maintenance?** | Server maintainer handles updates, not you |

---

## Key Takeaways

- **MCP = Delegation** — Tools are written and maintained elsewhere
- **MCP ≠ Tool Use** — MCP *uses* tool use, but abstracts away the implementation
- **Scaling** — One MCP server can provide hundreds of tools
- **Reusable** — Same MCP server can be used by many applications
- **Decoupled** — Your app logic separate from tool implementations
- **Maintained** — Service providers keep tools up-to-date

---

## Example Use Cases

| Service | MCP Server Provides | Benefit |
|---------|---|---|
| **GitHub** | 50+ PR, issue, repo tools | No GitHub API integration code |
| **AWS** | 100+ EC2, S3, Lambda tools | No AWS SDK wrapper code |
| **Stripe** | Payment, customer, invoice tools | No payment API integration code |
| **Database** | Query, table, schema tools | No SQL wrapper code |
| **Email** | Send, read, manage tools | No email service integration |

---

---

# MCP Client: The Communication Bridge

## What is an MCP Client?

An **MCP Client** is a component in **your application** that communicates with MCP servers. It's your access point to all the tools and resources that MCP servers provide.

Think of it as a **translator and messenger**:
- Sends requests to MCP servers
- Receives responses from MCP servers
- Translates between your app and the MCP protocol
- Handles all communication details

```
Your App
    ↓
MCP Client (sits in your app)
    ↓ (talks to)
MCP Server (external)
    ↓
Tools, Prompts, Resources
```

---

## Transport Agnostic Communication

MCP is **transport agnostic** — meaning the client and server can communicate using different methods:

### Most Common: Local stdio (Same Machine)
```
Your App
    ↓
MCP Client ←→ (stdin/stdout) ←→ MCP Server
                                  (on same machine)
```
Simple, fast, no network overhead.

### Network Based: HTTP/WebSockets
```
Your Server (MCP Client)
    ↓
Internet
    ↓
Remote MCP Server
```
Useful for:
- Remote services
- Cloud deployments
- Distributed systems

### Other Options
```
- gRPC
- Protocol Buffers
- Custom protocols
```

**Key point:** MCP doesn't dictate HOW they talk, just WHAT they talk about (message format).

---

## Message Types: The Conversation Format

Once connected, the MCP client and server exchange specific message types. The main ones you'll use:

### 1. ListToolsRequest / ListToolsResult

**Client asks:** "What tools do you provide?"

```
MCP Client → MCP Server
"ListToolsRequest: Give me your tools"
    ↓
MCP Server → MCP Client
"ListToolsResult: Here are my 50 tools:
  - github.list_repos
  - github.list_prs
  - github.get_pr_details
  - ... (47 more)"
```

### 2. CallToolRequest / CallToolResult

**Client asks:** "Execute this specific tool with these arguments"

```
MCP Client → MCP Server
"CallToolRequest: 
  tool = github.list_repos
  args = {owner: 'myname'}"
    ↓
MCP Server → MCP Client
"CallToolResult:
  result = [{name: 'repo1'}, {name: 'repo2'}, ...]"
```

### Other Message Types
- **ReadResourceRequest/Result** — Get data from MCP server
- **ListResourcesRequest/Result** — List available resources
- **ListPromptsRequest/Result** — List prompt templates
- **CallPromptRequest/Result** — Execute a prompt template

---

## Complete Communication Flow

Here's how everything works together. **Scenario:** User asks "What repositories do I have?"

### Step 1: User Submits Query
```
User: "What repositories do I have?"
    ↓
Your Server receives question
```

### Step 2: Get Available Tools
```
Your Server → MCP Client
"I need tools for this question"
    ↓
MCP Client → MCP Server
"ListToolsRequest"
    ↓
MCP Server → MCP Client
"ListToolsResult: [github.list_repos, github.list_prs, ...]"
    ↓
MCP Client → Your Server
"Here are the available tools"
```

### Step 3: Send Question to Claude (with Tools)
```
Your Server → Claude API
{
  "messages": [{"role": "user", "content": "What repositories do I have?"}],
  "tools": [
    {name: "github.list_repos", schema: {...}},
    {name: "github.list_prs", schema: {...}},
    ...
  ]
}
```

### Step 4: Claude Decides Which Tool to Use
```
Claude examines tools
    ↓
Claude decides: "I need to call github.list_repos"
    ↓
Claude → Your Server
"Use tool: github.list_repos with args: {owner: 'myname'}"
```

### Step 5: Execute the Tool via MCP
```
Your Server → MCP Client
"Execute github.list_repos with {owner: 'myname'}"
    ↓
MCP Client → MCP Server
"CallToolRequest: github.list_repos, {owner: 'myname'}"
    ↓
MCP Server → GitHub API
"Get repositories for owner 'myname'"
    ↓
GitHub → MCP Server
"[{name: 'repo1'}, {name: 'repo2'}, ...]"
    ↓
MCP Server → MCP Client
"CallToolResult: [{name: 'repo1'}, {name: 'repo2'}, ...]"
    ↓
MCP Client → Your Server
"Tool executed, result: [{name: 'repo1'}, {name: 'repo2'}, ...]"
```

### Step 6: Send Result Back to Claude
```
Your Server → Claude API
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "...",
      "content": "[{name: 'repo1'}, {name: 'repo2'}, ...]"
    }
  ]
}
```

### Step 7: Claude Formulates Final Answer
```
Claude reads the tool result
    ↓
Claude generates response:
"You have 2 repositories: repo1 and repo2"
    ↓
Your Server → User
"You have 2 repositories: repo1 and repo2"
```

---

## Flow Diagram: Complete Picture

```
┌─────────────────────────────────────────────────────────┐
│                    USER                                 │
│         "What repositories do I have?"                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│              YOUR SERVER / APP                          │
├─────────────────────────────────────────────────────────┤
│  1. Receive user question                               │
│  2. Ask MCP client for available tools                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│           MCP CLIENT (in your app)                      │
├─────────────────────────────────────────────────────────┤
│  • Sends: ListToolsRequest                              │
│  • Receives: ListToolsResult                            │
│  • Sends: CallToolRequest                               │
│  • Receives: CallToolResult                             │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         ↓                       ↓
  ┌──────────────┐      ┌──────────────────┐
  │ MCP Server   │      │  Claude API      │
  │ (GitHub)     │      │  (with tools)    │
  └──────────────┘      └──────────────────┘
         ↓                       ↑
    GitHub API          Claude decides which
         ↓              tool to call
    Repositories        │
                        ↓
                   (send result back)
                        │
                        ↓
                 Claude responds:
                 "You have 2 repos"
                        │
                        ↓
                 Your Server
                        │
                        ↓
                  USER (answer)
```

---

## Why This Matters

Yes, the flow has **many steps**, but each component has a **clear responsibility**:

| Component | Responsibility |
|-----------|---|
| **Your Server** | Handle user requests, orchestrate flow |
| **MCP Client** | Abstract communication protocol details |
| **MCP Server** | Execute tools, manage external service |
| **Claude** | Decide which tools to use, generate responses |

**The MCP client absorbs all the complexity**, letting you focus on your app logic, not message protocols.

---

## Key Insight: Abstraction

```
Without MCP:
Your Server → (handle GitHub API) → write HTTP → parse JSON → handle errors → Your Server

With MCP:
Your Server → MCP Client → (abstracted away) → Tool Result → Your Server
```

The MCP client handles the tedious communication details. You just ask it to call a tool and it returns the result.

---

---

# Building a CLI Chatbot: Hands-On MCP Project

## Project Overview

We'll build a **CLI-based document management chatbot** to understand how MCP clients and servers work together in practice.

### What You'll Build

```
User (Terminal)
    ↓
CLI Chatbot (Your Interface)
    ↓
MCP Client (Sends requests)
    ↓
MCP Server (Provides tools)
    ↓
Document Storage (In-memory)
```

### Two Main Components

1. **MCP Client** (`mcp_client.py`)
   - Runs in your application
   - Handles user interactions
   - Communicates with the MCP server
   - Sends user queries to Claude

2. **MCP Server** (`mcp_server.py`)
   - Provides document tools
   - Manages document operations
   - Stores documents in memory
   - Responds to tool requests

---

## Important Architecture Note

**In real-world projects**, you implement EITHER:
- ❌ NOT both MCP client AND server in the same app

### Real-World Scenarios

| Scenario | What You Build |
|----------|---|
| **Service Provider** | MCP Server only (publish for others) |
| **Application Dev** | MCP Client only (use others' servers) |
| **Internal Tool** | Both (for your own use) |

**This project** builds both for **educational purposes** — to see how they communicate and work together. This helps you understand the full picture.

---

## Project Structure

```
chatbot-project/
├── main.py              # Entry point, starts the chatbot
├── mcp_client.py        # MCP Client implementation
├── mcp_server.py        # MCP Server implementation
├── .env                 # Your API keys (create this)
├── requirements.txt     # Python dependencies
├── README.md            # Setup instructions
└── documents/           # Document storage (in-memory for this project)
```

---

## The Tools We'll Implement

### Tool 1: Read Documents
```
Tool Name: read_document
Purpose: Read the content of a document
Input: document_name
Output: document_content

Example:
  Input: "report.txt"
  Output: "This is the report content..."
```

### Tool 2: Update Documents
```
Tool Name: update_document
Purpose: Update document content
Input: document_name, new_content
Output: success/error message

Example:
  Input: "report.txt", "Updated content..."
  Output: "Document updated successfully"
```

### Tool 3: List Documents (Bonus)
```
Tool Name: list_documents
Purpose: List all available documents
Input: none
Output: list of document names

Example:
  Output: ["report.txt", "notes.md", "summary.txt"]
```

---

## Setup Steps

### 1. Download & Extract
```bash
# Download cli_project.zip
# Extract to your development directory
# Navigate to the project folder

cd /path/to/chatbot-project
```

### 2. Environment Setup

Create `.env` file:
```
ANTHROPIC_API_KEY=your-api-key-here
```

### 3. Install Dependencies

**Option A: Using UV (Recommended)**
```bash
uv sync
```

**Option B: Using pip**
```bash
pip install -r requirements.txt
```

### 4. Verify Setup

```bash
# Using UV
uv run main.py

# Using Python
python main.py
```

You should see:
```
Chat: > _
```

### 5. Test the Chatbot

```
Chat: > what's 1+1?
Claude: 1 + 1 = 2
```

If you get a response, **setup is complete!** ✅

---

## How the Chatbot Works

### User Flow

```
┌──────────────────────────────────────────────┐
│ User types in terminal                       │
│ "Can you read the report and summarize it?"  │
└────────────────┬─────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────┐
│ main.py receives input                       │
│ Passes to MCP Client                         │
└────────────────┬─────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────┐
│ MCP Client:                                  │
│ 1. Gets available tools from server          │
│ 2. Sends question + tools to Claude          │
│ 3. Claude decides: "I need read_document"    │
└────────────────┬─────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────┐
│ MCP Client requests tool execution           │
│ → MCP Server                                 │
│ "Execute read_document(report.txt)"          │
└────────────────┬─────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────┐
│ MCP Server:                                  │
│ 1. Finds document in memory                  │
│ 2. Returns content                           │
│ 3. Sends back to Client                      │
└────────────────┬─────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────┐
│ MCP Client:                                  │
│ 1. Receives document content                 │
│ 2. Sends to Claude as tool result            │
│ 3. Claude generates summary                  │
│ 4. Returns response to user                  │
└────────────────┬─────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────┐
│ Terminal displays response:                  │
│ "Here's a summary: ..."                      │
└──────────────────────────────────────────────┘
```

---

## Key Learning Points

### What You'll Understand

1. **MCP Client**
   - How to list tools from a server
   - How to request tool execution
   - How to handle tool results
   - How to send results back to Claude

2. **MCP Server**
   - How to define tools
   - How to handle tool requests
   - How to implement tool logic
   - How to return tool results

3. **Communication**
   - Message passing between client and server
   - Request/response patterns
   - Error handling
   - Data serialization

4. **Claude Integration**
   - How Claude chooses which tools to use
   - How to pass tool results back to Claude
   - Multi-turn conversations with tools

---

## Educational Value

This project is **not production-ready**, but it teaches you:

✅ How MCP clients and servers communicate  
✅ How tools are defined and executed  
✅ How Claude integrates with custom tools  
✅ The complete message flow  
✅ Error handling patterns  
✅ In-memory vs persistent storage trade-offs  

---

## Next Steps After Setup

1. ✅ **Setup complete** — Chatbot responds to basic questions
2. ⏭️ **Implement MCP Server** — Define document tools
3. ⏭️ **Implement MCP Client** — Connect to server
4. ⏭️ **Test Tools** — Ask Claude to read/update documents
5. ⏭️ **Debug Communication** — Watch message flow

---

## Running the Complete Application

Once everything is set up and tools are implemented:

```bash
# Terminal 1: Start the chatbot
uv run main.py

# Terminal 1: Try commands
Chat: > Read the report.txt file
Chat: > Update report.txt with new content
Chat: > List all available documents
Chat: > Summarize report.txt
```

Each command will:
1. Go through the MCP client
2. Contact the MCP server
3. Execute the document tool
4. Return results to Claude
5. Claude formulates a response
6. You see the answer in the terminal

---

## Important Reminders

- **No database** — Documents stored in memory (lost on shutdown)
- **Purely educational** — Not meant for production use
- **Both client & server** — Only for learning; real projects use one or the other
- **Clear responsibility** — Client/server separation is key learning goal

This hands-on project is your bridge between theory (understanding MCP) and practice (building with MCP).

---

# Building an MCP Server: Python SDK Approach

## Why the Python SDK Makes It Easy

Building an MCP server from scratch involves writing complex JSON schemas. The **official Python MCP SDK** eliminates this complexity with:

- ✅ **Decorators** — Define tools with `@mcp.tool()`
- ✅ **Type hints** — Python types automatically become JSON schemas
- ✅ **Pydantic integration** — Built-in validation and documentation
- ✅ **Minimal boilerplate** — Focus on business logic, not protocol

```python
# Without SDK (verbose, manual JSON)
tools = [
    {
        "name": "read_doc",
        "description": "...",
        "inputSchema": {
            "type": "object",
            "properties": {
                "doc_id": {"type": "string", "description": "..."}
            },
            "required": ["doc_id"]
        }
    }
]

# With SDK (clean, Python)
@mcp.tool(name="read_doc", description="...")
def read_document(doc_id: str = Field(description="...")):
    ...
```

---

## Initializing the MCP Server

The Python SDK makes server creation trivial:

```python
from mcp.server.fastmcp import FastMCP

# Create server in one line
mcp = FastMCP("DocumentMCP", log_level="ERROR")
```

That's it! You now have a working MCP server ready to add tools to.

---

## Document Storage: In-Memory Dictionary

For this educational project, we store documents in a simple Python dictionary:

```python
docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditure",
    "outlook.pdf": "This document presents the projected future performance of the",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment"
}
```

**Why in-memory?**
- ✅ Simple to understand
- ✅ No database setup needed
- ✅ Focus on MCP concepts, not persistence
- ❌ Data lost on shutdown
- ❌ Not suitable for production

---

## Tool 1: Read Document Contents

### Purpose
Allow Claude to read any document by its ID.

### Implementation

```python
from pydantic import Field

@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string."
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    """Read a document from the in-memory store."""
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    return docs[doc_id]
```

### How It Works

```
Claude says: "Read deposition.md"
    ↓
MCP Server executes: read_document(doc_id="deposition.md")
    ↓
Function returns: "This deposition covers the testimony of Angela Smith, P.E."
    ↓
Claude sees the document content and can analyze/summarize it
```

### SDK Magic

The `@mcp.tool()` decorator + `Field()` automatically generates:
```json
{
    "name": "read_doc_contents",
    "description": "Read the contents of a document and return it as a string.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "doc_id": {
                "type": "string",
                "description": "Id of the document to read"
            }
        },
        "required": ["doc_id"]
    }
}
```

You don't write that JSON — the SDK generates it from your Python code!

---

## Tool 2: Edit Document (Find & Replace)

### Purpose
Allow Claude to modify documents through find-and-replace operations.

### Implementation

```python
@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the document's content with a new string."
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    """Edit a document using find-and-replace."""
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    # Simple string replacement
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
```

### How It Works

```
Claude says: "In report.pdf, change '20m' to '25m'"
    ↓
MCP Server executes: edit_document(
    doc_id="report.pdf",
    old_str="20m",
    new_str="25m"
)
    ↓
Function replaces text in dictionary
    ↓
Claude: "Updated successfully"
```

### Three Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `doc_id` | Which document to edit | "report.pdf" |
| `old_str` | Text to find (exact match) | "20m condenser" |
| `new_str` | Replacement text | "25m condenser" |

---

## Error Handling

Both tools include error handling for invalid document IDs:

```python
if doc_id not in docs:
    raise ValueError(f"Doc with id {doc_id} not found")
```

**What happens:**
1. Claude requests a non-existent document
2. Tool raises `ValueError` with descriptive message
3. MCP Server sends error back to Claude
4. Claude sees the error and can inform user or try a different approach
5. Conversation continues

**Example:**
```
Claude: "Read nonexistent.txt"
    ↓
Tool raises: "Doc with id nonexistent.txt not found"
    ↓
Claude: "I couldn't find that document. Available documents are: ..."
```

---

## Type Hints → JSON Schema Conversion

The SDK transforms Python types into JSON schemas automatically:

```python
def example_tool(
    name: str,              # → "type": "string"
    age: int,               # → "type": "integer"
    enabled: bool,          # → "type": "boolean"
    tags: list[str],        # → "type": "array", "items": "string"
):
    pass
```

**Benefits:**
- ✅ Type safety in your code
- ✅ IDE autocomplete and error checking
- ✅ Claude knows parameter types
- ✅ Automatic validation

---

## The Complete Server Structure

```python
from mcp.server.fastmcp import FastMCP
from pydantic import Field

# 1. Initialize server
mcp = FastMCP("DocumentMCP", log_level="ERROR")

# 2. Define storage
docs = {
    "document1.txt": "content...",
    "document2.txt": "content...",
}

# 3. Define tools with decorators
@mcp.tool(name="read_doc_contents", description="Read a document")
def read_document(doc_id: str = Field(description="Document ID")):
    if doc_id not in docs:
        raise ValueError(f"Doc {doc_id} not found")
    return docs[doc_id]

@mcp.tool(name="edit_document", description="Edit a document")
def edit_document(
    doc_id: str = Field(description="Document ID"),
    old_str: str = Field(description="Text to find"),
    new_str: str = Field(description="Replacement text")
):
    if doc_id not in docs:
        raise ValueError(f"Doc {doc_id} not found")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)

# 4. Start server
if __name__ == "__main__":
    mcp.run()
```

---

## Key Benefits of Python SDK

| Aspect | Without SDK | With SDK |
|--------|---|---|
| **Schema Definition** | Manual JSON | Auto-generated |
| **Lines of Code** | 50+ per tool | 5-10 per tool |
| **Type Safety** | None | Full |
| **Validation** | Manual | Automatic |
| **Maintenance** | Error-prone | Simple |
| **IDE Support** | None | Full autocomplete |

---

## SDK Handles the Complexity

```
You write:
@mcp.tool(name="read", description="Read doc")
def read_document(doc_id: str):
    return docs[doc_id]

SDK automatically generates:
✓ JSON schema from type hints
✓ Parameter validation
✓ Error handling wrappers
✓ Protocol message formatting
✓ Server communication layer
```

You focus on **business logic** (reading/editing documents), the SDK handles **protocol details** (JSON schemas, message passing).

---

## Running the Server

```bash
# The mcp.run() command starts the server
python mcp_server.py

# Server is now listening for MCP client connections
# Ready to handle ListToolsRequest and CallToolRequest messages
```

The server will:
1. Listen for MCP client connections
2. Respond to `ListToolsRequest` with available tools
3. Execute tools when client sends `CallToolRequest`
4. Return results back to client

---

# Resources in MCP Servers: Exposing Data

## What are Resources?

**Resources** allow you to expose data to clients, similar to **GET request handlers** in a typical HTTP server. They're perfect for scenarios where you need to **fetch information** rather than perform actions.

### Tools vs Resources

| Aspect | Tools | Resources |
|--------|-------|-----------|
| **Purpose** | Perform actions (create, update, delete) | Fetch data (read-only) |
| **API Analogy** | POST/PUT/DELETE requests | GET requests |
| **Use Case** | Document editing, sending emails | Document listing, file browsing |
| **Client Impact** | Claude decides when to call | Data context for Claude |

---

## Understanding Resources Through an Example

Imagine building a **document mention feature** where users type `@document_name` to reference files.

This requires two operations:

1. **Get a list of all available documents** (for autocomplete)
2. **Fetch the contents of a specific document** (when mentioned)

**How it works:**
```
User types: "Can you summarize @report.pdf?"
    ↓
Your app reads from the @-mention
    ↓
Your app uses MCP client to fetch document content
    ↓
App injects document into Claude's prompt
    ↓
Claude analyzes the injected document and responds
```

Without resources, you'd have to manually code all this. With MCP resources, the server exposes the data, and clients can automatically fetch what they need.

---

## How Resources Work

Resources follow a **request-response pattern**:

```
MCP Client: "I want resource: docs://documents/report.pdf"
    ↓
MCP Server receives: ReadResourceRequest
    ↓
MCP Server executes: fetch_doc(doc_id="report.pdf")
    ↓
MCP Server returns: "The report details a 20m condenser tower..."
    ↓
MCP Client receives: ReadResourceResult
```

The **URI** acts like an address for the resource you want to access.

---

## Two Types of Resources

### Type 1: Direct Resources (Static)

URIs that don't change — they always point to the same data.

**Example:** `docs://documents`

```python
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    """Return all available document IDs."""
    return list(docs.keys())
```

**Usage:**
```
Client requests: docs://documents
Server returns: ["report.pdf", "deposition.md", "financials.docx"]
```

### Type 2: Templated Resources (Parameterized)

URIs with parameters — they fetch different data based on parameters.

**Example:** `docs://documents/{doc_id}`

```python
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    """Fetch a specific document by ID."""
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]
```

**How it works:**

The Python SDK **automatically parses parameters from the URI** and passes them as keyword arguments:

```
Client requests: docs://documents/report.pdf
    ↓
SDK extracts: doc_id = "report.pdf"
    ↓
SDK calls: fetch_doc(doc_id="report.pdf")
    ↓
Server returns: "The report details a 20m condenser tower..."
```

---

## MIME Types: Describing Resource Data

The `mime_type` parameter tells clients what kind of data you're returning:

```python
# Plain text content
@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_doc(doc_id: str) -> str:
    return docs[doc_id]

# JSON structured data
@mcp.resource("docs://metadata", mime_type="application/json")
def get_metadata() -> dict:
    return {"total_docs": len(docs), "last_updated": "2025-01-15"}

# HTML content
@mcp.resource("docs://preview/{doc_id}", mime_type="text/html")
def get_html_preview(doc_id: str) -> str:
    return f"<h1>{doc_id}</h1><p>{docs[doc_id]}</p>"

# Binary image data
@mcp.resource("images/{filename}", mime_type="image/png")
def get_image(filename: str) -> bytes:
    with open(f"images/{filename}", "rb") as f:
        return f.read()
```

**Common MIME Types:**
- `text/plain` — Plain text
- `text/html` — HTML content
- `application/json` — JSON data
- `image/png`, `image/jpeg` — Images
- `application/pdf` — PDF documents

**Benefits:**
- ✅ Clients know how to interpret the data
- ✅ Claude can use appropriate handling
- ✅ Clear API contracts
- ✅ Tool-agnostic data exchange

---

## Implementing Resources in Your Server

### Step 1: Add Direct Resource (List Documents)

```python
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    """Return a list of all available document IDs."""
    return list(docs.keys())
```

### Step 2: Add Templated Resource (Fetch Document)

```python
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    """Fetch the contents of a specific document."""
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]
```

### Step 3: Update Server Initialization

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")

docs = {
    "report.pdf": "The report details a 20m condenser tower.",
    "deposition.md": "This deposition covers Angela Smith's testimony.",
    # ... more documents
}

@mcp.tool(...)
def read_document(...):
    # ... existing tool code

@mcp.resource(...)
def list_docs() -> list[str]:
    return list(docs.keys())

@mcp.resource(...)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

---

## Testing Resources with the Inspector

### Running Your Server

```bash
uv run mcp dev mcp_server.py
```

Then open the inspector at `http://localhost:6277`.

### What You'll See

The inspector shows two sections:

**1. Resources: Static Resources**
```
docs://documents
├─ MIME Type: application/json
├─ Description: (auto-generated)
└─ Click to view data
```

**2. Resource Templates: Templated Resources**
```
docs://documents/{doc_id}
├─ Parameters: doc_id (string)
├─ MIME Type: text/plain
└─ Enter parameter value to test
```

### Testing Steps

**Test Direct Resource:**
1. Click on `docs://documents`
2. See returned list: `["report.pdf", "deposition.md", "financials.docx"]`

**Test Templated Resource:**
1. Click on `docs://documents/{doc_id}`
2. Enter `doc_id = "report.pdf"`
3. See returned content: `"The report details a 20m condenser tower."`
4. Try with invalid ID to test error handling
5. See error: `"Doc with id invalid.pdf not found"`

---

## Real-World Use Cases

### Use Case 1: Document Mention Feature

```python
# User types: "Summarize @report.pdf"
# Your app:
# 1. Detects @mention
# 2. Uses client to read: docs://documents/report.pdf
# 3. Injects content into Claude's prompt
# 4. Claude analyzes and responds
```

### Use Case 2: Autocomplete

```python
# User starts typing: "Show me @re..."
# Your app:
# 1. Uses client to read: docs://documents
# 2. Gets list: ["report.pdf", "requirements.md", ...]
# 3. Filters to matches: ["report.pdf", "requirements.md"]
# 4. Shows autocomplete suggestions
```

### Use Case 3: File Browser

```python
# User clicks "Browse files"
# Your app:
# 1. Uses client to read: docs://documents (direct resource)
# 2. Shows: report.pdf, deposition.md, etc.
# 3. User selects report.pdf
# 4. Your app reads: docs://documents/report.pdf (templated resource)
# 5. Shows preview/content
```

### Use Case 4: Metadata Queries

```python
@mcp.resource("docs://metadata", mime_type="application/json")
def get_metadata() -> dict:
    return {
        "total_documents": len(docs),
        "documents": list(docs.keys()),
        "last_updated": "2025-01-15",
        "total_size_bytes": sum(len(d) for d in docs.values())
    }
```

---

## Key Differences: Resources vs Tools

When deciding between resources and tools, ask:

**Use Resources if:**
- ✅ You're exposing data (reading)
- ✅ The operation is read-only
- ✅ Data is context for Claude (mention feature)
- ✅ Multiple clients need the same data
- ✅ You want automatic serialization

**Use Tools if:**
- ✅ You're performing actions
- ✅ State changes (create, update, delete)
- ✅ Client decides when to call
- ✅ Complex logic with side effects
- ✅ Requires parameter validation

---

## Combining Resources and Tools

Most servers use **both** resources and tools:

```python
@mcp.tool(
    name="edit_document",
    description="Edit a document"
)
def edit_document(doc_id: str, old_str: str, new_str: str):
    """Tool: Modifies document state."""
    if doc_id not in docs:
        raise ValueError(f"Doc {doc_id} not found")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    return docs[doc_id]

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    """Resource: Exposes document data."""
    if doc_id not in docs:
        raise ValueError(f"Doc {doc_id} not found")
    return docs[doc_id]
```

**Complete flow:**
```
1. Tool `edit_document` → Modifies document
2. Resource `docs://documents/{doc_id}` → Fetches updated content
3. Client shows updated content to user
```

---

## Error Handling

Resources use the same error handling as tools:

```python
@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        # Raise ValueError for meaningful error
        raise ValueError(f"Doc with id {doc_id} not found")
    
    if not doc_id.endswith(('.pdf', '.md', '.txt')):
        # Validate format
        raise ValueError(f"Unsupported document format: {doc_id}")
    
    return docs[doc_id]
```

When an error is raised:
1. MCP Server catches the exception
2. Returns error to client
3. Client sees meaningful error message
4. Claude can inform user or try alternative approach

---

## Summary: Resources Benefits

✅ **Clean API** — Define once, use everywhere  
✅ **Automatic Serialization** — SDK handles conversion  
✅ **MIME Type Hints** — Clients understand data format  
✅ **Parameter Parsing** — URIs become function arguments  
✅ **Error Handling** — Exceptions become error messages  
✅ **Read-Only Semantics** — Clear intent vs tools  
✅ **Inspector Testing** — Test without client code  

Resources provide a clean way to make data available to MCP clients, enabling features like document mentions, file browsing, autocomplete, or any scenario where you need to fetch information from your server.

---

## Next: Combining with Client

Once resources are defined, MCP clients can:
1. List available resources
2. Request resource data with URIs
3. Use returned data in their applications
4. Build features like document mentions and autocomplete

Resources and tools together form the complete MCP server API.

---

# Prompts in MCP Servers: Pre-Built Instructions

## What are Prompts?

**Prompts** in MCP servers let you define **pre-built, high-quality instructions** that clients can use instead of writing their own prompts from scratch.

Think of them as **carefully crafted templates** that give better results than what users might come up with on their own.

---

## Why Use Prompts?

### The Problem
A user could type: *"convert report.pdf to markdown"*

This would work, but they'd probably get inconsistent results.

### The Solution
Provide a tested prompt that includes:
- ✅ Specific formatting instructions
- ✅ Structure requirements
- ✅ Output specifications
- ✅ Best practices for the task
- ✅ Expected format examples

**Key insight:** Users can accomplish tasks on their own, but they get **more consistent and higher-quality results** when using prompts developed and tested by MCP server authors.

---

## How Prompts Work

Prompts define a set of **user and assistant messages** that clients can use directly. When a client requests a prompt, your server returns messages ready to send to Claude.

### Basic Flow

```
Client requests: "Get me the format_document prompt"
    ↓
Server returns: [UserMessage(...), AssistantMessage(...), ...]
    ↓
Client sends messages directly to Claude
    ↓
Claude executes using the prompt instructions
```

### Key Features

- ✅ **Define once** — Write the prompt in your server
- ✅ **Reuse everywhere** — All clients get the same quality
- ✅ **Parameter interpolation** — Insert dynamic data into prompts
- ✅ **Message structure** — Return complete conversation threads
- ✅ **Best practices built-in** — Benefit from server author's expertise

---

## Implementing Prompts

### Step 1: Import Message Types

```python
from mcp.server.fastmcp import FastMCP, base
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")
```

### Step 2: Define Your Prompt

```python
@mcp.prompt(
    name="format",
    description="Rewrites the contents of a document in Markdown format."
)
def format_document(
    doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
    """
    A prompt that instructs Claude to reformat a document to markdown.
    """
    prompt_text = f"""
Your goal is to reformat a document to be written with markdown syntax.

The document you need to reformat has id: {doc_id}

When reformatting:
- Add headers (#, ##, ###) to organize content
- Use bullet points and numbered lists
- Create tables where appropriate
- Use bold and italics for emphasis
- Include code blocks for technical content
- Maintain the original information and meaning

Use the 'edit_document' tool to apply changes to the document.
After reformatting is complete, verify the changes look correct.
"""
    
    return [
        base.UserMessage(prompt_text)
    ]
```

**What it does:**
1. Uses `@mcp.prompt()` decorator to define a prompt
2. Takes parameters (like `doc_id`)
3. Returns a list of `base.Message` objects
4. Messages can be `UserMessage`, `AssistantMessage`, etc.

---

## Message Types

### UserMessage
Messages from the user that set up the task:

```python
@mcp.prompt(name="analyze", description="Analyze a document")
def analyze_document(doc_id: str) -> list[base.Message]:
    return [
        base.UserMessage(f"Please analyze the document with id: {doc_id}")
    ]
```

### AssistantMessage
Pre-filled assistant responses that guide Claude:

```python
@mcp.prompt(name="format", description="Format as markdown")
def format_prompt() -> list[base.Message]:
    return [
        base.UserMessage("Format this as markdown"),
        base.AssistantMessage("I'll reformat the document using markdown syntax..."),
        base.UserMessage("Here's the document content to format...")
    ]
```

This creates a conversation thread that Claude continues.

---

## Real-World Example: Complete Formatting Prompt

```python
@mcp.prompt(
    name="summarize",
    description="Summarize a document into key points."
)
def summarize_document(
    doc_id: str = Field(description="Id of the document to summarize"),
    length: str = Field(
        description="Summary length: brief, medium, or detailed",
        default="medium"
    )
) -> list[base.Message]:
    """
    A comprehensive summarization prompt with length options.
    """
    length_guide = {
        "brief": "3-5 bullet points",
        "medium": "5-10 bullet points",
        "detailed": "10-15 bullet points or paragraphs"
    }
    
    prompt_text = f"""
You are a document summarization expert. Your task is to create a {length} summary of a document.

Document ID: {doc_id}
Summary Style: {length} ({length_guide.get(length, "medium summary")})

When summarizing:
1. Extract the most important information
2. Remove redundant details
3. Organize information logically
4. Use clear, concise language
5. Preserve key statistics and dates
6. Highlight any critical findings or recommendations

Format your summary as:
- Key Points (bullet list)
- Important Details (if applicable)
- Recommendations (if applicable)

After completing the summary, confirm that all critical information has been captured.
"""
    
    return [
        base.UserMessage(prompt_text)
    ]
```

**How it's used:**
```python
# Client requests the prompt
prompt_messages = await client.get_prompt(
    "summarize",
    {"doc_id": "report.pdf", "length": "detailed"}
)

# Server returns messages with interpolated values
# Client sends to Claude, who follows the instructions
```

---

## Testing Prompts with Inspector

### Step 1: Start Inspector
```bash
mcp dev mcp_server.py
```

### Step 2: Open Browser
Navigate to `http://localhost:6277`

### Step 3: Find Prompts Section
Look for **Prompts** in the inspector interface

### Step 4: Test Your Prompt
1. Select your prompt from the list
2. Enter any required parameters
3. Click "Get Prompt"
4. See the generated messages

**Inspector shows:**
```
Prompt: format
Description: Rewrites the contents of a document in Markdown format.
Parameters: doc_id (required)

Generated Messages:
[
  {
    "type": "user",
    "content": "Your goal is to reformat a document..."
  }
]
```

This verifies parameter interpolation and message structure before using in production.

---

## Prompts vs Tools vs Resources

| Feature | Tools | Resources | Prompts |
|---------|-------|-----------|---------|
| **Purpose** | Perform actions | Fetch data | Provide instructions |
| **Example** | Edit document | List documents | Format document instructions |
| **Who decides** | Claude | Your app | Your server |
| **API analogy** | POST/PUT/DELETE | GET | Template/Configuration |
| **Client integration** | Call via Claude | Read directly | Get and use |

---

## When to Use Prompts

### ✅ Good Use Cases
- Complex, multi-step tasks that benefit from careful instruction
- Domain-specific expertise you want to encapsulate
- Tasks where consistency is important
- Workflows that should follow specific patterns
- Reusable instructions for common operations

### ❌ Not Necessary
- Simple, straightforward requests
- Tasks where user input is the key factor
- One-off operations with no standard pattern
- Highly customizable workflows

---

## Best Practices for Prompts

### 1. **Focus on Core Value**
Only create prompts for tasks central to your server's purpose.

```python
# ✅ Good - Core to document server
@mcp.prompt(name="format", description="Format to markdown")

# ❌ Not necessary - Too generic
@mcp.prompt(name="hello", description="Say hello")
```

### 2. **Write Detailed Instructions**
Be specific about what you want Claude to do.

```python
# ❌ Vague
return [base.UserMessage("Summarize the document")]

# ✅ Specific
return [base.UserMessage("""
Summarize the document in 5-10 bullet points.
Focus on: key findings, risks, and recommendations.
Use technical language where appropriate.
Format as markdown with clear hierarchy.
""")]
```

### 3. **Test Thoroughly**
Verify prompts work with various inputs.

```python
# Test with different doc_ids
await client.get_prompt("format", {"doc_id": "report.pdf"})
await client.get_prompt("format", {"doc_id": "notes.md"})
await client.get_prompt("format", {"doc_id": "data.csv"})
```

### 4. **Clear Descriptions**
Help users understand what each prompt does.

```python
@mcp.prompt(
    name="format",
    # This description is what clients see
    description="Rewrites document content in well-structured Markdown format with proper headers, lists, and formatting."
)
def format_document(...):
    ...
```

### 5. **Leverage Your Expertise**
Include best practices and domain knowledge.

```python
@mcp.prompt(name="analyze", description="Analyze for security risks")
def analyze_security(doc_id: str) -> list[base.Message]:
    return [
        base.UserMessage(f"""
Analyze document {doc_id} for security risks.

Check for:
1. Hardcoded credentials
2. Unencrypted data transmission
3. Weak authentication mechanisms
4. SQL injection vulnerabilities
5. Cross-site scripting (XSS) risks
6. Insecure dependencies

Provide:
- Severity level (Critical, High, Medium, Low)
- Description of each risk
- Recommended fixes
- References to security standards (OWASP, CWE)
""")
    ]
```

---

## Real Application: Document Processing Pipeline

```python
@mcp.prompt(name="extract_metadata", description="Extract key metadata from document")
def extract_metadata(doc_id: str) -> list[base.Message]:
    return [base.UserMessage(f"Extract from {doc_id}: title, author, date, keywords")]

@mcp.prompt(name="format", description="Format to markdown")
def format_document(doc_id: str) -> list[base.Message]:
    return [base.UserMessage(f"Reformat {doc_id} as markdown")]

@mcp.prompt(name="summarize", description="Create summary")
def summarize_document(doc_id: str) -> list[base.Message]:
    return [base.UserMessage(f"Summarize {doc_id} in 5 key points")]

# Client workflow
async with MCPClient(...) as client:
    # Get list of available prompts
    prompts = await client.list_prompts()  # Shows all 3 prompts
    
    # Use each prompt in sequence
    metadata = await client.get_prompt("extract_metadata", {"doc_id": "report.pdf"})
    formatted = await client.get_prompt("format", {"doc_id": "report.pdf"})
    summary = await client.get_prompt("summarize", {"doc_id": "report.pdf"})
    
    # Send to Claude for execution
```

---

## Summary: Prompts Benefits

✅ **Quality Assurance** — Tested, optimized instructions  
✅ **Consistency** — Same results across all clients  
✅ **Expertise Sharing** — Server author's domain knowledge  
✅ **Parameter Flexibility** — Dynamic values in templates  
✅ **Message Threading** — Complete conversation structures  
✅ **Inspector Testing** — Verify before use  

Prompts let you encode best practices into your MCP server, ensuring all clients benefit from carefully crafted, high-quality instructions.

---

# Using Prompts in MCP Clients

## Overview

On the client side, you need to implement methods that work with server-provided prompts. The client fetches prompts from the server and integrates them into Claude conversations.

**Key principle:** Prompts define a set of **user and assistant messages** that can be used directly by the client. These should be high-quality, well-tested, and relevant to the overall purpose of the MCP server.

---

## Method 1: List Available Prompts

Retrieve all prompts offered by the MCP server:

```python
async def list_prompts(self) -> list[types.Prompt]:
    # Get all available prompts from the MCP server
    result = await self.session().list_prompts()
    return result.prompts
```

**What it does:**
1. Calls the session's built-in `list_prompts()` method
2. Extracts the prompts array from the result
3. Returns the list of available prompts

**Example usage:**
```python
async with MCPClient("uv", ["run", "mcp_server.py"]) as client:
    prompts = await client.list_prompts()
    for prompt in prompts:
        print(f"Prompt: {prompt.name}")
        print(f"Description: {prompt.description}")
        print(f"Arguments: {prompt.arguments}")
```

**Output:**
```
Prompt: format
Description: Rewrites the contents of the document in Markdown Format.
Arguments: [{'name': 'doc_id', 'description': 'Id of the document to format'}]

Prompt: summarize
Description: Summarize a document into key points.
Arguments: [{'name': 'doc_id', ...}]
```

---

## Method 2: Get a Specific Prompt with Arguments

Retrieve a specific prompt with arguments interpolated:

```python
async def get_prompt(self, prompt_name: str, args: dict[str, str]):
    # Request a specific prompt with arguments
    result = await self.session().get_prompt(prompt_name, args)
    return result.messages
```

**What it does:**
1. Takes the prompt name (e.g., `"format"`)
2. Takes an arguments dictionary with expected keys
3. Sends request to server with arguments
4. Server passes arguments as keyword arguments to prompt function
5. Returns the interpolated messages

**Example usage:**
```python
# Get the format prompt for a specific document
messages = await client.get_prompt(
    "format",
    {"doc_id": "report.pdf"}
)

# Messages now contain the interpolated prompt
# Example: "The id of the document you need to reformat is: report.pdf"
```

---

## How Prompt Arguments Work

When you define a prompt function on the server, it accepts parameters:

```python
# Server side
@mcp.prompt(name="format", description="...")
def format_document(
    doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
    prompt = f"Reformat document: {doc_id}"
    return [base.UserMessage(prompt)]
```

When the client calls `get_prompt`, arguments get passed as keyword arguments:

```python
# Client side
result = await client.get_prompt(
    "format",
    {"doc_id": "report.pdf"}  # This becomes: format_document(doc_id="report.pdf")
)
```

The server inserts the values into the prompt template before returning messages.

---

## Complete Client Method

Here's the complete implementation in your MCPClient class:

```python
async def list_prompts(self) -> list[types.Prompt]:
    """List all available prompts from the MCP server."""
    result = await self.session().list_prompts()
    return result.prompts

async def get_prompt(self, prompt_name: str, args: dict[str, str]):
    """Get a specific prompt with arguments interpolated."""
    result = await self.session().get_prompt(prompt_name, args)
    return result.messages
```

---

## Using Prompts with Claude

### Complete Workflow

```
1. USER SELECTS PROMPT
   Type: /format report.pdf
   
2. CLIENT LISTS PROMPTS
   prompts = await client.list_prompts()
   
3. CLIENT FINDS PROMPT
   prompt_obj = prompts[0]  # "format"
   
4. CLIENT GETS PROMPT WITH ARGS
   messages = await client.get_prompt("format", {"doc_id": "report.pdf"})
   
5. SEND TO CLAUDE
   response = await claude.messages.create(
       model="...",
       messages=messages,  # Pre-built messages from prompt
       tools=[...]  # Your MCP tools
   )
   
6. CLAUDE EXECUTES
   Claude uses the prompt instructions + tools to complete task
```

### Example: Format Document via Prompt

```python
async def format_document_command(doc_id: str):
    """User command: /format report.pdf"""
    
    async with MCPClient("uv", ["run", "mcp_server.py"]) as client:
        # Get tools for Claude to use
        tools = await client.list_tools()
        
        # Get the format prompt
        prompt_messages = await client.get_prompt(
            "format",
            {"doc_id": doc_id}
        )
        
        # Send to Claude
        response = await claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=prompt_messages,  # Prompt provides the instructions
            tools=[{
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            } for tool in tools]
        )
        
        # Claude now follows the prompt instructions
        # and uses tools as needed
        return response
```

---

## Testing Prompts in CLI

Once implemented, prompts appear as commands in your application:

```
User: /format report.pdf
   ↓
App shows available arguments:
   doc_id (required): Id of the document to format
   ↓
User enters: report.pdf
   ↓
App fetches prompt: get_prompt("format", {"doc_id": "report.pdf"})
   ↓
App sends prompt messages to Claude
   ↓
Claude executes using prompt instructions + available tools
```

---

## Real-World Example: Interactive CLI

```python
async def interactive_prompt_menu():
    """User selects and executes prompts interactively."""
    
    async with MCPClient("uv", ["run", "mcp_server.py"]) as client:
        # Step 1: List available prompts
        prompts = await client.list_prompts()
        
        print("Available Prompts:")
        for i, prompt in enumerate(prompts):
            print(f"{i+1}. {prompt.name} - {prompt.description}")
        
        # Step 2: User selects a prompt
        choice = int(input("Select prompt (1-3): ")) - 1
        selected_prompt = prompts[choice]
        
        # Step 3: Collect arguments
        args = {}
        for arg in selected_prompt.arguments:
            value = input(f"Enter {arg['name']}: ")
            args[arg['name']] = value
        
        # Step 4: Get the prompt with arguments
        messages = await client.get_prompt(selected_prompt.name, args)
        
        # Step 5: Send to Claude
        tools = await client.list_tools()
        response = await claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=messages,
            tools=[{
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            } for tool in tools]
        )
        
        print(response.content[0].text)
```

---

## Prompts vs Resources vs Tools

| Aspect | Tools | Resources | Prompts |
|--------|-------|-----------|---------|
| **Purpose** | Actions | Data | Instructions |
| **Called by** | Claude (tool use) | App (direct fetch) | App (before Claude) |
| **Returns** | Result of action | Data content | Message templates |
| **Example** | `edit_document()` | `docs://documents/x` | Format instructions |
| **Integration** | Multi-turn with Claude | Context injection | Single shot to Claude |

---

## Best Practices for Using Prompts

### 1. **Cache Prompt Arguments**
Store frequently used arguments:
```python
common_args = {"doc_id": "report.pdf", "length": "medium"}
messages = await client.get_prompt("summarize", common_args)
```

### 2. **Validate Arguments Before Requesting**
Check that required arguments are provided:
```python
required_args = {"doc_id", "format"}
provided_args = set(user_input.keys())
if not required_args.issubset(provided_args):
    print(f"Missing: {required_args - provided_args}")
```

### 3. **Combine Multiple Prompts**
Chain prompts for complex workflows:
```python
# First: Extract metadata
meta_messages = await client.get_prompt("extract_metadata", {"doc_id": "x"})
# Then: Format document
format_messages = await client.get_prompt("format", {"doc_id": "x"})
# Finally: Summarize
summary_messages = await client.get_prompt("summarize", {"doc_id": "x"})
```

### 4. **Handle Prompt Errors Gracefully**
```python
try:
    messages = await client.get_prompt("format", args)
except ValueError as e:
    print(f"Prompt error: {e}")
    # Fallback to basic instruction
    messages = [base.UserMessage("Please reformat this document")]
```

---

## Complete MCP Client API Summary

Your MCPClient now supports:

| Method | Purpose | Returns |
|--------|---------|---------|
| `list_tools()` | Get available tools | `list[types.Tool]` |
| `call_tool(name, input)` | Execute a tool | `types.CallToolResult` |
| `list_prompts()` | Get available prompts | `list[types.Prompt]` |
| `get_prompt(name, args)` | Get prompt with args | `list[base.Message]` |
| `read_resource(uri)` | Fetch resource data | Data (text, JSON, etc.) |

Together, these methods provide complete access to all MCP server capabilities!

---

## The Complete MCP Server API

Your MCP servers now provide:

1. **Tools** — Actions clients can request (edit, create, delete)
2. **Resources** — Data clients can fetch (files, metadata, lists)
3. **Prompts** — Instructions clients can use (workflows, templates)

Together, these three features create a complete API for AI applications.

---

# MCP Server Primitives: The Complete Picture

## Understanding Control Flow

MCP has three core primitives, each controlled by a different actor:

### **Tools** — Model-Controlled

```
Claude decides when to call these
    ↓
Results are used by Claude
    ↓
Used for: Giving additional functionality to Claude
```

**Who controls?** **Claude** (the AI model)

**When called?** When Claude decides they're useful

**Who uses results?** Claude uses them to answer questions

**Examples:**
- Edit documents
- Trigger builds
- Send emails
- Fetch real-time data

**Example flow:**
```
User: "Update the report to include 2024 data"
    ↓
Claude: "I need to read the report and edit it"
    ↓
Claude calls: read_document() → edit_document()
    ↓
Claude: "Done! I've updated the report."
```

---

### **Resources** — App-Controlled

```
Our app decides when to call these
    ↓
Results are used primarily by our app
    ↓
Used for: Getting data into our app, Adding context to messages
```

**Who controls?** **Your application**

**When called?** When your app logic decides it needs data

**Who uses results?** Your app uses them (optionally passes to Claude)

**Examples:**
- Fetch document content for display
- List available files for autocomplete
- Get metadata for context
- Search results for mentions (@document)

**Example flow:**
```
User types: "Summarize @report.pdf"
    ↓
App detects: @report.pdf mention
    ↓
App calls: read_resource("docs://documents/report.pdf")
    ↓
App gets: Document content
    ↓
App injects into prompt to Claude
    ↓
Claude: "Here's the summary..."
```

---

### **Prompts** — User-Controlled

```
The user decides when to use these
    ↓
Used for: Workflows to run based on user input
    ↓
Like: Slash command, button click, or menu option
```

**Who controls?** **The user/your app**

**When called?** When user explicitly selects/requests (via `/command`, button, menu)

**Who uses results?** Claude uses the prompt instructions

**Examples:**
- `/format document.txt` — Format to markdown
- `/analyze build-123` — Analyze for failures
- `/explain config.yml` — Explain configuration
- `/research topic` — Research using documents

**Example flow:**
```
User: /format report.pdf
    ↓
App detects: User selected format command
    ↓
App calls: get_prompt("format", {"doc_id": "report.pdf"})
    ↓
App sends prompt messages to Claude
    ↓
Claude follows prompt: "Format this as markdown"
    ↓
Claude calls tools as needed to complete task
```

---

## Control Flow Comparison

| Aspect | Tools | Resources | Prompts |
|--------|-------|-----------|---------|
| **Who controls?** | Claude (AI Model) | Your App | User/App |
| **When called?** | When Claude decides | When app needs data | When user requests |
| **Who uses result?** | Claude | Your app (context/display) | Claude (as instructions) |
| **Integration with Claude?** | Direct (tool use) | Indirect (context) | Direct (instructions) |
| **Decision maker** | AI | Application logic | Human/UI |
| **Used for** | Additional functionality | Data fetching | Guided workflows |

---

## Decision Tree: Which to Use?

```
Does Claude need to DO something?
├─ YES → Use TOOL (Claude decides when to call)
│   Example: edit_document, trigger_build
│
└─ NO → Do you need DATA?
   ├─ YES → Use RESOURCE (Your app decides when to fetch)
   │   Example: get_document, list_files
   │
   └─ NO → Is there a USER WORKFLOW?
      └─ YES → Use PROMPT (User triggers via /command)
          Example: /format, /analyze, /summarize
```

---

## Real-World Scenario: Build System MCP

Let's see how all three work together:

```python
# TOOLS - Claude can trigger builds
@mcp.tool(name="trigger_build")
def trigger_build(branch: str) -> str:
    """Claude decides when to trigger"""
    return run_build(branch)

# RESOURCES - App fetches status
@mcp.resource("builds://current/{branch}")
def get_build_status(branch: str) -> dict:
    """App decides when to check status"""
    return get_latest_build(branch)

# PROMPTS - User runs workflows
@mcp.prompt(name="debug_failure")
def debug_prompt(build_id: str) -> list[base.Message]:
    """User explicitly asks to debug"""
    return [base.UserMessage(f"Debug build {build_id}...")]
```

**User interaction:**
```
User: /debug_failure 456
    ↓
App gets prompt (USER CONTROLS)
    ↓
Claude follows instructions: "Analyze this build failure"
    ↓
Claude calls: trigger_build("main") (CLAUDE CONTROLS)
    ↓
Your app fetches: get_build_status("main") (APP CONTROLS)
    ↓
Claude gets all info, provides analysis
```

---

## Key Insight

The three primitives solve **who decides**:

- **Tools** answer: "What should Claude be able to do?"
- **Resources** answer: "What data should my app have access to?"
- **Prompts** answer: "What workflows should users be able to trigger?"

Each is controlled by a different actor, making MCP flexible for any architecture.

---

## Next: Connecting the MCP Client

---

## Next: Connecting the MCP Client

Once the server is running, the MCP client connects to it and:
1. Requests the tool list
2. Passes tools to Claude
3. Claude decides which tools to use
4. Client executes tools on the server
5. Results flow back to Claude

This is the power of separation: **server and client are independent processes** that communicate through the MCP protocol.

---

# Building an MCP Client: Connecting Your Application

## Understanding the Client Architecture

Now that we have our MCP server working, it's time to build the **client side**. The client is what allows your application to communicate with the MCP server and access its functionality.

**Important distinction:** In most real-world projects, you implement **either** an MCP client **OR** an MCP server, not both. We're building both here for educational purposes — to show you how they work together.

---

## Client Components

The MCP client consists of two main components:

### 1. Client Session
The actual connection to the server (provided by the MCP Python SDK):
```python
from mcp import ClientSession
```
This handles the low-level protocol communication.

### 2. MCPClient Class
A custom wrapper class we create to make using the session easier:
```python
class MCPClient:
    def __init__(self, command: str, args: list[str], env: Optional[dict] = None):
        self._session: Optional[ClientSession] = None
        self._exit_stack: AsyncExitStack = AsyncExitStack()
    
    async def connect(self):
        # Establish connection to server
        ...
```

**Why wrap it?** The client session requires proper **resource cleanup** when you're done. We wrap it in our custom class to handle cleanup automatically using async context managers.

---

## How the Client Fits Into Your Application

Our application needs to do two main things with the MCP server:

1. **Get available tools** — Retrieve all tools from the server to send to Claude
2. **Execute tools** — Run specific tools when Claude requests them

The MCP client provides these capabilities through simple method calls.

```
Your App
    ↓
"Give me tools" ← MCPClient.list_tools()
    ↓
MCP Server → [tool1, tool2, tool3...]
    ↓
"Execute tool1 with params" ← MCPClient.call_tool()
    ↓
MCP Server → result
    ↓
Your App
```

---

## Implementing the Core Methods

### Method 1: List Available Tools

```python
async def list_tools(self) -> list[types.Tool]:
    # Get all available tools from the MCP server
    result = await self.session().list_tools()
    return result.tools
```

**What it does:**
1. Accesses the client session (connection to server)
2. Calls the SDK's built-in `list_tools()` function
3. Extracts and returns the tools list

**Example usage:**
```python
client = MCPClient("uv", ["run", "mcp_server.py"])
await client.connect()
tools = await client.list_tools()
# Returns: [Tool(name='read_doc_contents', ...), Tool(name='edit_document', ...)]
```

### Method 2: Execute a Specific Tool

```python
async def call_tool(
    self, tool_name: str, tool_input: dict
) -> types.CallToolResult | None:
    # Execute a tool with the given parameters
    return await self.session().call_tool(tool_name, tool_input)
```

**What it does:**
1. Takes the tool name (e.g., "read_doc_contents")
2. Takes the parameters Claude wants to pass (e.g., `{"doc_id": "report.pdf"}`)
3. Sends the request to the MCP server
4. Returns the result

**Example usage:**
```python
result = await client.call_tool(
    "read_doc_contents", 
    {"doc_id": "report.pdf"}
)
# Returns: CallToolResult with document content
```

### Method 3: Read Resources from Server

Resources allow you to **fetch data directly from the server** without Claude making decisions. This is perfect for document mentions (`@document_name`) and autocomplete.

```python
async def read_resource(self, uri: str) -> Any:
    # Read a resource from the MCP server
    result = await self.session().read_resource(AnyUrl(uri))
    resource = result.contents[0]
    
    # Handle different content types
    if isinstance(resource, types.TextResourceContents):
        if resource.mimeType == "application/json":
            return json.loads(resource.text)
        return resource.text
```

**What it does:**
1. Takes a resource URI (e.g., `"docs://documents/report.pdf"`)
2. Sends ReadResourceRequest to the MCP server
3. Parses the response based on MIME type
4. Returns the parsed data

**Example usage:**
```python
# Get plain text resource
text_content = await client.read_resource("docs://documents/deposition.md")
# Returns: "This deposition covers the testimony of Angela Smith, P.E."

# Get JSON resource
json_content = await client.read_resource("api://documents/metadata")
# Returns: {"total": 6, "formats": ["pdf", "md", "docx"]}
```

**How it fits into your app:**
```
User types: "Summarize @report.pdf"
    ↓
Your app detects @mention
    ↓
App calls: await client.read_resource("docs://documents/report.pdf")
    ↓
Server returns: "The report details a 20m condenser tower..."
    ↓
Your app injects into Claude's prompt
    ↓
Claude analyzes and responds
```

---

## Required Imports for Resource Reading

To use the resource reading functionality, you need these imports:

```python
import json
from pydantic import AnyUrl
from mcp import types

# Then use them in your client:
async def read_resource(self, uri: str) -> Any:
    result = await self.session().read_resource(AnyUrl(uri))
    resource = result.contents[0]
    
    if isinstance(resource, types.TextResourceContents):
        if resource.mimeType == "application/json":
            return json.loads(resource.text)
        return resource.text
```

**Why these imports?**
- `json` — Parse JSON resources into Python objects
- `AnyUrl` — Properly validate and handle URI parameters
- `types` — Access TextResourceContents and other MCP types

---

## Resource vs Tool: Client Perspective

| Aspect | Tools | Resources |
|--------|-------|-----------|
| **How called** | `await client.call_tool(name, input)` | `await client.read_resource(uri)` |
| **Server decides** | Tool execution | Resource data |
| **When to use** | Actions (edit, create) | Data fetching |
| **Claude involved** | Yes (Claude calls tools) | Optional (app can fetch directly) |
| **Example** | Edit document | Get document contents |

---

## Real-World Example: Document Mention Feature

```python
async def handle_user_message(user_input: str):
    # Detect @mentions
    mentions = re.findall(r'@(\S+)', user_input)
    
    # Fetch resource data for each mention
    document_context = {}
    async with MCPClient("uv", ["run", "mcp_server.py"]) as client:
        for mention in mentions:
            # Read the document resource
            content = await client.read_resource(f"docs://documents/{mention}")
            document_context[mention] = content
    
    # Build enhanced prompt with document content
    enhanced_message = user_input
    for mention, content in document_context.items():
        enhanced_message += f"\n\n@{mention} contains:\n{content}"
    
    # Send to Claude with full context
    response = await claude.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": enhanced_message}]
    )
    
    return response
```

**What happens:**
```
User: "Compare @report.pdf and @financials.docx"
    ↓
App detects: ["report.pdf", "financials.docx"]
    ↓
App reads both resources
    ↓
App builds message with both documents injected
    ↓
Claude sees both documents in prompt
    ↓
Claude compares them directly
```

---

## Connection and Cleanup

### Async Context Manager Pattern

The client uses Python's async context manager pattern for automatic cleanup:

```python
async with MCPClient(
    command="uv",
    args=["run", "mcp_server.py"]
) as client:
    tools = await client.list_tools()
    result = await client.call_tool("read_doc_contents", {"doc_id": "report.pdf"})
    # Connection is automatically cleaned up when exiting the block
```

### What happens automatically:

1. **Enter (`__aenter__`):** Establishes connection to server
2. **Use (`async with`):** Use tools and methods normally
3. **Exit (`__aexit__`):** Cleans up connection and resources

This ensures proper cleanup even if errors occur.

---

## Testing the Client

To verify the client works, we can run a simple test:

```python
async def test_client():
    async with MCPClient(
        command="uv",
        args=["run", "mcp_server.py"]
    ) as client:
        # Test listing tools
        tools = await client.list_tools()
        print(f"Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool.name}")
        
        # Test executing a tool
        result = await client.call_tool(
            "read_doc_contents",
            {"doc_id": "report.pdf"}
        )
        print(f"\nTool result: {result}")
```

When run, this outputs:
```
Found 2 tools:
  - read_doc_contents
  - edit_document

Tool result: meta=None content=[TextContent(...)] isError=False
```

---

## The Client in Your Application Flow

Here's how the client integrates into the complete application:

```
1. USER INPUT
   "What's in report.pdf?"
       ↓
2. APP USES CLIENT
   tools = await client.list_tools()
       ↓
3. SEND TO CLAUDE
   messages=[...], tools=[tool schemas from step 2]
       ↓
4. CLAUDE DECIDES
   "I need to call read_doc_contents"
       ↓
5. APP EXECUTES VIA CLIENT
   result = await client.call_tool("read_doc_contents", {"doc_id": "report.pdf"})
       ↓
6. SEND RESULT TO CLAUDE
   "Tool executed, result: ..."
       ↓
7. CLAUDE RESPONDS
   "The report details a 20m condenser tower"
       ↓
8. USER GETS ANSWER
```

---

## Key Client Responsibilities

The MCP client abstracts away several complex tasks:

| Task | Without Client | With Client |
|------|---|---|
| **Connection management** | Manual stdio setup | Automatic via context manager |
| **Message protocol** | Handle JSON/MCP protocol | Transparent to your code |
| **Resource cleanup** | Manual cleanup (error-prone) | Automatic |
| **Tool listing** | Construct ListToolsRequest | Simple `list_tools()` call |
| **Tool execution** | Construct CallToolRequest | Simple `call_tool()` call |

The client makes server integration as simple as calling methods.

---

## Comparison: With vs Without Client

### Without MCP Client (Manual Approach)
```python
# Complex setup and protocol handling
server_params = StdioServerParameters(command="uv", args=["run", "mcp_server.py"])
transport = await stdio_client(server_params)
session = await ClientSession(transport[0], transport[1])
await session.initialize()

# Manually construct and send messages
tools_result = await session.list_tools()  # Still fairly simple with SDK

# Manual cleanup (prone to errors)
await session.close()
await transport.close()
```

### With MCP Client (Our Approach)
```python
# Clean and simple
async with MCPClient("uv", ["run", "mcp_server.py"]) as client:
    tools = await client.list_tools()
    result = await client.call_tool("read_doc_contents", {"doc_id": "report.pdf"})
    # Cleanup is automatic
```

The client class hides the complexity and provides a clean interface.

---

## Putting It All Together

Now that our client can list tools and call them, we have a complete system:

### Complete Application Flow

```
User: "Read report.pdf and tell me what it says"
    ↓
App: Uses MCPClient to get tools from server
    ↓
Claude: Sees tools and decides to use read_doc_contents
    ↓
App: Uses MCPClient to execute the tool
    ↓
Claude: Receives result and formulates response
    ↓
User: "The report details a 20m condenser tower..."
```

### Example: The Complete Conversation

```python
async with MCPClient("uv", ["run", "mcp_server.py"]) as client:
    # Get tools
    tools = await client.list_tools()
    
    # Send to Claude with user question
    messages = [
        {"role": "user", "content": "What's in report.pdf?"}
    ]
    
    response = claude.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=[{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in tools],
        messages=messages
    )
    
    # Claude decides to use read_doc_contents
    tool_use = response.content[0]  # {"name": "read_doc_contents", "input": {"doc_id": "report.pdf"}}
    
    # Execute the tool
    result = await client.call_tool(
        tool_use.name,
        tool_use.input
    )
    
    # Send result back to Claude
    # Claude now has the document content and can answer the user
```

---

## Client Design Patterns

### Pattern 1: Single Client Instance
For applications that make many calls:
```python
class MyApp:
    def __init__(self):
        self.client = None
    
    async def startup(self):
        self.client = MCPClient("uv", ["run", "mcp_server.py"])
        await self.client.connect()
    
    async def shutdown(self):
        await self.client.cleanup()
    
    async def handle_user_request(self, query):
        tools = await self.client.list_tools()
        # ... use tools with Claude
```

### Pattern 2: Context Manager (Per-Request)
For applications where clients are short-lived:
```python
async def handle_request(user_query):
    async with MCPClient("uv", ["run", "mcp_server.py"]) as client:
        tools = await client.list_tools()
        # ... process request
        # Client cleanup happens automatically
```

Choose pattern 1 for long-running servers, pattern 2 for serverless/per-request architecture.

---

## Next: Integration with Claude

Once your client is working:

1. ✅ Create MCPClient class
2. ✅ Implement `list_tools()` method
3. ✅ Implement `call_tool()` method
4. ⏭️ Integrate with Claude's tool use system
5. ⏭️ Build your application logic

The client is your bridge to Claude integration — it provides the tools, Claude decides which to use, and the client executes them.

---

# Testing MCP Servers: The MCP Inspector

## The Problem: Testing Without Claude

When building MCP servers, you face a challenge: **How do you test your tools without wiring them into a full Claude application?**

You could:
- ❌ Build a complete client app just to test
- ❌ Manually write test messages in JSON
- ❌ Deploy to production and test there
- ✅ Use the **MCP Inspector** — a built-in testing tool

---

## What is the MCP Inspector?

The **MCP Inspector** is a browser-based tool that comes with the Python MCP SDK. It lets you:

1. **Start your MCP server** in development mode
2. **Open a UI** in your browser
3. **Test tools directly** without Claude
4. **See tool schemas** and responses
5. **Debug communication** in real-time

Think of it as a **debugger for MCP servers**.

---

## Starting the Inspector

### Step 1: Start Your MCP Server

```bash
# From your project directory
mcp dev mcp_server.py
```

That's it! The command:
- Starts your MCP server
- Launches the inspector automatically
- Listens on a local port

### Step 2: Open the Inspector in Your Browser

The output will show something like:
```
✓ MCP Server started
✓ Inspector listening on http://localhost:6277
```

Open your browser to:
```
http://localhost:6277
```

You'll see a browser-based interface for testing your server.

---

## The Inspector Interface

### What You'll See

```
┌─────────────────────────────────────────┐
│         MCP Inspector Interface         │
├─────────────────────────────────────────┤
│                                         │
│  Available Tools:                       │
│  ├─ read_doc_contents                   │
│  │  Description: Read document content  │
│  │  Parameters: doc_id (string)         │
│  │                                      │
│  └─ edit_document                       │
│     Description: Edit document          │
│     Parameters: doc_id, old_str, ...    │
│                                         │
│  Test Tool:                             │
│  ├─ Select tool dropdown                │
│  ├─ Enter parameters                    │
│  ├─ Click "Execute"                     │
│  └─ See results in real-time            │
│                                         │
└─────────────────────────────────────────┘
```

### Key Components

| Component | Purpose |
|-----------|---------|
| **Tools List** | Shows all tools your server provides |
| **Tool Details** | Schema, parameters, description |
| **Test Panel** | Input parameters and execute tools |
| **Results** | See tool output and errors |
| **Logs** | View communication details |

---

## Testing Document Operations

### Example: Test read_doc_contents

1. **Open the inspector** at http://localhost:6277
2. **Select tool:** "read_doc_contents"
3. **Enter parameters:**
   ```
   doc_id: "deposition.md"
   ```
4. **Click "Execute"**
5. **See result:**
   ```
   "This deposition covers the testimony of Angela Smith, P.E."
   ```

### Example: Test edit_document

1. **Select tool:** "edit_document"
2. **Enter parameters:**
   ```
   doc_id: "report.pdf"
   old_str: "20m condenser tower"
   new_str: "25m condenser tower"
   ```
3. **Click "Execute"**
4. **See result:**
   ```
   "Document updated successfully"
   ```

### Example: Verify the Edit

1. **Select tool:** "read_doc_contents" again
2. **Enter parameters:**
   ```
   doc_id: "report.pdf"
   ```
3. **Click "Execute"**
4. **Confirm:** The document now contains "25m" instead of "20m"

---

## Development Workflow with Inspector

### Typical Development Loop

```
1. Write tool code in mcp_server.py
   ↓
2. Run: mcp dev mcp_server.py
   ↓
3. Open inspector at http://localhost:6277
   ↓
4. Test tool with different inputs
   ↓
5. See errors/results in real-time
   ↓
6. Fix issues in code
   ↓
7. Inspector auto-reloads server
   ↓
8. Repeat until tool works correctly
```

### Key Advantage

**You don't need to restart the server manually.** The inspector watches your code and reloads automatically when you make changes.

---

## Why Inspector is Essential

### Before Testing with Claude

- ✅ Verify tools work independently
- ✅ Debug parameter validation
- ✅ Check error handling
- ✅ Confirm schemas are correct
- ✅ Test edge cases quickly

### Then Test with Claude

Once tools are proven in the inspector, wire them into Claude with confidence that they work.

---

## Common Inspector Workflows

### Workflow 1: Schema Validation

```
Problem: Is my tool schema correct?
Solution: 
  1. Open inspector
  2. Check if parameters appear correctly
  3. Verify required vs optional fields
  4. Confirm descriptions are clear
```

### Workflow 2: Error Handling

```
Problem: Do errors show up properly?
Solution:
  1. Intentionally call tool with bad params
     Example: doc_id = "nonexistent.txt"
  2. See error message in inspector
  3. Verify error is helpful to Claude
```

### Workflow 3: Data Validation

```
Problem: Does find-and-replace work correctly?
Solution:
  1. Test edit_document with exact string
  2. Test with wrong/partial string
  3. Verify behavior matches expectations
  4. Check edge cases (whitespace, case sensitivity)
```

### Workflow 4: Integration Ready

```
Problem: Is my server ready for Claude?
Solution:
  1. Test all tools in inspector
  2. Verify all parameters work
  3. Check error messages are clear
  4. Confirm responses are formatted correctly
  5. Deploy server and connect Claude
```

---

## Tips for Using Inspector

### Tip 1: Test Invalid Inputs

Always test with invalid data:
```
doc_id: "docs-that-dont-exist.txt"
old_str: "text that doesn't appear"
```

This verifies your error handling works.

### Tip 2: Check Parameter Descriptions

When you see the parameter list in the inspector, verify:
- ✅ Descriptions are clear
- ✅ Types are correct (string vs integer)
- ✅ Required fields are marked

This helps Claude understand how to use your tools.

### Tip 3: Test Sequences

Simulate realistic workflows:
```
1. First, read_doc_contents (get document)
2. Then, edit_document (modify it)
3. Finally, read_doc_contents again (verify change)
```

This confirms tools work in sequence.

### Tip 4: Watch the Logs

The inspector shows detailed logs of:
- Tool requests
- Parameters received
- Execution time
- Responses sent

This helps debug communication issues.

---

## Inspector vs Full Integration Testing

| Scenario | Use Inspector | Use Claude |
|----------|---|---|
| **Testing individual tools** | ✅ Yes | ❌ No |
| **Verifying schemas** | ✅ Yes | ❌ No |
| **Testing error handling** | ✅ Yes | ✅ Optional |
| **Testing tool selection** | ❌ No | ✅ Yes |
| **Testing multi-turn conversations** | ❌ No | ✅ Yes |
| **Quick iteration** | ✅ Yes | ❌ No |

---

## Summary: Inspector Benefits

The MCP Inspector eliminates friction from development:

✅ **No client code needed** — Test server in isolation  
✅ **Instant feedback** — See results immediately  
✅ **Auto-reload** — Changes to server reflect instantly  
✅ **Visual interface** — Test without writing JSON  
✅ **Error clarity** — See exactly what's broken  
✅ **Quick iteration** — Fix and test in seconds  

Before wiring your MCP server into Claude, use the inspector to validate that your tools work correctly. This ensures a smooth integration.
