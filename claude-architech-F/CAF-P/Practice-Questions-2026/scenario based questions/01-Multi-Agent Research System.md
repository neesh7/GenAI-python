# Scenario: Multi-Agent Research System

> You are building a multi-agent research system using the Claude Agent SDK. A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports. The system researches topics and produces comprehensive, cited reports.
> - web search
> - analyzes documents
> - sythesizes finding
> - generate final reports

Questions for this scenario, collected from Practice Tests 1-3 (Claude Certified Architect - Foundations, v2.0).

**Total questions: 30**

---

## Q1  ·  Set 1 Question 2

*Domain: Context Management & Reliability*

**In pilot runs on fast-changing market topics, reviewers find final reports often make accurate individual claims but misstate whether evidence is current, peer-reviewed, or based on a small regional sample. When they ask the report generator to add citations, it sometimes cites the correct document but cannot identify the page, publication date, or study basis from earlier handoffs. What change would most effectively improve downstream synthesis reliability?**

**Options:**

- Increase synthesis context by passing full raw transcripts from every source instead of compact summaries between subagents.
- Sort all source summaries chronologically before synthesis so the newest evidence is more visible in the prompt.
- **Update each subagent's output contract to attach dates, source locations, and methodological notes to every extracted finding.**  ✅
- Add a report cleanup pass that infers missing citation details from wording and fills gaps before publishing.

**Correct answer:** **Update each subagent's output contract to attach dates, source locations, and methodological notes to every extracted finding.**

**Explanation:**

Long pipelines compress information at each handoff, so dates, source locations, and methodology vanish unless they travel with the claim. Update each subagent's output contract to attach that metadata to every finding, so synthesis can tell current from outdated, peer-reviewed from commentary, and broad from narrow samples. Passing full transcripts bloats context without guaranteeing the right details are used, a cleanup pass that infers citations risks hallucinated provenance, and chronological sorting fixes only one dimension. Preserve qualifiers explicitly.

---

## Q2  ·  Set 1 Question 6

*Domain: Tool Design & MCP Integration*

**During a run, the document-analysis subagent asks a source retrieval MCP tool for the full text of a licensed market report. The backend rejects the request because the license permits summaries and short excerpts only. Today the tool returns “access denied,” causing the coordinator to retry with paraphrased requests and then mark the source as unavailable. What change would best let the agents handle this case correctly?**

**Options:**

- Report a permission error and instruct the coordinator to escalate to infrastructure owners for immediate credential repair.
- Classify the rejection as transient and retry with backoff using progressively narrower full-text retrieval queries.
- **Return isError true with errorCategory business, isRetryable false, and guidance to request summaries or short excerpts instead.**  ✅
- Return a successful empty result set so the synthesis agent can continue without exposing licensing details.

**Correct answer:** **Return isError true with errorCategory business, isRetryable false, and guidance to request summaries or short excerpts instead.**

**Explanation:**

The backend is enforcing a licensing rule (summaries and short excerpts are allowed, full text is not), which is neither transient nor a credential problem. Return isError true with errorCategory "business", isRetryable false, and guidance to request summaries or excerpts, so the coordinator stops retrying and picks an allowed path. Retrying treats a stable rule like a timeout, an empty success hides that the source exists but is restricted, and escalating for credential repair misroutes recovery. Distinguish business-rule violations from transient and permission failures.

---

## Q3  ·  Set 1 Question 8

*Domain: Agentic Architecture & Orchestration*

**During production evaluation, reviewers find that first drafts are coherent and cited but often incomplete. For example, a report on AI regulation includes strong EU coverage, weak Asia-Pacific coverage, and unresolved contradictions between two market statistics. The current workflow sends the first synthesis directly to the report generator whenever all subagents return successfully. What change would most effectively improve report completeness without abandoning the coordinator-subagent architecture?**

**Options:**

- Raise the coordinator's maximum iteration count to a fixed cap, stopping after five passes regardless of remaining coverage gaps.
- Instruct the report generator to hide low-coverage sections unless the synthesis agent marks every subsection as fully supported.
- Have all subagents repeat their original broad assignments twice, then merge duplicate findings before sending results to synthesis.
- **Add a coordinator review loop that checks synthesis coverage, redelegates targeted follow-ups, and reruns synthesis until quality criteria are met.**  ✅

**Correct answer:** **Add a coordinator review loop that checks synthesis coverage, redelegates targeted follow-ups, and reruns synthesis until quality criteria are met.**

**Explanation:**

A subagent succeeding only means its assigned work finished, not that the research question is covered, which is why first drafts are coherent but incomplete. Add a coordinator review loop that checks synthesis coverage against explicit criteria, redelegates targeted follow-ups for gaps or contradictions, and reruns synthesis. Hiding weak sections masks the gap, repeating broad assignments duplicates work and misses the same gaps, and a fixed iteration cap ignores whether coverage is actually sufficient. The coordinator owns aggregation and quality control.

---

## Q4  ·  Set 1 Question 15

*Domain: Agentic Architecture & Orchestration*

**Over the weekend, several source documents were revised, a search index was refreshed, and two previously collected subagent outputs now cite superseded versions. The coordinator still has a saved investigation session containing the earlier web results, document analyses, and synthesis notes. What is the most reliable way to continue the research without contaminating the final report with outdated evidence?**

**Options:**

