# Claude 101 - Day 01 Study Notes

---

## Topic 01: What is Claude Code / AI Agent / Context Window

### Claude Code
**Definition:** Anthropic's official CLI and agentic IDE that lets Claude autonomously read, edit, and run code in your local environment using tools (Read, Edit, Bash, etc.).

Claude Code operates as an AI agent with direct access to your filesystem and terminal, enabling it to:
- Read and understand existing code
- Edit files intelligently
- Execute bash commands
- Manage git workflows
- All while reasoning about your project

### AI Agent
**Definition:** A model that runs in a loop—perceives state, chooses tools/actions, executes them, observes results, and iterates until a goal is reached.

The loop:
1. **Perceive** — Claude reads your prompt, file contents, or tool outputs
2. **Decide** — Chooses the best next action (Read a file, Edit code, Run tests, etc.)
3. **Act** — Executes the chosen tool
4. **Observe** — Reads the result
5. **Loop** — Repeats until the goal is achieved

### Context Window
**Definition:** The total token capacity Claude can "see" in one turn. Everything outside this window is invisible to the model.

Claude Sonnet 4.6 has a 200K token context window. As your conversation grows, available context shrinks. When capacity nears exhaustion, you can use `/compact` to summarize history and free tokens.

---

## Topic 02: How Claude Code Works / Agentic Loop

Claude Code follows this flow:

1. **You give a prompt** — e.g., "Fix the login bug"
2. **Claude reads context** — existing code, error messages, git history
3. **Claude selects a tool** — e.g., "Read src/auth.py"
4. **Tool executes and returns output**
5. **Claude observes the result** — decides the next action (Edit the file? Run tests?)
6. **Repeat** — until the bug is fixed

### Interrupting and Steering
During a run, you can:
- **Interrupt** — Press `Ctrl+C` to stop Claude mid-task
- **Steer** — Add a new message mid-run to change direction: "Actually, check the database schema first"
- **Add context** — Paste error logs, attach files, or link documentation to refocus Claude's reasoning

### Context Window and Compaction
When your conversation grows, the context window fills up. Claude can **compact** prior messages—summarizing key facts while discarding details—to free tokens. Use `/compact` to manually trigger this, or `/context` to see current usage.

---

## Topic 03: Claude Modes

Claude Code supports multiple modes, toggled with keyboard shortcuts:

| Mode | Description | How to Toggle |
|---|---|---|
| **Interactive (default)** | Normal session; Claude pauses for user input after each turn | Default mode |
| **Headless / Non-interactive** | No pauses; Claude runs end-to-end without waiting for you | `--print` flag at startup |
| **Plan Mode** | Claude designs a plan and waits for approval before coding | `Shift+Tab` once |
| **Auto-accept (YOLO)** | Claude auto-approves its own plans and runs autonomously | `Shift+Tab` twice |
| **Fast Mode** | Uses Claude Opus 4.6 with optimized speed for faster iteration | `/fast` command |
| **Worktree Mode** | Isolates work in a git worktree; does not modify main branch | `--worktree` flag |

**Quick reminder:** `Shift+Tab` cycles through: Interactive → Plan → Auto-accept → back to Interactive.

---

## Topic 04: Explore → Plan → Code → Commit Workflow

The canonical Claude Code workflow for any task:

### 1. Explore
- Read existing code and understand the codebase structure
- Look for similar patterns or functions you can reuse
- Understand the problem deeply before changing anything

### 2. Plan
- Use `/plan` or enter **Plan Mode** (`Shift+Tab`) to design your approach
- Present the plan to the user for feedback and alignment
- Refine based on user input

### 3. Code
- Implement the solution using tools (Read, Edit, Write, Bash)
- Run tests or validation as you go
- Iterate if issues arise

### 4. Commit
- Use `git commit` with a clear message
- Claude can author commit messages if needed
- Push to remote if applicable

### Pro Tip
If Claude keeps hitting the same error across multiple turns, document the root cause in **CLAUDE.md** at the project root. This makes the context persist across future sessions and helps Claude avoid repeating mistakes.

---

## Topic 05: Context Management

As your conversation grows, managing context is critical. Three key commands:

| Command | What it does |
|---|---|
| `/compact` | Summarizes conversation history to free context tokens while keeping essential facts |
| `/clear` | Wipes the entire conversation—fresh start, no context carried forward |
| `/context` | Displays current token usage (used / total) of the context window |

### Best Practice
If a context pattern or constraint needs to survive a `/clear`, write it to **CLAUDE.md**. For example:
- Coding standards for the project
- Forbidden commands (no `rm -rf`, no force-push)
- Architecture decisions
- Known workarounds for recurring bugs

Anything in CLAUDE.md is automatically loaded at session start.

---

## Topic 06: CLAUDE.md File

### What It Is
A markdown file that Claude reads automatically at the start of every session—acts as persistent project memory and enforces conventions.

### What to Put In It
- **Coding conventions** — Naming, structure, patterns specific to this repo
- **Forbidden commands** — e.g., "Never run `git push --force` without explicit user approval"
- **Architecture notes** — Key design decisions, file layout, data flow
- **Recurring constraints** — Budget limits, performance requirements, compliance rules
- **Known workarounds** — Bugs that Claude should avoid hitting repeatedly

### Creating CLAUDE.md
Use the `/init` command:
```
/init
```
This scans your codebase and generates a starter CLAUDE.md with auto-detected structure and conventions. You can then edit it to add project-specific rules.

