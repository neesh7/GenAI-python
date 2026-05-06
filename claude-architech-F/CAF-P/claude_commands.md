# Claude Code Commands Cheatsheet

> Quick reference for frequently used Claude Code CLI commands

---

## Installation & Setup

| Command | Description |
|---|---|
| `irm https://claude.ai/install.ps1 \| iex` | Install Claude Code on Windows (PowerShell) |
| `curl -fsSL https://claude.ai/install.sh \| sh` | Install Claude Code on macOS/Linux |
| `claude --version` | Check installed version |
| `claude doctor` | Diagnose installation issues |
| `claude --help` | Show all available commands |

---

## Authentication

| Command | Description |
|---|---|
| `claude` | Start Claude Code & trigger login |
| `claude auth login` | Login to your Claude account |
| `claude auth logout` | Logout from Claude account |
| `claude auth status` | Check current auth status |

---

## Starting & Sessions

| Command | Description |
|---|---|
| `claude` | Start interactive mode |
| `claude resume` | Resume last session |
| `claude --continue` | Continue most recent conversation |
| `claude --new-session` | Force start a fresh session |

---

## Running Tasks (Headless / Non-interactive)

| Command | Description |
|---|---|
| `claude -p "your prompt here"` | Run a one-shot prompt (headless mode) |
| `claude -p "fix this bug" --output-format json` | Run prompt and get JSON output |
| `echo "explain this" \| claude -p -` | Pipe input into Claude |
| `claude -p "review code" --max-turns 5` | Limit agentic turns |

---

## Context & Memory

| Command | Description |
|---|---|
| `claude compact` | Summarize context to free up space |
| `claude clear` | Clear current session context |
| `claude rewind` | Undo last action |
| `claude rename "session name"` | Rename current session |

---

## Model Selection & Context Window

| Command | Description |
|---|---|
| `claude --model claude-opus-4-7` | Use Opus 4.7 (most powerful) |
| `claude --model claude-sonnet-4-6` | Use Sonnet 4.6 (balanced, default) |
| `claude --model claude-haiku-4-5` | Use Haiku 4.5 (fastest, cheapest) |

### Context Window Info

| Model | Context Window | Notes |
|---|---|---|
| **Opus 4.7** | 200k tokens | Best for complex tasks, larger codebases |
| **Sonnet 4.6** | 200k tokens | Recommended default, best balance of speed/cost |
| **Haiku 4.5** | 200k tokens | Fast & cheap, best for CI/CD and scripts |

**Context Management Commands:**
- `/compact` or `claude compact` — Compress context to free up space
- `/clear` or `claude clear` — Completely clear conversation history
- `claude rewind` — Undo the last action
- **Prompt Caching** — Automatically enabled; repeated prompts reuse cached context (reduces cost)

### Usage & Length Limits

| Limit | Value | Notes |
|---|---|---|
| **Context Window** | 200,000 tokens | Shared between input & output for all models |
| **Max Input Length** | ~195,000 tokens | Leaves ~5k for model output per turn |
| **Max Output (per turn)** | Varies | Typically 4k-8k tokens depending on model & load |
| **Max File Size** | 512 KB | Per file upload/read |
| **Rate Limit** | Model dependent | Check with `claude usage` |
| **Concurrent Requests** | 1 per session | Queue subsequent prompts; no parallel requests |

**When You Hit Limits:**
- **Context Full?** → Use `/compact` to compress or `/clear` to start fresh
- **Token Budget Exceeded?** → Switch to `/fast` mode or `claude-haiku-4-5` for cheaper turns
- **File Too Large?** → Split into smaller files or chunks; use summarization
- **Need More Output?** → Ask Claude to continue in next turn with `/continue` or continue typing

**Tips to Stay Under Limits:**
- Use `claude -p` (headless mode) for disposable one-shot tasks
- Enable `/fast` mode for cost-sensitive operations
- Leverage `/compact` regularly in long sessions
- Use `CLAUDE.md` to persist context instead of keeping it in conversation

