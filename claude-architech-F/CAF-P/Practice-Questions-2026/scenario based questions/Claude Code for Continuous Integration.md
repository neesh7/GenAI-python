# Scenario: Claude Code for Continuous Integration

> You are integrating Claude Code into your CI/CD pipeline. The system runs automated code reviews, generates test cases, and provides feedback on pull requests. You need to design prompts that provide actionable feedback and minimize false positives.

Questions for this scenario, collected from Practice Tests 1-3 (Claude Certified Architect - Foundations, v2.0).

**Total questions: 30**

---

## Q1  ·  Set 2 Question 1

*Domain: Prompt Engineering & Structured Output*

**Your CI job invokes Claude Code in non-interactive mode to produce structured PR review findings. The output always passes JSON Schema validation, but your PR-comment step sometimes fails or posts misleading comments: a finding cites line 220 in a 90-line file, uses a file path not present in the diff, or places the vulnerable snippet inside the remediation field. What should you change in the review pipeline?**

**Options:**

- **Keep tool_use schema enforcement, add deterministic checks for line ranges and file membership, then retry with those failures included.**  ✅
- Replace tool_use with prompted raw JSON and reject any response containing markdown, explanations, or missing fields.
- Increase schema strictness by making every field required and using enums for all free-text review fields.
- Run up to three blind retries whenever inline posting fails, accepting the first schema-valid response.

**Correct answer:** **Keep tool_use schema enforcement, add deterministic checks for line ranges and file membership, then retry with those failures included.**

**Explanation:**

A schema only proves the JSON shape is valid, not that the values make sense — it will happily pass a line that doesn't exist, a file outside the diff, or a snippet placed in the wrong field. Keep tool_use schema enforcement and add deterministic checks (valid line ranges, file-in-diff membership, field placement), then retry with the specific errors so Claude can correct them. Switching to raw JSON makes syntax worse, more required fields and enums can't check relationships against the diff, and blind retries give no corrective signal.

---

## Q2  ·  Set 2 Question 3

*Domain: Claude Code Configuration & Workflows*

**A CI review job recently added strict accessibility guidance intended only for React UI files. After deployment, Claude starts flagging backend route handlers and migration scripts for missing ARIA labels because the guidance is loaded on every review. You need the guidance to apply automatically only when relevant changed files are in scope. What should you change?**

**Options:**

- Add a root CLAUDE.md instruction telling Claude to ignore accessibility guidance unless filenames look like React components.
- **Move the accessibility guidance into a .claude/rules/ file with YAML frontmatter paths matching React component globs.**  ✅
- Use @import from the project CLAUDE.md and ask Claude to decide whether the imported accessibility file applies.
- Create a .claude/commands/accessibility.md command and require CI to invoke it only for pull requests containing UI files.

**Correct answer:** **Move the accessibility guidance into a .claude/rules/ file with YAML frontmatter paths matching React component globs.**

**Explanation:**

The accessibility guidance is loaded on every review, so it leaks into backend handlers and migration scripts. Put it in a .claude/rules/ file with YAML paths globs matching React components so it loads only for those files. A root CLAUDE.md "ignore unless it's React" instruction or an unconditional @import still keeps the guidance in context, and a slash command needs manual invocation. The reliable fix is to prevent irrelevant conventions from loading at all rather than asking Claude to ignore them.

---

## Q3  ·  Set 2 Question 7

*Domain: Prompt Engineering & Structured Output*

**Your review job emits structured findings that always pass JSON parsing and required-field checks. However, production logs show some findings reference line numbers outside the pull request diff, classify test-only issues as production blockers, or include remediation text that contradicts the reported issue. What change would most effectively improve reliability before posting comments to pull requests?**

**Options:**

- Make every finding field required in the JSON schema so Claude cannot omit uncertain values during automated review generation.
- Replace tool use with markdown output and parse the natural language explanation for contradictions before posting review comments.
- **Keep tool-based structured output, then add semantic validation against diff metadata, severity rules, and finding consistency before publishing comments.**  ✅
- Lower temperature and instruct Claude to double-check every file path, line number, severity, and remediation before returning results.

**Correct answer:** **Keep tool-based structured output, then add semantic validation against diff metadata, severity rules, and finding consistency before publishing comments.**

**Explanation:**

Schema checks confirm types and required fields, but they can't prove a line actually exists in the diff or that a severity is justified. Keep the structured tool output and add semantic validation before posting — check file paths and lines against diff metadata, verify severity against the criteria, and reject internally inconsistent findings for retry or human review. Making more fields required increases fabrication, switching to markdown throws away the structured reliability, and lower temperature plus "double-check" are probabilistic, not deterministic.

---

## Q4  ·  Set 2 Question 11

*Domain: Claude Code Configuration & Workflows*

**A CI job generates test recommendations on every pull request. Developers report that many comments propose tests already present, such as empty-cart checkout and expired-token login cases. The job currently sends Claude only the PR diff and modified source files, then posts every suggested test as a comment. What change would best reduce these duplicate recommendations while preserving useful gap detection?**

**Options:**

- Have Claude generate a full replacement test suite for the modified module on every pull request run.
- **Pass the relevant current test files into the review context and ask Claude to target only uncovered behaviors.**  ✅
- Raise the severity threshold for generated test suggestions so duplicate scenarios are filtered from pull request comments.
- Add a prompt rule saying not to repeat existing coverage, while continuing to provide only implementation diffs.