- Resume the saved session and cap the coordinator to three additional iterations before generating the updated cited report.
- Resume the saved session with --resume and instruct the coordinator to ignore any results produced before the weekend.
- **Start a fresh session with a structured summary of still-valid findings, then re-run targeted searches and analyses for changed sources.**  ✅
- Create fork_session branches from the saved investigation and compare which branch produces the most internally consistent final report.

**Correct answer:** **Start a fresh session with a structured summary of still-valid findings, then re-run targeted searches and analyses for changed sources.**

**Explanation:**

Stale tool outputs stay in the conversation history and keep influencing reasoning even if you tell the coordinator to ignore them. Start a fresh session, inject a structured summary of the still-valid findings, then re-run targeted searches and analyses for the changed sources. --resume with "ignore old results" relies on prompt compliance while leaving invalid evidence in context, fork_session branches from the same stale baseline, and an iteration cap controls runtime rather than freshness. Resume only when the prior context is mostly still valid.

---

## Q5  ·  Set 1 Question 25

*Domain: Tool Design & MCP Integration*

**During testing, the document analysis subagent receives coordinator-selected PDFs and reports from an approved catalog, but it has a generic URL retrieval tool. It sometimes follows links inside documents to blogs, login pages, or duplicate HTML summaries, then cites those pages instead of the approved sources. You need reduce these citation and scope errors while preserving access to approved source material. What change best addresses this?**

**Options:**

- **Replace fetch_url with a load_document tool that accepts catalog document IDs or approved URLs and validates before fetching.**  ✅
- Give the document analysis subagent web search tools too, so it can independently confirm whether linked pages are relevant.
- Allow fetch_url for any link, then have synthesis discard citations whose domains are not in the approved catalog.
- Keep fetch_url available, but add prompt instructions warning the subagent never to open links found inside documents.

**Correct answer:** **Replace fetch_url with a load_document tool that accepts catalog document IDs or approved URLs and validates before fetching.**

**Explanation:**

A generic fetch_url lets the document analyzer wander to blogs and login pages inside documents and cite them instead of approved sources. Replace it with a load_document tool that only accepts catalog IDs or approved URLs and validates before fetching, so its action space matches its role. Prompt warnings rely on probabilistic compliance while leaving the unsafe action available, adding web search expands the agent beyond document analysis, and post-filtering citations still lets bad sources shape intermediate reasoning. Encode boundaries in the tool, not just the prompt.

---

## Q6  ·  Set 1 Question 29

*Domain: Agentic Architecture & Orchestration*

**Quality audits show that reports covering 25 or more source documents have uneven validation quality. Early sources receive detailed citation checks, later sources receive superficial checks, and the same evidence weakness is sometimes accepted in one source but rejected in another. What task decomposition change would most effectively improve review consistency?**

**Options:**

- Ask the synthesis agent to analyze all source documents in one prompt using stronger instructions about consistency.
- **Run focused document-level evidence checks first, then perform a separate cross-document consistency pass before synthesis and reporting.**  ✅
- Have every subagent review the full source bundle independently and report only issues found by most agents.
- Increase the coordinator loop limit so the synthesis agent can keep revisiting sources until quality appears acceptable.

**Correct answer:** **Run focused document-level evidence checks first, then perform a separate cross-document consistency pass before synthesis and reporting.**

**Explanation:**

One synthesis prompt over 25+ sources dilutes attention, so early sources get careful checks and later ones get superficial ones. Run focused document-level evidence checks first so each source gets comparable depth, then a separate cross-document pass for conflicts, duplicates, and consistency before synthesis. "Be more careful" leaves the overloaded design unchanged, majority voting across subagents wastes effort and can hide rare but real findings, and raising the loop limit doesn't define what good coverage means. Separate local analysis from integration analysis.

---

## Q7  ·  Set 1 Question 31

*Domain: Tool Design & MCP Integration*

**Your web search MCP tool occasionally times out. Today it returns a content block reading "Search provider timeout, try again later" as if the call succeeded. The synthesis subagent sometimes treats that text as a source note, and the report generator includes unsupported citations. What tool response change best prevents the model from confusing failures with valid research content?**

**Options:**

- Keep returning error text as normal content, but instruct synthesis to ignore passages containing timeout or unavailable.
- Convert failures into empty successful result lists, allowing the coordinator to proceed without additional error-handling complexity.
- **Return failed tool calls with isError set true, plus concise diagnostic content the subagent can use for recovery.**  ✅
- Raise uncaught server exceptions for all failures, letting the agent infer failure details from transport-level interruptions.

**Correct answer:** **Return failed tool calls with isError set true, plus concise diagnostic content the subagent can use for recovery.**

**Explanation:**

Returning timeout text as normal content makes the synthesis agent treat an error message as a source note. Mark failed tool calls with isError true plus concise diagnostic content, so the agent treats the response as a failure to recover from rather than evidence to cite. Telling synthesis to ignore passages containing "timeout" or "unavailable" is brittle string-matching, converting failures to an empty success hides the access failure, and raising uncaught exceptions can break the loop instead of enabling recovery. Give a machine-readable failure signal.

---

## Q8  ·  Set 1 Question 32

*Domain: Context Management & Reliability*

**After a pilot, the system assigns high confidence to most report claims and the team wants to auto-publish those claims. Later customer audits find citation mismatches concentrated in regulatory topics and newly added source types, even though overall quality dashboards remain strong. What review strategy should you implement before further reducing reviewer coverage?**

**Options:**

