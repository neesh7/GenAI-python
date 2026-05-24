# Domain 3: Claude Code Configuration & Workflows (20%)

Configure Claude Code for development workflows. Covers CLAUDE.md hierarchy, custom commands and skills, plan mode, iterative refinement, CI/CD integration, and batch processing.

---

## d3.1 — CLAUDE.md Hierarchy & Configuration

### Core Concepts

Claude Code uses a **hierarchical configuration system** with three layers that merge together. Understanding precedence and purpose of each layer is essential.

**Key Understanding:**
- **User-level** (`~/.claude/CLAUDE.md`) — Personal preferences, not shared (editor prefs, terminal settings)
- **Project-level** (`.claude/CLAUDE.md`) — Team standards, shared via git (language, framework, coding standards)
- **Directory-level** (`src/api/CLAUDE.md`) — Scoped to that directory and below (module-specific rules)
- **Precedence**: Directory-level > Project-level > User-level (more specific overrides more general)
- **Modular configuration** — Split rules into topic-specific files in `.claude/rules/` instead of one massive file
- **@import syntax** — Include external markdown files for organized, maintainable configuration

### Configuration Layers

| Level | Location | Shared? | Purpose | Example |
|---|---|---|---|---|
| **User** | ~/.claude/CLAUDE.md | No | Personal preferences | vim keybindings, dark theme |
| **Project** | .claude/CLAUDE.md | Yes (via git) | Team standards | TypeScript strict mode, ESLint config |
| **Directory** | src/api/CLAUDE.md | Yes (scoped) | Module-specific rules | API validation rules, endpoint conventions |

### Code Pattern

```markdown
~/.claude/
  CLAUDE.md                    # USER LEVEL (personal, not shared)
    "Use vim keybindings"
    "Prefer dark theme output"

project/
  .claude/
    CLAUDE.md                  # PROJECT LEVEL (shared via git)
      "Use TypeScript with strict mode"
      "Follow ESLint airbnb config"
      "@import ./rules/api-design.md"
    rules/
      typescript.md            # Auto-loaded rule file
      testing.md               # Auto-loaded rule file
      api-design.md            # Imported by CLAUDE.md
    
  src/
    api/
      CLAUDE.md                # DIRECTORY LEVEL (scoped rules)
        "All endpoints must validate auth tokens"
        "Use Zod schemas for request validation"
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **One massive CLAUDE.md (800+ lines)** | Hard to maintain, find rules, or delegate ownership |
| **Personal preferences in project config** | vim keybindings shouldn't be team standards |
| **Not understanding precedence** | Directory rules don't override project rules as expected |
| **Mixing concerns (testing, API, UI rules in one file)** | Makes rules harder to find and update |

### Exam Tip 🎯
**Personal preferences go in user-level config. Team standards go in project-level. Module-specific rules go in directory-level.** If an answer puts personal preferences in project config, it's wrong.

---

## d3.2 — Custom Commands & Skills

### Core Concepts

Claude Code supports two extension mechanisms: **custom commands** and **skills**. Understanding when to use each is critical.

**Key Understanding:**
- **Commands** (`.claude/commands/`) — Simple slash commands for quick, one-step actions
- **Skills** (`.claude/skills/`) — Complex, multi-step reusable behaviors with context isolation
- **Commands run in main context** — Same session, no isolation
- **Skills can fork context** — Isolated execution without polluting main session
- **SKILL.md frontmatter** — Controls context, tool restrictions, and argument hints
- **allowed-tools restriction** — Limit which tools a skill can use for security/clarity

### When to Use Each

| Scenario | Use Command | Use Skill |
|---|---|---|
| "Run lint and show me errors" | ✅ Simple, no isolation | ❌ Overkill |
| "Refactor this module to use DI" | ❌ Too complex, pollutes context | ✅ Needs isolation |
| "Quick fix: add log statement" | ✅ Simple | ❌ Unnecessary |
| "Audit codebase for security issues" | ❌ Complex, needs isolation | ✅ Perfect fit |

### SKILL.md Frontmatter Fields

```yaml
---
context: fork                    # Run in isolated context
allowed-tools:                   # Restrict tool access
  - Read
  - Edit
  - Grep
argument-hint: "file or directory to refactor"
---
```

### Code Pattern

```markdown
# .claude/commands/lint.md (SIMPLE COMMAND)
Check for linting errors and report them.
Use: /lint

---

# .claude/skills/refactor/SKILL.md (COMPLEX SKILL)
---
context: fork
allowed-tools:
  - Read
  - Edit
  - Grep
argument-hint: "file or directory to refactor"
---

# Refactoring Skill
When asked to refactor code:
1. **Analyze** the current code structure using Read and Grep
2. **Identify** patterns that violate SOLID principles
3. **Plan** the refactoring approach before making changes
4. **Apply** changes incrementally using Edit (never Write)
5. **Verify** each change maintains existing behavior

