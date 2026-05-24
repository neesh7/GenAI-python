# Domain 1: Agentic Architecture & Orchestration (25%)

Design and implement agentic systems using Claude's Agent SDK. Covers agentic loops, multi-agent orchestration, hooks, workflows, session management, and task decomposition patterns for production-grade AI applications.

---

## d1.1 — Agentic Loops & Core API

### Core Concepts

The agentic loop is the fundamental execution pattern for Claude-based agents. Unlike request-response interactions, an agentic loop allows Claude to iteratively plan, act, observe, and decide whether to continue or stop.

**Key Understanding:**
- **Agentic loop lifecycle**: The `stop_reason` field controls loop continuation
  - `"tool_use"` → Claude wants to call a tool → **continue the loop**
  - `"end_turn"` → Claude is done → **exit the loop**
  
- **Tool result appending**: After each tool call, results are appended to the conversation for the next iteration
- **Agent SDK control flow**: The SDK handles the loop automatically, but you must understand the mechanics
- **Loop termination rule**: The agent continues as long as `stop_reason` is `'tool_use'`; it terminates on `'end_turn'`

### How the Loop Works

1. Send a message to Claude with available tools
2. Claude responds — either with text (done) or a tool call (needs to act)
3. If Claude called a tool, execute it and append the result to the conversation
4. Send the updated conversation back to Claude
5. Repeat until Claude responds with text only (no more tool calls)

### Code Pattern

```python
import anthropic

client = anthropic.Anthropic()
tools = [{"name": "lookup_customer", "description": "...", "input_schema": {}}]
messages = [{"role": "user", "content": "Find customer John Smith"}]

# The Agentic Loop
while True:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        tools=tools,
        messages=messages
    )
    
    # KEY: Check stop_reason to control the loop
    if response.stop_reason == "end_turn":
        break  # Claude is done
    
    if response.stop_reason == "tool_use":
        tool_block = next(
            b for b in response.content if b.type == "tool_use"
        )
        result = execute_tool(tool_block.name, tool_block.input)
        
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [{"type": "tool_result",
                         "tool_use_id": tool_block.id,
                         "content": result}]
        })
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Parsing natural language output** to decide whether to continue the loop | `stop_reason` is the only reliable signal |
| **Setting arbitrary iteration caps** as the primary stopping mechanism | Caps may terminate prematurely or run too long |
| **Checking assistant text content** to determine loop termination | Text content is probabilistic; `stop_reason` is deterministic |
| Parsing "task complete" or "I'm done" in text | Model can be ambiguous or contradictory |

### Exam Tip 🎯
The exam will present 3-4 options for loop termination. The correct answer is **ALWAYS checking `stop_reason`**. Look for distractors like parsing text content, setting iteration limits, or monitoring token counts.

---

## d1.2 — Multi-Agent Orchestration

### Core Concepts

Multi-agent orchestration uses a **hub-and-spoke architecture** where a central coordinator delegates tasks to specialized subagents. Each subagent operates in its own isolated context.

**Key Understanding:**
- **Hub-and-spoke architecture**: Central coordinator delegates to specialized subagents
- **Context isolation**: Subagents have their own context and don't share state directly
- **Task tool for spawning**: The coordinator's `allowedTools` must include `'Task'` for subagent creation
- **Parallel execution**: Multiple `Task` calls in a single response enable parallel subagent work
- **fork_session**: Creates branched sessions for parallel exploration without context pollution

### Why Hub-and-Spoke Beats Flat Architectures

| Advantage | Why It Matters |
|---|---|
| **Context isolation** | Each subagent gets only context relevant to its task |
| **Focused tool access** | Each subagent has only 4-5 tools relevant to its specialty |
| **Parallel execution** | Multiple subagents can work simultaneously |
| **Clean synthesis** | Coordinator combines results without exploration noise |

### Context Passing Rule

**Critical**: Pass **ONLY the context specific** to each subagent's task. **Never share the full coordinator conversation history** — it wastes tokens and confuses the subagent with irrelevant information.

### Code Pattern

```python
from claude_agent import Agent, Task