**Correct answer:** **Pass the relevant current test files into the review context and ask Claude to target only uncovered behaviors.**

**Explanation:**

Seeing only the diff and source files, Claude can't know what's already tested, so it proposes duplicate cases. Pass the relevant existing test files into the review context and ask it to target only uncovered behaviors. A severity threshold doesn't detect duplicates, a "don't repeat coverage" rule asks Claude to honor a constraint it can't verify without the tests, and generating a full replacement suite causes needless churn. Ground the review in the artifacts needed to judge coverage.

---

## Q5  ·  Set 2 Question 22

*Domain: Claude Code Configuration & Workflows*

**Developers repeatedly ask Claude Code to run the same pre-PR test-gap analysis. The workflow needs a reusable checklist, should prompt for a target diff or file pattern when omitted, and must avoid tools unrelated to reading files and writing the generated test plan. Which configuration best supports this workflow?**

**Options:**

- **Create a project skill in .claude/skills/test-gap-review/SKILL.md, configuring argument-hint and allowed-tools frontmatter, then include the reusable checklist.**  ✅
- Store the workflow in ~/.claude/skills/test-gap-review/SKILL.md so every contributor inherits the same skill configuration automatically during CI work.
- Add the checklist to project CLAUDE.md and ask developers to remember expected arguments and permitted tools.
- Create a project slash command in .claude/commands/test-gap-review.md and document tool restrictions inside the command instructions.

**Correct answer:** **Create a project skill in .claude/skills/test-gap-review/SKILL.md, configuring argument-hint and allowed-tools frontmatter, then include the reusable checklist.**

**Explanation:**

This is a reusable, task-specific workflow that needs a checklist, should prompt for a target when omitted, and must limit tool access — so build a project skill in .claude/skills/ with argument-hint and allowed-tools frontmatter, shared through version control. CLAUDE.md is for always-on standards, not on-demand workflows; a user-scoped skill under ~/.claude won't ship with the repo; and a slash command can't constrain tools as cleanly as skill frontmatter. Match the mechanism to a packaged, invokable workflow.

---

## Q6  ·  Set 2 Question 35

*Domain: Prompt Engineering & Structured Output*

**Your CI workflow lets Claude Code generate fixes for failing checks, then immediately review the resulting pull request in the same continuing conversation. Audits show the review often overlooks defects tied to assumptions made during implementation, such as trusting a helper API it introduced without validating edge cases. The review prompt already has explicit severity criteria and a consistent finding format. What change would most improve defect detection?**

**Options:**

- **Run the review as a separate Claude Code invocation using only the diff, repository context, and review criteria.**  ✅
- Run multiple reviews in the original session and require the same finding to appear twice before reporting.
- Ask the generation session to explain its implementation rationale before reviewing the pull request for defects.
- Add stricter instructions telling the same session to challenge assumptions and search aggressively for mistakes.

**Correct answer:** **Run the review as a separate Claude Code invocation using only the diff, repository context, and review criteria.**

**Explanation:**

When the same session writes the code and then reviews it, it tends to trust the assumptions it just made. Run the review as a separate Claude Code invocation given only the diff, repo context, and review criteria, so it doesn't inherit the generator's rationale. Asking the same session for its rationale or adding skeptical instructions stays inside the biased context, and repeating reviews until findings appear twice keeps the same blind spots while filtering out valid single-pass findings.

---

## Q7  ·  Set 2 Question 38

*Domain: Prompt Engineering & Structured Output*

**Your automated pull request reviewer often flags issues such as "possible confusing naming" and "maybe incomplete validation" that developers dismiss as speculative. The current prompt already says "be conservative" and "only report high-confidence findings," but dismissal rates have not improved across three sprints. What prompt change is most likely to improve precision without eliminating useful findings?**

**Options:**

- Run the same broad prompt three times and report only findings appearing in at least two runs.
- Increase the required confidence threshold to 95%, requiring Claude to suppress any finding unless it can justify near certainty.
- Add "be extremely conservative" twice in the system prompt, placing it before and after the review checklist.
- **Replace vague confidence guidance with concrete reportable and non-reportable categories, severity definitions, and code examples for each finding type.**  ✅

**Correct answer:** **Replace vague confidence guidance with concrete reportable and non-reportable categories, severity definitions, and code examples for each finding type.**

**Explanation:**

"Be conservative" and "only report high-confidence findings" don't define the line between actionable and speculative, so dismissals persist. Replace them with concrete reportable and non-reportable categories, severity definitions, and code examples for each finding type. Self-reported confidence isn't reliably calibrated, and re-running the broad prompt with majority voting only changes how often Claude reports, not the underlying ambiguity. Translate review judgment into observable decision rules.

---

## Q8  ·  Set 2 Question 43

*Domain: Claude Code Configuration & Workflows*

**Your CI review recently started producing noisy feedback after you added a database migration checklist to shared instructions. Pull requests that only modify TypeScript handlers now receive warnings about lock duration and rollback scripts, but SQL migration pull requests still need those checks. Migration files appear under both `services/*/db/migrations/*.sql` and `packages/*/migrations/*.sql`. You want the guidance to apply automatically during review only when those files are edited, without adding CI path-routing logic. What should you do?**

