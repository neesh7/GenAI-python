# Scenario: Developer Productivity with Claude

> You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks. It uses built-in tools (Read, Write, Bash, Grep, Glob) and integrates with MCP servers.

Questions for this scenario, collected from Practice Tests 1-3 (Claude Certified Architect - Foundations, v2.0).

**Total questions: 20**

---

## Q1  ·  Set 1 Question 4

*Domain: Tool Design & MCP Integration*

**A team asks the agent to update every test fixture file ending in `.fixture.json` across a monorepo before reading only those files. In trials, the agent searches for the word "fixture" in file contents, producing noisy matches from comments and missing fixture files with sparse content. Which tool-use strategy should you adopt?**

**Options:**

- Use Read on all files under likely folders first, then recursively inspect contents until every fixture candidate is discovered.
- **Use Glob with patterns like `**/*.fixture.json` to enumerate matching paths, then Read only the files that require inspection.**  ✅
- Use Bash to run find and ls pipelines, then paste the complete directory listing into the conversation.
- Use Grep for the word fixture across the repository, then ask Claude to infer which results are fixture files.

**Correct answer:** **Use Glob with patterns like `**/*.fixture.json` to enumerate matching paths, then Read only the files that require inspection.**

**Explanation:**

The task is to find files by name and extension, so Glob with a pattern like `**/*.fixture.json` returns the matching paths directly, and the agent then Reads only those files. Grep searches file contents, so it produces noisy matches from comments and misses fixture files that don't contain the word. Reading whole folders or shelling out through Bash just wastes context. Match the tool to the search type: paths to Glob, contents to Grep.

---

## Q2  ·  Set 1 Question 5

*Domain: Claude Code Configuration & Workflows*

**Your team added a CI step that reviews code produced by an internal Claude-powered scaffolding workflow. The review job currently resumes the same named Claude session that generated the branch, then asks it to critique the resulting pull request. Human reviewers report that the automated review misses subtle design issues and often defends choices made during generation. What change would most improve review quality?**

**Options:**

- Ask the generating session to perform three consecutive review passes and report only issues found twice.
- **Run the review in a separate Claude Code invocation with the PR diff, repository context, and review criteria only.**  ✅
- Keep the existing session but add instructions requiring Claude to challenge its prior assumptions before approving changes.
- Resume the generation session after tests complete, then provide failing logs before requesting final review feedback.

**Correct answer:** **Run the review in a separate Claude Code invocation with the PR diff, repository context, and review criteria only.**

**Explanation:**

A session that wrote the code carries its own justifications and is unlikely to question them, so run the review as a fresh Claude Code invocation given only the PR diff, repo context, and review criteria. Repeated passes in the same session create fake rigor, and "report only issues found twice" can hide subtle bugs; skeptical instructions still keep the biased context; test logs help fixing, not independent review. Generation and review are different roles, so isolate them.

---

## Q3  ·  Set 1 Question 7

*Domain: Claude Code Configuration & Workflows*

**A team has built a Claude-powered helper that updates legacy configuration files to a new format. Initial generations look reasonable in code review, but repeated runs keep breaking different corner cases: missing optional sections, duplicate keys, and large files with thousands of entries. Developers have been sending follow-up prompts like "fix the migration bugs" and receiving inconsistent improvements. What refinement approach should they use next?**

**Options:**

- Tell Claude the output is still wrong, request a more careful implementation, and continue until reviewers approve it.
- **Share the failing test names, inputs, expected versus actual outputs, and stack traces, then iterate on minimal fixes.**  ✅
- Ask Claude to reread the entire legacy codebase and rewrite the migration helper from scratch after each failed run.
- Remove the most difficult corner-case checks temporarily so Claude can stabilize the happy-path migration behavior first.

**Correct answer:** **Share the failing test names, inputs, expected versus actual outputs, and stack traces, then iterate on minimal fixes.**

**Explanation:**

