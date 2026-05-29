# Multi-Agent Research System — Answering Strategy

> A study cheat sheet for the **Multi-Agent Research System** scenario, built from the 30 questions in [01-Multi-Agent Research System.md](01-Multi-Agent%20Research%20System.md).
> Goal: read any scenario the right way so your answers stay accurate — even under exam time pressure (4 sets × 15 questions).

---

## Step 1: Build the Mental Model Before Reading Any Question

Every question is set in the **same system**, so hold this architecture in your head:

```
Coordinator (hub) — owns decomposition, ordering, quality control, recovery, aggregation
   ├── Web search subagent
   ├── Document analysis subagent
   ├── Synthesis subagent
   └── Report generation subagent
```

The coordinator is **never just a router**. Across Q3, Q10, Q27, Q28, Q30 it owns: splitting work, enforcing prerequisites, checking coverage, handling errors, and aggregating. If an answer weakens the coordinator (peer-to-peer messaging, subagents calling each other), it's almost always wrong (Q28, Q30).

---

## Step 2: The 6 Patterns (Quick Reference)

All 30 questions collapse into **6 patterns**. Read the symptom, match the row, pick the structural fix.

| Symptom in the scenario | Fix category | Questions |
|---|---|---|
| Metadata/findings/conflicts lost or flattened across handoffs | Fix the output contract — pass structured records forward | Q1, Q13, Q14, Q15, Q22, Q25 |
| Multi-concern request or 25+/45 sources handled in one pass | Decompose into parallel threads, then a separate integration pass | Q6, Q9, Q12, Q21, Q23, Q30 |
| Workflow relies on prompts/text/optimism to decide state | Enforce in control flow — gates, review loops, hub-and-spoke routing | Q3, Q8, Q10, Q27, Q28 |
| Wrong tool, out-of-role tool, missing tool, or weak description | Role-scoped tools, clear descriptions, correct config scope | Q5, Q11, Q16, Q17, Q18, Q20, Q26 |
| Tool failure treated as valid content / wrong retries | Machine-readable error flags (`isError`, `errorCategory`, `isRetryable`) | Q2, Q7, Q29 |
| Stale sources/sessions pollute new work | Fresh session + structured summary; fork_session for isolated branches | Q4, Q19, Q24 |

**The one rule behind all six:** *fix the system itself — never count on the model being careful, on text instructions, or on stale context staying out of the way.*

So for any new question: **(1)** find which row the symptom fits, **(2)** pick the option that fixes it structurally — not the "just instruct the agent" option.

---

## Detailed Symptom → Fix Reference (all 30)

When you want the precise fix wording per question:

| Symptom in the scenario | Fix category | Questions |
|---|---|---|
| Lost dates/citations/methodology across handoffs | Fix the output contract (attach metadata) | Q1, Q22, Q25 |
| Tool failure treated as valid content / wrong retries | Machine-readable error flags (`isError`, `errorCategory`, `isRetryable`) | Q2, Q7, Q29 |
| Lopsided coverage on multi-concern requests | Decompose into parallel concern threads | Q9, Q21, Q23 |
| Independent branches run sequentially / too slow | Parallel Task calls, then aggregate | Q30 |
| Overload from 25+/45 sources | Focused per-source pass + separate integration pass | Q6, Q12, Q22 |
| First drafts coherent but incomplete | Coordinator review/coverage loop (redelegate gaps) | Q3 |
| Report built before synthesis finished | Enforce ordering in control flow (prerequisite gate) | Q10 |
| Only one of several requested tool calls returns | Execute all tool_use blocks until end_turn | Q27 |
| Subagent does work outside its role | Restrict tools to the role (not prompts) | Q5, Q18 |
| Subagents calling each other / weak observability | Route everything through coordinator (hub-and-spoke) | Q28 |
| Stale sources after updates | Fresh session + structured summary | Q4, Q19 |
| Two framings need same baseline but isolated exploration | fork_session branches | Q24 |
| Findings buried in long conversation turns | Scratchpad files at known paths (persistent memory) | Q15 |
| Teammates missing shared tools | Match config scope (project `.mcp.json` vs user) | Q11, Q16 |
| Tool exists but agents ignore it / pick wrong tool | Rewrite tool description (the selection contract) | Q20 |
| Edit fails (non-unique match) / context wasted finding files | Use the right Claude Code tool (Read-then-Write, Glob→Read) | Q17, Q26 |
| Conflicting credible evidence flattened to one number | Preserve both with conflict annotation / by evidentiary status | Q13, Q25 |
| Overconfident auto-publish hides clustered errors | Stratified sampling + monitoring before reducing review | Q8 |
| Escalation ticket lacks actionable state | Structured human handoff (topic, claims, citations, recommendations) | Q14 |

---

## Step 3: The "North Star" Principles