- **Randomly sample high-confidence claims across topic, source type, and report section, then track errors and new patterns by stratum.**  ✅
- Review only claims with low confidence scores, since high-confidence findings should be excluded from routine reviewer queues.
- Auto-publish all high-confidence reports immediately, then investigate only customer-reported defects to minimize reviewer workload.
- Compute one aggregate accuracy metric from accepted reports, then reduce review once the overall rate exceeds the target.

**Correct answer:** **Randomly sample high-confidence claims across topic, source type, and report section, then track errors and new patterns by stratum.**

**Explanation:**

The aggregate dashboards stay strong while errors cluster in regulatory topics and newly added source types. Randomly sample high-confidence claims across meaningful strata (topic, source type, report section) and track error rates and emerging patterns per stratum before reducing review. Reviewing only low-confidence claims assumes confidence is already calibrated, auto-publishing and waiting for customer complaints is reactive and biased, and one aggregate metric averages the weak segments away. Confidence is trustworthy only after it's monitored against real outcomes.

---

## Q9  ·  Set 1 Question 37

*Domain: Agentic Architecture & Orchestration*

**A user requests a report comparing how proposed AI copyright rules affect music licensing, model training data, and independent film production across the same jurisdictions and dates. Logs show the coordinator routes the entire request to one document analysis pass, then asks the report agent to write separate sections. The final report deeply covers licensing, barely addresses training data, and gives recommendations that conflict across sectors. What workflow change would most effectively improve the result?**

**Options:**

- **Split the request into distinct concern threads, investigate them in parallel with shared constraints, then synthesize one unified cross-sector report.**  ✅
- Process the concerns sequentially from highest commercial value to lowest, finalizing each report section before starting the next concern.
- Ask every subagent to independently analyze the full user request, then concatenate their outputs into the final report document.
- Add an instruction that the report agent should mention every requested sector at least once before delivering the final answer.

**Correct answer:** **Split the request into distinct concern threads, investigate them in parallel with shared constraints, then synthesize one unified cross-sector report.**

**Explanation:**

Routing a compound request through one analysis pass dilutes attention, so coverage is lopsided and recommendations conflict across sectors. Split it into distinct concern threads, investigate them in parallel while passing the shared constraints (jurisdictions, dates, definitions), then synthesize one report that reconciles conflicts. Finalizing sections sequentially detects cross-sector contradictions too late, independent full-scope analyses duplicate work and diverge, and telling the report agent to "mention every sector" is cosmetic. Separate focused parallel investigation from unified synthesis.

---

## Q10  ·  Set 1 Question 38

*Domain: Agentic Architecture & Orchestration*

**In staging, final reports occasionally include polished sections with missing or unverifiable citations. Traces show the coordinator sometimes invokes the report-generation subagent after receiving web-search and document-analysis outputs, while the synthesis subagent is still pending or has returned an error. What change would most effectively prevent these invalid reports?**

**Options:**

- **Add a coordinator-side prerequisite that blocks report-generation Task calls until synthesis returns a structured citation manifest and success status.**  ✅
- Strengthen the report-generation subagent prompt to refuse drafting unless it believes synthesis completed and all citations are available.
- Allow report generation to start immediately, then run a final citation scan and discard reports with missing references.
- Have the coordinator parse synthesis messages for phrases like "complete" or "ready" before starting the report-generation subagent.

**Correct answer:** **Add a coordinator-side prerequisite that blocks report-generation Task calls until synthesis returns a structured citation manifest and success status.**

**Explanation:**

Reports get missing citations because the coordinator sometimes starts report generation while synthesis is still pending or has errored. Add a coordinator-side prerequisite that blocks the report-generation Task call until synthesis returns a structured citation manifest and a success status. A prompt telling the generator to refuse can't be guaranteed once it's invoked with incomplete input, parsing "complete" or "ready" turns workflow state into unreliable text classification, and a post-hoc citation scan wastes work. Enforce ordering in control flow, not in prompts.

---

## Q11  ·  Set 1 Question 47

*Domain: Tool Design & MCP Integration*

**Your coordinator's document-analysis subagent depends on an internal library-catalog MCP server. It works in your local Claude Code session, but two teammates who cloned the repository cannot access the catalog tools, so their runs fall back to weaker web searches. Separately, one researcher is testing an experimental notes server that should not affect the team. What should you change?**

**Options:**

- Document per-user claude mcp add commands in README, and ask each researcher to recreate both servers locally.
- Combine the catalog and notes integrations into one MCP server, and expose only role-specific tools to subagents.
- Place both servers in each user's ~/.claude.json, and rely on onboarding scripts to synchronize changes across machines.
- **Move the required catalog server into project-scoped .mcp.json, and keep the experimental notes server in user-scoped ~/.claude.json.**  ✅

**Correct answer:** **Move the required catalog server into project-scoped .mcp.json, and keep the experimental notes server in user-scoped ~/.claude.json.**

**Explanation:**

The catalog server is required for the team but configured only locally, so teammates fall back to weaker web search, while the notes server is one researcher's experiment. Put the required catalog server in project-scoped .mcp.json so it travels with the repository, and keep the experimental notes server in user-scoped ~/.claude.json. Manual per-user setup drifts into inconsistent behavior, and merging required and experimental servers doesn't address scope. Match configuration scope to the intended audience: project for shared tools, user for personal ones.

---

## Q12  ·  Set 1 Question 55

*Domain: Agentic Architecture & Orchestration*