"Fix the migration bugs" is too vague to converge on a fix. Give Claude the failing test names, inputs, expected versus actual output, and stack traces, then iterate on small targeted changes. Rewriting from scratch after each failure throws away progress and risks new regressions, and removing the hard corner-case tests hides the exact cases that need fixing. Anchor each refinement in concrete, reproducible evidence rather than impressions like "be more careful."

---

## Q4  ·  Set 1 Question 9

*Domain: Claude Code Configuration & Workflows*

**An engineer asks the agent to add a caching layer around a legacy authorization module. The codebase has multiple tenants, audit logging, and inconsistent invalidation behavior, and the team has little domain knowledge. Past attempts produced working code that later failed on stale permissions and compliance edge cases. What should the engineer do before asking Claude to modify files?**

**Options:**

- Ask Claude to implement the simplest cache wrapper immediately, then iterate only if tests or reviewers expose issues.
- Provide a long prose description of desired performance goals and let Claude infer domain rules from surrounding code.
- **Have Claude first ask targeted questions about invariants, invalidation triggers, audit requirements, and failure modes before proposing implementation.**  ✅
- Tell Claude to copy caching patterns from a different module, assuming consistency across legacy authorization and unrelated services.

**Correct answer:** **Have Claude first ask targeted questions about invariants, invalidation triggers, audit requirements, and failure modes before proposing implementation.**

**Explanation:**

The domain is risky and poorly understood (multiple tenants, audit logging, inconsistent invalidation), so have Claude ask targeted questions about invariants, invalidation triggers, audit requirements, and failure modes before writing code. Jumping straight to a cache wrapper and waiting for reviewers or tests misses constraints that never appear in the first failing test; prose performance goals and copied patterns just make Claude guess domain rules. Refinement also means fixing the problem definition before implementation.

---

## Q5  ·  Set 1 Question 11

*Domain: Claude Code Configuration & Workflows*

**A team asks the productivity agent to add a "cancel renewal" workflow to a legacy subscription service. The initial implementation point is unclear because cancellation behavior appears split across command-line scripts, web handlers, and scheduled jobs. In earlier similar tasks, immediate edits repeatedly targeted the wrong abstraction and had to be rolled back after tests exposed broken shared behavior. Which workflow should the tool recommend first?**

**Options:**

- Proceed with direct execution, relying on test failures to reveal hidden dependencies and guide successive corrective edits.
- Instruct Claude to read every repository file first, then implement changes in the same extended session.
- **Use plan mode to map relevant flows and compare implementation points before allowing file modifications.**  ✅
- Start separate direct-execution sessions for each suspected module, then manually combine the resulting edits later.

**Correct answer:** **Use plan mode to map relevant flows and compare implementation points before allowing file modifications.**

**Explanation:**

Cancellation logic is spread across CLI scripts, web handlers, and scheduled jobs, and earlier direct edits hit the wrong abstraction and had to be rolled back. Use plan mode to map the flows and compare entry points before any files change. Letting test failures find the right abstraction is trial-and-error, reading every file overloads context, and separate per-module sessions edit without a shared design. A small upfront exploration cost prevents expensive rework in unfamiliar legacy code.

---

## Q6  ·  Set 1 Question 13

*Domain: Agentic Architecture & Orchestration*

**During a legacy billing-module analysis, a coordinator launches separate subagents to trace API handlers, database writes, and scheduled jobs. Each subagent returns useful narrative findings, but the final architecture brief often attaches claims to the wrong file or omits the line ranges engineers need for verification. What change best improves handoff reliability between the subagents and the final synthesizer?**

**Options:**

- **Require each subagent to return structured handoff records separating findings, file paths, symbols, line ranges, and evidence snippets.**  ✅
- Have the coordinator concatenate complete subagent transcripts so the synthesizer can search them for relevant provenance details.
- Add instructions asking the synthesizer to reconstruct file locations and line numbers from the subagents' narrative summaries.
- Apply regex parsing to subagent prose summaries, extracting anything that resembles a path, symbol, or citation.

