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
