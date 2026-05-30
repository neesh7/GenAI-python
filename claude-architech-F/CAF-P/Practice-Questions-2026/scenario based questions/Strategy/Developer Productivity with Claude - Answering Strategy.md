# Developer Productivity with Claude — Answering Strategy

> A study cheat sheet for the **Developer Productivity with Claude** scenario, built from the 20 questions in [04-Developer Productivity with Claude.md](../04-Developer%20Productivity%20with%20Claude.md).
> Goal: read any scenario the right way so your answers stay accurate — even under exam time pressure (3 sets × ~20 questions).

---

## Step 1: Build the Mental Model Before Reading Any Question

Every question is set in the **same system**, so hold this setup and its goal in your head:

```
Claude Agent SDK developer-productivity agent
  helps engineers: explore unfamiliar codebases · understand legacy systems ·
                   generate boilerplate · automate repetitive tasks

Built-in tools:    Glob  (find files by PATH/name)
                   Grep  (search file CONTENTS)
                   Read  (load specific files)
                   Write (create/replace files)
                   Bash  (run commands)
                   + MCP servers (metadata, dependency graphs, etc.)

Orchestration:     Coordinator → subagents (each has ISOLATED context)
                                → synthesizer

Persistent config: project CLAUDE.md (committed, shared) ·
                   .claude/rules/*.md (split by concern) ·
                   ~/.claude/CLAUDE.md (per-user, NOT shared)

Modes:             plan mode (explore/design first) vs direct execution (edit now)

TARGET: reliable help in unfamiliar/legacy code without expensive rework.
```

Two facts drive most answers:

1. **The agent works in *unfamiliar, legacy* code.** That biases answers toward **exploring/clarifying before editing** (plan mode, targeted clarifying questions) and **anchoring refinement in concrete evidence** (failing tests, stack traces) rather than vague "be more careful" loops. Trial-and-error via test failures and "just start editing" are usually wrong.
2. **Subagents inherit nothing and prose handoffs lose provenance.** The coordinator owns shared state and routing; subagents must return **structured handoff records** (finding separated from file path, symbol, line range, evidence) — never free-form summaries the synthesizer has to re-derive.

The recurring tensions are **(a)** plan vs direct execution, **(b)** clarify/test-first vs "be more careful," **(c)** where shared context lives (project CLAUDE.md / `.claude/rules/` vs personal/manual), and **(d)** Glob vs Grep vs Read for the search type.

---

## Step 2: The 8 Patterns (Quick Reference)

All 20 questions collapse into **8 patterns**. Read the symptom, match the row, pick the structural fix.

| Symptom in the scenario | Fix category | Questions |
|---|---|---|
| Need files by **name/extension** → Grep/Read produce noise or bloat | **Glob** for paths, then Read only matches | Q1 |
| Know a **string/symbol**, need where it lives in a big repo | **Grep** the exact string → Read matching files | Q15 |
| Same session generated the code, now reviews it → defends its choices | **Separate Claude invocation** with diff + repo context + criteria only | Q2 |
| "Fix the bugs / be more careful" loops; prose specs give uneven code | **Evidence-based refinement / test-first** — failing names, inputs, expected vs actual, stack traces | Q3, Q9, Q20 |
| Risky/poorly-understood domain; first drafts miss hidden constraints | **Have Claude ask targeted clarifying questions first** (improve the problem definition) | Q4, Q11 |
| Change spans many files/abstractions; approach not yet chosen | **Plan mode** to map flows & compare options before editing | Q5, Q17 |
| Subagent handoffs are free-form prose → misattributed claims, lost line ranges | **Structured handoff records** (finding ⟂ path ⟂ symbol ⟂ line range ⟂ excerpt) | Q6, Q13 |
| Shared guidance loads for one engineer but not clones / monolithic CLAUDE.md distracts | **Project-level config**: commit CLAUDE.md / split into `.claude/rules/` by concern | Q7, Q8, Q10 |

Plus four orchestration/interface calls:

- **Coordinator owns shared state:** pass relevant prior findings into each subsequent subagent prompt; don't let subagents message each other or use one bloated generalist. (Q14)
- **Coverage is a planning job:** the coordinator must enumerate plausible entry points (scheduled jobs, admin, CLI), not just the obvious REST path; don't make synthesis *infer* missing workflows. (Q18)
- **Force a true prerequisite with `tool_choice`:** name the required tool on the first request, then switch to `auto` for model-driven follow-up. (Q19)
- **Structured output as the integration contract:** `--output-format json` + `--json-schema`, not regex over markdown. (Q12)

**The one rule behind all eight:** *explore and clarify before editing in unfamiliar code, anchor every refinement in concrete evidence, keep the coordinator in control with explicit provenance, and put shared context in committed, scoped project config.*

---

## Detailed Symptom → Fix Reference (all 20)