Every correct answer follows one of these. When two options look plausible, the one matching a north star wins:

1. **Encode rules in structure, not prompts.** Tools, control-flow prerequisites, and scoped access beat "tell the agent to be careful." (Q5, Q10, Q15, Q18)
2. **Preserve provenance through every handoff.** Dates, source locations, methodology, conflict notes, evidentiary status travel *with* the claim. (Q1, Q13, Q22, Q25)
3. **Separate focused analysis from integration.** Per-source depth first, then a dedicated cross-source consistency pass. (Q6, Q12)
4. **Decompose multi-concern requests; parallelize independent work.** Split → shared constraints → parallel → unified synthesis. (Q9, Q21, Q23, Q30)
5. **Give failures machine-readable signals.** Distinguish business / transient / permanent. (Q2, Q7, Q29)
6. **Remove stale context, don't ask the model to ignore it.** Fresh session + summary of durable findings; fork_session for shared-baseline/isolated branches. (Q4, Q19, Q24)
7. **Coordinator owns quality control and aggregation.** Review loops, prerequisite gates, hub-and-spoke routing, the tool-use protocol. (Q3, Q10, Q27, Q28)
8. **Transfer actionable state and monitor before trusting.** Structured escalation handoffs and stratified sampling, not announcements or aggregate dashboards. (Q8, Q14)
9. **Use the right tool and a clear tool description.** Glob for discovery then Read; Read-then-Write fallback; descriptions are the model's selection contract. (Q17, Q20, Q26)

---

## Step 4: Eliminate the Recurring Wrong-Answer Traps

These distractors appear in nearly every question. **Cross them out on sight** — they are correct answers ~0% of the time in this scenario:

- ❌ "Add stronger prompt instructions / tell it to stay in its role" → structure is needed (Q5, Q10, Q18)
- ❌ "Be more careful" / "instruct it to read carefully" → leaves the overload unchanged (Q6, Q12, Q22)
- ❌ "Increase context budget / max_tokens / pass full transcripts" → worsens attention dilution (Q1, Q15, Q22)
- ❌ "Average / pick the bigger sample / suppress the weaker source / hunt a tie-breaker" → manufactures false certainty (Q13)
- ❌ "Convert failures to empty successful results" → hides coverage gaps (Q2, Q7, Q29)
- ❌ "Fixed iteration cap of N passes" → controls runtime, not quality/freshness (Q3, Q4, Q19)
- ❌ "Parse text for 'complete'/'ready'/confidence" → turns workflow state into brittle text classification (Q10, Q14, Q27)
- ❌ "Resume + tell coordinator to ignore old results" / "fork the stale session" → relies on prompt compliance over a bad baseline (Q4, Q19)
- ❌ "Concatenate independent outputs" / "let subagents negotiate or message each other" → no real integration, breaks observability (Q9, Q21, Q28)
- ❌ "Dump the full transcript" / "add a general disclaimer" / "rename the tool" → noise instead of actionable structure (Q14, Q20, Q25)
- ❌ "Grep file contents / Bash recursive listing / Read everything" when you know the naming convention → use Glob (Q26)

---

## Step 5: The Three-Question Decision Test

When down to two options, ask:

1. **Does it fix the design or just nudge the model?** Pick the design fix (structure over prompt).
2. **Does it keep the coordinator in control and preserve observability?** Reject peer-to-peer and "skip the coordinator" options.
3. **Does it preserve information rather than discard/flatten it?** Reject truncation, averaging, suppression, and "empty success."

---

## Exam-Specific Tactics (4 sets × 15 questions)

- **Identify the domain tag fast.** This scenario skews to *Agentic Architecture* (decomposition/orchestration), *Tool Design* (error flags, scoping, descriptions), and *Context Management* (staleness, handoffs, monitoring). Almost no pure prompt-engineering here.
- **The longer, mechanism-rich answer usually wins.** Correct answers describe *mechanisms* ("attach dates, source locations, and methodological notes"); traps are vague ("be more careful," "add a disclaimer").
- **"Fresh vs resume vs fork" is a recurring trio** (Q4, Q19, Q24): resume only when prior context is *still mostly valid*; start fresh when sources went stale; fork_session for a shared baseline with isolated branches.
- **Tool questions are about scope, signals, and descriptions** — match config scope to audience (Q11, Q16), make descriptions the selection contract (Q20), give machine-readable error flags (Q2, Q7, Q29), and pick the right Claude Code tool (Glob Q26, Read-then-Write Q17, execute all tool_use blocks Q27).
- **Reliability questions test discipline, not optimism** — monitor before trusting confidence (Q8), and escalate with actionable state (Q14).

---

**Bottom line:** internalize the 6-pattern table and the trap list, and most questions resolve in under a minute — classify the symptom, recall the north star, eliminate the two or three trap distractors, and the remaining mechanism-rich option is almost always correct.
