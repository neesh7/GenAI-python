# Claude Code for Continuous Integration — Answering Strategy

> A study cheat sheet for the **Claude Code for Continuous Integration** scenario, built from the 30 questions in [05-Claude Code for Continuous Integration.md](../05-Claude%20Code%20for%20Continuous%20Integration.md).
> Goal: read any scenario the right way so your answers stay accurate — even under exam time pressure (3 sets × ~20 questions).

---

## Step 1: Build the Mental Model Before Reading Any Question

Every question is set in the **same system**, so hold this pipeline and its goal in your head:

```
CI/CD pipeline
  └── Claude Code (non-interactive, -p/--print) reviews each PR
        ├── extract PR metadata  (tool_use)
        ├── generate review findings (tool_use → JSON schema)
        └── generate / gap-check tests
              │
              ▼
        Semantic validation  (line in diff? file in diff? severity justified? consistent?)
              │
              ▼
        Post inline PR comments  (needs a stable machine-readable contract)

Config that shapes behavior:
   project CLAUDE.md          → universal, always-on review principles
   .claude/rules/*.md (+ YAML paths globs) → load ONLY for matching changed files
   .claude/commands/*.md      → reusable invokable workflows (committed)
   .claude/skills/.../SKILL.md → packaged workflows; argument-hint, allowed-tools, context: fork
   ~/.claude/...              → per-user, NOT shared with CI (the trap)

TARGET: actionable feedback, minimal false positives, reliable automation on clean runners.
```

Two facts drive most answers:

1. **CI runs on clean, ephemeral runners with no human present.** So Claude must run **non-interactively (`-p`/`--print`)** or it hangs until timeout, and all guidance/commands/skills must be **committed to the repo** — anything in `~/.claude` or a personal home dir fails for fresh checkouts and runners.
2. **The integration is an automation contract, not prose.** Findings must be **structured JSON via tool_use/schema**, and schema-valid ≠ trustworthy — add **semantic validation** (line in diff, severity justified, internal consistency) before posting. False positives are the dominant failure: fix them with **concrete reportable/skip criteria + examples**, never "be conservative."

The four recurring levers: **(a)** non-interactive execution, **(b)** structured output + semantic validation, **(c)** precision via concrete criteria/examples (not vague caution or confidence scores), and **(d)** conditional/scoped context loading (`.claude/rules/` globs, skills, `context: fork`).

---

## Step 2: The 8 Patterns (Quick Reference)

All 30 questions collapse into **8 patterns**. Read the symptom, match the row, pick the structural fix.

| Symptom in the scenario | Fix category | Questions |
|---|---|---|
| CI command **hangs until timeout** (works in a terminal) | Run **`-p`/`--print`** non-interactive mode | Q17, Q28 |
| Inline-comment step breaks on markdown/bullets/renamed fields | **Structured JSON via tool_use + schema** as the contract | Q22 (and Q1, Q3, Q10 build on it) |
| Schema-valid findings still cite **lines outside the diff / wrong severity / contradictions** | **Semantic validation** against diff metadata + severity rules + consistency, then retry | Q1, Q3 |
| Required field (owner/ticket/evidence) **fabricated** when source absent | **Nullable/optional** source-dependent fields; **classify** missing-source vs correctable failures | Q14, Q30 |
| Reviewer is **noisy / speculative** ("might be slow", style nits); devs dismiss & tune out | **Concrete reportable & non-reportable criteria + severity defs + examples**; report bugs/security/test-gaps, skip undocumented style | Q7, Q9, Q16, Q20, Q24, Q27 |
| Test suggestions **duplicate existing coverage** | **Pass relevant existing test files**; target only uncovered behaviors | Q4 |
| Shared guidance fires on **irrelevant PRs** (docs/CSS/TS) → noise + tokens | **`.claude/rules/` with YAML `paths` globs** → load only for matching files | Q2, Q8, Q12, Q15, Q18, Q25 |
| Verbose setup/exploration **pollutes the final review** context | **Skill with `context: fork`** or an **Explore subagent** returning a concise summary | Q23, Q24, Q26 |

Plus four targeted calls:

- **Same session writes then reviews → blind spots:** run review as a **separate invocation** with diff + criteria only. (Q6)
- **Findings generated before metadata:** **force the metadata tool with `tool_choice`** on the first request, findings in a follow-up turn. (Q10)
- **Underspecified review criteria:** **interview-style refinement** — Claude asks maintainers targeted questions, fold answers into the prompt. (Q13)
- **Diagnose dismissals:** add a **structured "triggering code pattern" field**, analyze dismissal rates by it. (Q29)
- **Reusable workflow packaging:** **project skill** (`.claude/skills/`, argument-hint, allowed-tools) or **committed `.claude/commands/`**, never `~/.claude`. (Q5, Q11)

**The one rule behind all eight:** *make CI deterministic — non-interactive execution, structured output validated for meaning, precision from concrete criteria not caution, and context that loads only when relevant.*

---

## Detailed Symptom → Fix Reference (all 30)

| Symptom in the scenario | Fix | Questions |
|---|---|---|
| Schema passes but finding cites line 220 in a 90-line file / file not in diff / snippet in wrong field | Keep tool_use schema + **deterministic checks (line range, file-in-diff, placement)**, retry with errors | Q1 |
| Accessibility guidance flags backend handlers because it loads every review | **`.claude/rules/`** file with YAML `paths` globs for React components | Q2 |
| Findings reference lines outside diff / test-only as blocker / contradictory remediation | Keep structured output + **semantic validation** vs diff metadata, severity rules, consistency | Q3 |
| Test suggestions duplicate empty-cart/expired-token cases | **Pass current test files** into context; target only uncovered behaviors | Q4 |
| Repeated pre-PR test-gap analysis needs checklist, prompts for target, limited tools | **Project skill** in `.claude/skills/` with argument-hint + allowed-tools | Q5 |
| Generate-then-review in the same conversation trusts its own assumptions | **Separate Claude Code invocation** with diff + repo context + criteria only | Q6 |
| Speculative findings; "be conservative / high-confidence only" hasn't worked | **Concrete reportable/non-reportable categories, severity defs, code examples** | Q7, Q9, Q16, Q27 |
| Migration checklist warns on TS-only PRs; migrations under two glob patterns | **Rule file with YAML `paths`** for both migration globs | Q8 |
| Reviews drown in naming/import/refactor nits, burying correctness issues | Rewrite prompt: report **bugs/security/test-gaps**, skip undocumented style | Q9 |
| On docs-heavy PRs `generate_review_findings` runs before metadata | **Force `extract_pr_metadata` with `tool_choice`** first, findings in follow-up turn | Q10 |
| `/pr-feedback` works on a laptop but "command not found" on runners | **Commit command markdown under `.claude/commands/`** | Q11 |
| Docs/CSS PRs still get backend/API/migration rules → noise + tokens | **`.claude/rules/` YAML globs** load only relevant rules | Q12, Q15 |
| Migration review misses rollback/retention/compat; criteria undefined | **Interview-style refinement**; fold clarified criteria into the CI prompt | Q13 |
| Required `owner_team`/`linked_ticket` invented when PR lacks them | **Nullable/optional** source-dependent fields; return null unless evidenced | Q14 |
| 1,200-line root CLAUDE.md blends standards, causes conflicting edits | Move scoped guidance to **`.claude/rules/`**, keep only universal principles in root | Q17(codegen-style), Q18 |
| `claude "Review..."` stalls until CI timeout (works in terminal) | Run with **`-p`/`--print`** | Q17, Q28 |
| Bot flags safe null checks / ordinary retries; swapped vague phrase for vague phrase | **Concrete report/skip criteria per category + true-positive & non-issue examples** | Q16 |
| Coverage gen misses null/timezone/duplicate cases; "be more thorough" inconsistent | **Targeted test suite first**, iterate on specific failing results | Q19 |
| Flags branches already covered by table-driven/shared-fixture tests | **Targeted examples** of existing test structures vs genuine gaps, with reasoning | Q20, Q24 |
| Posting breaks on markdown tables/bullets, inconsistent field names | **Emit structured JSON matching a schema** with required inline-comment fields | Q22 |
| Setup-phase exploratory notes leak into main review | **Skill with `context: fork`** → isolated discovery, concise summary | Q23, Q24 |
| Verbose ownership/call-path/test discovery crowds the session | **Explore subagent** returns concise findings before structured comments | Q26 |
| Specialized CI workflows (security/release/migration) noisy on simple PRs | Universal principles in CLAUDE.md; **specialized workflows as project skills** | Q21 |
| Speculative perf findings ("this loop might be slow") dismissed | **Reportable evidence thresholds** (unbounded growth, hot path, DB calls in loops) | Q27 |
| Dashboard only shows broad categories → unfocused prompt iteration | Add **structured "triggering code pattern" field**; analyze dismissal by it | Q29 |
| `breaking_change_evidence` null because baseline/contract not in CI context | **Classify missing-baseline separately**, retry only format errors, **add the baseline artifact** | Q30 |