| Symptom in the scenario | Fix | Questions |
|---|---|---|
| Update all `*.fixture.json`; Grep on "fixture" is noisy and misses sparse files | **Glob** `**/*.fixture.json` → Read only matches | Q1 |
| CI review resumes the generating session → misses design issues, defends choices | **Separate Claude Code invocation** with PR diff + repo context + criteria only | Q2 |
| "Fix the migration bugs" gives inconsistent improvements | Share **failing test names, inputs, expected vs actual, stack traces**; iterate minimal fixes | Q3 |
| Caching on legacy auth; little domain knowledge; past code failed on edge cases | Claude **asks targeted questions** about invariants, invalidation, audit, failure modes first | Q4 |
| "Cancel renewal" logic split across CLI/web/jobs; earlier edits hit wrong abstraction | **Plan mode** to map flows & compare entry points before modifying files | Q5 |
| Subagent narrative findings misattribute files / drop line ranges | **Structured handoff records**: findings ⟂ paths ⟂ symbols ⟂ line ranges ⟂ excerpts | Q6, Q13 |
| 1,200-line root CLAUDE.md → merge conflicts, distraction | Split into focused topic files under **`.claude/rules/`** | Q7 |
| Conventions load for senior engineer but not clones; no repo files changed | Move to **committed project-level CLAUDE.md** | Q8 |
| Adapter drafts compile but miss nulls/retries/perf; prose specs uneven | **Write tests first** (behavior, edge cases, perf), iterate on failing results | Q9 |
| CI test suggestions are shallow / duplicate / ignore fixtures | Document standards, high-value criteria, reusable fixtures in **project CLAUDE.md** | Q10 |
| Brief prompts miss idempotency/tenant/observability/retention/rollback decisions | Claude **asks targeted clarification** about operational constraints first | Q11 |
| Inline-comment integration breaks on prose/markdown/renamed fields | Run with **`--output-format json` + `--json-schema`**; map validated findings | Q12 |
| Planning subagent ignores DB constraints & caller list already found | Coordinator **maintains shared state**, includes prior findings in each prompt | Q14 |
| Stack trace has error string + `validateTransition`; hundreds of files | **Grep** the string/function → Read matching files | Q15 |
| One agent does stable license reviews *and* open-ended bug investigations | **Fixed prompt chain** for stable rubric; **adaptive** subtasks for investigation | Q16 |
| Replace permissions layer across handlers/CLI/middleware/tests/docs; approach unchosen | **Plan mode** to explore deps, compare strategies, produce a plan first | Q17 |
| "How does user export work?" misses scheduled/admin/CLI paths | **Coordinator planning** enumerates entry points, delegates distinct areas before synthesis | Q18 |
| Agent starts dependency/plan work before collecting canonical versions | **Force metadata tool with `tool_choice`** on first request, then `auto` | Q19 |
| Three coupled failures; single-issue fixes reintroduce each other | **One refinement request** describing all failures, shared constraints, expected behavior | Q20 |

---

## Step 3: The "North Star" Principles

Every correct answer follows one of these. When two options look plausible, the one matching a north star wins:

1. **Explore/design before editing in unfamiliar, multi-file, or unchosen-approach work.** Use plan mode; don't let test/compile failures "discover" the architecture. (Q5, Q17)
2. **Improve the problem definition first for ambiguous/risky tasks.** Have Claude ask targeted clarifying questions about invariants, operational constraints, and edge cases before writing code. (Q4, Q11)
3. **Anchor refinement in concrete, reproducible evidence.** Failing test names, inputs, expected vs actual, stack traces — and write tests first to convert vague quality into acceptance criteria. (Q3, Q9, Q20)
4. **Match decomposition and refinement style to the work shape.** Fixed prompt chain for stable rubrics; adaptive subtasks for open-ended investigation; one combined request for *coupled* failures, separate turns only for *independent* ones. (Q16, Q20)
5. **Generation and review are different roles — isolate them.** Run review as a fresh invocation with only the diff, repo context, and criteria. (Q2)
6. **Subagents inherit nothing; the coordinator owns shared state and routing.** Pass relevant prior findings forward; no peer-to-peer messaging, no bloated generalist. (Q14)
7. **Provenance is part of the deliverable.** Structured handoff records separate the claim from its path, symbol, line range, and excerpt — never reconstructed from prose. (Q6, Q13)
8. **Coverage on broad questions is a planning/routing responsibility.** Enumerate plausible entry points up front; don't make synthesis infer missing workflows. (Q18)
9. **Shared team context belongs in committed, scoped project config.** Project CLAUDE.md for always-on standards; split into `.claude/rules/` by concern; never personal `~/.claude` or manual paste/copy steps. (Q7, Q8, Q10)
10. **Force true prerequisites deterministically; define interfaces with schemas.** `tool_choice` names the required first tool then restores `auto`; `--output-format json --json-schema` for automation contracts. (Q19, Q12)

---

## Step 4: Eliminate the Recurring Wrong-Answer Traps

These distractors appear in nearly every question. **Cross them out on sight** — they're correct answers ~0% of the time in this scenario:

- ❌ "**Start direct execution** and let test/compile failures reveal the architecture" → trial-and-error in legacy code causes rework (Q5, Q17, Q8-codegen)
- ❌ "Tell Claude it's wrong and to **be more careful** / reason carefully" → no evidence, no convergence (Q3, Q9, Q20)
- ❌ "Give a **longer prose spec** and let it infer domain rules" → prose can't supply unknown constraints; clarify or test instead (Q4, Q9, Q11)
- ❌ "**Read every file** / load the whole module tree first" → bloats context before the agent knows what matters (Q1, Q5, Q15, Q18)
- ❌ "Use **Grep on contents** to find files by name" or "**Glob** to find a known string" → wrong tool for the search type (Q1, Q15)
- ❌ "**Resume the generating session** to review its own code" / self-critique / report-only-if-found-twice → biased context, hides subtle bugs (Q2)
- ❌ "Let **subagents message each other**" / "replace specialists with one generalist" / "infer deps from file names" → breaks coordinator control & evidence (Q14)
- ❌ "Have the **synthesizer reconstruct** locations / infer missing workflows from naming" → unsupported guesses, lost provenance (Q6, Q13, Q18)
- ❌ "**Regex over markdown**" / "demand JSON then reject bad output" / "second normalization pass" → brittle; use a schema at the source (Q12)
- ❌ "Move shared guidance to **`~/.claude/CLAUDE.md`**" / "paste at session start" / "copy a personal memory file" → not shared, depends on manual steps (Q7, Q8, Q10)
- ❌ "Keep the **monolithic root CLAUDE.md**, add stronger headings to ignore sections" → still loaded, still distracting (Q7)
- ❌ "**Slash command / personal command** for an always-on standard" → needs manual invocation, not shared with CI (Q7, Q8, Q10)
- ❌ "`tool_choice: any`" / "system-prompt says do X first" / "parse text for a completion phrase" → doesn't force the *right* tool deterministically (Q19)
- ❌ "**Separate session per package/module**, don't share findings" → loses consistency and shared design (Q5, Q17, Q20)
- ❌ "Fix coupled failures **sequentially / in isolated parallel sessions**" → reintroduces the others; produces incompatible patches (Q20)

---

## Step 5: The Decision Test (when down to two options)

1. **Is the work multi-file / unfamiliar / approach-not-chosen?** → **Plan mode** first. Reject "just start editing" and "let failures guide it." (Q5, Q17)
2. **Is the task ambiguous or domain-risky?** → **Ask targeted clarifying questions** before implementing. (Q4, Q11)
3. **Is refinement looping on vague feedback?** → Anchor in **failing tests / stack traces / expected vs actual**; write tests first. (Q3, Q9, Q20)
4. **Is it review of generated code?** → **Separate invocation**, diff + criteria only. Reject same-session and majority-vote. (Q2)
5. **Is it multi-agent handoff/coverage?** → **Coordinator holds state, structured handoff records, planned entry points.** Reject prose handoffs, peer messaging, and synthesis-inferred coverage. (Q6, Q13, Q14, Q18)
6. **Is it shared team guidance?** → **Committed project CLAUDE.md / `.claude/rules/`.** Reject `~/.claude`, paste, copy, and slash-command-for-always-on. (Q7, Q8, Q10)

---

## Exam-Specific Tactics

- **Glob vs Grep vs Read is a free point.** Files by **name/extension → Glob**; known **string/symbol → Grep**; then **Read** only matches. Bash recursion and "read everything" are always wrong (Q1, Q15).
- **Plan mode vs direct execution hinges on uncertainty + blast radius.** Many files + unchosen approach + risk of breaking unrelated workflows → **plan mode**. A single mechanical change wouldn't need it (Q5, Q17).
- **"Be more careful" is never the answer.** Every refinement question rewards **concrete evidence** — failing tests, stack traces, expected vs actual — or **clarifying questions** when requirements are missing (Q3, Q4, Q9, Q11, Q20).
- **Couple vs independent decides refinement shape.** Shared helper/template/call-paths → **one combined request**; truly independent bugs → separate turns. Isolated parallel sessions produce incompatible patches (Q20).
- **Config scope = collaboration boundary.** Team + always-on → committed **project CLAUDE.md**; topic-specific → **`.claude/rules/`**; personal `~/.claude` and manual copy/paste fail the "every clone / CI runner" test (Q7, Q8, Q10).
- **Provenance & coverage are structural, not narrative.** Structured handoff records preserve attribution; coordinator planning ensures coverage. Never ask the synthesizer to re-derive what subagents already knew (Q6, Q13, Q18).
- **The longer, mechanism-rich answer usually wins.** Correct answers name concrete mechanisms ("force `extract_metadata` with `tool_choice`, then `auto`," "`.claude/rules/` topic files"); traps are vague ("reason carefully," "be conservative," "add stronger headings").

---

**Bottom line:** the agent lives in **unfamiliar legacy code**, so classify each scenario by **(1)** whether you should *explore/clarify before editing* (plan mode / clarifying questions), **(2)** whether refinement needs *concrete evidence* (tests, traces) instead of "be careful," **(3)** whether it's an *orchestration/provenance* problem (coordinator state + structured handoffs + planned coverage), or **(4)** a *config-scope* problem (committed project config vs personal/manual). The mechanism-rich option that designs before changing files and keeps shared context committed and scoped is almost always correct.