**Correct answer:** **Require each subagent to return structured handoff records separating findings, file paths, symbols, line ranges, and evidence snippets.**

**Explanation:**

Findings get misattributed because subagents hand off free-form prose. Require each subagent to return structured records that keep the claim separate from its file path, symbol, line range, and evidence snippet, so the synthesizer can merge results while preserving attribution. Asking the synthesizer to reconstruct lost locations can't recover them reliably, concatenating full transcripts wastes context, and regex over prose is brittle. Subagents have isolated context, so provenance must be passed explicitly, not inferred.

---

## Q7  ·  Set 1 Question 14

*Domain: Claude Code Configuration & Workflows*

**Your repository's root CLAUDE.md has grown to 1,200 lines covering testing, API conventions, migration rules, deployment checks, and review norms. Engineers complain that small standards changes cause frequent merge conflicts, and Claude sometimes appears distracted by unrelated guidance. The team wants shared, version-controlled instructions, but needs a more maintainable layout without relying on developers to remember extra steps. What should you do?**

**Options:**

- Keep one root CLAUDE.md and add stronger section headings telling Claude to consult only relevant parts.
- Create slash commands for each standards topic and ask engineers to invoke the right command before coding.
- Move the shared standards into ~/.claude/CLAUDE.md so each engineer loads the same instructions outside repository files.
- **Split the guidance into focused topic files under .claude/rules/, such as testing.md, api-conventions.md, and deployment.md.**  ✅

**Correct answer:** **Split the guidance into focused topic files under .claude/rules/, such as testing.md, api-conventions.md, and deployment.md.**

**Explanation:**

One 1,200-line shared file causes merge conflicts and distracts Claude with unrelated guidance. Split it into focused topic files under .claude/rules/ (testing.md, api-conventions.md, deployment.md) so each concern evolves independently and stays version-controlled. Moving it to ~/.claude/CLAUDE.md breaks team sharing because that file is per-user; stronger headings just preserve the monolith; slash commands need manual invocation and don't fit always-on standards. Organize persistent project context by concern.

---

## Q8  ·  Set 1 Question 17

*Domain: Claude Code Configuration & Workflows*

**A senior engineer reports that Claude Code consistently follows your team's codebase exploration notes, legacy module warnings, and boilerplate conventions. New engineers who clone the repository see generic behavior instead, and no repository files changed when the senior engineer originally added those notes. What is the most effective way to make this guidance consistent for the team?**

**Options:**

- Create a slash command that reminds Claude to apply the conventions whenever developers remember to invoke it.
- Paste the conventions into the first prompt of each new session instead of changing repository configuration files.
- **Move the shared conventions into a project-level CLAUDE.md file and commit it so every clone loads them.**  ✅
- Ask each developer to copy the senior engineer’s personal memory file into their home directory before using Claude Code.

**Correct answer:** **Move the shared conventions into a project-level CLAUDE.md file and commit it so every clone loads them.**

**Explanation:**

The guidance loads for the senior engineer but not for new clones, and no repo files changed, which means it was saved to personal user-level memory rather than the repository. Move the conventions into a committed project-level CLAUDE.md so every clone loads them automatically. Slash commands, pasting at session start, or copying a personal memory file all depend on each developer remembering a manual step and will drift. Team standards belong in version-controlled project configuration.

---

## Q9  ·  Set 1 Question 22

*Domain: Claude Code Configuration & Workflows*

**Your internal agent is generating repository-specific data adapter classes from interface definitions. In pilots, the first drafts compile, but later reviews find unhandled null fields, incorrect retry behavior, and slow processing on large fixtures. Engineers can state expected outcomes and edge cases before implementation, but prose-only instructions have produced uneven results. Which workflow should you add?**

**Options:**