**Options:**

- Duplicate migration instructions into every service and package directory CLAUDE.md so nearby files inherit local conventions.
- **Create a focused rule file with YAML frontmatter paths for both migration globs, containing only the migration review checklist.**  ✅
- Create a project slash command for migration reviews and make CI select it when SQL files appear.
- Move the migration checklist into the root CLAUDE.md and add instructions telling Claude to ignore unrelated sections.

**Correct answer:** **Create a focused rule file with YAML frontmatter paths for both migration globs, containing only the migration review checklist.**

**Explanation:**

The shared migration checklist now warns on PRs that only touch TypeScript handlers. Put it in a .claude/rules/ file with YAML paths globs for both migration patterns so it loads only when those SQL files change — no CI path-routing required. A root checklist stays loaded and relies on Claude ignoring it, duplicating directory-level files drifts and misses new folders, and a slash command needs external routing logic. Make the guidance load conditionally on the files that make it relevant.

---

## Q9  ·  Set 2 Question 47

*Domain: Prompt Engineering & Structured Output*

**After rollout, automated pull request reviews generate many comments about naming preferences, import ordering, and subjective refactoring suggestions. Developers now skim past the bot's feedback, and important correctness issues are sometimes overlooked in the noise. What should you change first?**

**Options:**

- **Rewrite the review prompt to report demonstrable bugs, security risks, and test gaps, while skipping stylistic preferences without documented impact.**  ✅
- Instruct Claude to report only findings it rates above 8/10 confidence, while keeping the same broad review scope.
- Ask Claude to include every possible improvement, then rely on developers to triage severity labels during pull request review.
- Limit each review to five comments sorted by severity, leaving the existing broad issue categories otherwise unchanged.

**Correct answer:** **Rewrite the review prompt to report demonstrable bugs, security risks, and test gaps, while skipping stylistic preferences without documented impact.**

**Explanation:**

Reviews are drowning in naming, import-order, and refactor noise, burying real correctness issues. Rewrite the prompt to report demonstrable bugs, security risks, and meaningful test gaps while skipping style preferences without documented impact. A self-reported confidence threshold relies on poor calibration, arbitrary comment caps or severity-only triage hide volume without fixing selection, and "report every improvement" pushes triage onto developers and erodes trust. Define concrete reportability rules first.

---

## Q10  ·  Set 2 Question 48

*Domain: Prompt Engineering & Structured Output*

**Your pull request review workflow exposes two structured tools: extract_pr_metadata and generate_review_findings. Recent CI logs show that on documentation-heavy pull requests, Claude sometimes calls generate_review_findings first, so findings lack required repository area, file ownership, and review policy metadata. The metadata must be captured before later review and enrichment steps run. What change best improves reliability?**

**Options:**

- Set tool_choice to any and place extract_pr_metadata first, allowing Claude to choose the best structured tool.
- Keep tool_choice as auto and strengthen the prompt to always complete metadata extraction before generating findings.
- **Configure tool_choice to force extract_pr_metadata on the first request, then run review findings in a follow-up turn.**  ✅
- Gate the loop by parsing assistant text for 'metadata complete' before accepting generated review findings.

**Correct answer:** **Configure tool_choice to force extract_pr_metadata on the first request, then run review findings in a follow-up turn.**

**Explanation:**

On documentation-heavy PRs Claude sometimes calls generate_review_findings before extracting metadata, so findings miss required fields. Force extract_pr_metadata on the first request with tool_choice naming that tool, then run findings in a follow-up turn that includes the metadata. tool_choice "any" requires some tool but not the right one, "auto" may return plain text instead of a tool call, and parsing the reply for "metadata complete" couples control flow to wording. Make the deterministic dependency explicit through tool_choice.

---

## Q11  ·  Set 2 Question 49

*Domain: Claude Code Configuration & Workflows*

**A senior engineer created a /pr-feedback workflow that applies your team's review checklist and suppresses known false-positive categories. It works on their laptop, but clean CI runners and new contributors report "command not found" unless they manually copy files from that engineer's home directory. You want the same command to be available from a fresh repository checkout and reviewed alongside workflow changes. What should you do?**

**Options:**

- Keep the command in ~/.claude/commands/ and add onboarding instructions for each developer and runner to copy it.
- **Store the command markdown under .claude/commands/ in the repository, then commit it with the CI workflow changes.**  ✅
- Embed the review checklist directly in each workflow step so every pipeline job constructs its own prompt.
- Move the checklist into CLAUDE.md and instruct reviewers to type the same prompt whenever CI needs review.

**Correct answer:** **Store the command markdown under .claude/commands/ in the repository, then commit it with the CI workflow changes.**

**Explanation:**

The /pr-feedback command lives in the engineer's home directory, so clean runners and new contributors get "command not found." Store the command markdown under .claude/commands/ in the repository and commit it, so it ships with a fresh checkout and is reviewed alongside workflow changes. User-scoped commands suit personal use, copying from a home directory creates hidden drift, CLAUDE.md isn't a command definition, and embedding the checklist in each CI step duplicates logic. Match the scope to the collaboration boundary.

---

## Q12  ·  Set 2 Question 59

*Domain: Claude Code Configuration & Workflows*