coordinator = Agent(
    model="claude-sonnet-4-20250514",
    tools=[
        Task,              # Required for spawning subagents
        summarize_results, # Coordinator-level synthesis
        format_report,     # Final output formatting
    ]
)

# Subagent with scoped tool access (4 tools each)
market_researcher = Agent(
    model="claude-sonnet-4-20250514",
    tools=[web_search, read_doc, extract_data, format_citation],
)

tech_analyst = Agent(
    model="claude-sonnet-4-20250514",
    tools=[read_code, grep_patterns, analyze_deps, format_report],
)

# Coordinator delegates with EXPLICIT context per subtask
coordinator.run("""
Research AI infrastructure market. Delegate:
1. Market research → market_researcher
2. Technology analysis → tech_analyst
Pass each subagent ONLY the context relevant to their task.
""")
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Sharing full coordinator context with subagent** | 90% of the context is irrelevant; wastes tokens and confuses the agent |
| **Assuming subagents inherit coordinator knowledge** | Subagents can only access explicitly passed context |
| **Overly narrow task decomposition** | Gaps in coverage between subagents |

### Exam Tip 🎯
The exam tests context isolation heavily. If an answer shares full coordinator context with subagents, **it's wrong**. Each subagent should receive only context specific to its assigned subtask.

---

## d1.3 — Hooks & Programmatic Enforcement

### Core Concepts

**Hooks provide deterministic, programmatic enforcement of business rules.** They intercept tool calls before or after execution, allowing you to block, modify, or augment behavior without relying on the model's compliance.

**Key Understanding:**
- **Hooks = Deterministic** (100% reliable) → Use for critical business rules, compliance, security
- **Prompts = Probabilistic** (model may ignore) → Use for style preferences, soft guidelines
- **PostToolUse hooks**: Intercept after execution — can modify output, normalize data, trigger side effects
- **PreToolUse hooks**: Intercept before execution — can block, modify params, add validation

### The Critical Distinction

This is what the exam emphasizes:

| Approach | Reliability | Use Case |
|---|---|---|
| **Programmatic Hooks** | Deterministic (100%) | Critical business rules, compliance, security |
| **Prompt Instructions** | Probabilistic (variable) | Style preferences, soft guidelines |

**Example**: A $500 refund limit is a critical business rule. If you put it in a prompt, the model might process a $700 refund anyway. A PostToolUse hook guarantees the block because it runs as code, not as a suggestion.

### Valid Escalation Triggers ✅

- Customer explicitly requests a human
- Policy gap detected (no rule covers the situation)
- Task exceeds agent capabilities
- Business threshold exceeded (e.g., refund > $500)

### Invalid Escalation Triggers ❌

| Invalid Trigger | Why It Fails |
|---|---|
| **Negative sentiment** | Sentiment does not equal task complexity |
| **Self-reported low confidence** | Model confidence is unreliable |

### Code Pattern