**Your document-analysis subagent receives 45 reports and policy papers in a single pass before synthesis. The final outputs cite many sources but miss source-specific caveats, merge incompatible methodologies, and sometimes contradict earlier extracted facts. What workflow change would most effectively improve reliability?**

**Options:**

- **Analyze each source in a focused pass with structured findings, then run a separate cross-source integration pass before reporting.**  ✅
- Set a maximum number of synthesis iterations and stop once the report includes citations from every source category.
- Send all sources to the synthesis agent together and instruct it to be more careful with citations and contradictions.
- Partition sources randomly across parallel subagents, concatenate their summaries, and have the report agent polish the combined narrative.

**Correct answer:** **Analyze each source in a focused pass with structured findings, then run a separate cross-source integration pass before reporting.**

**Explanation:**

One pass over 45 sources overloads the model, so it misses source-specific caveats, merges incompatible methodologies, and contradicts earlier facts. Analyze each source or small group in a focused pass that produces structured findings with caveats and provenance, then run a separate cross-source integration pass before reporting. "Be more careful" leaves the overload in place, random parallel partitioning without an integration step yields fluent but inconsistent reports, and iteration or citation-count targets don't measure whether conflicts were handled. Chain focused stages instead of one broad prompt.

---

## Q13  ·  Set 1 Question 59

*Domain: Context Management & Reliability*

**During testing, a report on remote work productivity cites two recent, credible studies with different productivity statistics. The synthesis agent currently chooses the higher number because it appears in a larger sample study, and the report presents it as the single definitive result. Reviewers note that both studies are methodologically credible but measure productivity differently. What change would most improve the reliability of the final report?**

**Options:**

- Average the conflicting statistics into one blended estimate and cite both sources as supporting the combined value.
- Select the statistic from the study with the largest sample size and suppress the smaller study to avoid confusing readers.
- Ask the web search subagent to keep searching until it finds a third source matching one of the reported statistics.
- **Preserve both statistics with source attribution, methodology notes, and a conflict annotation for the report generator to present transparently.**  ✅

**Correct answer:** **Preserve both statistics with source attribution, methodology notes, and a conflict annotation for the report generator to present transparently.**

**Explanation:**

Two credible studies measure productivity differently, so picking the larger-sample number and presenting it as definitive manufactures false certainty. Preserve both statistics with source attribution, methodology notes, and a conflict annotation, and let the report present the disagreement transparently. Averaging incompatible values, suppressing the smaller study, or hunting for a convenient tie-breaker source all obscure real uncertainty and weaken traceability. Keep claim-source mappings and the reasons findings disagree so readers can interpret the evidence.

---

## Q14  ·  Set 3 Question 1

*Domain: Agentic Architecture & Orchestration*

**During a run on regional climate adaptation funding, the document analysis subagent finds two credible government reports with incompatible cost estimates. The synthesis agent cannot determine whether the difference reflects methodology, geography, or time period. Current escalation tickets only say "conflicting sources found," and human reviewers must restart the investigation from scratch. What change would best improve this mid-process escalation?**

**Options:**

- Have the report generator omit contested sections from final reports and notify reviewers only after unrelated sections finish.
- Attach the complete coordinator and subagent transcript so reviewers can reconstruct the investigation without model summarization.
- **Generate a structured handoff with research topic, disputed claims, source citations, analysis performed, and recommended reviewer decisions.**  ✅
- Ask the synthesis agent to choose the most plausible estimate and escalate only when its confidence score is low.

**Correct answer:** **Generate a structured handoff with research topic, disputed claims, source citations, analysis performed, and recommended reviewer decisions.**

**Explanation:**

A ticket that only says "conflicting sources found" forces reviewers to restart the investigation from scratch. Generate a structured handoff with the research topic, the disputed claims, source citations, the analysis already performed, and recommended reviewer decisions, so the human continues from the system's work. Dumping the full transcript is noisy and makes reviewers rediscover the facts, choosing the most plausible estimate hides uncertainty, and omitting contested sections creates silent gaps. Escalation should transfer actionable state, not just announce failure.

---

## Q15  ·  Set 3 Question 3

*Domain: Context Management & Reliability*

**Your team uses the system to investigate an unfamiliar legacy repository that powers citation extraction. After several hours, the coordinator starts answering follow-up questions with generic claims about "typical pipeline patterns" and contradicts earlier discoveries about specific classes and data flows. The earlier discoveries were recorded only in long conversation turns mixed with verbose Read, Grep, and test outputs. What change would most effectively preserve accurate findings for later questions?**

**Options:**

- Add a final synthesis subagent that summarizes the entire conversation only after answers begin becoming inconsistent.
- **Have each exploration subagent write key findings to scratchpad files at known paths, and require later prompts to reference them.**  ✅
- Increase the coordinator's context budget and retain every verbose tool output in conversation history for later retrieval.
- Ask the coordinator to answer from memory unless uncertain, then rerun broad repository searches for missing details.

**Correct answer:** **Have each exploration subagent write key findings to scratchpad files at known paths, and require later prompts to reference them.**

**Explanation:**

After hours of exploration, findings buried in long turns mixed with verbose tool output degrade, so the coordinator falls back on generic pipeline claims. Have each exploration subagent write key findings — file paths, class names, data flows, open questions — to scratchpad files at known paths, and require later prompts to reference them. Increasing context or keeping all verbose output worsens attention dilution, relying on memory or uncertainty triggers is fragile, and a late one-time summary can compress away the exact facts. Separate working memory from persistent state.