- Let Claude implement the adapter, then rely on manual code review to catch missed cases after generation.
- Give Claude a longer prose specification and ask it to reason carefully before producing the complete implementation.
- **Create tests for expected behavior, edge cases, and performance constraints first, then iterate by sending Claude failing results.**  ✅
- Run the generated code once on a representative happy-path input, then approve if the output matches.

**Correct answer:** **Create tests for expected behavior, edge cases, and performance constraints first, then iterate by sending Claude failing results.**

**Explanation:**

Engineers can state expected behavior and edge cases, but prose alone gives uneven results, so write tests for behavior, edge cases, and performance first and then feed failing results back to Claude. That turns vague quality into concrete targets like a null-field assertion or a performance threshold. Longer prose specs still rely on interpretation, manual review is slow and reactive, and a single happy-path run skips exactly the null, retry, and scale cases that fail. Convert requirements into executable acceptance criteria.

---

## Q10  ·  Set 1 Question 24

*Domain: Claude Code Configuration & Workflows*

**In your CI pipeline, a Claude Code job proposes unit tests for pull requests touching legacy modules. Developers report that many suggestions are superficial, duplicate scenarios already covered elsewhere, or ignore reusable factories and fixtures described only in scattered onboarding notes. What change would most effectively improve the usefulness of generated tests across the team?**

**Options:**

- Move test generation into a personal command so each engineer can tune prompts for their preferred style.
- **Document team testing standards, high-value test criteria, and reusable fixtures in project CLAUDE.md consumed by the CI job.**  ✅
- Increase the requested number of tests per file so Claude explores more scenarios before selecting final suggestions.
- Add a post-processing script that rejects generated tests containing duplicate names or assertions under five lines.

**Correct answer:** **Document team testing standards, high-value test criteria, and reusable fixtures in project CLAUDE.md consumed by the CI job.**

**Explanation:**

The suggestions are shallow and duplicate existing coverage because Claude lacks the team's testing standards and fixture knowledge. Document valuable-test criteria, fixture conventions, and reusable helpers in a project CLAUDE.md that the CI job reads, so every run gets the same repository context. Personal commands aren't shared with CI or teammates, asking for more tests adds volume not value, and syntactic dedup filters miss semantic duplicates while rejecting good short tests.

---

## Q11  ·  Set 1 Question 26

*Domain: Claude Code Configuration & Workflows*

**Engineers often ask the agent to generate new scheduled jobs with brief prompts like "add cleanup for expired sessions." The generated code compiles, but reviewers repeatedly find missing decisions around idempotency, tenant scoping, observability naming, data retention exceptions, and operational rollback. These requirements vary across teams and are not reliably documented in one place. What refinement approach should you apply before the agent begins implementation?**

**Options:**

- Add a global CLAUDE.md instruction requiring all scheduled jobs to handle every possible edge case conservatively.
- Ask Claude to implement only the simplest cleanup path first, then rely on code review to discover missing requirements.
- Tell Claude to infer the missing conventions from nearby scheduled jobs and implement the most common observed pattern.
- **Have Claude ask targeted clarification questions about operational constraints, ownership assumptions, and edge cases before proposing implementation changes.**  ✅

**Correct answer:** **Have Claude ask targeted clarification questions about operational constraints, ownership assumptions, and edge cases before proposing implementation changes.**

**Explanation:**

The decisions reviewers keep finding missing (idempotency, tenant scoping, retention, rollback) vary by team and aren't documented anywhere, so have Claude ask targeted clarification questions before implementing. A vague global "handle every edge case" rule can't supply team-specific answers, inferring from nearby jobs copies possibly-wrong assumptions, and relying on code review to surface gaps just creates rework. For ambiguous tasks, refinement should start by improving the problem definition.

---

## Q12  ·  Set 1 Question 28

*Domain: Claude Code Configuration & Workflows*

**Your CI job already invokes Claude Code successfully and posts a single pull request summary comment. The team now wants automated inline comments for each finding, but the integration frequently breaks because Claude sometimes adds prose, changes field names, or formats findings as markdown. What change best supports reliable automation?**