---

## Step 3: The "North Star" Principles

Every correct answer follows one of these. When two options look plausible, the one matching a north star wins:

1. **CI is non-interactive — use `-p`/`--print`.** A hang-until-timeout that "works in a terminal" is always the interactive-mode bug. (Q17, Q28)
2. **Treat output as an automation contract.** Structured JSON via tool_use/schema, not regex over markdown, label policing, or one big comment. (Q22, Q1, Q3, Q10)
3. **Schema-valid ≠ trustworthy — validate meaning before posting.** Deterministic checks against diff metadata, severity rules, and finding consistency; retry with the specific errors. (Q1, Q3)
4. **Precision comes from concrete criteria and examples, not caution.** Define reportable vs non-reportable categories, severity definitions, evidence thresholds, and true-positive/non-issue examples. (Q7, Q9, Q16, Q20, Q24, Q27)
5. **Let the schema represent absent evidence; classify failure types.** Nullable/optional source-dependent fields, return null unless evidenced; separate missing-baseline gaps from correctable format errors. (Q14, Q30)
6. **Ground the review in the artifacts needed to judge it.** Pass existing test files to detect coverage; add the baseline artifact for breaking-change checks. (Q4, Q30)
7. **Load context conditionally by path.** `.claude/rules/` with YAML `paths` globs so guidance fires only for matching changed files. (Q2, Q8, Q12, Q15, Q18, Q25)
8. **Isolate verbose exploration from the final-judgment context.** `context: fork` skills or an Explore subagent return a concise summary; don't rely on `/compact` after the fact. (Q23, Q24, Q26)
9. **Generation and review are different roles — isolate them.** Separate invocation with diff + criteria only; no self-review or majority voting. (Q6)
10. **Match the mechanism to scope and trigger.** Universal/always-on → project CLAUDE.md; path-triggered → `.claude/rules/`; on-demand reusable workflow → committed `.claude/commands/` or project skill; force a true prerequisite → `tool_choice`. (Q5, Q11, Q21, Q10)

---

## Step 4: Eliminate the Recurring Wrong-Answer Traps

These distractors appear in nearly every question. **Cross them out on sight** — they're correct answers ~0% of the time in this scenario:

- ❌ "Add **`--output-format json`** to fix a hang" / "redirect stdin from /dev/null" / "tell Claude to avoid follow-up questions" → the fix for hanging is **`-p`/`--print`** (Q17, Q28)
- ❌ "**Regex / parser** over every markdown table & bullet variant" / "police identical labels" → brittle; emit schema JSON at the source (Q22, Q1)
- ❌ "Make **every field required**" / "infer the value from naming conventions" → forces fabrication when the source lacks it (Q1, Q3, Q14, Q30)
- ❌ "Reject findings missing routing metadata" → hides valid issues (Q14)
- ❌ "**Be conservative / extremely conservative / be exhaustive**" (even twice in the prompt) → no decision boundary (Q7, Q9, Q16, Q27, Q13)
- ❌ "Require a **self-reported confidence score**, suppress below threshold (8/10, 9/10, 95%)" → uncalibrated, not a real control (Q7, Q9, Q16, Q19, Q27, Q29)
- ❌ "Run the broad prompt 3× and **report findings appearing twice**" → keeps blind spots, drops valid single-pass findings (Q6, Q7)
- ❌ "Keep everything in **root CLAUDE.md** and tell Claude to ignore irrelevant sections" → still loaded, still noisy (Q2, Q8, Q12, Q15, Q18)
- ❌ "**Duplicate** guidance into directory-level CLAUDE.md files" → drifts and misses new folders (Q8, Q15, Q25)
- ❌ "**Slash command that CI must select** by filename" / "split CI jobs per language" → external routing logic, breaks on mixed PRs (Q2, Q8, Q12, Q15, Q25)
- ❌ "Put it in **`~/.claude/`** (skills/commands/CLAUDE.md)" → not shared with clean runners or new contributors (Q5, Q11, Q21)
- ❌ "Run the **review in the same generating session**" / add skeptical instructions / ask for its rationale → biased context (Q6)
- ❌ "`tool_choice: any`" / "`auto` + stronger prompt" / "parse text for 'metadata complete'" → doesn't force the *right* tool (Q10)
- ❌ "Rely on **`/compact`** after verbose output crowds the session" → reactive, after the damage (Q23, Q26)
- ❌ "**Don't repeat coverage** rule while still sending only the diff" / "generate a full replacement suite" → can't verify without the tests; causes churn (Q4)
- ❌ "**Same-directory filename** / fixed test-count rules" → ignore how real suites are organized (Q20, Q24)
- ❌ "Accept high-confidence findings **without evidence** and let devs dismiss" → erodes trust, makes devs the filter (Q9, Q30)
- ❌ "Parse dismissals for **sentiment**" / weekly **natural-language summaries** for diagnosis → weaker than structured metadata (Q29)

