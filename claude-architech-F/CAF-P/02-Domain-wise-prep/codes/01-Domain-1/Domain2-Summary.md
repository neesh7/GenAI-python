# Domain 2: Tool Design & MCP Integration (20%)

Design effective tools and integrate with Model Context Protocol (MCP) servers. Covers tool description best practices, structured error responses, tool distribution, MCP configuration, and Claude's built-in tools.

---

## d2.1 — Tool Description Best Practices

### Core Concepts

Tool descriptions are the primary mechanism Claude uses to decide when and how to use a tool. Think of them as **documentation written specifically for the model**.

**Key Understanding:**
- **Tool descriptions act as documentation for the model** — more detail is better
- **Input format specifications** with examples help Claude understand how to call the tool
- **Edge cases and boundary conditions** prevent unexpected tool behavior
- **Clear parameter descriptions** including types, ranges, and constraints
- **When NOT to use** — clarify tool boundaries to prevent misuse

### What Makes a Great Tool Description

1. **Clear purpose** — What the tool does in one sentence
2. **Input specifications** — Exact types, formats, ranges, and constraints
3. **Examples** — Show expected input/output pairs for common cases
4. **Edge cases** — Document what happens with empty inputs, invalid data, boundary values
5. **When NOT to use** — Clarify tool boundaries

### Code Pattern

```json
{
  "name": "lookup_customer",
  "description": "Search for a customer by email, phone number, or account ID. Returns customer profile including name, account status, and order history summary. Input: exactly ONE of email, phone, or account_id. Email must contain @. Phone must be E.164 format (e.g., +15551234567). Account ID must start with ACC-. Returns: customer object or empty array if not found. Note: empty result means customer not found, this is NOT an error.",
  "input_schema": {
    "type": "object",
    "properties": {
      "email": {
        "type": "string",
        "description": "Customer email address (must contain @)"
      },
      "phone": {
        "type": "string",
        "description": "Phone in E.164 format, e.g., +15551234567"
      },
      "account_id": {
        "type": "string",
        "description": "Account ID starting with ACC-, e.g., ACC-12345"
      }
    }
  }
}
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Vague descriptions** like "Searches for stuff" | Claude must guess what it searches, when to use it, what format |
| **Missing input specifications** | Claude doesn't know expected types, ranges, or format constraints |
| **No edge case documentation** | Claude may mishandle empty inputs, invalid data, or boundary values |
| **Missing examples** | Claude doesn't see how to properly call the tool |

### Exam Tip 🎯
When comparing tool descriptions, the correct answer **ALWAYS has the most detailed description with input formats, examples, edge cases, and boundary documentation**. Vague descriptions are always wrong.

---

## d2.2 — Structured Error Responses

### Core Concepts

When a tool fails, the error response must give the agent enough information to decide what to do next: **retry, try an alternative, or escalate**.

**Key Understanding:**
- **isError flag** — explicitly signals tool failure (true/false)
- **errorCategory** — classifies error type ("auth", "not_found", "rate_limit", "timeout", "validation")
- **isRetryable** — tells agent whether retrying might succeed
- **Structured error context** — includes what was attempted and what failed
- **Critical distinction**: Access failure ≠ Empty result

### The Critical Distinction: Access Failure vs Empty Result

This is **one of the most tested concepts** on the exam:

| Scenario | isError | Why |
|---|---|---|
| **Access Failure** | true | "I couldn't check the database" — the search was NOT performed |
| **Empty Result** | false | "I checked the database, found nothing" — the search WAS performed |

**Never silently suppress access failures by returning empty results.** If the database was down, returning `[]` makes the agent think no customers exist — a **catastrophic misunderstanding**.

### Code Pattern

```json
{
  "access_failure_example": {
    "isError": true,
    "errorCategory": "timeout",
    "isRetryable": true,
    "context": {
      "attempted": "Customer lookup by email: user@example.com",
      "service": "customer-database",
      "timeout_ms": 5000,
      "suggestion": "Retry after 2 seconds or try account ID lookup"
    }
  },
  "empty_result_example": {
    "isError": false,
    "customers": [],
    "metadata": {
      "searched_by": "email",
      "query": "user@example.com",
      "results_count": 0
    }
  }
}
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Returning `[]` for a failed connection** | Agent thinks no data exists; actually the search failed |
| **Generic errors like "Operation failed"** | Hides context needed for recovery |
| **Not distinguishing access failures from empty results** | Silent, catastrophic misunderstandings |
| **Omitting isRetryable flag** | Agent doesn't know if retry might help |