**Options:**

- Parse Claude's markdown bullets with regular expressions, adding patterns as new review formats appear in CI logs.
- Store the prior summary comment and ask Claude to rewrite it into comment-ready records on a second pass.
- **Run Claude Code with --output-format json and --json-schema, then map validated findings to inline PR comments.**  ✅
- Strengthen the review prompt to demand valid JSON only, then reject responses containing markdown or explanatory text.

**Correct answer:** **Run Claude Code with --output-format json and --json-schema, then map validated findings to inline PR comments.**

**Explanation:**

The integration breaks because it depends on Claude's prose and markdown formatting. Run Claude Code with --output-format json and --json-schema so the pipeline receives predictable fields to validate and map to inline comments. Regex over markdown is brittle, a second normalization pass adds cost while still relying on model formatting, and "demand JSON then reject bad output" pushes the problem into CI failure handling. Define the interface with a schema at the source instead of cleaning up afterward.

---

## Q13  ·  Set 1 Question 30

*Domain: Agentic Architecture & Orchestration*

**A coordinator agent delegates codebase exploration to subagents before asking an implementation subagent to generate migration scaffolding. In reviews, engineers find the final proposal often mixes findings from different packages, cites helper functions without file locations, and cannot explain which search result or source file supports a recommended change. The individual subagents found useful facts, but their handoffs were free-form summaries. What change would best improve downstream reliability while preserving attribution?**

**Options:**

- Strip source details from subagent outputs to reduce context size, then use Grep later when reviewers request justification.
- Have each exploration subagent write longer narrative summaries that include reasoning traces and repeated reminders to cite sources.
- Ask the implementation subagent to reread the repository broadly and infer supporting locations from each summarized recommendation before editing.
- **Require subagents to return structured handoff records with findings separated from file paths, symbols, line ranges, commands, and source excerpts.**  ✅

**Correct answer:** **Require subagents to return structured handoff records with findings separated from file paths, symbols, line ranges, commands, and source excerpts.**

**Explanation:**

Free-form summaries lose which file and line support each claim, so require structured handoff records that separate the finding from its file path, symbol, line range, command, and source excerpt. Stripping metadata to save space creates the exact traceability gap reviewers report, longer narrative reasoning isn't machine-usable provenance, and asking the implementation agent to re-derive locations wastes work and can misattribute across similar packages. Attribution is part of the deliverable, not decoration.

---

## Q14  ·  Set 1 Question 39

*Domain: Agentic Architecture & Orchestration*

**During a legacy payment module analysis, the coordinator first assigns one subagent to map database tables and another to trace API callers. Both return useful findings. The coordinator then invokes a planning subagent to propose a migration strategy, but the plan ignores the database constraints and caller list already discovered, recommending changes that would break known integrations. What should you change to make this orchestration more reliable?**

**Options:**

- Instruct the planning subagent to infer missing dependencies from file names when prior findings are unavailable.
- **Have the coordinator maintain shared investigation state and include relevant prior findings in each subsequent subagent prompt.**  ✅
- Replace the specialized subagents with one long-running generalist subagent that performs discovery and planning together.
- Allow subagents to message each other directly so the planning subagent can request missing analysis details.

**Correct answer:** **Have the coordinator maintain shared investigation state and include relevant prior findings in each subsequent subagent prompt.**

**Explanation:**

The planning subagent ignores earlier findings because subagents don't automatically see each other's context. Have the coordinator hold the investigation state (discovered tables, caller list, constraints) and pass the relevant parts into each subsequent subagent prompt. Direct subagent-to-subagent messaging hides information flow from the coordinator, one generalist subagent loses specialization and bloats context, and inferring dependencies from file names substitutes guesses for evidence. The coordinator owns shared state and routing.

---

## Q15  ·  Set 1 Question 40

*Domain: Tool Design & MCP Integration*