```python
from claude_agent import Agent, Hook

# PostToolUse hook: Block refunds above $500
def refund_limit_hook(tool_name, tool_input, tool_output):
    if tool_name == "process_refund":
        amount = tool_input.get("amount", 0)
        if amount > 500:
            return {
                "blocked": True,
                "reason": f"Refund ${amount} exceeds $500 limit",
                "action": "escalate_to_human",
                "context": {
                    "customer_id": tool_input.get("customer_id"),
                    "requested_amount": amount,
                    "agent_limit": 500,
                }
            }
    return tool_output  # Allow all other tool calls

agent = Agent(
    model="claude-sonnet-4-20250514",
    tools=[lookup_customer, check_order, process_refund],
    hooks={"PostToolUse": [refund_limit_hook]},
)
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Using prompt-based enforcement for critical business rules** | Unreliable — the model can and will ignore prompts |
| **Self-reported confidence scores for escalation** | Model confidence is unreliable |
| **Sentiment-based escalation** | Sentiment does not equal complexity |

### Exam Tip 🎯
When the exam asks about enforcing critical business rules (refund limits, data access, compliance), the correct answer is **ALWAYS programmatic hooks**, never prompt instructions.

---

## d1.4 — Session Management & Workflows

### Core Concepts

Session management controls how agent conversations persist, resume, and branch.

**Key Understanding:**
- **--resume flag**: Continue previous sessions with preserved context
- **fork_session**: Branch sessions for exploration without polluting the main context
- **Named sessions**: Organize multi-session workflows with explicit names
- **Stale context detection**: Mitigate outdated data in long-running sessions
- **Task decomposition strategies**: Choose between prompt chaining (static) and dynamic adaptive (flexible)

### Key Session Operations

| Operation | Purpose | Use Case |
|---|---|---|
| **--resume** | Continue a previous session with full context | Picking up where you left off |
| **fork_session** | Create a branch for exploration without polluting main | Parallel exploration paths |
| **--session-name** | Organize multi-session workflows | Organizing complex, multi-step projects |

### Stale Context Risk

In long-running sessions, data retrieved early may become outdated. **Mitigation strategies:**
- Periodically re-fetch critical data
- Use scratchpad files for tracking state changes
- Explicitly note timestamp of last data refresh

### Task Decomposition Strategies

**Prompt Chaining** (predictable, linear):
- Fixed sequence of steps
- Each step's input/output is predictable
- Linear workflow with no branching

**Dynamic Adaptive Decomposition** (unpredictable, complex):
- Agent decides next steps based on intermediate results
- Task has unknown complexity
- Intermediate results may change the approach

**Rule**: Use dynamic adaptive when the task has unknown complexity or intermediate results may change the approach. Use prompt chaining when the workflow is well-defined and predictable.

### Code Pattern

```bash
# Resume a previous session (preserves full context)
claude --resume

# Resume a specific named session
claude --resume --session-name "feature-auth-redesign"

# Fork for exploration (inherits context, diverges)
# Changes in fork do NOT affect the main session
claude fork_session --reason "Exploring alternative API"

# Start a new named session
claude --session-name "sprint-47-backend"
```

### Anti-Pattern: Static Chains for Dynamic Tasks

```python
# ANTI-PATTERN: Static prompt chain for a DYNAMIC task
steps = [
    "Step 1: Read the codebase",
    "Step 2: Find all bugs",
    "Step 3: Fix each bug",
]
# Problem: What if step 2 finds no bugs? Static chains can't adapt
```

### Correct Approach: Dynamic Adaptive

```python
# CORRECT: Dynamic adaptive decomposition
agent.run("""
Analyze the codebase for issues. For each:
1. Assess severity and complexity
2. If simple: fix directly
3. If complex: create a plan first
4. After each fix: run relevant tests
Adapt your approach based on what you find.
""")
```

### Exam Tip 🎯
If the task is unpredictable or has conditional branches, **dynamic adaptive decomposition is correct**. If it's a fixed, linear pipeline, **prompt chaining works**.

---

## Key Exam Tips for Domain 1

1. **Always check `stop_reason` for loop control**, never parse natural language
2. **Programmatic hooks for business rules**, prompts for preferences
3. **Subagents need explicit context** — don't assume they inherit coordinator knowledge
4. **Understand `fork_session` vs `--resume`** and when to use each
5. **Hooks are deterministic; prompts are probabilistic** — use accordingly for critical rules

---

## Related Exam Scenarios

- **Scenario 1**: Customer Support Resolution Agent — Tests Agent SDK usage, MCP tools, and escalation logic
- **Scenario 3**: Multi-Agent Research System — Tests multi-agent orchestration, context passing, error propagation

---

## Summary Table

| Sub-Domain | Focus | Critical Concept | Exam Weight |
|---|---|---|---|
| **d1.1** | Agentic Loops | Check `stop_reason`, not text content | 30% of Domain 1 |
| **d1.2** | Multi-Agent Orchestration | Pass explicit context to subagents | 30% of Domain 1 |
| **d1.3** | Hooks & Enforcement | Use hooks for critical rules, not prompts | 25% of Domain 1 |
| **d1.4** | Session Management | Dynamic adaptive > prompt chaining for complex tasks | 15% of Domain 1 |