### Exam Tip 🎯
If an exam question asks about a tool that fails to connect to an external service, the correct answer **ALWAYS distinguishes the access failure from an empty result**. Returning `[]` for a failed connection is always wrong.

---

## d2.3 — Tool Distribution & Selection

### Core Concepts

The number of tools given to a single agent **directly impacts its ability to select the correct one**. Research shows **4-5 tools per agent is optimal**.

**Key Understanding:**
- **4-5 tools per agent** is optimal; too many tools degrade selection quality
- **Scoped tool access** — each agent only gets tools relevant to its task
- **tool_choice options** — 'auto' (model decides), 'any' (must use a tool), or forced specific tool
- **Tool grouping** — organize related tools and assign to specialized agents
- **18+ tools** creates ambiguity and degrades selection accuracy

### Why Too Many Tools is a Problem

With 18+ tools:
- Claude must evaluate each one against the current task
- Similar tools create ambiguity (search_customers vs find_customer vs lookup_user)
- Selection accuracy degrades as the option space grows
- More tool descriptions consume valuable context window space

### The Solution: Distribute Across Specialized Subagents

Instead of one agent with 18 tools, create a **coordinator with 3-4 subagents**, each having 4-5 focused tools:

| Agent | Tools |
|---|---|
| **Customer Agent** | lookup_customer, update_account, check_status, verify_identity |
| **Order Agent** | find_order, process_refund, update_shipping, track_package |
| **Communication Agent** | send_email, send_sms, create_ticket, escalate_human |
| **Coordinator** | Task (delegate), summarize, format_response |

### Code Pattern