**An engineer asks the agent to investigate a production stack trace from an unfamiliar legacy service. The trace contains the message "InvalidInventoryTransition" and references a helper named validateTransition, but the repository has hundreds of source files and inconsistent directory naming. What should the agent do first to find the relevant implementation and usage sites efficiently?**

**Options:**

- Use Glob to list likely source files by extension, then Read each candidate file until the error appears.
- Use Bash to run ad hoc recursive shell commands, then paste the raw terminal output into context.
- Use Read to load the entire module tree upfront, then ask the agent to infer all relevant references.
- **Use Grep to search file contents for the error string and function names, then Read the matching files.**  ✅

**Correct answer:** **Use Grep to search file contents for the error string and function names, then Read the matching files.**

**Explanation:**

The agent already knows specific strings (the error message and a function name), so start with Grep to find where they appear and then Read only the matching files. Glob matches file paths, not contents; loading the whole module tree bloats context before the agent knows what matters; ad hoc Bash recursion produces noisy output. The principle is progressive exploration: a narrow content search first, then read the smallest useful set to understand control flow.

---

## Q16  ·  Set 1 Question 42

*Domain: Agentic Architecture & Orchestration*

**The same agent now handles two request types. Dependency license reviews follow a stable rubric with known checks, while production bug investigations in unfamiliar services vary based on discovered call paths, logs, and failing tests. The current single-pass prompt misses checklist items during reviews and wastes effort during investigations. Which decomposition strategy is most appropriate?**

**Options:**

- Use dynamic task planning for every workflow, allowing the agent to redefine review criteria as it discovers code patterns.
- Use one large prompt for both request types, asking the agent to reason carefully before using any tools.
- **Use a fixed prompt chain for stable review rubrics, and let the agent adapt subtasks during open-ended investigations.**  ✅
- Use the same fixed sequential checklist for both workflows, requiring every investigation to complete every predefined step.

**Correct answer:** **Use a fixed prompt chain for stable review rubrics, and let the agent adapt subtasks during open-ended investigations.**

**Explanation:**

Match the decomposition to the workflow shape. The license review follows a stable rubric, so a fixed prompt chain gives each pass a focused objective and stops checklist items from being missed; the bug investigation is open-ended, so the agent should adapt subtasks from discovered call paths, logs, and failing tests. One big prompt dilutes attention, a fixed checklist wastes effort on investigations, and dynamic planning adds needless variability to the stable review. Use the simplest structure that preserves quality.

---

## Q17  ·  Set 1 Question 43

*Domain: Claude Code Configuration & Workflows*

**A senior engineer asks Claude to replace a legacy permissions layer across API handlers, CLI tools, shared middleware, tests, and documentation. The team has not chosen between adapting existing interfaces or introducing a new authorization boundary, and incorrect sequencing could break unrelated workflows. What should you have Claude do first?**

**Options:**

- Begin direct execution on the highest-traffic package, then let failing tests reveal additional files that require changes.
- Start a fresh session for each package and avoid sharing findings, preventing earlier assumptions from influencing later edits.
- **Use plan mode to explore dependencies, compare viable migration strategies, and produce an implementation plan before modifying files.**  ✅
- Ask Claude to edit every file matching the legacy permission imports, then manually review the diff afterward.

**Correct answer:** **Use plan mode to explore dependencies, compare viable migration strategies, and produce an implementation plan before modifying files.**

**Explanation:**

The team hasn't chosen an approach and bad sequencing could break unrelated workflows, so use plan mode first to explore dependencies, compare migration strategies, and produce a reviewable plan before editing. Mechanically editing import matches or driving discovery through test failures treats an architectural change like a simple refactor, and isolating each package in its own session breaks consistency across the migration. Design before changing files when the work spans many files and approaches.

---

## Q18  ·  Set 1 Question 45

*Domain: Agentic Architecture & Orchestration*

**An engineer asks the agent to explain how the "user export" capability works in a legacy repository. The final answer confidently covers REST controllers and serializers, but misses scheduled exports, admin-triggered jobs, and CLI invocations. Logs show every subagent completed successfully; their prompts were "inspect export controller," "trace export API request," and "summarize export endpoint tests." What should you change first to improve coverage on similar broad codebase questions?**