**Recent PR review runs produce noisy findings when a pull request touches only Markdown docs or CSS files. Claude still applies backend transaction rules, API error-handling rules, and database migration standards, which increases context size and creates irrelevant comments. What configuration change best reduces this noise while keeping review guidance automatic?**

**Options:**

- Keep every convention in root CLAUDE.md, adding instructions that Claude should ignore sections unrelated to each pull request.
- Split the CI job into separate review commands per language, manually selecting one command based on changed filenames.
- Add a shorter maximum prompt budget for CI reviews, truncating convention text whenever the pull request appears simple.
- **Move specialized guidance into .claude/rules/ files with YAML paths globs so only rules relevant to changed files load.**  ✅

**Correct answer:** **Move specialized guidance into .claude/rules/ files with YAML paths globs so only rules relevant to changed files load.**

**Explanation:**

Backend, API, and migration rules fire even on docs-only and CSS PRs, adding noise and tokens. Move the specialized guidance into .claude/rules/ files with YAML paths globs so only the rules relevant to the changed files load. A root CLAUDE.md loads everything and "ignore irrelevant sections" still leaves that content in context; routing CI jobs by language duplicates logic and breaks on mixed PRs; truncating by perceived simplicity can drop critical rules unpredictably. Load context conditionally by path.

---

## Q13  ·  Set 3 Question 2

*Domain: Claude Code Configuration & Workflows*

**Your pilot review for database migration pull requests produces uneven feedback. Claude catches obvious syntax issues, but misses risks such as rollback safety, data retention, backward compatibility, and fixture setup because the team has not yet clarified what a good review should cover. You need to improve the workflow before enabling required CI checks. What should you do next?**

**Options:**

- **Run an interview-style refinement pass where Claude asks maintainers targeted questions, then fold clarified criteria into the CI review prompt.**  ✅
- Proceed with required CI enforcement now, using developer complaints from failed builds to discover missing criteria.
- Create several examples from previous clean migrations, then require Claude to imitate those comments exactly during review.
- Add a broad instruction to be extremely thorough, then suppress review comments unless Claude reports high confidence.

**Correct answer:** **Run an interview-style refinement pass where Claude asks maintainers targeted questions, then fold clarified criteria into the CI review prompt.**

**Explanation:**

Claude misses rollback, retention, and compatibility risks because the team hasn't defined what a good migration review covers — the requirements are underspecified, not the wording. Run an interview pass where Claude asks maintainers targeted questions, then fold the clarified criteria into the CI prompt before enabling required checks. "Be thorough" plus confidence filtering gives no concrete criteria, imitating clean examples won't surface hidden edge cases, and enforcing checks early creates false positives and developer distrust. Match the refinement method to the failure mode.

---

## Q14  ·  Set 3 Question 6

*Domain: Prompt Engineering & Structured Output*

**Your CI review uses tool_use to produce a JSON finding object with required fields file_path, start_line, severity, owner_team, linked_ticket, and suggested_fix. In PRs that lack ownership or ticket metadata, reviews contain plausible but nonexistent owner teams and tickets, which downstream automation routes incorrectly. What schema change best addresses this while preserving useful findings?**

**Options:**

- Keep all fields required and add stronger prompt wording telling Claude never to invent values from context.
- Infer absent metadata from repository naming conventions so every finding contains complete routing information for automation.
- **Redesign the schema so unavailable source-dependent fields are nullable or optional, with instructions to return null unless directly evidenced.**  ✅
- Reject any finding missing routing metadata before posting comments, ensuring only fully populated findings reach developers.

**Correct answer:** **Redesign the schema so unavailable source-dependent fields are nullable or optional, with instructions to return null unless directly evidenced.**

**Explanation:**

Forcing owner_team and linked_ticket as required makes Claude invent values when the PR lacks them, which misroutes automation. Make source-dependent fields nullable or optional and instruct Claude to return null unless directly evidenced, while keeping core fields like file_path and suggested_fix required. Stronger "never invent" wording still fights the schema's pressure to fill fields, inferring metadata from naming conventions turns guesses into authoritative data, and rejecting findings that lack routing metadata hides valid issues. Let the schema represent absent evidence.

---

## Q15  ·  Set 3 Question 8

*Domain: Claude Code Configuration & Workflows*

**A new CI review prompt loads the same repository guidance for every pull request. Review comments for generated API clients and database migrations now cite React accessibility rules and frontend naming standards, creating noisy false positives. The repository already keeps file-type conventions in separate markdown snippets, and you want Claude Code to consider each snippet only when the reviewed files are relevant. What should you configure?**

**Options:**

- Add every convention to root CLAUDE.md and instruct Claude to ignore sections unrelated to each pull request.
- Place directory-level CLAUDE.md files near current source folders and duplicate rules for generated or relocated files.
- **Create focused .claude/rules/ files with YAML frontmatter paths globs targeting generated clients, migrations, and frontend files.**  ✅
- Create separate project slash commands for each file type and require CI to choose one command before review.

**Correct answer:** **Create focused .claude/rules/ files with YAML frontmatter paths globs targeting generated clients, migrations, and frontend files.**

**Explanation:**