---

## Q16  ·  Set 3 Question 11

*Domain: Tool Design & MCP Integration*

**A researcher adds an internal corpus MCP server that exposes tools for searching licensed journals and exporting citation metadata. The coordinator uses it successfully on that researcher's laptop, but teammates running the same workflow see only the default tools and produce reports with weaker public web citations. The server needs to be part of the team's reproducible research setup without exposing credentials. What should you change?**

**Options:**

- Describe the server in CLAUDE.md and instruct the coordinator to request those research tools by name.
- **Define the shared server in the repository's .mcp.json, using environment variable placeholders for credentials rather than committed secrets.**  ✅
- Add the server to each developer profile in ~/.claude.json, then document manual setup steps in the project README.
- Let each subagent call generic web search when MCP tools are unavailable, avoiding repository-level server configuration.

**Correct answer:** **Define the shared server in the repository's .mcp.json, using environment variable placeholders for credentials rather than committed secrets.**

**Explanation:**

The licensed-journal MCP server works on one laptop but teammates see only default tools, weakening citations. Define the shared server in the repository's .mcp.json using environment-variable placeholders for credentials, so everyone gets the tool without committing secrets. ~/.claude.json is per-user and doesn't travel with the repository, CLAUDE.md can describe a server but can't make unconfigured tools callable, and falling back to web search masks the misconfiguration and lowers quality. Scope shared integrations to the project and keep credentials in the environment.

---

## Q17  ·  Set 3 Question 12

*Domain: Tool Design & MCP Integration*

**A report-generation subagent must update a shared Markdown template used for final research reports. The template contains the same phrase, "TODO: add source summary," in several sections, and repeated attempts to make a targeted replacement keep failing because the match is not unique. What should you do next?**

**Options:**

- Use Grep to locate every matching phrase, then replace all occurrences so the failed edit cannot recur.
- Use Bash with a scripted search-and-replace command to bypass Edit and update the template automatically.
- Keep retrying Edit with broader surrounding text until one replacement succeeds without manually inspecting the full file.
- **Use Read to load the full template, modify the intended section, then Write the complete corrected file back.**  ✅

**Correct answer:** **Use Read to load the full template, modify the intended section, then Write the complete corrected file back.**

**Explanation:**

The Edit fails because "TODO: add source summary" appears in several sections and only one should change. Read the full template, change the intended section in context, then Write the complete corrected file. Replacing every Grep match changes sections that should keep their placeholder, a scripted Bash replace just makes the same ambiguous change faster, and retrying Edit with broader text still doesn't guarantee a unique anchor. Use the Read-then-Write fallback when a targeted edit can't uniquely identify the text to replace.

---

## Q18  ·  Set 3 Question 14

*Domain: Tool Design & MCP Integration*

**During evaluation, the document analysis subagent sometimes initiates new web searches instead of analyzing the assigned PDFs, while the report generator occasionally rewrites evidence summaries before formatting them. Engineers added the extra tools to reduce coordinator round trips, but citation quality and role consistency have declined. What change best addresses the design issue?**

**Options:**

- Keep the broad tool access, but add stronger prompts telling each subagent to avoid using tools outside its primary role.
- **Restrict each subagent to role-relevant tools, adding only narrow cross-role utilities for frequent simple checks like source metadata lookup.**  ✅
- Move all tool access to the coordinator and require subagents to return plain text requests whenever they need information.
- Give all subagents the same complete tool list so each agent can independently choose the fastest path to completion.

**Correct answer:** **Restrict each subagent to role-relevant tools, adding only narrow cross-role utilities for frequent simple checks like source metadata lookup.**

**Explanation:**

Broad tool access let the document analyzer start web searches and the report generator rewrite evidence — classic role drift. Restrict each subagent to role-relevant tools, adding only narrow cross-role utilities for frequent simple needs like a source-metadata lookup. Stronger "stay in your role" prompts leave the confusing tool surface unchanged, routing every call through the coordinator over-corrects with round trips, and giving everyone every tool increases decision complexity and misuse. Constrain tool availability first, then use descriptions to guide selection within scope.

---

## Q19  ·  Set 3 Question 18

*Domain: Agentic Architecture & Orchestration*

**Last week, a long research investigation produced a draft report on a market topic. Since then, several source documents were replaced and the web index was refreshed. When the coordinator resumes the named investigation session, it repeatedly cites withdrawn documents and treats old search outputs as current, even after the user points out the updates. What should you do before continuing the report?**

**Options:**

- Resume the original session, remind the coordinator that some sources changed, and ask it to disregard outdated evidence.
- Fork the old session into separate branches, compare their reports, and select the branch with fewer citation conflicts.
- Continue the session until contradictions stop appearing, using a fixed maximum of five additional analysis iterations.
- **Start a new session, provide a structured summary of durable findings, and explicitly identify changed sources for fresh analysis.**  ✅

**Correct answer:** **Start a new session, provide a structured summary of durable findings, and explicitly identify changed sources for fresh analysis.**

**Explanation:**

The resumed session keeps citing withdrawn documents because the stale tool results remain in context, even after the user flags the updates. Start a new session, provide a structured summary of the durable findings, and explicitly identify the changed sources for fresh analysis. Telling the coordinator to disregard outdated evidence relies on probabilistic compliance, forking duplicates the stale baseline, and iterating until contradictions stop with a fixed cap treats symptoms rather than removing invalid context. Resume only when the prior context is still mostly valid.

