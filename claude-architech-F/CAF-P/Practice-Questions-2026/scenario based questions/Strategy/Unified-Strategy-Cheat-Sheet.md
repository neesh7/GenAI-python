# Unified Strategy Cheat Sheet

A compact yet complete guide to the shared strategy patterns across:
- Customer Support Resolution Agent
- Multi-Agent Research System
- Developer Productivity with Claude
- Claude Code for Continuous Integration
- Structured Data Extraction

Use this as a fast decision guide for exam-style scenario questions.

---

## 1. Start with the system model

Always begin by identifying the scenario’s architecture.

- **Structured Data Extraction**: linear pipeline — extraction → validation → QA → downstream.
- **Multi-Agent Research**: hub-and-spoke coordinator with specialized subagents.
- **Developer Productivity**: coordinator + isolated exploration in unfamiliar code.
- **Customer Support**: coordinator enforces identity, rules, escalation, irreversible actions.
- **CI/CD**: headless non-interactive pipeline, committed repo config, structured review output.

If the question doesn’t mention a coordinator, don’t invent one. If it does, keep the coordinator in control.

---

## 2. Universal patterns and optimal fixes

### 2.1 Structure beats prompts

When the model is failing, the best fix is usually a structural one.

- Use `tool_use` + JSON schema for output contracts.
- Use scoped tools, control flow gates, hooks, or config files.
- Avoid "be careful", "be conservative", or longer general instructions.

This rule appears in all scenarios:
- extraction schemas (Structured Data)
- tool selection and error flags (Multi-Agent, Customer Support)
- plan mode vs direct execution (Developer Productivity)
- CI automation contracts (CI)

### 2.2 Right tool, right scope

Pick the right tool before changing the prompt.

- `Glob` for filename/path search.
- `Grep` for content search.
- `Read` for file contents.
- `Edit` for existing files, `Write` only for new files.
- `tool_choice`, rich descriptions, and least-privilege tool lists make selection reliable.

Wrong tool traps are common in Developer Productivity and Customer Support.

### 2.3 Validate meaning, not just shape

Schema validation proves structure, not correctness.

- When output is valid but wrong, use semantic validation and retry with exact error context.
- For sums/dates/field relationships, send the failed extraction + validator message back to the model.
- For noisy or inconsistent outputs, add targeted examples showing the ideal result.

This is the core failure mode in Structured Data Extraction and CI.

### 2.4 Preserve uncertainty honestly

Don’t force answers when evidence is missing.

- Use `null` for genuinely absent values.
- Add fallback enum values like `other`, `unclear`, or `unknown` with a required detail field.
- Distinguish "no data found" from "tool access failed."
- Stop retries when the source is absent and request the needed input.

This keeps downstream systems honest in Extraction and CI.

### 2.5 Keep provenance and durable state

Carry source + location + excerpt through every handoff.

- Structured handoffs preserve evidence and avoid reconstruction.
- Scratchpad files, external state stores, and resume manifests survive long runs.
- In Multi-Agent and Structured Data, provenance is part of the data contract.

### 2.6 Separate roles and sessions

Review and generation are different work.

- Use separate invocations for review to avoid self-bias.
- Use a fresh session or fork when the baseline is stale or branching.
- Avoid subagents messaging each other; route results through the coordinator.

This is critical in CI, Multi-Agent, and Customer Support.

---

## 3. Common symptom categories

### Symptom: schema-valid but semantically wrong

Fix: semantic validation + retry with error details.

Example: totals don’t add, wrong date field, severity mismatch.

### Symptom: output is inconsistent, vague, or format-incorrect

Fix: targeted few-shot examples, clear output format, schema tool-use.

Example: fields appear in wrong locations, markdown fences, bad commas.

### Symptom: tool selection is wrong or ignored

Fix: improve tool description, use `tool_choice`, scope tools by role.

Example: agent ignores a capable tool or replies without calling any tool.

### Symptom: critical action or rule is broken despite instructions

Fix: encode it in a gate/hook or config, not in the prompt.

Example: refund limits, escalation thresholds, irreversible money transfers.

### Symptom: stale context or lost progress

Fix: resume only when valid, fork for isolated branches, persist state externally.

Example: long-running review loses earlier findings or repeats work.

### Symptom: irrelevant guidance fires on unrelated files

Fix: path-scoped config (`.claude/rules/` globs) or committed project CLAUDE.md.

Example: accessibility rules triggering on backend code or docs PRs.

### Symptom: missing source/evidence

Fix: preserve nulls, classify missing-source separately, request the missing artifact.

Example: required approval date absent because the approval letter wasn’t provided.

### Symptom: noisy reviewer feed

Fix: concrete reportable/non-reportable categories, severity definitions, and examples.

Example: speculative "might be slow" findings that developers ignore.

---

## 4. Scenario-specific quick facts

### Structured Data Extraction

- Linear pipeline, not orchestration.
- Main test: schema shape vs semantic meaning.
- Best fixes: examples, trusted nulls/other, provenance, separate QA reviewer.
- Bonus: pilot batch before full scale, sync for latency-bound, batch for bulk.

### Multi-Agent Research System

- Coordinator owns decomposition, quality, recovery, aggregation.
- Fixes: structured records forward, machine-readable error flags, fresh/forked sessions.
- Never let subagents message each other or infer coverage from prose.

### Developer Productivity with Claude

- Explore/clarify before editing in unfamiliar code.
- Use plan mode when the approach is unknown.
- Anchor fixes in failing tests, stack traces, expected vs actual.
- Shared guidance belongs in committed project config, preferably `.claude/rules/`.

### Customer Support Resolution Agent

- Coordinator hub with identity, eligibility, escalation rules.
- Critical actions need deterministic hooks/gates, not prompts.
- Use structured error categories and preserve operational meaning.
- Escalate on objective criteria, not sentiment or low confidence.

### Claude Code for Continuous Integration

- Always run CI non-interactively with `-p`/`--print`.
- Use structured JSON output and semantic validation.
- Load context conditionally by file/path globs.
- Keep tooling and workflows committed, not in `~/.claude`.

---

## 5. Fast decision test

When you are down to two options, ask:

1. Does this fix the system or just tweak prompts?
2. Does it preserve structure, evidence, and provenance?
3. Does it keep control with the coordinator/review pipeline?
4. Does it use the correct tool/scoped config instead of a generic fallback?
5. Does it treat missing evidence honestly instead of forcing a value?

If the answer is yes, it is probably the right choice.

---

## 6. Recurring wrong-answer traps

- `"Be more careful"` or `"be conservative"`
- `"Make every field required"`
- `"Retry until it fills"`
- `"Convert failures to empty success"`
- `"Use ~./claude for CI or team rules"`
- `"Let subagents message each other"`
- `"Resume and ask the model to ignore stale context"`
- `"Regex over markdown instead of schema JSON"`
- `"Aggregate confidence / overall accuracy only"`

Cross these out first.

---

## 7. One-liner summary

Fix the architecture, not the wording: use tools and schemas for structure, preserve evidence and uncertainty, separate roles and sessions, validate meaning, and keep shared behavior in committed config.