One always-loaded guidance set makes generated-client and migration reviews cite React accessibility and naming rules. Create focused .claude/rules/ files with YAML paths globs targeting generated clients, migrations, and frontend files so each loads only for matching files. A root CLAUDE.md asks the model to ignore irrelevant rules after they're already in context, and directory-level files with duplicated rules are brittle when file types span multiple locations. Scope conventions to the paths they apply to.

---

## Q16  ·  Set 3 Question 9

*Domain: Prompt Engineering & Structured Output*

**After changing the pull request review prompt from "find all potential reliability issues" to "be conservative and include only actionable comments," the bot still flags defensive null checks as bugs and ordinary retry loops as performance defects. Developers dismiss more than half of its comments and say they cannot predict what the bot considers worth reporting. What change should you make next?**

**Options:**

- Post all findings as non-blocking informational comments so developers can ignore false positives without changing review criteria.
- Require every finding to include a self-reported confidence score, then suppress comments below a configured confidence threshold.
- Add stronger wording that Claude must be extremely conservative and should only comment when it feels completely certain.
- **Replace broad caution language with concrete report and skip criteria for each review category, including representative true-positive and non-issue examples.**  ✅

**Correct answer:** **Replace broad caution language with concrete report and skip criteria for each review category, including representative true-positive and non-issue examples.**

**Explanation:**

Swapping one vague phrase ("find all issues") for another ("be conservative") didn't help — the bot still flags safe null checks and ordinary retry loops. Replace the caution language with concrete report and skip criteria per category, plus true-positive and non-issue examples, defining when those patterns are actually problematic (unbounded retries, swallowed errors). Non-blocking comments, confidence filtering, and louder caution words don't fix the model's decision boundary. Give operational criteria, not intensity words.

---

## Q17  ·  Set 3 Question 10

*Domain: Claude Code Configuration & Workflows*

**A new GitHub Actions step invokes `claude "Review the changed files for regressions"` and then stalls until the CI timeout. The repository checkout is valid, and the same prompt works when a developer runs it manually in a terminal. What change should you make to the pipeline command?**

**Options:**

- Redirect stdin from /dev/null so Claude Code cannot wait for additional input during the CI job.
- Add --output-format json and --json-schema so the runner receives a parseable response without prompts.
- **Run Claude Code with the -p or --print flag so it processes the prompt and exits after output.**  ✅
- Append prompt instructions telling Claude to avoid follow-up questions and finish the review automatically.

**Correct answer:** **Run Claude Code with the -p or --print flag so it processes the prompt and exits after output.**

**Explanation:**

Claude Code is interactive by default, so in CI it waits for input and hangs until the timeout; it works in a terminal because a human is present. Run it with -p or --print so it processes the prompt, writes to stdout, and exits. Redirecting stdin treats a CLI-mode issue as a stream issue, the JSON flags solve parsing rather than interactivity, and telling Claude to avoid follow-up questions can't control whether the CLI waits. Use the documented non-interactive execution mode.

---

## Q18  ·  Set 3 Question 17

*Domain: Claude Code Configuration & Workflows*

**Your repository's root CLAUDE.md has grown to 1,200 lines after adding review criteria, testing standards, API conventions, deployment notes, and migration guidance. CI-invoked Claude Code now produces noisy feedback that blends unrelated standards, and teams frequently create conflicting edits when updating guidance for their area. What restructuring approach best improves maintainability while preserving shared repository behavior?**

**Options:**

- Keep all guidance in root CLAUDE.md, but add stronger headings telling Claude to ignore sections unrelated to each pull request.
- **Move narrowly scoped guidance into topic-specific files under .claude/rules/, leaving root CLAUDE.md with only universal CI review principles.**  ✅
- Move the CI review checklist into ~/.claude/CLAUDE.md on the build runner to reduce repository instruction size.
- Copy the relevant paragraphs into each package's CLAUDE.md so every directory contains a complete local instruction set.

**Correct answer:** **Move narrowly scoped guidance into topic-specific files under .claude/rules/, leaving root CLAUDE.md with only universal CI review principles.**

**Explanation:**

A 1,200-line root CLAUDE.md blends unrelated standards into every review and causes conflicting edits when teams update their area. Move narrowly scoped guidance into topic files under .claude/rules/ and keep only universal CI review principles in the root. Stronger headings preserve the monolith and rely on Claude ignoring sections, copying guidance into package files drifts, and moving it to ~/.claude/CLAUDE.md removes it from version-controlled project config. Reduce irrelevant context while keeping shared configuration.

---

## Q19  ·  Set 3 Question 19

*Domain: Claude Code Configuration & Workflows*

**A new CI job asks Claude Code to improve coverage for a data normalization utility. The first generated tests pass, but they miss null inputs, timezone boundary cases, and duplicate IDs. Follow-up prompts like "be more thorough" produce inconsistent additions and occasional regressions. What workflow should you use to make improvement more reliable?**

**Options:**

- Ask Claude to assign confidence scores to each proposed test, then merge only cases above a fixed threshold.
- **Create a targeted test suite for expected behavior and edge cases, then iterate by feeding Claude the specific failing results.**  ✅
- Have CI randomly rerun Claude Code until generated tests cover the missed cases, stopping after three unsuccessful attempts.
- Rewrite the prompt to say be exhaustive and conservative, then accept only tests whose descriptions sound sufficiently precise.