---

## Step 5: The Decision Test (when down to two options)

1. **Does the job hang / stall in CI?** → **`-p`/`--print`**. Reject JSON-flags, stdin redirects, and prompt wording. (Q17, Q28)
2. **Is the posting/integration breaking on format?** → **Structured JSON via schema** at the source. Reject regex and label policing. (Q22)
3. **Is it schema-valid but wrong-in-meaning?** → **Semantic validation** vs diff + severity + consistency, then retry. (Q1, Q3)
4. **Is the reviewer noisy/speculative?** → **Concrete report/skip criteria + examples / evidence thresholds.** Reject "be conservative" and confidence scores. (Q7, Q9, Q16, Q20, Q24, Q27)
5. **Is guidance firing on irrelevant PRs?** → **`.claude/rules/` with `paths` globs.** Reject root-CLAUDE.md-ignore, duplication, and CI routing. (Q2, Q8, Q12, Q15, Q25)
6. **Is verbose setup polluting the review?** → **`context: fork` skill / Explore subagent.** Reject `/compact`. (Q23, Q24, Q26)
7. **Does shared config reach clean runners?** → **Committed `.claude/...`**, never `~/.claude`. (Q5, Q11, Q21)

---

## Exam-Specific Tactics

- **Hang in CI = `-p`/`--print`, every time.** The stem always says "works in a terminal" — that's the tell for interactive-by-default. Other "fixes" (JSON flags, stdin, prompt wording) are decoys (Q17, Q28).
- **"Schema vs semantic" recurs constantly.** A schema proves shape; it can't prove a line is in the diff or a severity is justified. When the stem says "always passes JSON validation but…," pick **semantic validation + retry**, not more required fields or lower temperature (Q1, Q3).
- **Precision is the #1 theme — and "be conservative" is the #1 trap.** Multiple questions show vague caution and self-reported confidence already failing; the answer is concrete **reportable/non-reportable categories, severity definitions, evidence thresholds, and examples** (Q7, Q9, Q16, Q20, Q24, Q27).
- **Context-loading questions → `.claude/rules/` with `paths` globs.** Six near-identical questions. The pattern: root CLAUDE.md loads everything, directory copies drift, slash commands need routing → **path-scoped rules** win (Q2, Q8, Q12, Q15, Q18, Q25).
- **Verbose-exploration-pollution → `context: fork` or Explore subagent.** When a setup/discovery phase floods the session and the final review degrades, isolate it; `/compact` is reactive and an anti-pattern (Q23, Q24, Q26).
- **Scope = collaboration boundary.** Anything personal (`~/.claude`) fails clean runners; always-on universal → CLAUDE.md; reusable on-demand → committed command or **project skill** with argument-hint/allowed-tools (Q5, Q11, Q21).
- **Fabrication vs gap.** Missing routing/evidence fields → **nullable + return null unless evidenced**; missing baseline artifact → **classify separately and add the artifact**, don't retry or infer (Q14, Q30).
- **The longer, mechanism-rich answer usually wins.** Correct answers name concrete mechanisms ("YAML `paths` globs," "`context: fork`," "force `extract_pr_metadata` with `tool_choice`"); traps are vague ("be conservative," "be thorough," "add stronger headings").

---

**Bottom line:** CI is **deterministic, headless, and shared**. Classify each scenario by **(1)** execution (hang → `-p`), **(2)** output contract (format breakage → schema JSON; valid-but-wrong → semantic validation), **(3)** precision (noise → concrete criteria/examples, never caution or confidence scores), **(4)** context loading (irrelevant firing → `.claude/rules/` globs; pollution → `context: fork`), and **(5)** scope (must reach clean runners → committed config). The mechanism-rich option that makes CI deterministic and loads context only when relevant is almost always correct.
