# Claude Architect Handbook / Cheat Sheet

A single reference covering Domains 1 through 5 for Claude architecture, prompt engineering, tool design, MCP integration, configuration, workflows, context, reliability, and production-grade agent systems.

---

## Domain 1: Agentic Architecture & Orchestration (25%)

### d1.1 — Agentic Loops & Core API

- The agentic loop is the core execution pattern.
- Use `stop_reason` to control continuation:
  - `tool_use` → continue the loop and execute the tool.
  - `end_turn` → exit the loop.
- Do not parse natural language or text output to decide whether to continue.
- Tool results are appended to the conversation and fed back on the next iteration.
- The SDK automates loop mechanics, but you must understand the semantics.

Key rule:
- `stop_reason` is the only reliable loop signal.

Anti-patterns:
- Parsing assistant text for completion.
- Using arbitrary iteration caps as the main stop condition.
- Checking token usage or text content instead of `stop_reason`.

### d1.2 — Multi-Agent Orchestration

- Use a hub-and-spoke architecture: coordinator + specialized subagents.
- Subagents must receive explicit task-specific context only.
- Do not pass the entire coordinator conversation to subagents.
- Specialized subagents should have 4-5 focused tools each.
- Use `Task` or `fork_session` for parallel or isolated work.
- Context isolation avoids pollution and improves accuracy.

Correct structure:
- Coordinator tools: delegation, synthesis, formatting.
- Customer/order/comms subagents: focused domain tools.

Anti-patterns:
- Sharing full coordinator context with every subagent.
- Expecting subagents to inherit coordinator knowledge implicitly.
- Giving a single agent 18+ tools.

### d1.3 — Hooks & Programmatic Enforcement

- Hooks enforce critical business rules deterministically.
- Prompts are probabilistic and should not be used for essential enforcement.
- Use pre-tool-use hooks to validate and block invalid calls.
- Use post-tool-use hooks to inspect output and enforce rules.

Example:
- Refund limit > $500 should be enforced by a hook, not a prompt.

Anti-patterns:
- Placing critical compliance or threshold rules only in prompts.
- Using model confidence or sentiment as escalation triggers.

### d1.4 — Session Management & Workflows

- `--resume` continues a previous session with preserved context.
- `fork_session` creates a branch for exploration without polluting the main session.
- Use named sessions to organize workflows.
- Detect stale context in long-running sessions and refresh critical data.
- Choose between prompt chaining and dynamic adaptive decomposition:
  - Prompt chaining for predictable linear workflows.
  - Dynamic adaptive for unknown complexity or branching decisions.

Anti-pattern:
- Static step chains for tasks that require adaptation.

Summary:
- `stop_reason` for loop control.
- Hooks for deterministic enforcement.
- Subagents need explicit scoped context.
- Fork/resume for session control.

---

## Domain 2: Tool Design & MCP Integration (20%)

### d2.1 — Tool Description Best Practices

- Tool descriptions are model-facing documentation.
- Include purpose, input format, examples, edge cases, and when not to use it.
- A strong description prevents misuse and improves tool selection.

Best practices:
- Clear one-sentence purpose.
- Exact input types, formats, and constraints.
- Examples for common cases.
- Edge case behavior for empties, invalid inputs, and boundaries.

Anti-patterns:
- Vague descriptions.
- Missing input formats or edge cases.
- No examples.

### d2.2 — Structured Error Responses

- Error responses must be structured and informative.
- Include `isError`, `errorCategory`, `isRetryable`, and failure context.
- Distinguish access failure from empty result.

Critical distinction:
- Access failure = `isError: true` (could not perform the operation).
- Empty result = `isError: false` (operation succeeded, no matches found).

Anti-pattern:
- Returning `[]` for a failed database connection.

### d2.3 — Tool Distribution & Selection

- Optimal agent tool count: 4-5 tools.
- Too many tools degrade selection accuracy.
- Distribute tools across specialized subagents.
- Use `tool_choice` to constrain tool invocation when needed.

Anti-pattern:
- Giving one agent 18+ tools.
- Ambiguous tool names or overlapping capabilities.

### d2.4 — MCP Server Configuration

