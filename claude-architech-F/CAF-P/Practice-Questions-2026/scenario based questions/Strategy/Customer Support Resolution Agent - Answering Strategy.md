# Customer Support Resolution Agent — Answering Strategy

> A study cheat sheet for the **Customer Support Resolution Agent** scenario, built from the 58 questions in [02-Customer Support Resolution Agent.md](../02-Customer%20Support%20Resolution%20Agent.md).
> Goal: read any scenario the right way so your answers stay accurate — even under exam time pressure (3 sets × ~20 questions).

---

## Step 1: Build the Mental Model Before Reading Any Question

Every question is set in the **same system**, so hold this architecture and its goal in your head:

```
Coordinator (hub) — verifies identity, decomposes the case, delegates, aggregates,
                     enforces rules, decides refund vs escalate
   ├── Intake / identity subagent
   ├── Billing / order-investigation subagent
   ├── Returns / refund-policy subagent
   └── Account / risk subagent

Backend via MCP tools:
   get_customer        → read-only  (identity)
   lookup_order        → read-only  (order state, return window)
   process_refund      → MUTATING, irreversible (financial action)
   escalate_to_human   → handoff (creates a human ticket)

TARGET: 80%+ first-contact resolution, while knowing when to escalate.
```

Two facts drive most answers:

1. **The 80% target biases *against* over-escalation.** Any option that escalates on sentiment, on "any failure," or on "any duplicate record" is almost always wrong (Q1 is the exception — an *explicit* human request).
2. **`process_refund` is irreversible and `escalate_to_human` is a handoff.** Irreversible/financial actions must be guarded by **deterministic gates/hooks**, not prompts (Q8, Q35, Q48, Q50, Q58). Read-only tools can be scoped more loosely (Q15).

The coordinator is **never just a router** — it owns identity verification, decomposition, prerequisite enforcement, aggregation, and escalation decisions. If an answer weakens it (peer-to-peer subagent messaging, last-subagent-answers, "let them message each other"), it's wrong (Q17, Q40, Q3, Q25).

---

## Step 2: The 9 Patterns (Quick Reference)

All 58 questions collapse into **9 patterns**. Read the symptom, match the row, pick the structural fix.

| Symptom in the scenario | Fix category | Questions |
|---|---|---|
| Backend failures all return the same "Operation failed" → wrong retries/escalations | **Structured, categorized tool errors** (`isError` + `errorCategory` + `isRetryable` + safe guidance) | Q4, Q7, Q13, Q16, Q20, Q30, Q46 |
| Agent breaks an ordering/financial/format rule even though the prompt says not to | **Enforce in code, not prompts** — prerequisite gates, interception hooks, PostToolUse normalization | Q8, Q9, Q21, Q35, Q48, Q50, Q58 |
| Subagent re-asks for facts already known / app never feeds tool results back | **Pass case state explicitly + run a real agentic loop** (`tool_use_id`, drive on `stop_reason`) | Q2, Q22, Q33, Q37, Q42, Q47, Q53 |
| Multi-issue message → overlap, missed concerns, conflicting steps, slow | **Decompose by concern, share facts once, synthesize centrally; match delegation to complexity** | Q3, Q19, Q25, Q28, Q29, Q43, Q57 |
| Subagents talk to each other / specialists never start / over-broad tool access | **Hub-and-spoke + least privilege + flexible delegation prompts** | Q14, Q15, Q17, Q39, Q40, Q51 |
| Agent picks the wrong tool, ignores a capable tool, or replies with no tool | **Make tools discoverable & selectable** — rich descriptions, resources vs tools, `tool_choice` | Q5, Q12, Q23, Q24, Q27, Q34, Q36, Q52 |
| Stale files/sessions, lost provenance, lost progress after restart | **Session lifecycle & durable state** — resume vs fresh vs fork, scratchpad, crash recovery, provenance | Q10, Q11, Q18, Q31, Q32, Q38, Q56 |
| Wrong identity match, over/under-escalation, hidden segment failures | **Human-in-the-loop discipline** — disambiguate identity, calibrate escalation, stratified monitoring | Q1, Q6, Q54, Q55 |
| Wasting context locating files / ambiguous edit fails | **Right Claude Code tool** — Glob→Read, Grep for content, Read-then-Write | Q26, Q41, Q44, Q45, Q49 |

