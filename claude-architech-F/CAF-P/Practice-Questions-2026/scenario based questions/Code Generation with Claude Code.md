# Scenario: Code Generation with Claude Code

> You are using Claude Code to accelerate software development. Your team uses it for code generation, refactoring, debugging, and documentation. You need to integrate it into your development workflow with custom slash commands, CLAUDE.md configurations, and understand when to use plan mode vs direct execution.

Questions for this scenario, collected from Practice Tests 1-3 (Claude Certified Architect - Foundations, v2.0).

**Total questions: 9**

---

## Q1  ·  Set 2 Question 5

*Domain: Claude Code Configuration & Workflows*

**A CI review job already runs non-interactively and completes, but the script that posts inline pull request comments frequently fails because Claude's findings vary between markdown bullets, paragraphs, and code fences. Sometimes severity labels are missing or line ranges are formatted differently, so valid findings are dropped or posted to the wrong lines. What change would best make the review results reliable for automated consumption?**

**Options:**

- Post Claude’s entire text response as one pull request comment and ask developers to review manually.
- Use the -p flag alone and have the CI script split Claude’s response into sections by heading.
- **Run Claude Code with --output-format json and --json-schema defining required fields for each pull request finding.**  ✅
- Keep markdown output but add stricter prompt wording and regex patterns for severity, filename, and line extraction.

**Correct answer:** **Run Claude Code with --output-format json and --json-schema defining required fields for each pull request finding.**

**Explanation:**

JSON output with a schema gives the CI script a stable, machine-readable contract with predictable fields (file, line, severity, fix). The real problem is treating free-form text as the integration boundary. Posting one big comment gives up automation, splitting by headings or regex-parsing markdown stays brittle, and "be more consistent" prompting doesn't guarantee parseable output. Generate structured output at the source instead of cleaning it up afterward.

---

## Q2  ·  Set 2 Question 6

*Domain: Context Management & Reliability*

**Your /migrate-to-new-logger command uses a coordinator that launches subagents to scan packages and propose edits. In a dry run, the final plan says the legacy logger appears only in billing and notifications. Later, reviewers discover the auth package was never scanned because a subagent hit a path permission error, while the search subagent for reporting scanned successfully and found no matches. The coordinator received both results as "no findings." What change would most improve reliability of future migration plans?**

**Options:**

- Terminate the entire migration workflow whenever any package scan fails, discarding successful findings from other subagents.
- **Have subagents report successful empty searches separately from access failures, including attempted paths, queries, partial results, and suggested next steps.**  ✅
- Treat every subagent result with no code references as successful, then rely on reviewers to catch any missing packages.
- Ask each subagent to summarize failures in natural language, letting the coordinator infer whether missing findings indicate clean code.

**Correct answer:** **Have subagents report successful empty searches separately from access failures, including attempted paths, queries, partial results, and suggested next steps.**

**Explanation:**

Subagents must report "searched and found nothing" differently from "couldn't access the code." Only then can the coordinator retry, reroute, annotate a coverage gap, or escalate — instead of treating unscanned packages as clean. Returning empty-as-success hides the failure and produces unsafe plans; killing the whole run throws away good results from other subagents; free-text summaries force the coordinator to guess. The principle: propagate failures with enough structured detail to act on.

---

## Q3  ·  Set 2 Question 8

*Domain: Claude Code Configuration & Workflows*

**Your monorepo stores database migration files in several unrelated locations, including service folders, package folders, and an importer tool. All migration files must follow the same rollback, idempotency, and naming conventions. The team tried local instruction files near some migration folders, but new locations are frequently missed; placing the guidance in the root instructions makes Claude apply migration-specific advice during unrelated edits. What is the most maintainable configuration?**

**Options:**

- Put migration conventions in root CLAUDE.md and instruct Claude to ignore them when editing non-migration files.
- Create a migration skill that developers manually invoke before editing database files in each package.
- Duplicate identical CLAUDE.md files into every current migrations directory and update them manually as packages change.
- **Create a .claude/rules/ migration file with paths matching all migration patterns so guidance loads only for those files.**  ✅

**Correct answer:** **Create a .claude/rules/ migration file with paths matching all migration patterns so guidance loads only for those files.**

**Explanation:**