---

## Q20  ·  Set 3 Question 20

*Domain: Tool Design & MCP Integration*

**A new MCP server exposes a working literature database tool that searches licensed journals and returns abstracts, DOI links, publication dates, and citation-ready source metadata. In test runs, the web-search subagent often uses general web search for peer-reviewed evidence, while the document-analysis subagent scans exported PDFs manually. The MCP tool appears in the available tool list, but its surfaced description is only "Search articles by query." What change should you make first?**

**Options:**

- Add coordinator instructions requiring academic prompts to include the word literature so keyword matching routes agents correctly.
- **Rewrite the MCP tool description to specify coverage, accepted queries, returned citation metadata, and when agents should prefer it.**  ✅
- Rename the tool to authoritative_research_supertool while leaving its inputs, outputs, and usage boundaries unchanged for stronger agent selection.
- Remove web search and file-search tools from all research subagents so the literature database becomes the only retrieval path.

**Correct answer:** **Rewrite the MCP tool description to specify coverage, accepted queries, returned citation metadata, and when agents should prefer it.**

**Explanation:**

The literature tool works manually but agents prefer generic web search because its surfaced description is only "Search articles by query." Rewrite the description to specify journal coverage, accepted query formats, the returned citation metadata (DOI, dates), and when to prefer it over web search. MCP tools are still model-selected, so the description is the selection contract. Keyword routing depends on phrasing rather than task semantics, renaming without clarifying capabilities leaves the same ambiguity, and removing every other retrieval tool forces usage and masks the real problem.

---

## Q21  ·  Set 3 Question 21

*Domain: Agentic Architecture & Orchestration*

**A user asks for a report comparing how proposed AI copyright regulations affect music licensing, film post-production, and book publishing in the United States and European Union. Test runs produce reports that mix jurisdictions, duplicate background sections, and leave some industry-specific risks unresolved because the coordinator sends the whole prompt to one research pass before synthesis. What workflow change best improves coverage and consistency?**

**Options:**

- Send the full prompt to every subagent sequentially, asking each one to improve whatever the previous agent missed.
- **Split the request into distinct industry and jurisdiction workstreams, pass shared scope definitions, investigate in parallel, then synthesize one report.**  ✅
- Run the broad research pass repeatedly until the synthesis agent reports high confidence that no topics remain missing.
- Let subagents negotiate scope directly with each other, then have the coordinator accept whichever division they choose.

**Correct answer:** **Split the request into distinct industry and jurisdiction workstreams, pass shared scope definitions, investigate in parallel, then synthesize one report.**

**Explanation:**

Routing the whole multi-industry, multi-jurisdiction prompt through one pass mixes jurisdictions, duplicates background, and leaves industry-specific risks unowned. Split it into distinct industry and jurisdiction workstreams, pass each the same shared scope definitions and dates, investigate in parallel, then synthesize one report. Passing the full prompt agent-to-agent gives no clear ownership and amplifies duplication, letting subagents negotiate scope bypasses the coordinator's control plane, and repeating the broad pass until "confident" doesn't measure completeness. The coordinator owns decomposition and aggregation.

---

## Q22  ·  Set 3 Question 26

*Domain: Context Management & Reliability*

**During load testing, reports on broad topics become inconsistent once the research phase produces more than 30 source analyses. The document analysis subagent completes successfully, but its outputs are long narrative memos with internal reasoning, copied verbatim into the synthesis prompt. The synthesis agent omits high value evidence from earlier analyses and sometimes cites sources that were discussed but not central. What redesign best addresses the reliability problem?**

**Options:**

- Ask the synthesis agent to summarize each long subagent narrative first, then synthesize from its own summaries.
- **Modify upstream subagents to return compact structured records: key facts, citations, relevance scores, and only synthesis-relevant details.**  ✅
- Truncate each subagent response after a fixed character limit before sending it to the synthesis agent for review.
- Increase the synthesis agent's max_tokens and ask it to carefully read every upstream narrative before writing reports.

**Correct answer:** **Modify upstream subagents to return compact structured records: key facts, citations, relevance scores, and only synthesis-relevant details.**

**Explanation:**

Verbose narrative memos with internal reasoning copied into the synthesis prompt blow the context budget, so high-value evidence is dropped and tangential sources get cited. Have upstream subagents return compact structured records — key facts, citations, relevance scores, and only synthesis-relevant details — instead of long narratives. Raising max_tokens doesn't fix noisy input or attention dilution, fixed truncation discards evidence arbitrarily, and having synthesis summarize the narratives adds another lossy compression step. Fix the upstream handoff contract, not just the length.

---

## Q23  ·  Set 3 Question 28

*Domain: Agentic Architecture & Orchestration*

**A user asks for a report evaluating whether an organization should enter a new AI-assisted drug discovery market, covering scientific feasibility, regulatory exposure, partnership opportunities, and commercialization timing. In testing, the system often produces duplicated sections, misses relationships between findings, and takes longer than expected because each broad request is handled as a single chain of subagent calls. Which orchestration change would most effectively improve completeness and latency?**

**Options:**

- Ask the synthesis agent to resolve coverage gaps after receiving one broad search summary and one document summary.
- Send the full request sequentially through every subagent, requiring each agent to append comments before report generation.
- **Decompose the request into concern-specific tasks, run relevant subagents in parallel with shared context, then synthesize one integrated report.**  ✅
- Let subagents message each other directly, allowing whichever agent finds decisive evidence to produce the final report.