```python
# WRONG: One agent with too many tools
overloaded_agent = Agent(
    tools=[
        lookup_customer, update_account, verify_identity,
        find_order, process_refund, update_shipping,
        track_package, send_email, send_sms,
        create_ticket, escalate, search_kb,
        check_inventory, apply_coupon, schedule_callback,
        log_interaction, generate_report, update_preferences,
    ]  # 18 tools — selection quality degrades!
)

# CORRECT: Coordinator + specialized subagents
coordinator = Agent(
    tools=[Task, summarize_results, format_response],  # 3 tools
)

customer_agent = Agent(
    tools=[lookup_customer, update_account, verify_identity, check_status],
)

order_agent = Agent(
    tools=[find_order, process_refund, update_shipping, track_package],
)

comms_agent = Agent(
    tools=[send_email, send_sms, create_ticket, escalate_human],
)
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Giving an agent 18+ tools** | Selection quality degrades; Claude struggles to pick the right tool |
| **Not using tool_choice to constrain selection** | When the task is clear, force the tool instead of letting Claude guess |
| **Creating ambiguous tool names** | Similar names cause selection errors |

### Exam Tip 🎯
When the exam presents a scenario with many tools, the correct answer **ALWAYS distributes them across specialized subagents with 4-5 tools each**. Never give one agent 18+ tools.

---

## d2.4 — MCP Server Configuration

### Core Concepts

Model Context Protocol (MCP) servers extend Claude's capabilities with custom tools and data sources. Configuration happens at **two levels**.

**Key Understanding:**
- **.mcp.json** — Project-level MCP configuration (shared with team via version control)
- **~/.claude.json** — User-level MCP configuration (personal tools, not shared)
- **Environment variable expansion** — Use `${ENV_VAR}` syntax for secrets management
- **MCP servers provide** — Tools, resources, and prompt templates
- **Never hardcode secrets** in configuration files

### Configuration Files

| File | Level | Shared? | Use Case |
|---|---|---|---|
| **.mcp.json** | Project | Yes (via git) | Team tools, project-specific integrations |
| **~/.claude.json** | User | No | Personal API keys, individual tools |

### Security: Environment Variable Expansion

**Never hardcode secrets in configuration files.** Use `${ENV_VAR}` syntax:
- Secrets stay out of version control
- Each developer uses their own credentials
- CI/CD can inject environment-specific values

### What MCP Servers Can Provide

- **Tools** — Custom functions Claude can call (e.g., Jira integration, database queries)
- **Resources** — Static data or documentation (e.g., API specs, schema docs)
- **Prompts** — Pre-built prompt templates for common tasks

### Code Pattern

```json
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["@company/jira-mcp-server"],
      "env": {
        "JIRA_URL": "${JIRA_URL}",
        "JIRA_TOKEN": "${JIRA_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["@company/pg-mcp-server", "--read-only"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Hardcoding secrets in .mcp.json** | Gets committed to git = leaked secrets |
| **Mixing project and user configs without understanding precedence** | Can cause unexpected tool availability or credential conflicts |
| **Not using environment variable expansion** | Secrets exposed in version control |

### Exam Tip 🎯
If an exam answer hardcodes API keys in `.mcp.json`, it's **always wrong**. The correct approach **always uses `${ENV_VAR}` for secrets management**.

---

## d2.5 — Built-in Tools

### Core Concepts

Claude Code comes with **6 built-in tools**. Knowing when to use each is heavily tested on the exam.

**Key Understanding:**
- **Read** — Read file contents (understanding code, examining data)
- **Write** — Create new files from scratch (new files only!)
- **Edit** — Modify existing files with targeted changes
- **Bash** — Execute shell commands (tests, builds, installs)
- **Grep** — Search for text patterns across files
- **Glob** — Find files matching name patterns

### Critical Distinctions

| Decision | Rule |
|---|---|
| **Write vs Edit** | Use Write for new files only. Use Edit for modifying existing files. Write replaces the entire file. |
| **Bash vs built-in tools** | Never use Bash for operations that have dedicated tools. Don't use `cat file.txt` when Read exists. |
| **Grep vs Glob** | Grep searches **inside files** for content patterns. Glob searches **file names** for path patterns. |

### Code Pattern

```markdown
Task: "Read the configuration file"
  Correct: Read("config.json")
  Wrong:   Bash("cat config.json")

Task: "Create a new test file"
  Correct: Write("tests/new-test.ts", content)
  Wrong:   Bash("echo '...' > tests/new-test.ts")

Task: "Fix a bug in line 42 of server.ts"
  Correct: Edit("server.ts", old_text, new_text)
  Wrong:   Write("server.ts", entire_file_content)

Task: "Find all usages of getUserById"
  Correct: Grep("getUserById", "src/")
  Wrong:   Bash("grep -r 'getUserById' src/")

Task: "Find all TypeScript test files"
  Correct: Glob("**/*.test.ts")
  Wrong:   Bash("find . -name '*.test.ts'")

Task: "Run the test suite"
  Correct: Bash("npm test")
  (No built-in alternative — Bash is correct here)
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Using Write when Edit would be more precise** | Write replaces entire file; Edit is surgical |
| **Using Bash for file operations** | Wastes context; purpose-built tools are available |
| **Confusing Grep (content search) with Glob (file name pattern)** | Wrong tool for the task |

### Exam Tip 🎯
The exam frequently presents scenarios where an agent uses Bash for file operations. The correct answer **ALWAYS uses the purpose-built tool** (Read, Write, Edit, Grep, Glob) instead of Bash equivalents.

---

## Key Exam Tips for Domain 2

1. **Keep tools per agent to 4-5** for optimal selection quality
2. **Structured error responses are critical** — always include isError, errorCategory, isRetryable
3. **Know the difference** between .mcp.json (project) and ~/.claude.json (user)
4. **Built-in tools** — know when to use Grep vs Glob vs Read vs Edit
5. **Never hardcode secrets** in configuration files; use `${ENV_VAR}`
6. **Access failure ≠ Empty result** — always distinguish them in error responses

---

## Related Exam Scenarios

- **Scenario 1**: Customer Support Resolution Agent — Tests Agent SDK usage, MCP tools, and escalation logic
- **Scenario 4**: Developer Productivity with Claude — Tests tool selection, codebase exploration, and code generation workflows

---

## Summary Table

| Sub-Domain | Focus | Critical Concept | Exam Weight |
|---|---|---|---|
| **d2.1** | Tool Descriptions | Detailed descriptions with examples and edge cases | 20% of Domain 2 |
| **d2.2** | Error Responses | isError, errorCategory, isRetryable; access failure ≠ empty result | 25% of Domain 2 |
| **d2.3** | Tool Distribution | 4-5 tools per agent; distribute across subagents | 25% of Domain 2 |
| **d2.4** | MCP Configuration | .mcp.json vs ~/.claude.json; use ${ENV_VAR} for secrets | 20% of Domain 2 |
| **d2.5** | Built-in Tools | Read/Write/Edit/Bash/Grep/Glob; choose the right tool | 10% of Domain 2 |
