# Code Generation with Claude Code — Answering Strategy

> A study cheat sheet for the **Code Generation with Claude Code** scenario, built from the 9 questions in [06-Code Generation with Claude Code.md](../06-Code%20Generation%20with%20Claude%20Code.md).
> Goal: read any scenario the right way so your answers stay accurate — even under exam time pressure.

---

## Step 1: Build the Mental Model Before Reading Any Question

Every question is set in the **same system**, so hold this setup and its goal in your head:

```
Claude Code accelerates development: code generation · refactoring · debugging · documentation

Workflow controls:
   plan mode            → explore deps & choose an approach BEFORE editing
   direct execution     → make the agreed mechanical edits
   custom slash commands / skills
   project CLAUDE.md     → committed, shared standards
   .claude/rules/*.md (+ YAML path globs) → load ONLY for matching files
   ~/.claude/CLAUDE.md   → per-user, NOT shared (the trap)

Multi-agent:  coordinator → search/scan subagents (ISOLATED context) → plan

Reliability themes: structured output · empty-vs-failure reporting ·
                    per-field calibrated confidence · segment-level validation

TARGET: integrate Claude Code into the dev workflow reliably across a monorepo.
```

Two facts drive most answers:

1. **Conventions defined by *file type*, not directory, belong in `.claude/rules/` with path globs.** When the same standards apply to files scattered across many folders (migrations, components, stories), root CLAUDE.md over-loads context, directory copies drift, and slash commands need someone to remember them — **path-scoped rules** load automatically for matching files with no upkeep.
2. **Aggregate confidence hides clustered risk; confidence must be calibrated before you trust it.** A 96% overall acceptance rate is inflated by easy README edits while the risky outputs (API schemas, rollback notes) cluster in the failures. Break results down **by segment/field**, attach **per-critical-field confidence**, and calibrate against labeled outcomes — never auto-approve on one global threshold.

The recurring tensions: **(a)** where shared/scoped config lives, **(b)** plan vs direct execution, **(c)** structured output and honest empty-vs-failure reporting, and **(d)** calibrated/segmented confidence vs a single global number.

---

## Step 2: The 4 Patterns (Quick Reference)

All 9 questions collapse into **4 patterns**. Read the symptom, match the row, pick the structural fix.

| Symptom in the scenario | Fix category | Questions |
|---|---|---|
| Same conventions copied into scattered folders → drift, missed new locations, or root file leaks into unrelated edits | **`.claude/rules/` file with YAML path globs** (file-type-scoped, auto-loading) | Q3, Q9 |
| Monorepo packages each own a standards doc that changes often; one giant root file | **Small package-level CLAUDE.md that `@import`s** the canonical docs; keep root minimal | Q7 |
| CI test/code suggestions are low-value because clean runners lack local context | **Commit project CLAUDE.md** with valuable-test criteria, fixtures, reusable helpers | Q6 |
| Multi-file change with two viable approaches & unknown wrappers | **Plan mode** to investigate & choose, **then direct execution** for the agreed edits | Q8 |

Plus the reliability cluster (one each):

- **Empty vs failure:** subagents must report "searched and found nothing" **separately** from "couldn't access the code," with attempted paths/queries/partial results/next steps — so the coordinator never treats an unscanned package as clean. (Q2)
- **Structured output:** emit JSON via `--output-format json` + `--json-schema` so the posting step has a stable contract, instead of regex over markdown. (Q1)
- **Segment-level validation:** break acceptance down by artifact category & field; reduce review only where data proves a segment reliable. (Q4)
- **Per-field calibrated confidence:** attach confidence to each critical field and calibrate routing thresholds against labeled past reviews — not one overall score. (Q5)

**The one rule behind all four:** *scope context by file type, design before editing multi-path changes, propagate failures honestly, and never trust an uncalibrated aggregate confidence number.*

---

## Detailed Symptom → Fix Reference (all 9)