**Correct answer:** **Create a targeted test suite for expected behavior and edge cases, then iterate by feeding Claude the specific failing results.**

**Explanation:**

"Be more thorough" produces inconsistent additions and occasional regressions. Create a targeted test suite for the expected behavior and edge cases (null inputs, timezone boundaries, duplicate IDs), then feed the specific failing results back to Claude. CI is ideal for this because test output, stack traces, and failing inputs are concrete feedback for the next pass. Confidence scores aren't calibrated, "be exhaustive" doesn't say what's missing, and random reruns with a cap waste cycles without new information.

---

## Q20  ·  Set 3 Question 24

*Domain: Prompt Engineering & Structured Output*

**Your automated PR review has started posting comments that claim error-path tests are missing. Manual spot checks show many flagged cases are already covered through table-driven tests, shared fixtures, or helper-generated cases, but some genuinely uncovered branches still need comments. What change would most effectively improve the review prompt?**

**Options:**

- Tell Claude to report only high-confidence missing-test findings and suppress anything that might already be covered indirectly.
- Require CI to flag gaps only when changed files lack a same-directory test file with matching filename patterns.
- Add a fixed minimum test-count rule per changed file and comment whenever the threshold is not met.
- **Add targeted examples showing varied existing test structures and genuine gaps, including why each should be reported or skipped.**  ✅

**Correct answer:** **Add targeted examples showing varied existing test structures and genuine gaps, including why each should be reported or skipped.**

**Explanation:**

The reviewer wrongly flags branches already covered by table-driven tests, shared fixtures, or helper-generated cases, while some real gaps remain. Add targeted examples showing varied existing test structures and genuine gaps, explaining why each should be reported or skipped, so Claude generalizes the judgment. "High-confidence only" is too vague to resolve the ambiguity, and same-directory-filename or fixed-count rules ignore how real test suites are organized. Examples teach nuanced judgment better than brittle heuristics.

---

## Q21  ·  Set 3 Question 25

*Domain: Claude Code Configuration & Workflows*

**Your pull request review job has become noisy after teams added security audit steps, release-note checks, dependency migration guidance, and test generation procedures to the repository's main Claude instructions. Simple documentation-only PRs now receive irrelevant warnings, while specialized jobs still need the detailed procedures when explicitly run. What configuration approach best balances consistency with focused context?**

**Options:**

- Duplicate the complete workflow prompt inside each CI command, avoiding shared Claude Code configuration files entirely.
- Store workflow instructions in user-scoped skills on the CI runner, updating them manually when jobs change.
- Consolidate every CI checklist into root CLAUDE.md so each automated review receives identical instructions for maximum consistency.
- **Keep universal review principles in project CLAUDE.md, and move specialized CI workflows into project skills invoked by relevant jobs.**  ✅

**Correct answer:** **Keep universal review principles in project CLAUDE.md, and move specialized CI workflows into project skills invoked by relevant jobs.**

**Explanation:**

Adding security, release-note, migration, and test procedures to the main instructions makes docs-only PRs get irrelevant warnings, yet specialized jobs still need them on demand. Keep universal review principles in project CLAUDE.md and move the specialized workflows into project skills invoked by the relevant jobs. User-scoped skills aren't shared and drift from the repo, and duplicating large prompts across CI jobs is brittle since every change must be copied everywhere. Always-on for universal standards, on-demand for specialized workflows.

---

## Q22  ·  Set 3 Question 32

*Domain: Claude Code Configuration & Workflows*

**Your CI job asks Claude Code to review each pull request and then posts findings as inline comments. The posting step intermittently fails because some runs return markdown tables, others return bullet lists, and field names like file path, line number, severity, and remediation are phrased inconsistently. The team wants a low-maintenance fix that lets the pipeline reliably validate findings before posting them. What should you do?**

**Options:**

- Keep markdown output, then strengthen the parser with regular expressions covering every observed table and bullet format.
- **Configure Claude Code to emit structured JSON matching a schema containing required fields for inline review comments.**  ✅
- Post Claude Code's raw review text as one general pull request comment instead of creating inline annotations.
- Ask Claude Code to begin every finding with identical labels, then reject runs containing unexpected label text.

**Correct answer:** **Configure Claude Code to emit structured JSON matching a schema containing required fields for inline review comments.**

**Explanation:**

The posting step breaks because runs return inconsistent markdown tables or bullet lists with inconsistently phrased field names. Configure Claude Code to emit JSON matching a schema with required fields (file path, line, severity, suggested fix) so the pipeline validates findings before posting. Hardening regex over every markdown variant is brittle, policing labels relies on natural-language consistency, and posting one raw comment gives up the inline annotations the workflow needs. Treat the output as an automation contract, not prose.

---

## Q23  ·  Set 3 Question 34

*Domain: Claude Code Configuration & Workflows*

**A custom CI skill first inspects the repository's dependency graph, flaky test history, and prior pull request comments before producing review guidance. In recent runs, the main review output increasingly repeats exploratory notes from that setup phase, reports issues unrelated to the changed files, and sometimes misses straightforward diff-specific problems. What change would best preserve review focus while keeping the setup workflow available?**

**Options:**