**The one rule behind all nine:** *fix the system itself — never count on the model being careful, on prompt wording, on stale context staying out of the way, or on sentiment as a signal.*

---

## Detailed Symptom → Fix Reference (all 58)

When you want the precise fix wording per question:

| Symptom in the scenario | Fix | Questions |
|---|---|---|
| Same "Operation failed" for timeout/validation/business/permission | Categorized errors: `isError`, `errorCategory`, `isRetryable`, customer-safe guidance | Q4, Q7, Q13, Q30, Q46 |
| "No order found" returned during a backend outage | Empty success **only** for completed searches; retryable error when backend unreachable | Q16 |
| Subagent error is just `{"status":"failed"}` | Return failure type + partial data + cached summaries + suggested fallback | Q20 |
| Refund issued before eligibility/identity/amount confirmed | **Prerequisite gate** on `process_refund` (state-based) | Q8, Q35, Q48 |
| Refund above policy dollar limit ($500 / $150) | **Tool-call interception hook** that blocks and redirects to escalation | Q50, Q58 |
| Inconsistent timestamp/status formats across tools/regions | **PostToolUse hook** → canonical structure before Claude sees it | Q9, Q21 |
| Subagent re-asks for known customer/order facts | Put verified facts, order records, prior findings, goal **in the Task prompt** | Q2, Q22, Q47 |
| New investigation wave loses earlier constraints | Build a **structured findings brief**, include it in each wave's prompt | Q37 |
| Loop exits on assistant text / never feeds results back | Drive loop on `stop_reason`; append results with matching `tool_use_id`; run until `end_turn` | Q33, Q42, Q53 |
| Multi-issue message → overlap & missed concerns | Distinct issue boundary + shared facts → synthesize centrally | Q3, Q25, Q43 |
| Predictable per-charge work, missed cross-account reconciliation | Prompt chain: review each charge, then account-level consistency pass | Q28 |
| First synthesized reply is incomplete | Coordinator compares draft vs request → targeted follow-up → rerun synthesis | Q19 |
| Simple request runs through all specialists (slow, noisy) | Coordinator assesses scope, delegates only to relevant specialists | Q29 |
| Vague request needs different paths after first lookup | Brief fact-gathering pass, then **adaptive** follow-up subtasks | Q57 |
| Subagents message each other → lost rationale/observability | Route all handoffs/results **through the coordinator** | Q17, Q40 |
| Defined specialists never start | Add **`Task`** to coordinator `allowedTools`; keep MCP tools scoped | Q39 |
| Read-only tool needed often but only coordinator has it | **Scoped** access to `lookup_order`; keep mutating tools coordinator-only | Q15 |
| Long prescriptive checklist makes subagent brittle | Delegate **objective + context + criteria + return format**, flexible path | Q14, Q51 |
| Agent passes wrong identifier / wrong tool for colloquial requests | Rewrite **tool descriptions** (purpose, identifiers, fields, edge cases, boundaries) | Q5, Q24, Q34, Q36, Q52 |
| Agent burns turns probing read-only catalogs | Expose catalogs as **MCP resources**; keep actions as tools | Q12, Q23 |
| Agent replies with no backend action when one is required | Set **`tool_choice: "any"`** (must call some tool, still model-selected) | Q27 |
| Resume session after a teammate changed a few files | Resume + **identify changed files** + targeted re-analysis | Q11, Q31 |
| Two resolution paths over a verified baseline | **`fork_session`** from the baseline, isolate each, compare | Q32 |
| Findings degrade over a long investigation | **Scratchpad files** at known paths; reference later | Q18 |
| Coordinator loses progress after a service restart | Subagents **export structured state** to a known location; reload on resume | Q56 |
| Case notes can't tell allegation from verified fact | Structured **claim-source mappings** (source type, field, timestamp, verification) | Q10 |
| Escalations bounce back; humans re-ask for details | Structured **escalation handoff** (ID, facts, root cause, amounts, attempts, next steps) | Q38 |
| Multiple customer matches on common names | Treat as **unresolved identity**; ask for a disambiguating identifier first | Q6 |
| Customer explicitly asks for a human on an easy case | **Honor the request**, escalate cleanly with context (don't resolve first) | Q1 |
| Frustrated but straightforward case auto-escalated | Acknowledge frustration, proceed with supported steps, escalate only if asked again | Q55 |
| 96% dashboard hides reversals in rare segments | **Stratified random sampling** across issue type / age / channel / action | Q54 |
| Context wasted finding files by known naming convention | **Glob** patterns → Read only matches | Q26, Q41, Q49 |
| Find every code path emitting a specific string | **Grep** the exact string → Read matches | Q45 |
| Edit fails (same text in several handlers) | **Read-then-Write** the whole file, change only the intended block | Q44 |

---

## Step 3: The "North Star" Principles

Every correct answer follows one of these. When two options look plausible, the one matching a north star wins:

1. **Encode rules in structure, not prompts.** Prerequisite gates and interception hooks for irreversible/financial actions; PostToolUse hooks for normalization. (Q8, Q9, Q35, Q48, Q50, Q58)
2. **Tool results must carry operational meaning.** Distinguish transient / validation / business / permission with retryability and customer-safe guidance; never collapse them, never fake an empty success. (Q4, Q7, Q13, Q16, Q20, Q30, Q46)
3. **Subagents inherit nothing — package their context.** Verified facts, order records, prior findings, goal, and return format go *in the Task prompt*; findings briefs carry state across waves. (Q2, Q22, Q37, Q47)
4. **Every model request must include the new tool results.** Drive the loop on `stop_reason`, append results with the matching `tool_use_id`, return only at `end_turn`. (Q33, Q42, Q53)
5. **Decompose multi-issue work; match effort to complexity.** Distinct concern boundaries + shared facts → central synthesis; delegate only to relevant specialists; go adaptive when the path is unknown. (Q3, Q25, Q28, Q29, Q43, Q57, Q19)
6. **Coordinator owns the control plane; specialists keep least privilege.** Hub-and-spoke routing, `Task` to spawn, scoped tools, flexible (goal-based) delegation prompts. (Q14, Q15, Q17, Q39, Q40, Q51)
7. **Descriptions and tool/resource shape are the agent interface.** Rich differentiated descriptions drive selection; read-only catalogs are resources; `tool_choice: "any"` forces an action without choosing it. (Q5, Q12, Q23, Q24, Q27, Q34, Q36, Q52)
8. **Persist durable state and provenance.** Resume when mostly valid (refresh what changed), fork for isolated branches, scratchpad/export for long runs and crash recovery, claim-source mappings and structured handoffs for review/escalation. (Q10, Q11, Q18, Q31, Q32, Q38, Q56)
9. **Be disciplined about humans and monitoring.** Honor explicit human requests, disambiguate identity before sensitive ops, never use sentiment as a complexity proxy, and sample by stratum before trusting confidence. (Q1, Q6, Q54, Q55)
10. **Use the most constrained tool for the job.** Glob for paths, Grep for content, Read-then-Write when an edit can't anchor uniquely. (Q26, Q41, Q44, Q45, Q49)

---

## Step 4: Eliminate the Recurring Wrong-Answer Traps

These distractors appear in nearly every question. **Cross them out on sight** — they're correct answers ~0% of the time in this scenario:

- ❌ "Strengthen the system prompt / add few-shot examples to enforce the rule" → for ordering and financial rules you need a gate/hook (Q8, Q35, Q48, Q50, Q58)
- ❌ "Tell subagents to *remember* earlier facts" / "rely on parent conversation history" → subagents inherit nothing (Q2, Q22, Q47)
- ❌ "Retry every failed call N times before escalating" → wastes attempts on non-retryable failures (Q4, Q7, Q13, Q16, Q23, Q30, Q46)
- ❌ "Convert failures to empty successful results" → hides outages as no-matches, risks wrong answers (Q16, Q20)
- ❌ "Use sentiment / angry language to decide escalation or priority" → tone ≠ complexity or preference (Q1, Q4, Q55)
- ❌ "Escalate every duplicate / every failure / every negative case" → kills the 80% resolution target (Q6, Q7, Q55)
- ❌ "Let subagents message each other" / "last subagent writes the reply" / "majority vote" → breaks hub-and-spoke and observability (Q3, Q17, Q19, Q25, Q40)
- ❌ "Add a keyword router mapping phrases → tools" → brittle for colloquial, multi-intent support language (Q5, Q12, Q23, Q24, Q34, Q44, Q52)
- ❌ "Merge tools into one broad tool" → blurs boundaries instead of clarifying them (Q5, Q13, Q34, Q36, Q52)
- ❌ "Parse assistant text for 'complete'/'ready'/'verified'/'eligible'" → workflow state ≠ text classification (Q8, Q33, Q35, Q42, Q48, Q53)
- ❌ "Self-rated confidence score, escalate below threshold" → uncalibrated, not a real control signal (Q19, Q31, Q54, Q55, Q58)
- ❌ "Fixed N-iteration cap" / "fixed tool sequence for every case" → controls runtime, not correctness; ignores complexity (Q28, Q29, Q33, Q42, Q57)
- ❌ "Force a tool with `tool_choice`/startup call on every turn" → over-constrains; resources solve the catalog case (Q12, Q23, Q27, Q52)
- ❌ "Fix formats during final-response generation / via the response parser" → too late; the decision is already made (Q9, Q21)
- ❌ "Start fresh and re-explore everything" when only a couple files changed → wasteful; resume + refresh what changed (Q11, Q31)
- ❌ "Grep file *contents* / Bash recursive listing / Read everything" when you know the filename convention → use Glob (Q26, Q41, Q49)

---

## Step 5: The Decision Test (when down to two options)

1. **Is the rule hard (financial, irreversible, ordering, identity)?** → Pick the **gate/hook**, not the prompt. (Q8, Q35, Q48, Q50, Q58)
2. **Does it keep the coordinator in control and preserve observability?** → Reject peer-to-peer and "skip the coordinator." (Q17, Q40)
3. **Does it preserve information and operational meaning?** → Reject empty-success, generic errors, truncation, lost provenance. (Q16, Q20, Q10, Q38)
4. **Does it protect the 80% target?** → Reject blanket escalation and sentiment triggers; prefer clarify/scope over hand off. (Q1, Q6, Q55)
5. **Is the symptom "wrong/ignored tool"?** → Fix the **description** (or use a resource / `tool_choice`), not a keyword router or a merged tool. (Q5, Q12, Q23, Q24, Q27)

---

## Exam-Specific Tactics

- **Spot the tool type.** `process_refund` (mutating/irreversible) and `escalate_to_human` (handoff) demand gates, hooks, least privilege, and structured handoffs; `get_customer`/`lookup_order` (read-only) can be scoped to subagents and exposed more freely. Many answers hinge on this distinction (Q15, Q35, Q50, Q58).
- **"Gate vs hook vs prompt" is the signature trio here.** Prerequisite **gate** = block a tool until required state exists (Q8, Q35, Q48). Interception **hook** = block/redirect based on arguments like a dollar limit (Q50, Q58). **PostToolUse hook** = normalize tool output before the model sees it (Q9, Q21). Prompts/few-shot are always the trap.
- **"Resume vs fresh vs fork" recurs** (Q11, Q31, Q32): resume + refresh changed files when mostly valid; fork_session for a shared baseline with isolated branches; fresh only when the baseline is genuinely stale (rare here).
- **Tool-selection problems are almost always "rewrite the description."** Five separate questions reward the same fix (Q5, Q24, Q34, Q36, Q52). Resources (Q12, Q23) and `tool_choice: "any"` (Q27) are the close cousins.
- **Escalation/identity questions test discipline, not optimism.** Honor explicit human requests (Q1), disambiguate before sensitive ops (Q6), don't auto-escalate on frustration (Q55), and never trust an aggregate dashboard over stratified sampling (Q54).
- **The longer, mechanism-rich answer usually wins.** Correct answers name concrete mechanisms ("prerequisite gate on structured state," "PostToolUse hook to canonical structure"); traps are vague ("be exhaustive," "think carefully," "add a disclaimer").

---

**Bottom line:** internalize the 9-pattern table and the trap list, then classify each scenario by **(1)** which tool/action is involved (irreversible? read-only? handoff?), **(2)** whether the failure is a *rule*, a *handoff*, a *tool-selection*, or a *decomposition* problem, and **(3)** the north star that applies. The mechanism-rich option that keeps the coordinator in control and protects the 80% target is almost always correct.