**Correct answer:** **Decompose the request into concern-specific tasks, run relevant subagents in parallel with shared context, then synthesize one integrated report.**

**Explanation:**

Handling a broad multi-concern request as one sequential chain causes duplicated sections, missed relationships, and slow runs. Decompose it into concern-specific tasks (feasibility, regulatory exposure, partnerships, timing), run the relevant subagents in parallel with shared framing, then synthesize one integrated report. A fixed full pipeline is slow and duplicative, direct subagent messaging weakens observability, and asking synthesis to patch gaps fails when the evidence was never collected. The coordinator defines boundaries, runs independent work in parallel, and aggregates results.

---

## Q24  ·  Set 3 Question 30

*Domain: Agentic Architecture & Orchestration*

**The coordinator has finished an initial literature map for a controversial research topic. Two stakeholders now want independently developed report outlines, one focused on regulatory risk and one focused on commercial opportunity. Both outlines should start from the same verified source set, but exploratory assumptions from either outline must not influence the other before final comparison. What should you do?**

**Options:**

- Start two fresh sessions with only the original user request, then let each branch rediscover relevant sources independently.
- Continue in the existing coordinator session, alternate prompts for each framing, and instruct Claude to keep assumptions separate.
- **Create separate fork_session branches from the completed analysis baseline, develop each framing independently, then compare outputs through the coordinator.**  ✅
- Run both framing tasks in parallel Task calls that share a scratchpad file for notes and evolving assumptions.

**Correct answer:** **Create separate fork_session branches from the completed analysis baseline, develop each framing independently, then compare outputs through the coordinator.**

**Explanation:**

Two stakeholders need independent outlines from the same verified sources, but neither's exploratory assumptions should leak into the other before comparison. Create separate fork_session branches from the completed analysis baseline, develop each framing independently, then compare through the coordinator. Alternating prompts in one session shares conversation history, fully fresh sessions lose the verified source set, and a shared scratchpad leaks state between branches. The pattern here is a shared baseline with isolated exploration, which ordinary parallel execution doesn't guarantee.

---

## Q25  ·  Set 3 Question 37

*Domain: Context Management & Reliability*

**Your report generator receives synthesis notes from a peer-reviewed meta-analysis, two industry surveys, and several vendor benchmarks. In the final report, a vendor benchmark's narrow claim is presented with the same authority as a repeated meta-analysis finding, and readers cannot judge how much weight to give each conclusion. What change would best improve the reliability of the report?**

**Options:**

- Have the synthesis agent select the most authoritative-looking source for each topic and omit weaker conflicting evidence.
- Normalize all findings into one uniform summary style, then place complete citations in a bibliography at the end.
- **Organize conclusions by evidentiary status, retaining source characterization and methodological context for each major claim in the final report.**  ✅
- Ask the report agent to add a general disclaimer that some sources may vary in quality and methodology.

**Correct answer:** **Organize conclusions by evidentiary status, retaining source characterization and methodological context for each major claim in the final report.**

**Explanation:**

A vendor benchmark's narrow claim is presented with the same authority as a repeated meta-analysis finding, so readers can't weigh the conclusions. Organize conclusions by evidentiary status (well-supported, emerging, contested) and keep each major claim's source type, scope, methodology, and limitations nearby. Flattening everything into one uniform style looks polished but hides epistemic differences, picking the most authoritative-looking source suppresses legitimate disagreement, and a generic disclaimer is too vague to help per-claim. Provenance-aware synthesis preserves the context needed to interpret each citation.

---

## Q26  ·  Set 3 Question 40

*Domain: Tool Design & MCP Integration*

**In the research pipeline, the report generator subagent is wasting context while locating reusable markdown templates and citation-style files. The team already knows the naming conventions for these files, but the subagent currently inspects broad directory contents before deciding what to read. Which approach best reduces unnecessary context while preserving accuracy?**

**Options:**

- Use Read on all files under the reports directory, then summarize away files that appear irrelevant.
- **Use Glob with the known path patterns to enumerate candidate template files, then Read only the selected matches.**  ✅
- Use Bash to run recursive directory listings, then have the subagent infer relevant templates from raw output.
- Use Grep for template filenames across the repository, then Read every file returned by matching content lines.

**Correct answer:** **Use Glob with the known path patterns to enumerate candidate template files, then Read only the selected matches.**

**Explanation:**

The team already knows the naming conventions for the template and citation-style files, but the subagent inspects broad directory contents first. Use Glob with the known path patterns to enumerate candidate files, then Read only the selected matches. Reading everything under the reports directory wastes tokens and dilutes attention, Bash recursive listings add raw output the model must parse, and Grep searches file contents rather than filenames. Separate file discovery (Glob) from content analysis (Read) to keep the context focused.

---

## Q27  ·  Set 3 Question 42

*Domain: Agentic Architecture & Orchestration*

**During load testing, broad topics often produce reports missing either web evidence or document evidence. Logs show the coordinator requested both search and document analysis in the same model response, but the next model input contains only one returned result before synthesis begins. What change best fixes the orchestration bug?**

**Options:**

