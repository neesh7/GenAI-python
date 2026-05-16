# Anthropic Apps: Claude Code & Computer Use

## Overview

This module explores two powerful Anthropic applications: **Claude Code** and **Computer Use**. Both are practical examples of AI agents in action, demonstrating key principles you'll use when building your own agents.

---

## Our Learning Path

1. **Claude Code** — Terminal-based coding assistant
2. **Computer Use** — Desktop application interaction tools
3. **Agent Principles** — What makes these successful
4. **Your Agent** — Apply these lessons to your own

---

## Claude Code

### What It Is

A terminal-based agentic coding assistant that integrates Claude directly into your development workflow.

### Capabilities

- ✅ Edit and fix code files
- ✅ Answer programming questions
- ✅ Assist with debugging and refactoring
- ✅ Guide development workflows
- ✅ Understand project context

### Key Features

| Feature | Benefit |
|---------|---------|
| File editing | Modify code directly without manual edits |
| Context awareness | Understands your project structure |
| Multi-step tasks | Handles complex refactoring |
| Interactive loop | Ask follow-up questions naturally |
| Error recovery | Suggests fixes for compilation/runtime errors |

### Built-in Tools

Claude Code provides a comprehensive toolkit for development:

| Tool | Purpose |
|------|---------|
| **File Operations** | Search, read, and edit files in your project |
| **Terminal Access** | Run commands directly from the conversation |
| **Web Access** | Search documentation, fetch code examples |
| **Project Search** | Find files and symbols across your codebase |
| **Error Analysis** | Understand compilation and runtime errors |

### MCP Server Integration

The most powerful feature: **extend Claude Code with custom tools**

```
Base Claude Code
    ↓
+ Connect MCP Servers
    ↓
+ Database tools
+ API clients
+ Custom services
    ↓
Specialized agent for your workflow
```

**Examples of MCP Extensions:**
- Database query tools (PostgreSQL, MongoDB, etc.)
- API client libraries
- Cloud service integration (AWS, GCP, Azure)
- Version control systems
- CI/CD pipeline tools
- Custom company tools and services

This makes Claude Code adaptable to any development stack.

### Platform Support

Works across all major platforms:
- ✅ **MacOS** — Native terminal support
- ✅ **Windows WSL** — Windows Subsystem for Linux
- ✅ **Linux** — Direct terminal access

### How It Works

```
Your request
    ↓
Claude Code uses available tools:
  • Reads files
  • Runs commands
  • Searches web
  • Calls MCP services
    ↓
Claude analyzes and generates code
    ↓
Files updated, commands executed
    ↓
You verify and iterate
```

### Workflows & Project Management

Claude Code isn't just a tool for writing code—it's designed to work alongside you throughout every phase of a software project.

#### The /init Command & CLAUDE.md

Start every new project with `/init`:

```bash
claude code /init
```

This creates a `CLAUDE.md` file that serves as Claude Code's persistent knowledge base:
- **What it stores**: Project goals, architecture decisions, file conventions, testing guidelines
- **How it helps**: Claude Code reads CLAUDE.md first, so it understands your project's context and constraints
- **Persistence**: Stays in your repo and travels with your code

**Example CLAUDE.md:**
```markdown
# Project Context

## Architecture
- MVC pattern with separation of concerns
- Database layer isolated in `/models`
- API routes in `/routes`

## Testing
- All new features require unit tests in `/tests`
- Run `npm test` before committing
- Aim for >80% coverage

## Naming Conventions
- React components: PascalCase
- Helper functions: camelCase
- Database queries: snake_case

## Recent Decisions
- Switched to TypeScript for type safety
- Using Tailwind CSS for styling
```

#### Three Common Workflows

**1. Basic Workflow (Context → Implement)**
```
Your request (e.g., "Add a login form")
    ↓
Claude Code reads CLAUDE.md for context
    ↓
Claude Code reads relevant files
    ↓
Claude Code writes/modifies code
    ↓
You verify and iterate
```
Best for: Simple features, bug fixes, small refactors

**2. Planning-First Workflow (Context → Plan → Implement)**
```
Your request (e.g., "Build a payment system")
    ↓
You type /init to think through the design
    ↓
Claude Code proposes architecture
    ↓
You refine the plan together
    ↓
Claude Code implements based on approved plan
    ↓
You test and iterate
```
Best for: Complex features, architectural changes, multi-file implementations

**3. Test-Driven Development Workflow**
```
You write a failing test
    ↓
You ask Claude Code: "Make this test pass"
    ↓
Claude Code writes minimal implementation
    ↓
You review the change
    ↓
Iterate: new test → implementation → review
```
Best for: Critical code paths, ensuring correctness, documentation through tests

#### Practical Example: Document Processing Tool

Let's say you want Claude Code to help build a tool that converts markdown files to HTML. Here's how you'd guide it:

**Initial request:**
```
I want a tool that reads markdown files and converts them to HTML. 
Create a `document_path_to_markdown` function that takes a file path, 
reads the content, and parses markdown to HTML.
```

**What Claude Code does:**
1. Creates the function with proper error handling
2. Adds markdown parsing library integration
3. Returns structured output (HTML + metadata)

**Follow-up for completeness:**
```
Add unit tests for edge cases: empty files, invalid markdown, nested headers
```

Claude Code adds comprehensive tests because it now understands your project's testing conventions from CLAUDE.md.