- **Configure the skill with context: fork so verbose exploration runs separately and returns only a concise summary.**  ✅
- Increase the skill's argument-hint details so developers provide narrower module names and reduce exploratory output during invocation.
- Have the CI prompt ignore earlier verbose notes and report only high-confidence findings from the pull request.
- Move the workflow into project-level CLAUDE.md so every review session consistently receives the same investigation instructions.

**Correct answer:** **Configure the skill with context: fork so verbose exploration runs separately and returns only a concise summary.**

**Explanation:**

The setup skill's exploratory notes leak into the main review, causing off-target comments and missed diff issues. Configure the skill with context: fork so the verbose discovery runs in an isolated sub-agent and returns only a concise summary to the main session. Putting it in CLAUDE.md makes it always loaded, argument-hint improves usability but doesn't isolate output, and telling Claude to ignore the earlier notes tries to repair context pollution after it has already happened. Isolate verbose exploration from the review context.

---

## Q24  ·  Set 3 Question 39

*Domain: Claude Code Configuration & Workflows*

**During an automated pull request review, your team added a reusable repository impact analysis step before generating final findings. The step produces long dependency traces, rejected hypotheses, and intermediate notes. When the same Claude Code session continues into final review, the posted comments become noisy and sometimes cite exploratory dead ends instead of actionable issues. What configuration change best preserves final review quality while keeping the reusable analysis available?**

**Options:**

- Move the repository analysis instructions into the root CLAUDE.md so every CI invocation shares the same discovery context.
- Add a required manual /compact step after exploration, then continue the same session for final pull request feedback.
- Split the exploration into a separate slash command that writes findings directly into the main conversation transcript.
- **Configure the review helper as a skill with context: fork, returning only a concise summary to the main CI review.**  ✅

**Correct answer:** **Configure the review helper as a skill with context: fork, returning only a concise summary to the main CI review.**

**Explanation:**

The reusable impact-analysis step floods the session with dependency traces and rejected hypotheses, so final comments cite dead ends. Make the helper a skill with context: fork so the heavy discovery runs separately and returns a compact summary for review. Moving the instructions into root CLAUDE.md makes them always loaded, a manual /compact step isn't true isolation and is an automation anti-pattern, and a slash command that writes all its exploration into the same transcript still pollutes it. Keep the final review context decision-ready.

---

## Q25  ·  Set 3 Question 43

*Domain: Claude Code Configuration & Workflows*