- `.mcp.json` is project-level and shared via git.
- `~/.claude.json` is user-level and personal.
- Use `${ENV_VAR}` for secrets, never hardcode credentials.
- MCP servers provide tools, resources, and prompt templates.

Anti-pattern:
- Hardcoding API keys in `.mcp.json`.

### d2.5 — Built-in Tools

- Know the six built-ins: `Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`.
- Use `Write` only for new files.
- Use `Edit` for existing file modifications.
- Use `Read` instead of Bash to inspect file contents.
- Use `Grep` for content search and `Glob` for filename matching.

Anti-patterns:
- Using Bash for file operations that have dedicated tools.
- Confusing `Grep` with `Glob`.

Summary:
- Detailed tool docs, structured errors, narrow tool sets, proper MCP config, and built-in tool discipline.

---

## Domain 3: Claude Code Configuration & Workflows (20%)

### d3.1 — CLAUDE.md Hierarchy & Configuration

- Claude Code uses hierarchical config:
  - User-level: `~/.claude/CLAUDE.md` (personal preferences)
  - Project-level: `.claude/CLAUDE.md` (shared standards)
  - Directory-level: `src/.../CLAUDE.md` (scoped rules)
- Precedence: directory > project > user.
- Modular config is better than one giant file.
- Use `@import` for organized rule files.

Anti-patterns:
- One massive `CLAUDE.md`.
- Personal preferences in project config.
- Mixing unrelated concerns in the same file.

### d3.2 — Custom Commands & Skills

- Commands are simple, one-step actions run in main context.
- Skills are complex, isolated behaviors that can fork context.
- Skills should use `context: fork` for isolation and `allowed-tools` restrictions.
- Use commands for quick tasks and skills for complex workflows.

Anti-patterns:
- Using commands for complex exploration.
- Using skills for trivial tasks.
- Forgetting to restrict allowed tools.

### d3.3 — Plan Mode & Iterative Refinement

- Plan mode is valuable for complex tasks and architecture decisions.
- Direct execution is fine for simple, well-defined work.
- Iterative refinement should follow a TDD-style loop:
  1. Write failing test.
  2. Implement.
  3. Run tests.
  4. Refine.
- Use concrete examples to specify style and output format.
- Use the interview pattern when requirements are ambiguous.

Anti-patterns:
- Plan mode for trivial fixes.
- No planning for complex work.
- Skipping concrete examples.

### d3.4 — CI/CD Integration & Batch Processing

- Use `-p` for non-interactive CI/CD execution.
- Use `--output-format json` for machine-readable results.
- Use `--json-schema` to enforce output shape.
- Separate generator and reviewer sessions to avoid confirmation bias.
- Batch API is 50% cheaper for non-urgent workloads.
- Use `custom_id` to track batch requests.

Anti-patterns:
- Interactive mode in CI/CD.
- Same-session self-review.
- Skipping structured JSON output.

Summary:
- Understand CLAUDE.md layers, commands vs skills, planning vs direct execution, and CI/CD flags.

---

## Domain 4: Prompt Engineering & Structured Output (20%)

### d4.1 — Explicit Criteria & Instruction Design

- Use explicit, measurable criteria in production prompts.
- Avoid vague instructions like "make it better" or "be thorough." 
- Measurable criteria enable validation and reduce false positives.

Example:
- Wrong: "Find issues"
- Right: "Flag functions >50 lines, missing async error handling, hardcoded API keys."

Anti-patterns:
- Vague instructions.
- Ignoring false positive impact.
- Unmeasurable requirements.
- Over-flagging for perfection.

### d4.2 — Few-Shot Prompting

- Use 2-4 examples for pattern establishment.
- Keep output format consistent across examples.
- Include at least one edge case or ambiguous example.
- Use few-shot for ambiguous or domain-specific tasks.
- Avoid few-shot for simple extraction tasks.

Anti-patterns:
- Too many examples (>6).
- Inconsistent example format.
- No edge case coverage.
- Using few-shot for simple tasks.

### d4.2.5 — Chain-of-Thought Prompting

- Chain-of-thought forces step-by-step reasoning.
- Use it for complex multi-step logic and decision-making.
- Not necessary for simple extraction.
- Combining few-shot and CoT is powerful for complex analysis.