## Rules
- Never delete existing tests
- Preserve all public API signatures
- Add JSDoc comments to refactored functions
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Using commands for complex exploration** | Pollutes main context with noise; no tool restrictions |
| **Using skills for simple one-step tasks** | Unnecessary context forking overhead |
| **Not restricting allowed-tools in skills** | Leaves overly broad, risky tool access |
| **Forgetting context: fork for complex work** | Pollution of main session context |

### Exam Tip 🎯
**If the task requires context isolation or tool restriction, the answer is a skill (not a command).** Look for `context: fork` and `allowed-tools` in the correct answer.

---

## d3.3 — Plan Mode & Iterative Refinement

### Core Concepts

**Plan mode** tells Claude to think and outline an approach before executing. Critical for complex tasks, wasteful for simple ones.

**Key Understanding:**
- **Plan mode** — Think before acting; useful for complex multi-step tasks with architectural implications
- **Direct execution** — Appropriate for well-defined, simple tasks with obvious solutions
- **Iterative refinement** — Concrete examples, TDD iteration, and interview patterns improve output quality
- **TDD iteration** — Write tests first → implement → test → refine until green
- **Concrete examples** — "Here's what I want: [specific example]" guides formatting and style
- **Interview pattern** — "Ask me 3 questions before you start" clarifies ambiguous requirements

### When to Use Plan Mode ✅

- Multi-file architectural changes
- Tasks affecting many interconnected components
- Situations where mistakes are expensive to undo
- New feature implementation requiring design decisions
- Refactoring with potential ripple effects

### When to Use Direct Execution ✅

- Simple, well-defined tasks (fix typo, add log statement)
- Single-file changes with clear scope
- Tasks where the correct approach is obvious

### TDD Iteration Cycle

The TDD iteration gives Claude a concrete, verifiable goal at each step:

1. **Write failing test** — Defines expected behavior
2. **Implement** — Make the test pass
3. **Run tests** — Verify correctness
4. **Refine** — Improve code quality while keeping tests green
5. **Repeat** — Next requirement

### Code Pattern

```markdown
# TDD ITERATION WITH CLAUDE CODE

## Step 1: Write the test first (defines the goal)
You: "Write a test for getUserById that:
      - Returns user with id, name, email
      - Throws NotFoundError if user doesn't exist
      - Validates that id is a positive integer"

## Step 2: Run the test (should fail)
You: "Run the test"
Claude: "Test fails: getUserById is not defined"

## Step 3: Implement to pass the test
You: "Implement getUserById to pass all tests"
Claude: [implements the function]

## Step 4: Run tests again (should pass)
You: "Run the tests"
Claude: "All 3 tests pass ✅"

## Step 5: Refine the implementation
You: "Add input sanitization and connection pooling,
      keeping all tests green"
Claude: [refines with constraints]
```

### Iterative Refinement Patterns

| Pattern | Use Case | Example |
|---|---|---|
| **Concrete Examples** | Formatting, styling | "Here's the output format I want: [example]" |
| **TDD Iteration** | Correctness, quality | Write test → implement → refine loop |
| **Interview Pattern** | Ambiguous requirements | "Ask me 3 questions before you start" |

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Using plan mode for simple fixes** | Unnecessary overhead; slows down simple tasks |
| **Skipping planning for complex tasks** | Expensive mistakes, rework, poor architecture |
| **"Just implement this feature" without refinement loop** | Output quality degrades; no verification |
| **No concrete examples for style/format tasks** | Claude guesses at your intent; produces wrong style |

### Exam Tip 🎯
**For complex multi-file tasks use plan mode. For simple fixes use direct execution. TDD iteration (write test, implement, verify) is the preferred refinement pattern.**

---

## d3.4 — CI/CD Integration & Batch Processing

### Core Concepts

Claude Code integrates into CI/CD pipelines using the **-p flag** for non-interactive execution and **structured output flags** for automated processing. **Batch Processing API** offers 50% cost savings.

**Key Understanding:**
- **-p flag** — Non-interactive mode (required for CI/CD pipelines)
- **--output-format json** — Structured JSON output for automated parsing
- **--json-schema** — Enforce specific output shape for validation
- **Session isolation** — Separate generator and reviewer contexts (no confirmation bias)
- **Message Batches API** — 50% cost savings with 24-hour processing window
- **custom_id** — Track individual requests in batch processing
- **Never self-review in same session** — Reviewer retains generator's reasoning (confirmation bias)

### When to Use Synchronous vs Batch

| Approach | Processing | Cost | Best For |
|---|---|---|---|
| **Synchronous (-p flag)** | Immediate | Standard | Blocking PR reviews, real-time feedback |
| **Batch API** | Within 24 hours | 50% cheaper | Nightly audits, weekly reviews, non-urgent analysis |

### Key CI/CD Flags

```bash
-p                          # Non-interactive mode (required)
--output-format json        # Structured JSON output
--json-schema '{...}'       # Enforce output shape
```

### Code Pattern