**Options:**

- Require each subagent to read every file matching export-related terms before returning any findings to the coordinator.
- Run a fixed pipeline that always invokes controller, database, CLI, worker, and test subagents for every codebase query.
- Strengthen the synthesis subagent prompt to infer missing workflows from naming conventions and common framework patterns.
- **Revise coordinator planning to identify plausible entry points, then delegate distinct code areas to subagents before synthesis.**  ✅

**Correct answer:** **Revise coordinator planning to identify plausible entry points, then delegate distinct code areas to subagents before synthesis.**

**Explanation:**

Every subagent succeeded, but the coordinator only pointed them at the REST path, so scheduled jobs, admin actions, and CLI commands were never explored. Fix the coordinator's planning to enumerate plausible entry points first, then delegate distinct code areas before synthesis. Having synthesis infer missing workflows invites unsupported guesses, making every subagent read every matching file bloats context, and a fixed full pipeline wastes work. Coverage on broad questions is a decomposition and routing responsibility.

---

## Q19  ·  Set 1 Question 51

*Domain: Tool Design & MCP Integration*

**Your codebase migration assistant has access to tools for repository metadata extraction, dependency graph analysis, and migration plan generation. Evaluation runs show it sometimes begins dependency analysis or plan generation before collecting canonical package manager and framework versions, producing plans with incorrect assumptions. What change would most reliably enforce the intended first step while preserving model-driven follow-up behavior?**

**Options:**

- **Force the metadata extraction tool with tool_choice for the first request, then continue subsequent analysis in follow-up turns.**  ✅
- Inspect the assistant's natural language for phrases indicating metadata completion, then retry when the expected phrase is absent.
- Set tool_choice to any for the first request, relying on tool descriptions to make metadata extraction the likely selection.
- Strengthen the system prompt to say metadata extraction must happen first before any dependency or migration planning tools.

**Correct answer:** **Force the metadata extraction tool with tool_choice for the first request, then continue subsequent analysis in follow-up turns.**

**Explanation:**

A required prerequisite step needs deterministic sequencing, so force the metadata tool on the first request with tool_choice naming extract_metadata, then switch to "auto" so Claude drives the follow-up analysis. tool_choice "any" requires some tool but not the right one, a system-prompt instruction stays probabilistic, and parsing the reply for a completion phrase couples control flow to wording rather than structured tool use. Force the prerequisite, then restore model-driven flexibility.

---

## Q20  ·  Set 1 Question 58

*Domain: Claude Code Configuration & Workflows*

**In a developer productivity workflow, Claude has generated a helper that scaffolds new internal SDK integrations. Review shows three failures: retry handling conflicts with your error-normalization helper, generated config duplicates an existing block, and the naming fix proposed for one path breaks another path using the same template. Each attempted single-issue fix has reintroduced one of the other failures. What is the best next refinement step?**

**Options:**

- Tell Claude the output is wrong and ask it to be more careful before trying again.
- **Send one detailed refinement request describing all observed failures, shared constraints, and expected behavior across the affected call paths.**  ✅
- Open separate Claude sessions for each failure and merge whichever patch passes its local test first.
- Ask Claude to fix the failures sequentially in separate turns, starting with the easiest failing assertion.

**Correct answer:** **Send one detailed refinement request describing all observed failures, shared constraints, and expected behavior across the affected call paths.**

**Explanation:**

The three failures share the same helper, template, and call paths, and fixing them one at a time keeps reintroducing the others. Send one refinement request describing all the failures, the shared constraints, and the expected behavior across the affected paths so Claude can weigh the tradeoffs together. Sequential fixes suit independent problems, isolated parallel sessions produce incompatible patches, and "be more careful" gives no test evidence or constraints. Match the refinement style to how coupled the problems are.

---