Anti-patterns:
- Using CoT for trivial tasks.
- Asking for reasoning without verification steps.
- Vague thought prompts.

### d4.3 — Tool Use for Structured Output

- `tool_use` guarantees structure, not semantics.
- The model may still return wrong values even if the schema is valid.
- Design robust JSON schemas with required fields, enums, and nullable fields.
- Always validate extracted values after tool_use.

Anti-patterns:
- Assuming tool_use eliminates all errors.
- Skipping semantic validation.
- Using rigid schemas without `other` enums or nullable fields.

### d4.4 — Validation-Retry Loops & Multi-Pass Review

- Use validation-retry loops to catch and correct tool or extraction mistakes.
- Multi-pass review improves reliability: validate, retry, and then review.
- Always verify structured output before accepting it.

Summary:
- Explicit instructions, 2-4 few-shot examples, CoT for hard reasoning, tool_use for structure, and validation loops.

---

## Domain 5: Context & Reliability (15%)

### d5.1 — Context Optimization & Positioning

- Preserve critical information while managing the context window.
- Avoid progressive summarization of essential facts.
- Use immutable case facts blocks for always-available reference data.
- Place the most important information at the beginning or end of context.
- The middle of the context is the least reliable.

Example:
- Keep a `CASE FACTS` block with customer, order, amounts, and rules.
- Do not summarize critical data into progressively shorter forms.

Anti-patterns:
- Summarizing critical details repeatedly.
- Ignoring the lost-in-the-middle effect.
- No case facts block.
- Keeping verbose tool outputs untrimmed.

### d5.2 — Escalation & Error Propagation

- Escalate only on valid criteria: explicit customer request, policy gap, capability limit, business threshold, repeated failures.
- Never escalate based on sentiment or model confidence.
- Propagate errors with structured context.
- Access failure and empty result must remain distinct.
- Local recovery should be attempted before escalation.

Anti-patterns:
- Sentiment-based escalation.
- Generic error propagation.
- Silent error suppression.
- Confidence-based escalation.

### d5.3 — Context Degradation & Extended Sessions

- Extended sessions degrade over time: forgetting instructions, generic responses, and tool accuracy drops.
- Use scratchpad files for persistent state.
- Use `/compact` or equivalent to reclaim context space.
- Delegate verbose tasks to subagents.
- Track stratified metrics per document type, not just aggregate.
- Preserve provenance and confidence metadata.

Anti-patterns:
- Long sessions without monitoring.
- No scratchpad for state.
- Aggregate metrics only.
- No subagent delegation.

### d5.4 — Human Review & Information Provenance

- Track source, confidence, timestamp, and agent ID for each data point.
- Use field-level confidence and claim-source mappings.
- Annotate conflicts explicitly instead of choosing silently.
- Use human checkpoints for high-risk or conflicting decisions.

Provenance metadata:
- `source`: where the data came from.
- `confidence`: verified/extracted/inferred/estimated.
- `timestamp`: when it was retrieved.
- `agent_id`: which subagent produced it.

Anti-patterns:
- No provenance tracking.
- Silent conflict resolution.
- Missing timestamps or source metadata.

Summary:
- Preserve critical facts, escalate on objective signals, manage long session degradation, and track provenance with human review where needed.

---

## Fast Reference Summary

- Domain 1: `stop_reason`, hooks, subagents, session management.
- Domain 2: tool descriptions, structured errors, tool distribution, MCP config, built-in tools.
- Domain 3: CLAUDE.md hierarchy, commands vs skills, plan mode, CI/CD integration.
- Domain 4: explicit criteria, few-shot, CoT, tool_use structure, validation loops.
- Domain 5: context positioning, escalation rules, session degradation, provenance.

## Quick Exam Tips

- Always use `stop_reason`, not text output.
- Use programmatic hooks for critical rules.
- Keep tools per agent to 4-5.
- Separate project-level vs user-level config.
- Use `-p` for CI/CD and JSON output for automation.
- `tool_use` guarantees structure, not correctness.
- Preserve case facts and avoid progressive summarization.
- Escalate on objective criteria, not sentiment.
- Track provenance for trust and conflict resolution.