| Symptom in the scenario | Fix | Questions |
|---|---|---|
| Inline-comment script fails on varying markdown/bullets/fences, missing severity labels | Run with **`--output-format json` + `--json-schema`** defining required finding fields | Q1 |
| Migration subagent hit a permission error returned as "no findings"; auth package never scanned | Report **successful empty searches separately from access failures** (paths, queries, partial results, next steps) | Q2 |
| Migration files scattered across service/package/importer folders; local files miss new locations, root leaks advice | **`.claude/rules/` migration file with path globs** matching all patterns | Q3 |
| 96% acceptance, but failures cluster in API schemas & rollback notes; leadership wants 0.9 cutoff | **Break validation down by artifact category & generated field**; reduce review only for reliable segments | Q4 |
| One overall confidence score; high-scoring records still miss rollback/security (highest-risk fields) | **Per-critical-field confidence**, calibrate routing thresholds on a labeled set | Q5 |
| Nightly CI test suggestions duplicate snapshots, ignore existing helpers/team rules; ephemeral runners | **Commit project CLAUDE.md** with valuable-test criteria, fixtures, reusable helpers | Q6 |
| Per-package standards docs change monthly; copied 900-line root file drifts & adds noise | **Package-level CLAUDE.md `@import`ing** canonical docs; minimal root | Q7 |
| Replace logging library across 18 packages; two viable paths, unknown wrappers, mechanical edits | **Plan mode** to investigate & choose, then **direct execution** for agreed edits | Q8 |
| Accessibility/Storybook conventions copied to several component dirs; drift, missed new folders | **Repository `.claude/rules/` file with YAML path globs** for component & story files; remove duplicated dir instructions | Q9 |

---

## Step 3: The "North Star" Principles

Every correct answer follows one of these. When two options look plausible, the one matching a north star wins:

1. **Scope conventions to the files they govern.** When standards are defined by file *type* and the files are scattered, use `.claude/rules/` with YAML path globs — automatic, targeted, no upkeep. (Q3, Q9)
2. **Keep per-area standards close to their owner and import the canonical source.** Package-level CLAUDE.md with `@import` beats one monolithic root file that drifts and over-loads context. (Q7)
3. **CI runs on clean runners — commit the context.** Project CLAUDE.md gives every ephemeral run the same repository knowledge a local developer would have. (Q6)
4. **Design before editing multi-path changes; then execute directly.** Plan mode for real uncertainty (multiple approaches, unknown wrappers), direct execution for the agreed mechanical edits. (Q8)
5. **Propagate failures with enough structured detail to act on.** "Found nothing" must be distinguishable from "couldn't access"; never collapse them into success. (Q2)
6. **Generate structured output at the source.** Schema-defined JSON, not regex cleanup of markdown afterward. (Q1)
7. **Aggregate accuracy hides clustered risk — validate by segment.** Reduce review only where labeled data proves a segment reliable. (Q4)
8. **Confidence must be validated, not just reported — and risk is per-field.** Attach confidence to each critical field and calibrate thresholds against labeled outcomes. (Q5)

---

## Step 4: Eliminate the Recurring Wrong-Answer Traps

These distractors appear in nearly every question. **Cross them out on sight** — they're correct answers ~0% of the time in this scenario:

- ❌ "Keep everything in **root CLAUDE.md** and tell Claude to ignore unrelated sections" → still loaded, still leaks advice into unrelated edits (Q3, Q7, Q9)
- ❌ "**Duplicate** identical CLAUDE.md files into every current directory and update manually" → drifts and misses new folders (Q3, Q7, Q9)
- ❌ "Put shared standards in **`~/.claude/CLAUDE.md`** / on the maintainer's laptop" → not shared through version control, invisible to CI (Q5-style, Q6, Q7)
- ❌ "Create a **slash command / skill the developer must remember** to invoke" for an always-on convention → manual step, drifts (Q3, Q9)
- ❌ "**Regex / split-by-heading** over markdown output" → brittle; emit schema JSON instead (Q1)
- ❌ "Treat **no code references as success**" / "kill the whole run on any scan failure" / "free-text failure summaries" → hides coverage gaps or discards good results (Q2)
- ❌ "Adopt the **global 0.9 / fixed overall threshold**, monitor incidents" → auto-approves exactly the segments reviewers reject (Q4, Q5)
- ❌ "Increase the **overall random sample size**, decide on combined acceptance" → just averages the weak spots away (Q4)
- ❌ "Force **coarse high/medium/low** confidence" → still meaningless until calibrated (Q5)
- ❌ "**Start direct execution**, let compile errors reveal wrappers" / "stay in plan mode and re-plan after every edit" / "separate session per package" → rework, wasted time, or lost shared context (Q8)
- ❌ "Add **'be conservative' / 'be careful'**" or "hide existing tests so Claude infers coverage" → vague; causes duplicate/mismatched suggestions (Q6)

---

## Step 5: The Decision Test (when down to two options)

1. **Is the convention defined by file type across scattered folders?** → **`.claude/rules/` with path globs.** Reject root-ignore, directory duplication, and manual commands. (Q3, Q9)
2. **Do per-area standards change independently?** → **Package-level CLAUDE.md `@import`ing** canonical docs. (Q7)
3. **Does CI need the context on clean runners?** → **Commit project CLAUDE.md.** Reject `~/.claude` and hidden tests. (Q6)
4. **Is the change multi-path with real uncertainty?** → **Plan mode, then direct execution.** Reject "let failures guide it" and per-package sessions. (Q8)
5. **Does it preserve failure information?** → Reject empty-as-success and free-text summaries; **structured empty-vs-failure**. (Q2)
6. **Is it about trusting confidence?** → **Segment/field-level + calibrated against labels**, never a single global number. (Q4, Q5)

---

## Exam-Specific Tactics

- **"Scattered files, same convention" → `.claude/rules/` path globs.** This is the dominant pattern here (Q3, Q9). The three decoys are always the same: root-CLAUDE.md-ignore, directory duplication, and a manual slash command/skill.
- **`@import` is the monorepo answer when per-area docs change often.** Q7 specifically rewards small package CLAUDE.md files that import canonical, maintainer-owned docs — not one 900-line root file.
- **CI = clean ephemeral runners → committed config.** Anything in `~/.claude` or on a laptop fails. Hiding existing tests to "infer coverage" backfires (Q6).
- **Plan mode is for uncertainty + blast radius; switch to direct execution once decided.** Q8's correct answer explicitly does both phases; staying in plan mode forever or starting direct both lose (Q8).
- **Confidence/validation questions reward calibration and granularity.** Break down by segment (Q4), attach per-field confidence and calibrate on labeled data (Q5); reject global thresholds, bigger pooled samples, and coarse labels.
- **Empty vs failure must be structurally distinct.** A scan that found nothing and a scan that couldn't run are different facts; collapsing them produces unsafe plans (Q2).
- **The longer, mechanism-rich answer usually wins.** Correct answers name concrete mechanisms ("`.claude/rules/` with YAML path globs," "per-field confidence calibrated on labeled reviews"); traps are vague ("be conservative," "monitor incidents," "ignore unrelated sections").

---

**Bottom line:** classify each scenario by **(1)** *config scope* — file-type-scattered → `.claude/rules/` globs, per-area → package CLAUDE.md `@import`, CI → committed project CLAUDE.md; **(2)** *workflow* — multi-path uncertainty → plan mode then direct execution; **(3)** *reliability* — honest empty-vs-failure reporting and structured output; **(4)** *trust* — segment/field-level calibrated confidence, never a global aggregate. The mechanism-rich option that scopes context automatically and validates confidence against labeled outcomes is almost always correct.