Because migration files are scattered across unrelated folders, put the guidance in a .claude/rules/ file with path globs so it loads only for matching files. Root CLAUDE.md applies everywhere and leaks migration advice into unrelated edits; directory-level files keep missing new locations; duplicated copies drift out of sync; a manual skill depends on someone remembering it. Path-scoped rules give automatic, targeted loading with no manual upkeep.

---

## Q4  ·  Set 2 Question 15

*Domain: Context Management & Reliability*

**A three-month pilot dashboard reports 96% reviewer acceptance for Claude Code generated artifacts. Review notes show most accepted outputs are README edits and changelogs, while rejected outputs cluster around OpenAPI response schemas and database migration rollback notes. Leadership wants to stop manual review for any output where Claude reports confidence above 0.9. What is the most reliable next step?**

**Options:**

- Adopt the 0.9 confidence threshold globally, then monitor incidents and re-enable review if production defects increase.
- **Break down validation results by artifact category and generated field, then reduce review only for consistently reliable segments.**  ✅
- Increase the overall random sample size for two more sprints, then decide using the combined acceptance rate.
- Require reviewers to check only low-confidence outputs, since high-confidence Claude Code results already passed aggregate evaluation.

**Correct answer:** **Break down validation results by artifact category and generated field, then reduce review only for consistently reliable segments.**

**Explanation:**

A 96% overall score hides that failures cluster in the risky outputs (API schemas, rollback notes), while easy README edits inflate the average. Break results down by artifact type and field, and stop review only where the data proves a segment is reliable. A global 0.9 cutoff would auto-approve the exact things reviewers reject, a bigger pooled sample just averages the weak spots away, and waiting for production defects is reactive. Confidence must be calibrated against labeled outcomes before you trust it.

---

## Q5  ·  Set 2 Question 18

*Domain: Context Management & Reliability*

**Your team added a custom review workflow that summarizes generated code changes into structured records containing modified files, test coverage, security impact, rollback risk, and reviewer recommendation. Each record currently has one overall confidence score. In pilot runs, high-scoring records often have accurate file lists and test summaries but occasionally miss rollback or security concerns, which are the highest-risk fields. What change would best support safe routing of low-risk records while preserving reviewer attention for uncertain areas?**

**Options:**

- Send every generated record to senior reviewers until the workflow reaches a stable overall accuracy percentage for one month.
- Reduce confidence variance by forcing Claude Code to output only high, medium, or low confidence for each record.
- **Require confidence per critical record field, then calibrate routing thresholds using a labeled set of previously reviewed changes.**  ✅
- Automatically approve records above a fixed overall confidence threshold after adding instructions to be conservative on risky changes.

**Correct answer:** **Require confidence per critical record field, then calibrate routing thresholds using a labeled set of previously reviewed changes.**

**Explanation:**

Different fields carry different risk, so attach a confidence score to each critical field and calibrate the routing thresholds against past labeled reviews — don't rely on one overall number. Accurate file lists shouldn't excuse missed rollback or security concerns. A single threshold can auto-approve the exact failures reviewers are catching; reviewing everything wastes capacity; and coarse high/medium/low labels still mean nothing until calibrated. The rule: confidence must be validated, not just reported.

---

## Q6  ·  Set 2 Question 24

*Domain: Claude Code Configuration & Workflows*

**Your nightly CI job asks Claude Code to propose tests for changed modules. Suggestions are consistently low value: duplicating brittle snapshots, mocking helpers your repository already provides, and ignoring team rules that prioritize behavior tests over implementation details. Developers run the job from ephemeral runners, so ad hoc local preferences are not present. What change would most effectively improve the quality and consistency of generated test suggestions?**

**Options:**

- **Commit project-level CLAUDE.md guidance describing valuable test criteria, fixture conventions, and reusable helpers for CI-invoked Claude Code.**  ✅
- Store preferred testing style in ~/.claude/CLAUDE.md on the maintainer's laptop and copy outputs into pull requests.
- Add a prompt line asking Claude to be conservative and avoid unnecessary tests whenever reviewing changed files in CI.
- Require developers to omit existing test files from CI context so Claude infers coverage needs from product code alone.

**Correct answer:** **Commit project-level CLAUDE.md guidance describing valuable test criteria, fixture conventions, and reusable helpers for CI-invoked Claude Code.**