### Location
- **Project-level**: `./CLAUDE.md` (at the repo root)
- **Global-level**: `~/.claude/CLAUDE.md` (applies to all your projects)

---

## Topic 07: Subagents

### What They Are
Child Claude instances spawned by the main Claude to parallelize independent tasks. For example:
- Main Claude designs the architecture
- Subagent A explores existing code patterns
- Subagent B writes unit tests
- Subagent C documents the API

All three work in parallel, then report back.

### Why Use Them
- **Protect context window**: Each subagent has its own context; the main session doesn't bloat
- **Parallelization**: Independent tasks run simultaneously instead of sequentially
- **Isolation**: Subagents don't interfere with each other's work
- **Summaries**: Each subagent returns a brief summary, not raw output

### Custom Subagents
Define your own subagents in `.claude/agents/<name>.md` with YAML frontmatter:

```markdown
---
name: code-explorer
description: Fast read-only search agent for locating code
tools: [Glob, Grep, Read, WebSearch]
model: claude-opus-4-7
---

Your specialized system prompt here...
```

---

## Topic 08: Skills / skills.md

### What Skills Are
Reusable prompt templates (slash commands) stored as markdown files with YAML frontmatter. When you invoke a skill, Claude runs the prompt with your current context.

Examples: `/simplify`, `/review`, `/security-review`, `/init`

### Location
Skills can be stored at:
- **Project-level**: `.claude/skills/<skill-name>/skill.md`
- **Global-level**: `~/.claude/skills/<skill-name>/skill.md`

### File Format
```markdown
---
name: pr-summary
description: Generate a concise PR summary from git diff
---

Prompt content here...
```

### Key Distinction: Skills vs CLAUDE.md

| Aspect | Skills | CLAUDE.md |
|---|---|---|
| **Loading** | On-demand (only when you invoke the skill) | Always loaded at session start |
| **Context cost** | Zero cost unless invoked | Consumes context every turn |
| **Use case** | Reusable workflows, utilities | Persistent rules and conventions |

**Best practice**: Use skills for optional workflows; use CLAUDE.md for mandatory constraints.

---

## Topic 09: MCP (Model Context Protocol)

### What It Is
An open standard (not specific software) that defines how AI models receive context from external tools and data sources.

**Key insight**: It's a protocol—a set of rules for communication—not a product. Any LLM can speak MCP to any compatible server.

### The Four Primitives
MCP allows servers to expose four types of capabilities to the model:

| Primitive | What it provides | Example |
|---|---|---|
| **Tools** | Callable functions the model can invoke | `search_github()`, `query_database()` |
| **Resources** | Attached files, documentation, blobs of data | Project README, schema files, logs |
| **Sampling** | Ability for the server to query the LLM back | Server asks Claude for advice; Claude responds |
| **Prompts** | Template prompts the server suggests to the client | "Write a unit test for this function" |

### Transport Types
- **`stdio`** — Local process communication; low latency, fast, best for local tools
- **`SSE`** — HTTP server with Server-Sent Events; remote/cloud-based, higher latency

### Adding an MCP Server
```bash
claude mcp add --transport stdio <server-name> <command>
```

Example:
```bash
claude mcp add --transport stdio github gh api
```

### Context Cost
Every tool call and resource fetch consumes context tokens. Prefer narrowly-scoped tools over broad ones. A tool that returns 10 results is cheaper than one that returns 1000 and forces Claude to filter.

---

## Topic 10: Hooks

### What They Are
Shell commands that Claude Code executes automatically at lifecycle events—configured in `settings.json`, not controlled by the model's reasoning.

**Key distinction**: Hooks are **deterministic** (always fire, bypass Claude's reasoning). Prompts are **probabilistic** (Claude may choose to ignore them). Use hooks for hard enforcement.

### Configuration
Hooks are defined in `.claude/settings.json`:
```json
{
  "hooks": {
    "UserPromptSubmit": ["npm run lint"],
    "PostToolUse": ["echo 'Tool executed'"]
  }
}
```

### The Five Hook Types

| Hook | Fires when | Use case |
|---|---|---|
| **UserPromptSubmit** | User sends a message to Claude | Validate input, enforce checks before Claude even sees the message |
| **PreToolUse** | Before Claude calls any tool | Logging, permission checks, dry-run mode |
| **PostToolUse** | After a tool returns its result | Process output, validation, metrics |
| **Notification** | Claude sends a notification event | Send alerts to Slack, log to monitoring system |
| **Stop** | Claude finishes its turn | Cleanup, summary reports, resource deallocation |

### Example: Enforce No Force-Push
```json
{
  "hooks": {
    "PreToolUse": ["bash -c \"if [[ $CLAUDE_TOOL == 'Bash' && $CLAUDE_COMMAND == *'--force'* ]]; then echo 'Force-push blocked'; exit 1; fi\""]
  }
}
```

---

## Summary
These 10 topics form the foundation of Claude 101:
1. **Claude Code, AI Agents, Context Windows** — What you're working with
2. **Agentic Loop** — How Claude thinks and acts
3. **Modes** — Different ways to run Claude
4. **Workflow** — Best practices (Explore → Plan → Code → Commit)
5. **Context Management** — `/compact`, `/clear`, `/context`
6. **CLAUDE.md** — Project memory and rules
7. **Subagents** — Parallel execution and isolation
8. **Skills** — Reusable workflows
9. **MCP** — Connecting external tools and data sources
10. **Hooks** — Deterministic automation and enforcement

Master these, and you're ready for the deeper Claude architecture topics!