---

## MCP (Model Context Protocol)

| Command | Description |
|---|---|
| `claude mcp list` | List all configured MCP servers |
| `claude mcp add <name> -- <command>` | Add a local MCP server |
| `claude mcp add --transport http <name> <url>` | Add a remote HTTP MCP server |
| `claude mcp remove <name>` | Remove an MCP server |

---

## Permissions & Settings

| Command | Description |
|---|---|
| `claude --allowedTools "bash,editor"` | Allow specific tools only |
| `claude --dangerously-skip-permissions` | Skip permission prompts (use carefully!) |
| `claude config list` | View current config settings |
| `claude config set <key> <value>` | Update a config value |

---

## Usage & Cost Tracking

| Command | Description |
|---|---|
| `claude usage` | Show usage stats for current session |
| `claude cost` | Show estimated cost of session |
| `ccusage` | Detailed usage across all sessions |
| `claude stats` | Show session statistics |

---

## Claude Modes

| Mode | How to Activate | Description |
|---|---|---|
| **Interactive** | `claude` (default) | Full REPL chat session with tool use and memory |
| **Headless** | `claude -p "prompt"` | One-shot, non-interactive — for scripts and CI/CD |
| **Plan Mode** | `/plan` or `EnterPlanMode` | Claude plans steps before executing; no tools run until approved |
| **Auto-accept** | `Shift+Tab` (toggle) | Automatically approves tool permission prompts without pausing |
| **Fast Mode** | `/fast` (toggle) | Faster output using Opus 4.6; only available on Opus model |
| **Worktree** | `EnterWorktree` | Isolated git worktree for safe, sandboxed changes |

> **Tip:** Auto-accept (`Shift+Tab`) is great for unattended runs but skips safety prompts — use with care.

---

## Keyboard Shortcuts (Inside Interactive Mode)

| Shortcut | Description |
|---|---|
| `Ctrl+C` | Cancel current input or interrupt running tool |
| `Ctrl+D` | Exit Claude Code (EOF / quit session) |
| `Ctrl+L` | Clear the terminal screen |
| `Ctrl+T` | Open session list / switch sessions |
| `Shift+Tab` | Toggle auto-accept (agentic mode) on/off |
| `Alt+V` | Paste images from clipboard (Windows) |
| `Up Arrow` | Navigate to previous input in history |
| `Down Arrow` | Navigate to next input in history |
| `Ctrl+R` | Reverse search through input history |

---

## Slash Commands (Inside Interactive Mode)

| Command | Description |
|---|---|
| `/help` | Show available slash commands |
| `/clear` | Clear conversation history |
| `/compact` | Compress context window |
| `/status` | Show session status |
| `/model` | Switch model mid-session |
| `/exit` or `/quit` | Exit Claude Code |
| `/stats` | Show token usage and cost stats for the current session |
| `/cost` | Display estimated cost breakdown for the session |

---

## GitHub Actions (CI/CD)

```yaml
# Example: Run Claude Code in GitHub Actions
- name: Claude Code Review
  run: claude -p "review this PR for bugs" --output-format json
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

---

## Useful Environment Variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Set your API key |
| `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` | Enable native PowerShell tool |
| `CLAUDE_CODE_GIT_BASH_PATH` | Custom Git Bash path on Windows |
| `USE_BUILTIN_RIPGREP=0` | Disable built-in ripgrep (Alpine Linux) |

---

## Quick Tips

- Run `claude doctor` first if anything breaks
- Use `claude -p` for scripting and automation pipelines
- Add `CLAUDE.md` to your project root for persistent context
- Use `--model claude-haiku-4-5` for cheaper, faster tasks in CI/CD
- `ALT+V` to paste images on Windows (not `Ctrl+V`)

---

*Generated for CCAF exam prep | Master Shifu approved 🥋*