**Explanation:**

CI runs on clean, ephemeral runners, so the guidance has to live in a committed project CLAUDE.md describing what makes a valuable test, fixture conventions, and reusable helpers. That gives every run the same repository context a local developer would have. "Be conservative" is too vague to teach standards, ~/.claude files aren't shared with CI or teammates, and hiding existing tests just causes duplicate and mismatched suggestions.

---

## Q7  ·  Set 2 Question 39

*Domain: Claude Code Configuration & Workflows*

**Your repository has separate frontend, backend, and data packages. Each package has a maintainer-owned standards document that changes monthly, and Claude Code currently receives a copied, 900-line root instruction file covering every package. Developers report inconsistent behavior because irrelevant conventions appear in context, and standards drift when copied sections are not updated. What is the most maintainable configuration change?**

**Options:**

- Move package standards into each developer's ~/.claude/CLAUDE.md so individual users can customize package guidance locally.
- Keep all standards in the root CLAUDE.md, adding stronger headings that tell Claude to ignore unrelated package sections.
- **Use small package-level CLAUDE.md files that reference the relevant standards documents with @import, keeping shared root guidance minimal.**  ✅
- Duplicate the current standards into every package subdirectory CLAUDE.md, and assign maintainers to update copied sections manually.

**Correct answer:** **Use small package-level CLAUDE.md files that reference the relevant standards documents with @import, keeping shared root guidance minimal.**

**Explanation:**

Each package has its own standards doc that changes monthly, so use small package-level CLAUDE.md files that @import the canonical docs and keep the root file minimal. One 900-line root file pushes irrelevant conventions into every edit and relies on Claude to filter them; copying standards into directories causes drift; user-level ~/.claude files aren't shared through version control. Imports keep guidance scoped, shared, and easy to maintain.

---

## Q8  ·  Set 2 Question 41

*Domain: Claude Code Configuration & Workflows*

**A developer asks Claude Code to replace a legacy logging library across 18 packages. There are two viable migration paths, several unknown wrapper modules, and likely mechanical edits after the team chooses one approach. What workflow best balances careful discovery with efficient implementation?**

**Options:**

- Use direct execution from the start, letting compile errors reveal hidden wrappers and adjusting the migration strategy afterward.
- Remain in plan mode for the entire task, requiring Claude to re-plan after every package-level edit before continuing.
- **Use plan mode to investigate dependencies and choose the migration path, then switch to direct execution for the agreed edits.**  ✅
- Split the task into separate direct-execution sessions per package, avoiding shared context so each migration stays locally focused.

**Correct answer:** **Use plan mode to investigate dependencies and choose the migration path, then switch to direct execution for the agreed edits.**

**Explanation:**

The task mixes real uncertainty (two viable paths, unknown wrapper modules) with mechanical edits, so use plan mode to investigate dependencies and pick the approach, then switch to direct execution for the agreed changes. Starting directly and letting compile errors reveal the architecture causes avoidable rework; staying in plan mode for every edit wastes time once the decision is made; and per-package sessions lose shared context and can miss common abstractions.

---

## Q9  ·  Set 2 Question 57

*Domain: Claude Code Configuration & Workflows*

**Your frontend repo has component files under src/ui, packages/admin/widgets, and legacy/screens. The same accessibility and Storybook conventions were copied into several local instruction files, but updates drift and Claude misses conventions when editing new component folders. What should you change?**

**Options:**

- Create a custom slash command for component generation that includes conventions, and ask developers to remember using it.
- **Create a repository rule file with YAML path globs matching component and story files, then remove duplicated directory instructions.**  ✅
- Put all component conventions in the root CLAUDE.md and tell Claude to apply only relevant sections.
- Add a CLAUDE.md file to every existing component directory and require maintainers to copy updates manually.

**Correct answer:** **Create a repository rule file with YAML path globs matching component and story files, then remove duplicated directory instructions.**

**Explanation:**

The accessibility and Storybook conventions apply to component and story files spread across several folders, so a .claude/rules/ file with YAML path globs loads them automatically for matching files — then remove the duplicated directory copies. Copies drift out of sync, a root CLAUDE.md over-loads context and depends on Claude filtering sections, and a slash command only helps when a developer remembers to run it. Use path-scoped rules for conventions defined by file type rather than directory.

---