**Your repository stores database migrations under services/*/db/migrations, packages/*/migrations, and legacy/*/schema. CI reviews often miss migration-specific rollback and locking requirements unless the changed files are in the one directory that already contains local guidance. You want review behavior to follow the relevant file patterns as packages move, without loading migration guidance for unrelated changes. What should you do?**

**Options:**

- **Create a .claude/rules/migrations.md file with YAML paths matching all migration locations and keep the conventions there.**  ✅
- Move all migration review guidance into the root CLAUDE.md so every CI run consistently sees the rules.
- Copy identical CLAUDE.md files into every current migration directory and update them whenever packages are reorganized.
- Add a /review-migrations command and require the CI job to invoke it only when migration files change.

**Correct answer:** **Create a .claude/rules/migrations.md file with YAML paths matching all migration locations and keep the conventions there.**

**Explanation:**

Migrations live under three different path patterns, and reviews only catch rollback and locking rules where local guidance already happens to sit. Put the conventions in a .claude/rules/migrations.md file with YAML paths globs matching all locations so they load whenever matching files change, even as packages move. Duplicating CLAUDE.md files across directories drifts and misses new folders, a root file loads the rules globally, and a slash command needs manual invocation. Attach guidance to the condition that makes it relevant, not to one folder.

---

## Q26  ·  Set 3 Question 44

*Domain: Claude Code Configuration & Workflows*

**A nightly CI review job for large pull requests first asks Claude Code to map ownership boundaries, trace affected call paths, and inspect related tests before producing review findings. On broad changes, the job often fills the conversation with verbose search results and file excerpts, then the final review misses earlier discoveries or gives shallow comments. What adjustment would best preserve review quality while still allowing necessary investigation?**

**Options:**

- Limit CI review to changed diff hunks only, avoiding exploratory reads so Claude spends attention on final comments.
- Keep all repository discovery in the main CI session, relying on /compact whenever verbose outputs crowd the conversation.
- **Run verbose repository discovery in an Explore subagent, returning concise findings before the main CI review produces structured comments.**  ✅
- Paste complete grep outputs and dependency trees into the initial prompt so Claude has maximum codebase context.

**Correct answer:** **Run verbose repository discovery in an Explore subagent, returning concise findings before the main CI review produces structured comments.**

**Explanation:**

Verbose ownership, call-path, and test discovery crowds the session, so the final review misses earlier findings or gives shallow comments. Run the broad discovery in an Explore subagent that returns concise findings, then let the main session produce the structured comments. Relying on /compact reacts only after the context is already overloaded, reviewing only diff hunks loses cross-file understanding, and pasting full grep and dependency output recreates the overload. Isolate noisy investigation from the final-judgment context.

---

## Q27  ·  Set 3 Question 48

*Domain: Prompt Engineering & Structured Output*

**A pilot of your pull request reviewer shows developers dismiss most performance findings. The current review prompt says: "Only report actionable issues you are highly confident about. Be conservative and avoid nitpicks." The dismissed findings are usually speculative comments like "this loop might be slow" without evidence about input size, hot paths, or repeated work. What prompt change would most effectively improve review precision?**

**Options:**

- Repeat "be conservative" and "avoid speculation" in the system prompt header, review checklist, and final output instructions.
- **Define reportable evidence thresholds for performance findings, including unbounded input growth, hot paths, or repeated database calls inside loops.**  ✅
- Require Claude to include longer reasoning for every performance concern, then post findings whose explanations sound specific and cautious.
- Raise the required self-reported confidence score to 9/10 and automatically suppress any performance finding below that threshold.

**Correct answer:** **Define reportable evidence thresholds for performance findings, including unbounded input growth, hot paths, or repeated database calls inside loops.**

**Explanation:**

Developers dismiss speculative comments like "this loop might be slow" that lack any evidence. Define reportable evidence thresholds for performance findings — unbounded input growth, hot paths, repeated database calls inside loops — so a finding requires observable evidence. Repeating "be conservative" or raising a self-reported confidence score doesn't define the boundary, and selecting findings that merely sound careful rewards style over correctness and can amplify false positives. Encode review judgment as category-specific evidence rules.

---

## Q28  ·  Set 3 Question 57

*Domain: Claude Code Configuration & Workflows*

**A pull request review workflow launches `claude "Review the changed files for security regressions"` from a CI step. The process starts successfully, but the job sits idle until the CI timeout because the command is waiting for an interactive session instead of returning review text to stdout. What change should you make first?**

**Options:**

- Move the review command into a background terminal session so CI logs continue while Claude Code remains active.
- Wrap the existing command in a shell timeout and rerun the CI job whenever no output appears promptly.
- **Run Claude Code with `claude -p "Review the changed files for security regressions"` so it prints output and exits.**  ✅
- Pipe the prompt into the existing `claude` command and rely on end-of-file to close the interactive session.

**Correct answer:** **Run Claude Code with `claude -p "Review the changed files for security regressions"` so it prints output and exits.**

**Explanation:**

The command hangs until the CI timeout because it's waiting for an interactive session instead of returning text to stdout. Run it as `claude -p "..."` so it prints the result and exits. A background terminal session, a shell timeout with reruns, or piping the prompt and relying on EOF all work around the hang instead of selecting the correct non-interactive mode, which produces flaky jobs, missing output, or orphaned processes. Use the documented -p/--print mode for pipelines.

---

## Q29  ·  Set 3 Question 59

*Domain: Prompt Engineering & Structured Output*

**Your automated PR reviewer emits structured findings with fields for file, line, severity, category, and suggested fix. Developers dismiss 38% of comments, but the dashboard only shows broad categories like "bug" and "maintainability," making prompt iteration unfocused. What schema and workflow change would best support systematic improvement?**

**Options:**

- Parse developer dismissal comments for negative sentiment, then prioritize prompt changes for the most frustrated responses.
- Combine dismissed findings into weekly natural-language summaries, then ask Claude to infer the recurring root causes.
- Require Claude to include a higher self-reported confidence score, then suppress comments below the team's chosen threshold.
- **Add a structured field capturing the triggering code pattern, then analyze dismissal rates by that field during prompt iterations.**  ✅

**Correct answer:** **Add a structured field capturing the triggering code pattern, then analyze dismissal rates by that field during prompt iterations.**

**Explanation:**

The dashboard only shows broad categories like "bug" and "maintainability," so prompt iteration is unfocused. Add a structured field capturing the triggering code pattern and analyze dismissal rates by that field, which reveals whether dismissals cluster around specific constructs like generated files, DI wrappers, or defensive null checks. Confidence thresholds don't identify the cause of false positives, sentiment analysis confuses emotion with error type, and weekly natural-language summaries are weaker than structured metadata for measuring patterns over time. Preserve diagnostic metadata at generation time.

---

## Q30  ·  Set 3 Question 60

*Domain: Prompt Engineering & Structured Output*

**A structured CI review step extracts findings from pull request diffs into fields including `changed_file`, `changed_line`, `breaking_change_evidence`, and `suggested_fix`. Validation rejects several potential API-breaking findings because `breaking_change_evidence` is null. The rejected cases only include generated client changes in the CI context, while the previous API contract and baseline generated files are unavailable. What change best improves extraction quality without increasing unsupported findings?**

**Options:**

- **Classify missing-baseline failures separately, retry only format or placement errors, and add the baseline artifact before re-extracting.**  ✅
- Accept the highest-confidence findings despite missing evidence, then rely on developers to dismiss unsupported CI comments.
- Retry every rejected finding with stronger instructions to fill all required evidence fields before CI posts comments.
- Make evidence fields required and ask Claude to infer baseline behavior from generated filenames and changed imports.

**Correct answer:** **Classify missing-baseline failures separately, retry only format or placement errors, and add the baseline artifact before re-extracting.**

**Explanation:**

breaking_change_evidence is null because the prior API contract and baseline generated files aren't in the CI context, so retrying the same extraction can't conjure the evidence. Classify missing-baseline failures separately, retry only format or placement errors, and add the baseline artifact before re-extracting. Accepting high-confidence findings without provenance or inferring baselines from filenames produces unsupported comments, and forcing the evidence field required just pressures fabrication. Distinguish correctable validation failures from coverage gaps that need more input.

---