#### Additional Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/init` | Initialize project with CLAUDE.md context | `claude code /init` |
| `/clear` | Clear conversation history | `claude code /clear` |
| `#filename` | Reference specific file in chat | `@app.py tell me what this does` |
| `/help` | Show available commands | `claude code /help` |
| `@context` | Include full project context | `@context refactor this endpoint` |

### MCP Server Integration

Claude Code has an MCP client built right into it, which means you can connect MCP servers to dramatically expand what Claude can do. This opens up powerful possibilities for customizing your development workflow.

#### How MCP Extends Claude

The Model Context Protocol allows Claude Code to connect to external services and tools through MCP servers. Instead of being limited to Claude's built-in capabilities, you can add custom functionality by connecting servers that provide specific tools, resources, or integrations.

Each MCP server can expose different types of functionality to Claude through three main components:
- **Tools** — for taking actions (e.g., reading files, executing queries)
- **Prompts** — for templates and structured workflows
- **Resources** — for accessing data (e.g., documents, database contents)

#### Setting Up an MCP Server

Adding an MCP server to Claude Code is straightforward using the command line:

```bash
claude mcp add [server-name] [command-to-start-server]
```

**Example:** If you have a document processing server that starts with `uv run main.py`:

```bash
claude mcp add documents uv run main.py
```

Once registered, Claude Code will automatically connect to your server when it starts up.

#### Example: Document Processing

A practical example is creating a tool that lets Claude read PDF and Word documents. By building an MCP server with a `document_path_to_markdown` tool, you can ask Claude to convert document contents to markdown format.

When you ask Claude: *"Convert the tests/fixtures/mcp_docs.docx file to markdown"*, it will automatically use your custom tool to read the document and return the converted content.

#### Popular MCP Integrations

The MCP ecosystem includes servers for many common development tools:

| Server | Purpose |
|--------|---------|
| `sentry-mcp` | Automatically discover and fix bugs logged in Sentry |
| `playwright-mcp` | Browser automation capabilities for testing and troubleshooting |
| `figma-context-mcp` | Exposes Figma designs to Claude |
| `mcp-atlassian` | Access Confluence and Jira |
| `firecrawl-mcp-server` | Web scraping capabilities |
| `slack-mcp` | Post messages or reply to specific threads |

#### Building Your Development Workflow

The real power comes from combining multiple MCP servers that match your specific development process. You might set up:

- **Sentry server** — fetch production error details
- **Jira server** — read ticket requirements
- **Slack server** — notify your team when work is complete
- **Custom servers** — for your internal tools and APIs

This creates a development environment where Claude can seamlessly work with all the tools and services you already use, making it a much more powerful coding assistant tailored to your specific workflow.

---

## Computer Use

### What It Is

A collection of tools enabling Claude to interact with desktop environments, websites, and applications.

### Capabilities

- ✅ Navigate websites and browse internet
- ✅ Interact with desktop applications (click, type, screenshot)
- ✅ Perform visual-based tasks
- ✅ Automate repetitive workflows
- ✅ Extract information from graphical interfaces

### Key Differences from Claude Code

| Aspect | Claude Code | Computer Use |
|--------|------------|--------------|
| **Interface** | Terminal/CLI | GUI applications |
| **Scope** | Code and development | Any desktop task |
| **Input method** | Text commands | Screen interaction (click, type) |
| **Use case** | Programming | Automation, data entry, research |

### How It Works

```
Your request (e.g., "Book a flight")
    ↓
Computer Use sees current screen (screenshot)
    ↓
Claude analyzes visual information
    ↓
Claude decides actions (click, type, scroll)
    ↓
Actions executed on desktop
    ↓
Loop until task complete
```

---

## Why These Matter for Agents

Both applications demonstrate core agent principles:

### 1. Tool Integration
Both use specialized tools to interact with their environment (file I/O for Claude Code, screen interaction for Computer Use).

### 2. Multi-Step Execution
Neither solves tasks in one step. They break problems down, execute actions, observe results, and adjust.

### 3. Environmental Awareness
They maintain context about their environment and adapt actions based on current state.

### 4. Autonomous Problem-Solving
They don't ask you for every small decision—they take initiative and handle failures gracefully.

### 5. Natural Iteration
You can ask follow-up questions and refine results through conversation, not rigid APIs.

---

## Agent Pattern Comparison

| Pattern | Claude Code | Computer Use | Your Agents |
|---------|------------|--------------|------------|
| **Observe** | Read file contents | Take screenshot | Your environment |
| **Think** | Analyze code structure | Identify UI elements | Your problem |
| **Act** | Edit files | Click/type | Your tools |
| **Iterate** | Handle errors | Adapt to new screens | Refine solution |

---

## Key Takeaways

**Claude Code teaches:**
- How agents leverage specialized knowledge (programming)
- File-based interaction patterns
- Error handling and recovery

**Computer Use teaches:**
- How agents see and understand visual information
- Navigation and interaction patterns
- Handling unexpected states

**Together they show:**
- Agents aren't one-shot; they iterate
- Context is critical (file structure, screen state)
- Error recovery is essential
- Multi-modal input (visual + text) is powerful

---

## What's Next

Use these insights to understand:
- How to define tools for your agents
- How to structure observation → decision → action loops
- How to handle failures and recover
- How to design agent-friendly task specifications

Both applications prove that with the right tools and structure, Claude can successfully operate in complex environments autonomously.