- Treat preliminary report text as completion unless it contains explicit phrases like NEED_MORE_TOOLS or CONTINUE_RESEARCH.
- Serialize the workflow by preventing simultaneous subagent requests, requiring search, analysis, synthesis, and reporting in fixed order.
- Execute the first requested tool immediately, then ask the coordinator to reissue any remaining requests on the next turn.
- **When the API response has stop_reason tool_use, execute all tool_use blocks, append matching results, and continue until end_turn.**  ✅

**Correct answer:** **When the API response has stop_reason tool_use, execute all tool_use blocks, append matching results, and continue until end_turn.**

**Explanation:**

The coordinator requested two tools in one response, but the loop returned only one result before synthesis, so the evidence is incomplete. When the API response has stop_reason tool_use, execute all the tool_use blocks, append matching tool_result blocks, and continue until end_turn. Forcing a fixed sequence sacrifices the model-driven planning that makes agentic research useful, asking the coordinator to reissue ignored requests adds latency, and parsing text or preliminary output for completion is brittle because text and tool calls can appear together. Treat tool use as a structured protocol.

---

## Q28  ·  Set 3 Question 45

*Domain: Agentic Architecture & Orchestration*

**In a multi-agent research pipeline with a coordinator and specialized search, analysis, synthesis, and report agents, a prototype allows subagents to call one another whenever they need clarification. After several runs, audit logs are incomplete, retries are handled differently by each agent, and report outputs sometimes include findings the coordinator never reviewed. What architectural change would best improve reliability and observability?**

**Options:**

- Let subagents continue direct communication, but require each agent to append a natural-language summary after every handoff.
- Replace coordinator decisions with a fixed pipeline that always runs search, analysis, synthesis, and reporting sequentially.
- **Route subagent messages, errors, and follow-up requests through the coordinator, which manages delegation, recovery, and information flow.**  ✅
- Give every subagent access to all research tools so each can independently recover from missing information.

**Correct answer:** **Route subagent messages, errors, and follow-up requests through the coordinator, which manages delegation, recovery, and information flow.**

**Explanation:**

Letting subagents call each other directly produced incomplete audit logs, inconsistent retries, and report findings the coordinator never reviewed. Route all subagent messages, errors, and follow-up requests through the coordinator, which manages delegation, recovery, and information flow. A peer-to-peer mesh is hard to audit and control, natural-language summaries give no deterministic routing, broad tool access breaks specialization, and a rigid fixed pipeline loses adaptive decomposition. Hub-and-spoke coordination keeps the system observable while subagents stay focused on their tasks.

---

## Q29  ·  Set 3 Question 49

*Domain: Tool Design & MCP Integration*

**During evaluation, the document-analysis subagent repeatedly calls an MCP tool to fetch the same unavailable source URL. Logs show the tool marks every failed fetch the same way, so the subagent retries permanent failures such as deleted documents and unsupported file formats, adding minutes of latency before the coordinator receives partial findings. What change would best improve recovery behavior?**

**Options:**

- Convert non-retryable failures into empty successful results so synthesis can continue without interruption or coordinator intervention.
- **Return errorCategory and isRetryable per failure, marking permanent source issues non-retryable and transient timeouts retryable with clear messages.**  ✅
- Ask the coordinator to classify retryability from the tool's natural-language error text before deciding whether to rerun.
- Retry every failed fetch three times before reporting failure, since repeated attempts smooth over temporary provider instability.

**Correct answer:** **Return errorCategory and isRetryable per failure, marking permanent source issues non-retryable and transient timeouts retryable with clear messages.**

**Explanation:**

The tool marks every failure the same way, so the subagent retries permanent failures like deleted documents and unsupported formats, adding minutes of latency. Return errorCategory and isRetryable per failure — permanent source issues non-retryable, transient timeouts retryable — with clear messages. Converting non-retryable failures into empty successes hides coverage gaps from synthesis, asking the coordinator to infer retryability from prose is brittle, and a blanket three-retry rule burns latency on failures that cannot succeed. Different failure types should trigger different recovery behavior.

---

## Q30  ·  Set 3 Question 51

*Domain: Agentic Architecture & Orchestration*

**Research runs are meeting quality expectations, but they take too long. Logs show the coordinator assigns three independent investigation branches (market adoption, regulatory responses, and technical limitations) one after another, waiting for each subagent to finish before starting the next. The branches do not depend on each other's intermediate findings, and the coordinator still needs to aggregate results before synthesis. What change best reduces elapsed time while preserving the intended orchestration pattern?**

**Options:**

- Allow the market adoption subagent to invoke the regulatory and technical subagents directly, then return a merged result.
- **Have the coordinator issue separate Task calls for independent research branches in one response, then aggregate their returned findings before synthesis.**  ✅
- Combine all branches into one broad Task prompt for a generalist subagent, then ask it to produce synthesis-ready findings.
- Keep the coordinator's sequential Task calls, but shorten each subagent prompt and cap each branch at one tool iteration.

**Correct answer:** **Have the coordinator issue separate Task calls for independent research branches in one response, then aggregate their returned findings before synthesis.**

**Explanation:**

Three independent branches run one after another, so runs are slow even though the branches don't depend on each other's intermediate findings. Have the coordinator issue separate Task calls for the independent branches in one response, then aggregate their returned findings before synthesis. Letting one subagent invoke the others undermines coordinator-controlled information flow, collapsing everything into one generalist subagent weakens specialization and coverage, and keeping sequential calls with a one-iteration cap may cut completeness without fixing scheduling. Parallelize independent work while keeping hub-and-spoke aggregation.

---