```yaml
# ci-review.yml — CI/CD Code Review Pipeline
name: Claude Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Use -p flag for non-interactive mode
      # Use a SEPARATE session from code generation
      - name: Run Claude Code Review
        run: |
          claude -p "Review this PR diff for:
            1. Functions exceeding 50 lines
            2. Missing error handling on async ops
            3. Hardcoded credentials or API keys
            4. Missing unit tests for new functions
          Provide results as structured JSON." \
          --output-format json \
          --json-schema '{
            "type": "object",
            "properties": {
              "issues": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "file": {"type": "string"},
                    "severity": {"type": "string"},
                    "description": {"type": "string"}
                  }
                }
              }
            }
          }'
```

### Session Isolation for Code Review

**Critical Rule**: The generator session (that wrote the code) must be completely separate from the reviewer session.

| Pattern | Confirmation Bias? | Why |
|---|---|---|
| **Same session self-review** | ❌ YES | Reviewer retains generator's reasoning |
| **Separate sessions** | ✅ NO | Reviewer has fresh perspective, no context |

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Using interactive mode in CI/CD** | Blocks the pipeline; requires human input |
| **Same-session self-review** | Confirmation bias; reviewer sees through generator's eyes |
| **Not isolating generator and reviewer sessions** | Reviewer bias leads to missed issues |
| **Using synchronous for all reviews** | Wastes money; use Batch API for non-urgent work |
| **Not using --output-format json** | Hard to parse results; breaks automation |

### Exam Tip 🎯
**Three must-know CI/CD facts:**
1. **Always use -p for non-interactive mode**
2. **Never self-review in the same session** (confirmation bias)
3. **Use Batch API for non-urgent reviews (50% savings)**

---

## Key Exam Tips for Domain 3

1. **Know the CLAUDE.md hierarchy** — User > Project > Directory (more specific wins)
2. **Commands vs Skills** — Commands for simple actions, skills for complex work with isolation
3. **Plan mode for complex tasks** — Multi-file changes, architectural decisions
4. **-p flag is mandatory for CI/CD** — Non-interactive mode is required
5. **Separate sessions for review** — Avoid confirmation bias; use different contexts
6. **Batch API for cost savings** — 50% cheaper for non-urgent work (within 24 hours)

---

## Related Exam Scenarios

- **Scenario 2**: Code Generation with Claude Code — Tests CLAUDE.md configuration, plan mode, slash commands, and iterative refinement
- **Scenario 4**: Developer Productivity with Claude — Tests tool selection, codebase exploration, and code generation workflows
- **Scenario 5**: Claude Code for CI/CD — Tests -p flag usage, structured output, batch API, and multi-pass code review

---

## Summary Table

| Sub-Domain | Focus | Critical Concept | Exam Weight |
|---|---|---|---|
| **d3.1** | CLAUDE.md Hierarchy | User > Project > Directory; modular rules | 25% of Domain 3 |
| **d3.2** | Commands & Skills | Skills for isolation; context: fork | 25% of Domain 3 |
| **d3.3** | Plan Mode & Iteration | Plan for complex; TDD iteration for quality | 20% of Domain 3 |
| **d3.4** | CI/CD & Batch | -p flag, separate sessions, Batch API 50% savings | 30% of Domain 3 |

---

## .claude Folder Structure Reference

The `.claude/` directory (in your repo root) contains the complete Claude Code configuration:

```
.claude/
├── CLAUDE.md                    # Main project configuration (shared via git)
├── settings.json                # Hooks, permissions, env vars (project-level)
├── rules/                       # Topic-specific rule files (auto-loaded)
│   ├── typescript.md
│   ├── testing.md
│   └── api-design.md
├── commands/                    # Custom slash commands (/lint, /review, etc.)
│   ├── lint.md
│   ├── review.md
│   └── deploy.md
└── skills/                      # Complex behaviors with context isolation
    ├── refactor/
    │   └── SKILL.md
    └── audit/
        └── SKILL.md
```

### What Each Component Does

| Component | Type | Purpose | Scope |
|---|---|---|---|
| **CLAUDE.md** | File | Main project configuration; uses @import for modularity | Shared |
| **settings.json** | File | Hooks, tool permissions, environment variables | Project-level |
| **rules/** | Folder | Topic-specific rules (auto-loaded); organized by concern | Shared |
| **commands/** | Folder | Simple slash commands for quick actions | Shared |
| **skills/** | Folder | Complex multi-step behaviors with context: fork | Shared |

### Hooks (in settings.json)

Hooks are **deterministic, code-based enforcement** configured in `settings.json`:

```json
{
  "hooks": {
    "before-submit": "npm run lint",
    "after-file-edit": "npm test",
    "pre-tool-use": "validate-tool-call.sh"
  }
}
```

**Key Distinction**: 
- **Hooks** = Deterministic (100% reliable) — Enforce business rules via code
- **Prompts** = Probabilistic (variable) — Model may ignore; use for preferences

### Configuration Precedence

```
User-level (~/.claude/)
    ↓ (can be overridden by)
Project-level (./.claude/)
    ↓ (can be overridden by)
Directory-level (./src/api/CLAUDE.md)
    
Result: More specific configs win
```

**Remember**: Only `project-level` and `directory-level` configs go in the repo. `User-level` (`~/.claude/`) is personal and never committed.
