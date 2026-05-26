# Scenario: Customer Support Resolution Agent

> You are building a customer support resolution agent using the Claude Agent SDK. The agent handles high-ambiguity requests like returns, billing disputes, and account issues. It has access to backend systems through MCP tools (get_customer, lookup_order, process_refund, escalate_to_human). Your target is 80%+ first-contact resolution while knowing when to escalate.

Questions for this scenario, collected from Practice Tests 1-3 (Claude Certified Architect - Foundations, v2.0).

**Total questions: 58**

---

## Q1  ·  Set 1 Question 18

*Domain: Context Management & Reliability*

**A customer starts a chat with: "I don't want to go through a bot. Put me through to a person about order 8421." The message includes enough details that your normal automation would probably resolve the delayed-shipment issue in one or two tool calls. You are tuning the escalation policy and want to avoid both unnecessary deflection and unnecessary automation. What should the agent do next?**

**Options:**

- Use sentiment analysis on the message, escalating only when the customer appears highly frustrated or hostile.
- Acknowledge the request, run lookup_order to confirm eligibility, then offer the replacement before considering escalation.
- Ask the customer to explain why human help is needed, then continue autonomously if the reason seems resolvable.
- **Call escalate_to_human with the order context and brief summary, without attempting autonomous lookup or replacement processing first.**  ✅

**Correct answer:** **Call escalate_to_human with the order context and brief summary, without attempting autonomous lookup or replacement processing first.**

**Explanation:**

An explicit request for a human is a hard escalation signal, so call escalate_to_human with the order context and a brief summary instead of attempting lookups first. Trying to resolve it autonomously first feels like deflection and breaks trust even when the case is easy. Sentiment isn't a reliable trigger because frustration doesn't indicate preference or complexity, and asking the customer to justify the request adds friction. Honor the stated preference and hand off cleanly.

---

## Q2  ·  Set 1 Question 20

*Domain: Agentic Architecture & Orchestration*

**During evaluation, the coordinator first verifies the customer and retrieves two recent orders, then delegates a billing-dispute investigation. The delegated investigator often asks for the order status again or analyzes the wrong order when the customer mentioned several purchases. You want the coordinator to preserve accuracy without giving the investigator all support tools. What should you change?**

**Options:**

- Update coordinator instructions to tell subagents they should remember all facts discovered earlier in the case.
- Have the investigator rerun get_customer and lookup_order for every dispute before assessing refund eligibility or billing adjustments.
- Rely on the parent conversation history because Task-spawned investigators can inspect earlier tool results when needed.
- **Include verified customer identity, relevant order records, prior findings, and exact investigation goal in each subagent prompt.**  ✅

**Correct answer:** **Include verified customer identity, relevant order records, prior findings, and exact investigation goal in each subagent prompt.**

**Explanation:**

The investigator re-asks for order status because subagents don't inherit the coordinator's conversation or tool results. Include the verified customer identity, the relevant order records, prior findings, and the exact investigation goal directly in each subagent prompt. Telling subagents to "remember" facts assumes shared memory that doesn't exist, relying on parent history assumes inheritance that doesn't happen, and re-running lookups adds latency, duplicates work, and broadens tool access. Pass the case state explicitly.

---

## Q3  ·  Set 1 Question 23

*Domain: Agentic Architecture & Orchestration*

**A customer writes: "I was charged twice, my return label never arrived, and I cannot sign in to check the order." The coordinator currently launches billing, returns, and account subagents with the same prompt: "Investigate this customer issue and recommend a resolution." Logs show each subagent calls overlapping tools for the same order, repeats the same facts, and sometimes recommends conflicting next steps. What orchestration change would most effectively improve reliability and efficiency?**

**Options:**

- **Assign each subagent a distinct issue boundary and shared case facts, then synthesize their non-overlapping findings centrally.**  ✅
- Allow subagents to message each other directly so they can divide remaining work without coordinator involvement.
- Send the full customer transcript to every subagent, then use majority agreement to choose the resolution.
- Route every request through returns, billing, and account subagents sequentially, regardless of the customer's stated concerns.

**Correct answer:** **Assign each subagent a distinct issue boundary and shared case facts, then synthesize their non-overlapping findings centrally.**

**Explanation:**

Giving every subagent the same broad prompt makes them overlap, duplicate tool calls, and recommend conflicting steps. Assign each subagent a distinct issue boundary (billing, return label, account access) with shared case facts, then synthesize their non-overlapping findings centrally. Majority voting over duplicate investigations doesn't create independent coverage, a fixed full pipeline is inefficient and unscoped, and direct subagent messaging bypasses the coordinator's observability and control. Partition work by issue and aggregate centrally.

---

## Q4  ·  Set 1 Question 27

*Domain: Tool Design & MCP Integration*

**Production logs show several distinct backend problems all being returned to the agent as the same text: "Operation failed." Examples include an invalid order ID, a temporary billing service timeout, an expired permission token, and a refund blocked by policy. The agent wastes turns retrying non-retryable failures, asks customers to re-enter valid information after timeouts, and escalates cases it could have resolved. What change would most directly improve recovery behavior?**

**Options:**

- **Return structured MCP errors with categories, retryability, and user-safe details so the agent can choose recovery, clarification, or escalation.**  ✅
- Keep a single generic failure message, but instruct the agent to infer retryability from surrounding conversation and customer urgency.
- Retry every failed tool call twice before responding, then escalate if the same MCP tool still reports failure.
- Map failures to customer sentiment levels, escalating angry customers first and retrying only when the conversation remains neutral.

**Correct answer:** **Return structured MCP errors with categories, retryability, and user-safe details so the agent can choose recovery, clarification, or escalation.**

**Explanation:**

"Operation failed" hides whether a failure is transient, validation, permission, or business-rule, so the agent retries non-retryable cases and escalates solvable ones. Return structured MCP errors with category, retryability, and customer-safe details so the agent can choose recovery, clarification, or escalation. Inferring retryability from conversation or urgency is unreliable, blanket retries waste calls on non-retryable failures, and sentiment-based routing doesn't reveal technical recoverability. Tool results must preserve operational meaning.

---

## Q5  ·  Set 1 Question 36

*Domain: Tool Design & MCP Integration*

**Production traces show that mixed requests such as “I moved and need to return the charger from order 8831” alternate unpredictably between get_customer and lookup_order as the first call. In some sessions Claude passes an order number to get_customer; in others it passes a customer name to lookup_order. The current tool catalog exposes only terse autogenerated summaries, and no backend errors are occurring. What change should you make first to improve tool selection reliability?**

**Options:**

- Consolidate get_customer and lookup_order into one broad lookup tool that chooses internally which backend records to retrieve.
- Add a keyword router that maps phrases like “order” or “refund” to one tool before Claude sees the request.
- Update the system prompt to tell Claude to think carefully before selecting tools, without changing schemas or tool metadata.
- **Rewrite each MCP tool description to specify purpose, accepted identifiers, returned fields, edge cases, and boundaries versus related tools.**  ✅

**Correct answer:** **Rewrite each MCP tool description to specify purpose, accepted identifiers, returned fields, edge cases, and boundaries versus related tools.**

**Explanation:**

With only terse autogenerated summaries, Claude can't tell get_customer from lookup_order and passes the wrong identifier to each. Rewrite every tool description to specify purpose, accepted identifiers, returned fields, edge cases, and boundaries versus related tools. Keyword routing is brittle for multi-intent support language, a vague "think carefully" instruction doesn't supply the missing metadata, and merging into one broad lookup tool blurs boundaries rather than clarifying them. Descriptions are the primary selection signal, so make them explicit and differentiated.

---

## Q6  ·  Set 1 Question 44

*Domain: Context Management & Reliability*

**Production logs show misdirected refunds and privacy disclosures when users provide common names and partial addresses. In these cases, get_customer returns several plausible profiles, and the agent chooses one using recent order activity or name similarity. What change best improves reliability without unnecessarily routing routine cases to humans?**

**Options:**

- Rank matching customers by recent activity and continue with the highest ranked profile when confidence exceeds a threshold.
- Escalate every request with duplicate customer records to a human agent before performing any lookup_order calls.
- Call lookup_order for each matching customer profile, then select the account whose order details best match the message.
- **Treat multiple customer matches as unresolved identity and request a disambiguating identifier before any order or refund operations.**  ✅

**Correct answer:** **Treat multiple customer matches as unresolved identity and request a disambiguating identifier before any order or refund operations.**

**Explanation:**

When get_customer returns several plausible profiles, picking one by recency or name similarity causes misdirected refunds and privacy leaks. Treat multiple matches as unresolved identity and ask for a disambiguating identifier before any order or refund action. Escalating every duplicate to a human is unnecessary since clarification usually recovers it, heuristic ranking can make a wrong account look deceptively likely, and calling lookup_order for every match leaks unrelated customer data. Limit sensitive operations until identity is unique.

---

## Q7  ·  Set 1 Question 46

*Domain: Tool Design & MCP Integration*

**Production logs show that lookup_order and process_refund both return the same failure text, "Operation failed." The agent retries declined refunds, tells customers to try again later when they provided invalid order IDs, and escalates temporary timeout cases that would likely succeed on retry. What change would best improve the agent's recovery decisions?**

**Options:**

- **Return MCP tool errors with isError plus category, retryability, and safe messages distinguishing transient, validation, business, and permission failures.**  ✅
- Route all refund and order lookup failures to escalate_to_human, avoiding autonomous recovery entirely after backend errors.
- Standardize every tool failure as a generic message, then ask Claude to infer recovery steps from conversation context.
- Retry every failed backend tool call three times, then escalate unresolved cases without exposing error details to Claude.

**Correct answer:** **Return MCP tool errors with isError plus category, retryability, and safe messages distinguishing transient, validation, business, and permission failures.**

**Explanation:**

lookup_order and process_refund both return "Operation failed," so the agent retries declines, tells customers with invalid order IDs to try later, and escalates recoverable timeouts. Return errors with isError plus category, retryability, and safe messages that distinguish transient, validation, business, and permission failures. Escalating every failure is too conservative for an 80% resolution target, generic text forces guessing, and a fixed three-retry rule ignores whether the error is actually retryable. Recovery logic depends on the failure type.

---

## Q8  ·  Set 1 Question 48

*Domain: Agentic Architecture & Orchestration*

**In a compliance review, you find several transcripts where the agent called `process_refund` immediately after a customer claimed an order was damaged. In those cases, `lookup_order` later showed the order was past the return window or the refund amount differed from the customer's estimate. The current system prompt says to verify customers and check order eligibility before refunds. What change best reduces this risk?**

**Options:**

- **Add a prerequisite gate that rejects process_refund until verified customer, eligible order, and computed refund amount are present in state.**  ✅
- Strengthen the system prompt to require checking customer identity and order eligibility before any refund-related tool call.
- Add a text parser that permits process_refund only after assistant messages contain verified, eligible, and refund amount.
- Add few-shot examples where the assistant calls get_customer and lookup_order before refunds, including damaged-order and late-return cases.

**Correct answer:** **Add a prerequisite gate that rejects process_refund until verified customer, eligible order, and computed refund amount are present in state.**

**Explanation:**

The system prompt says verify first, but the model still calls process_refund early, issuing refunds on past-window or wrong-amount orders. Add a prerequisite gate that rejects process_refund until verified customer, eligible order, and computed refund amount are present in state. Prompt wording and few-shot examples improve the tendency but can't guarantee ordering when the model chooses tools autonomously, and a text parser over assistant messages isn't a source of truth. Back business-critical prerequisites with programmatic checks on structured state.

---

## Q9  ·  Set 1 Question 49

*Domain: Agentic Architecture & Orchestration*

**Production logs show get_customer returns ISO 8601 timestamps and numeric loyalty tiers, while lookup_order returns Unix timestamps and numeric status codes. The agent sometimes miscomputes return windows or mislabels order status after otherwise successful tool calls. You cannot change upstream MCP servers this quarter, but you need consistent reasoning across cases. What change best addresses the reliability issue?**

**Options:**

- Route all cases with mixed timestamp formats directly to escalate_to_human until the upstream MCP servers are standardized.
- Add system instructions telling Claude to remember each tool's timestamp format and translate status codes during every reasoning step.
- Modify the final customer response parser to correct dates and statuses after Claude has already decided the resolution.
- **Add a PostToolUse hook that converts each tool result into canonical dates, status labels, and tier fields before Claude sees it.**  ✅

**Correct answer:** **Add a PostToolUse hook that converts each tool result into canonical dates, status labels, and tier fields before Claude sees it.**

**Explanation:**

get_customer and lookup_order return inconsistent formats (ISO vs Unix timestamps, numeric status codes), and you can't change the servers this quarter, so the agent miscomputes return windows and statuses. Add a PostToolUse hook that converts each tool result into canonical dates, status labels, and tier fields before Claude sees it. Prompt instructions to remember each format rely on repeated compliance, final-response parsing happens after the decision is made, and broad escalation sacrifices resolution for a difference that can be normalized locally. Make input transforms deterministic.

---

## Q10  ·  Set 1 Question 56

*Domain: Context Management & Reliability*

**During billing disputes, the agent creates condensed case notes before responding or escalating. Human reviewers report that notes sometimes say things like "refund approved" or "customer was promised free return shipping," but they cannot tell whether each claim came from the customer, an order record, a policy document, or the agent's inference. In several escalations, customer allegations were treated as verified backend facts. What change would most effectively reduce this reliability risk?**

**Options:**

- Store complete raw transcripts and tool outputs only, relying on human reviewers to reconstruct sources when disputes arise.
- Ask the agent to include only high-confidence claims in final responses, omitting uncertain details from summaries and escalations.
- Compress each case into a shorter narrative summary and instruct reviewers to ask follow-up questions when provenance seems unclear.
- **Require summaries and handoffs to carry structured claim-source mappings with source type, excerpt or tool field, timestamp, and verification status.**  ✅

**Correct answer:** **Require summaries and handoffs to carry structured claim-source mappings with source type, excerpt or tool field, timestamp, and verification status.**

**Explanation:**

Case notes say "refund approved" without showing whether each claim came from the customer, a record, policy, or inference, so allegations get treated as verified facts. Require summaries and handoffs to carry structured claim-source mappings: source type, excerpt or tool field, timestamp, and verification status. Shorter narratives worsen provenance loss, confidence filtering doesn't prove grounding and can hide uncertainty, and raw transcripts force reviewers to reconstruct evidence manually. Summarization is lossy, so preserve provenance through the workflow.

---

## Q11  ·  Set 1 Question 57

*Domain: Agentic Architecture & Orchestration*

**During development, you resume yesterday's named investigation session about refund errors. In that session, Claude had read `refund_policy.md`, the `process_refund` tool schema, and `escalation_rules.md`, and most of its analysis is still relevant. Since then, a teammate changed the refund threshold rules and updated `process_refund` parameter names. You need Claude to continue designing the fix without repeating the whole investigation or relying on stale assumptions. What is the best next step?**

**Options:**

- **Resume the session, identify the changed policy and tool files, and request targeted re-analysis before continuing implementation decisions.**  ✅
- Start a fresh session and require complete codebase re-exploration whenever any previously analyzed file has changed.
- Resume the session normally and rely on Claude to infer changed assumptions from the prior conversation history during implementation.
- Fork the old session into competing branches and let each branch decide whether prior tool results remain trustworthy.

**Correct answer:** **Resume the session, identify the changed policy and tool files, and request targeted re-analysis before continuing implementation decisions.**

**Explanation:**

Most prior analysis is still valid, but a teammate changed the refund threshold rules and the process_refund parameter names. Resume the named session, identify the changed policy and tool files, and request targeted re-analysis before continuing implementation. Starting fresh wastes useful context, resuming and hoping Claude infers the changes risks stale assumptions, and forking branches from the same stale baseline without refreshing it. Resume when the context is mostly valid, but explicitly tell the agent what changed.

---

## Q12  ·  Set 1 Question 60

*Domain: Tool Design & MCP Integration*

**During rollout, the agent frequently spends its first several turns probing the support knowledge server with broad queries such as “what policies exist for billing disputes?” and “which return exceptions are available?” These exploratory calls consume context, sometimes miss relevant policy documents, and delay straightforward resolutions before any customer-specific action occurs. What design change would best improve the agent’s visibility into available support information while preserving tools for customer-specific actions?**

**Options:**

- Build keyword rules that map phrases like refund, late, or angry to predefined policy documents before tool use.
- Add a mandatory startup tool call that lists every policy document before the agent handles each customer request.
- Copy the full return, billing, and escalation knowledge base into the system prompt for every agent session.
- **Expose the support policy index and knowledge-base catalog as MCP resources, while keeping tools for selected record actions.**  ✅

**Correct answer:** **Expose the support policy index and knowledge-base catalog as MCP resources, while keeping tools for selected record actions.**

**Explanation:**

The agent burns its first turns probing the knowledge server with broad policy queries that consume context and sometimes miss documents. Expose the policy index and knowledge-base catalog as MCP resources (read-oriented context) while keeping tools for record actions like lookup_order and process_refund. A mandatory startup listing tool still forces a call on every request, copying the whole knowledge base into the system prompt bloats context and resists updates, and keyword routing is brittle for ambiguous language. Separate visibility into content from model-initiated actions.

---

## Q13  ·  Set 2 Question 2

*Domain: Tool Design & MCP Integration*

**Pilot logs show that `process_refund` returns the same short failure text for processor timeouts, expired refund windows, missing staff permissions, and malformed amounts. The agent responds inconsistently: it retries policy denials, escalates simple input mistakes, and gives customers vague explanations when permission is missing. What change would most directly improve the agent's recovery decisions?**

**Options:**

- Configure the agent to retry every failed tool call three times before escalating unresolved requests to a human.
- Replace process_refund with separate tools for timeouts, policy denials, permission issues, and invalid input cases.
- Add prompt instructions telling the agent to infer failure causes from customer wording and conversation sentiment.
- **Update each MCP tool to return categorized failures with retryability and customer-safe guidance tailored to the specific backend condition.**  ✅

**Correct answer:** **Update each MCP tool to return categorized failures with retryability and customer-safe guidance tailored to the specific backend condition.**

**Explanation:**

process_refund returns the same text for timeouts, expired windows, missing permissions, and malformed amounts, so the agent recovers inconsistently. Update each MCP tool to return categorized failures with retryability and customer-safe guidance tailored to the specific condition. Retrying every failure is wrong because many aren't retryable, inferring causes from sentiment or wording is unreliable since the real cause is in system state, and splitting into failure-named tools adds ambiguity because the agent can't know the failure mode before calling. Generic text forces the model to guess.

---

## Q14  ·  Set 2 Question 4

*Domain: Agentic Architecture & Orchestration*

**During testing, the coordinator sends refund-investigation subagents long prompts that prescribe exact tool sequences and conditional branches. These subagents work on standard returns, but they fail or ask for unnecessary escalation when a customer describes unusual evidence, missing order numbers, or mixed billing and delivery concerns. What change would most improve subagent performance while preserving coordinator control?**

**Options:**

- Expand delegated prompts with more detailed step-by-step branches covering missing order numbers, mixed issues, and unusual evidence types.
- Require subagents to follow a fixed tool order and escalate whenever any expected intermediate field is unavailable.
- Have the coordinator parse each subagent's natural-language response for completion phrases before deciding whether to continue.
- **Rewrite delegated prompts to state the support objective, known context, quality criteria, constraints, and required structured return format.**  ✅

**Correct answer:** **Rewrite delegated prompts to state the support objective, known context, quality criteria, constraints, and required structured return format.**

**Explanation:**

Long prescriptive prompts with exact tool sequences make subagents brittle on unusual evidence, missing order numbers, or mixed concerns. Rewrite delegated prompts to state the support objective, known context, quality criteria, constraints, and required structured return format, letting the subagent choose its tool path. More procedural branches make prompts more fragile, a fixed tool order with escalate-on-missing-field lowers first-contact resolution, and parsing completion phrases is an unstable interface. The coordinator keeps control of decomposition and output shape while the subagent adapts within scope.

---

## Q15  ·  Set 2 Question 10

*Domain: Tool Design & MCP Integration*

**You split the support system into a coordinator plus specialized subagents for intake, order investigation, and refund-policy evaluation. Production traces show the refund-policy subagent needs order delivery dates and return-window status in most refund cases, but only the coordinator can currently call lookup_order, adding multiple round trips. The lookup_order tool is read-only, while process_refund changes backend state and escalate_to_human creates a handoff. What change best balances latency reduction with reliable control of sensitive actions?**

**Options:**

- Give every support subagent access to all four MCP tools so each can resolve cases without coordinator round trips.
- Create a keyword router that sends any message mentioning refunds directly to process_refund before subagent review.
- Keep all tools coordinator-only and have subagents return natural-language requests whenever they need order or customer details.
- **Grant the refund-policy subagent scoped access to lookup_order, while keeping process_refund and escalation routed through the coordinator.**  ✅

**Correct answer:** **Grant the refund-policy subagent scoped access to lookup_order, while keeping process_refund and escalation routed through the coordinator.**

**Explanation:**

The refund-policy subagent constantly needs delivery dates and return-window status, but only the coordinator can call the read-only lookup_order, adding round trips. Grant the refund-policy subagent scoped access to lookup_order while keeping process_refund and escalation routed through the coordinator. Giving every subagent all four tools over-provisions and invites misuse, keeping all tools coordinator-only is safe but slow for a frequent low-risk read, and keyword-routing straight to a mutating tool is especially dangerous. Apply least privilege with targeted exceptions.

---

## Q16  ·  Set 2 Question 12

*Domain: Tool Design & MCP Integration*

**Production logs show that during short order-service outages, customers with valid orders are sometimes told that no matching order exists. The same tool response shape is currently used when a search completes with zero matches and when the order backend cannot be reached. What change would best improve the agent's recovery behavior?**

**Options:**

- Add a prompt instruction telling the agent to apologize and explain uncertainty whenever lookup_order returns empty results.
- Automatically retry every empty lookup_order response three times before telling customers that no matching orders were found.
- **Return successful empty results only for completed searches, and structured retryable errors when order lookup cannot access the backend.**  ✅
- Treat all lookup_order failures as no-match outcomes, and escalate only if the customer disputes the result.

**Correct answer:** **Return successful empty results only for completed searches, and structured retryable errors when order lookup cannot access the backend.**

**Explanation:**

The same empty shape is used for "search completed with zero matches" and "backend unreachable," so valid customers are told no order exists during outages. Return a successful empty result only for completed searches, and a structured retryable error when the backend can't be reached. Retrying all empty results treats valid no-matches as failures, suppressing access failures as no-match misleads customers, and a prompt-only apology doesn't give the agent the structured state it needs. Preserve outcome semantics so the agent can choose the right recovery path.

---

## Q17  ·  Set 2 Question 13

*Domain: Agentic Architecture & Orchestration*

**A prototype uses specialized subagents for identity verification, billing investigation, return eligibility, and account-risk review. Engineers want billing and returns subagents to pass partial findings directly to each other to resolve linked refund disputes faster. In tests, directly exchanged findings sometimes bypass escalation notes and leave the final customer response missing why one subagent retried a failed lookup. What architecture change best improves reliability without eliminating specialization?**

**Options:**

- Allow subagents to message each other directly, but require each message to include a free-form summary of rationale.
- Give each subagent access to every MCP tool, so agents can independently verify missing context before responding.
- Have the last subagent invoked produce the customer response, using whatever findings it has already received.
- **Route all subagent requests and results through the coordinator, which records context, errors, and final resolution inputs.**  ✅

**Correct answer:** **Route all subagent requests and results through the coordinator, which records context, errors, and final resolution inputs.**

**Explanation:**

Direct billing-to-returns messaging bypasses escalation notes and drops the retry rationale from the final response. Route all subagent requests and results through the coordinator, which records context, errors, and final resolution inputs. Direct subagent messaging creates hidden, unauditable pathways, giving every subagent all tools weakens specialization and still fragments aggregation, and letting the last subagent answer makes correctness depend on invocation order. Hub-and-spoke centralizes observability and error handling while preserving specialization.

---

## Q18  ·  Set 2 Question 14

*Domain: Context Management & Reliability*

**During a multi-hour investigation of the refund workflow, the agent correctly identifies several important files, policy branches, and edge cases. Later in the same session, it starts contradicting earlier findings, references generic support-system patterns, and asks to rediscover classes it already inspected. What change would best improve reliability across the rest of the investigation?**

**Options:**

- Append every raw tool result to each follow-up request so the agent can reconsider all discovered evidence each turn.
- **Have agents maintain concise scratchpad files with key findings, file paths, and decisions, then reference them in later prompts.**  ✅
- Use /compact after every major tool call so the entire conversation remains summarized before additional investigation continues.
- Restart the session whenever answers become inconsistent and require the agent to scan the entire repository again.

**Correct answer:** **Have agents maintain concise scratchpad files with key findings, file paths, and decisions, then reference them in later prompts.**

**Explanation:**

In a multi-hour investigation, findings degrade and the agent starts rediscovering classes and contradicting itself. Have agents maintain concise scratchpad files with key findings, file paths, and decisions, then reference them in later prompts. Appending all raw tool results increases token pressure and attention dilution, frequent /compact can blur critical details, and restarting wastes work and lets the problem recur once the new session grows long. Separate the working conversation from durable persistent state.

---

## Q19  ·  Set 2 Question 16

*Domain: Agentic Architecture & Orchestration*

**Production QA finds final replies often address refunds and returns but overlook shipping address corrections or unresolved account-lock evidence. Logs show subagents return partial findings successfully, but the coordinator accepts the first synthesized reply. Which change best improves completeness without escalating every multi-concern case?**

**Options:**

- **Have the coordinator compare the draft resolution with the original request, assign targeted follow-up subagent work, then rerun synthesis.**  ✅
- Let the synthesis subagent directly contact investigation subagents for missing details, bypassing coordinator turns to reduce handoff latency.
- Run the complete fixed subagent pipeline twice for every complex case, keeping whichever final answer is longer.
- Instruct each subagent to include an overall confidence score, then escalate cases whenever any score falls below 0.8.

**Correct answer:** **Have the coordinator compare the draft resolution with the original request, assign targeted follow-up subagent work, then rerun synthesis.**

**Explanation:**

Subagents return partial findings successfully, but the coordinator ships the first synthesized reply, missing address corrections and account-lock evidence. Have the coordinator compare the draft resolution against the original request, assign targeted follow-up subagent work, then rerun synthesis. Direct subagent contact bypasses the coordinator, running the whole pipeline twice and keeping the longer answer confuses length with completeness, and confidence-based escalation over-escalates resolvable cases. The coordinator owns aggregation and quality control.

---

## Q20  ·  Set 2 Question 17

*Domain: Context Management & Reliability*

**You added an order-investigation subagent that checks identity and order state before the coordinator decides whether to refund or escalate. Production traces show many escalations where the only subagent output is `{"status":"failed","message":"backend unavailable"}`. Manual review finds some cases had a verified customer record, a timeout on only one order lookup, and cached order summaries that could have supported a safe response. What change would best enable the coordinator to recover more intelligently?**

**Options:**

- Retry lookup_order several times inside the subagent, then return a single backend unavailable message to the coordinator.
- **Return error details that include failure type, attempted order lookup, partial customer data, cached summaries, and suggested fallback actions.**  ✅
- Convert lookup_order timeouts into successful empty results so the coordinator can continue without triggering unnecessary escalations.
- Escalate any case after one order lookup failure, since support workflows should avoid acting on incomplete backend data.

**Correct answer:** **Return error details that include failure type, attempted order lookup, partial customer data, cached summaries, and suggested fallback actions.**

**Explanation:**

The subagent returns only {"status":"failed","message":"backend unavailable"} even when a verified customer, a single failed lookup, and usable cached summaries exist. Return error details with failure type, attempted order lookup, partial customer data, cached summaries, and suggested fallback actions. Local retries that still collapse to a generic message block intelligent recovery, marking a timeout as a successful empty result risks a wrong answer, and escalating after one failure is too blunt. A generic status hides the operational context the coordinator needs.

---

## Q21  ·  Set 2 Question 19

*Domain: Agentic Architecture & Orchestration*

**After adding regional order backends, production traces show the agent sometimes misreads raw lookup_order payloads: one region returns status_code: 3, another returns state: "RETURN_PENDING", and a third includes nested timestamps. The agent's final responses are inconsistent, even though each backend response is technically valid. What change best improves reliability without modifying every MCP tool implementation?**

**Options:**

- Parse the assistant's final text for status words and retry lookup_order whenever inconsistent wording appears.
- **Add a PostToolUse hook that transforms lookup_order outputs into a canonical support-case structure before Claude receives them.**  ✅
- Require each customer message to include the customer's region so Claude can choose the correct payload interpretation.
- Expand the system prompt with every regional status mapping and ask Claude to normalize payloads during response generation.

**Correct answer:** **Add a PostToolUse hook that transforms lookup_order outputs into a canonical support-case structure before Claude receives them.**

**Explanation:**

Regional backends return different valid shapes (status_code 3, state "RETURN_PENDING", nested timestamps), so the agent's responses are inconsistent. Add a PostToolUse hook that transforms lookup_order outputs into a canonical support-case structure before Claude sees them. Expanding the prompt with every mapping relies on compliance and bloats context, asking customers for their region doesn't fix schema differences within tool outputs, and parsing final assistant text is fragile because language is an output surface, not a control mechanism. Let the model reason over stable semantic inputs.

---

## Q22  ·  Set 2 Question 20

*Domain: Agentic Architecture & Orchestration*

**After the coordinator verifies a customer and retrieves two recent orders, it invokes a refund-policy subagent to assess eligibility. In production, the subagent often ignores the verified customer ID and latest order status, then asks for details already present in the coordinator's transcript. Logs show the Task prompt only says, "assess refund eligibility for this customer." What change best addresses this reliability issue?**

**Options:**

- Rely on a prior refund-policy subagent invocation to remember customer context for subsequent eligibility checks.
- **Populate each Task prompt with the verified customer facts, relevant order records, prior findings, and needed decision criteria.**  ✅
- Have the subagent call get_customer and lookup_order again whenever details are missing from its prompt.
- Keep the facts in the coordinator transcript and instruct subagents to review the parent conversation before deciding.

**Correct answer:** **Populate each Task prompt with the verified customer facts, relevant order records, prior findings, and needed decision criteria.**

**Explanation:**

The refund-policy subagent ignores the verified ID and latest order because the Task prompt only says "assess refund eligibility for this customer." Populate each Task prompt with the verified customer facts, relevant order records, prior findings, and decision criteria. Keeping facts only in the coordinator transcript doesn't help because the subagent can't see it, recalling prior invocations treats subagents as persistent shared memory, and re-running tools adds latency without fixing the handoff. Context isolation means the coordinator must package what each subagent needs.

---

## Q23  ·  Set 2 Question 21

*Domain: Tool Design & MCP Integration*

**During a pilot, the agent often spends its first two turns asking backend tools what refund policies, return reason codes, and escalation queues exist. These lists are read-only, change weekly, and help the agent choose the right customer-specific actions, but the extra calls increase latency and sometimes consume context before order lookup. Which MCP integration change best addresses this issue?**

**Options:**

- **Expose the read-only policy, reason-code, and queue catalogs as MCP resources, while keeping customer-changing operations as tools.**  ✅
- Instruct the agent to skip catalog discovery unless its response text mentions uncertainty about policy applicability.
- Combine catalog listing and action execution into each backend tool so every call returns available policies and queues.
- Add a mandatory first-turn tool_choice forcing list_policy_catalog before any customer lookup, then let normal tool selection resume.

**Correct answer:** **Expose the read-only policy, reason-code, and queue catalogs as MCP resources, while keeping customer-changing operations as tools.**

**Explanation:**

The agent spends early turns asking which refund policies, reason codes, and escalation queues exist — read-only lists that change weekly. Expose those catalogs as MCP resources while keeping customer-changing operations as tools. A forced first-turn catalog call still adds latency on every request, merging catalogs into every action tool produces verbose outputs and muddier contracts, and skipping discovery based on the agent's own "uncertainty" text is fragile. Resources are for context and tools are for actions, so surface stable catalogs as resources.

---

## Q24  ·  Set 2 Question 23

*Domain: Tool Design & MCP Integration*

**In a customer support resolution agent using Claude Agent SDK and MCP-backed support tooling, you add an MCP server with policy_search and case_history_search tools that use backend ranking, policy metadata, and customer-safe summaries. In evaluation runs, Claude frequently searches raw policy markdown files instead and sometimes returns outdated refund rules. The MCP tools are connected and return better results when explicitly called, but they are rarely chosen spontaneously. What is the most effective first change?**

**Options:**

- Merge the MCP policy tools into one broad support_lookup tool that searches customers, orders, refunds, and policy files together.
- Add a system prompt rule that says MCP tools are always preferred whenever a customer request mentions returns or billing.
- **Rewrite the MCP tool descriptions to detail support-specific capabilities, accepted identifiers, returned fields, and when to use them instead of generic search.**  ✅
- Disable generic file-search tools for all sessions so the agent cannot inspect policy documents without calling the MCP server.

**Correct answer:** **Rewrite the MCP tool descriptions to detail support-specific capabilities, accepted identifiers, returned fields, and when to use them instead of generic search.**

**Explanation:**

The capable policy_search and case_history_search MCP tools work when forced, but Claude defaults to raw policy markdown and returns stale refund rules. Rewrite the MCP tool descriptions to detail support-specific capabilities, accepted identifiers, returned fields, and when to prefer them over generic search. Disabling file search treats the symptom and removes useful flexibility, "always prefer MCP tools" is brittle keyword guidance, and merging unrelated functions into one broad tool increases ambiguity. Descriptions are part of the agent interface, so make the tool's value and use-when explicit.

---

## Q25  ·  Set 2 Question 26

*Domain: Agentic Architecture & Orchestration*

**In testing, complex customer messages with several concerns take too long. For example, "refund the damaged item, explain a duplicate charge, and update my locked account email" causes the returns, billing, and account subagents to each retrieve the customer profile and inspect the same order history before producing overlapping summaries. Some issues are still missed because each subagent spends context on the entire case rather than its specialty. What orchestration change best addresses this?**

**Options:**

- Route all cases through the same fixed sequence of subagents so each can review identical tool results before responding.
- Allow specialized subagents to message each other directly whenever overlap appears, reducing coordinator involvement during investigation.
- **Have the coordinator assign each subagent a distinct concern and shared verified facts, then combine findings into one customer response.**  ✅
- Have every subagent independently investigate the full case, then let the coordinator choose the most complete final answer.

**Correct answer:** **Have the coordinator assign each subagent a distinct concern and shared verified facts, then combine findings into one customer response.**

**Explanation:**

A multi-issue message makes the returns, billing, and account subagents each fetch the profile and inspect the same order history, producing overlap while still missing issues. Have the coordinator assign each subagent a distinct concern with shared verified facts passed once, then combine findings into one customer response. Having every subagent investigate everything amplifies duplication, a fixed sequence ignores complexity and invokes irrelevant specialists, and direct subagent communication breaks the hub-and-spoke. Partition scope so each subagent spends context on its specialty.

---

## Q26  ·  Set 2 Question 27

*Domain: Tool Design & MCP Integration*

**During a maintenance task, Claude must update refund eligibility rules that may live in several packages. Recent attempts used broad repository reads, filling context with unrelated source files before finding the relevant configuration and test fixtures. The files follow naming conventions such as refund-policy.yaml, return-policy.json, and *.refund.test.ts, but their directories vary across services. What should you have Claude do first?**

**Options:**

- Use Read on each service directory recursively, then ask Claude to infer which files match the policy naming conventions.
- **Use Glob with targeted filename patterns to list candidate policy and refund test files, then Read only the relevant matches.**  ✅
- Use Bash to run recursive find commands for every possible extension, then paste the full command output into context.
- Use Grep for refund and return keywords across the repository, then Read every file containing either term.

**Correct answer:** **Use Glob with targeted filename patterns to list candidate policy and refund test files, then Read only the relevant matches.**

**Explanation:**

Broad repository reads fill context before finding the refund-policy.yaml and *.refund.test.ts files scattered across services. Use Glob with targeted filename patterns to list candidate policy and refund test files, then Read only the relevant matches. Recursive Read consumes context before relevance is known, Grep searches contents and is noisy when the criterion is the filename, and ad hoc Bash listings dump excessive output. Narrow the search space with the path-matching tool first, then read only what matters.

---

## Q27  ·  Set 2 Question 29

*Domain: Tool Design & MCP Integration*

**During intake testing, when a customer provides enough identifying details but asks, "Can you just check this?", the agent sometimes replies with generic guidance instead of using any backend tool. You do not know in advance whether get_customer, lookup_order, or escalate_to_human is appropriate, but every production response must be grounded in at least one backend action. What configuration best addresses this behavior?**

**Options:**

- Keep tool_choice on auto and strengthen system prompt instructions requiring backend lookup before every customer-facing response.
- Force get_customer as the required tool for all turns, then let Claude decide whether additional tools are needed.
- **Configure tool_choice to any so Claude must call one available tool while retaining model-driven selection among applicable tools.**  ✅
- Retry whenever assistant text sounds generic, using phrase matching to continue the loop until a tool appears.

**Correct answer:** **Configure tool_choice to any so Claude must call one available tool while retaining model-driven selection among applicable tools.**

**Explanation:**

Every production response must be grounded in a backend action, but for "Can you just check this?" the agent sometimes replies with generic guidance. Set tool_choice to "any" so Claude must call some tool while still choosing among get_customer, lookup_order, or escalate_to_human. Prompt-only instructions with "auto" still allow plain text replies, forcing get_customer over-constrains the agent when another tool fits, and retrying on "generic-sounding" text is an unreliable control signal. Use tool_choice to express the requirement precisely: "any" when some tool must run.

---

## Q28  ·  Set 2 Question 32

*Domain: Agentic Architecture & Orchestration*

**Production logs show that when customers describe several related problems in one message, the agent often gives a detailed answer for the first issue, misses later issues, and sometimes recommends a refund without reconciling other charges on the same account. The workflow is predictable: each order or charge must be assessed, then the overall account resolution must be checked before the customer receives a response. What design should you use?**

**Options:**

- Ask one agent to process the entire case in a single prompt with stricter instructions to be exhaustive.
- **Use a prompt chain that reviews each order or charge independently, then runs a final account-level consistency pass.**  ✅
- Route the case through every available MCP tool in a fixed sequence before allowing any customer response.
- Set a maximum of three agent iterations, escalating cases that still contain unresolved issues after the cap.

**Correct answer:** **Use a prompt chain that reviews each order or charge independently, then runs a final account-level consistency pass.**

**Explanation:**

A multi-issue message gets a detailed answer for the first concern, misses later ones, and recommends a refund without reconciling other charges. Use a prompt chain that reviews each order or charge independently, then runs a final account-level consistency pass. One broad prompt with "be exhaustive" still juggles too much and dilutes attention, running every MCP tool in a fixed order confuses execution with reasoning and risks unsafe operations, and an iteration cap is a generic limit rather than a structure. Decompose predictable work into focused passes, then synthesize.

---

## Q29  ·  Set 2 Question 33

*Domain: Agentic Architecture & Orchestration*

**Production logs show simple requests like "Can you resend my tracking link?" take nearly as long as multi-issue cases because every request runs through all specialist subagents. The extra passes sometimes introduce irrelevant refund or policy details into final responses, even when no refund is requested. Complex cases still require multiple specialists and a unified customer-facing answer. What change best improves the orchestration design?**

**Options:**

- Keep the fixed specialist sequence, but lower each subagent's max_tokens so simple requests complete with less overhead.
- Route each request to a single keyword-matched specialist, bypassing aggregation unless the customer explicitly asks about multiple issues.
- **Have the coordinator assess request scope, delegate only to relevant specialist subagents, then aggregate their findings into one response.**  ✅
- Let specialist subagents message each other directly, allowing whichever agent finishes first to assemble the final customer response.

**Correct answer:** **Have the coordinator assess request scope, delegate only to relevant specialist subagents, then aggregate their findings into one response.**

**Explanation:**

Simple "resend my tracking link" requests run through all specialists, adding latency and injecting irrelevant refund or policy details. Have the coordinator assess request scope, delegate only to relevant specialist subagents, then aggregate their findings. Lowering max_tokens only shortens responses and hurts quality, keyword-matched single-agent routing is brittle for ambiguous or multi-issue requests, and direct subagent messaging removes coordinator observability and synthesis. Match delegation to request complexity.

---

## Q30  ·  Set 2 Question 34

*Domain: Tool Design & MCP Integration*

**During refund testing, four backend failure modes are collapsed into the same MCP tool result: payment-service timeout, malformed refund_amount from the agent, an order outside the return window, and the tool account lacking refund permissions. Production simulations show the agent gives the same apology for all failures, retries cases that cannot succeed, and hides access problems as policy denials. What change would most improve the tool contract?**

**Options:**

- Treat all refund failures as non-retryable business denials, then have the agent explain return policy to customers.
- Retry every failed refund call three times before escalating, regardless of whether the backend reported policy or permission issues.
- **Return distinct structured categories for transient, validation, business, and permission failures, with retryability flags and customer-safe recovery guidance.**  ✅
- Configure the agent to parse backend error strings for keywords, choosing retries, clarifications, or escalation from matched phrases.

**Correct answer:** **Return distinct structured categories for transient, validation, business, and permission failures, with retryability flags and customer-safe recovery guidance.**

**Explanation:**

One refund tool result collapses timeout, malformed amount, out-of-window, and missing permission, so the agent apologizes identically, retries impossible cases, and hides access problems as policy denials. Return distinct structured categories for transient, validation, business, and permission failures, with retryability flags and customer-safe recovery guidance. Treating everything as a business denial misleads customers and hides access issues, keyword-parsing prose is brittle, and retrying every failure confuses transient errors with deterministic ones. Don't collapse operationally different failures into one message.

---

## Q31  ·  Set 2 Question 36

*Domain: Agentic Architecture & Orchestration*

**A debugging session named "refund-escalation-tuning" previously inspected the support agent's system prompt, refund policy file, process_refund tool schema, and production traces. Before you continue, a teammate changed only the refund policy file and the process_refund tool schema. You want to keep useful prior analysis without letting outdated assumptions drive the next changes. What should you do?**

**Options:**

- Use the previous plan unchanged because Claude already inspected relevant files and session history preserves that earlier analysis.
- **Resume the named session, identify the changed policy and tool-schema files, and request targeted revalidation before implementing fixes.**  ✅
- Resume the session, ask Claude for a single confidence score, and proceed when the score is above threshold.
- Start a new session and have Claude rediscover the entire repository before considering any prior conclusions or proposed fixes.

**Correct answer:** **Resume the named session, identify the changed policy and tool-schema files, and request targeted revalidation before implementing fixes.**

**Explanation:**

Prior analysis is mostly valid, but a teammate changed only the refund policy file and the process_refund schema. Resume the named session, identify the changed files, and request targeted revalidation before implementing fixes. Reusing the old plan unchanged is wrong because resumed sessions don't automatically know files changed, asking for a single confidence score doesn't validate the underlying facts, and full from-scratch rediscovery is inefficient for narrow, well-understood changes. Resume when mostly valid, but refresh exactly what changed.

---

## Q32  ·  Set 2 Question 37

*Domain: Agentic Architecture & Orchestration*

**After verified customer, order, and policy facts are already collected for a difficult billing dispute, two plausible resolution paths remain. In previous tests, exploring both paths in one conversation caused later analysis to inherit assumptions from earlier analysis, while starting from scratch created inconsistent fact bases and extra backend calls. What is the best way to compare the two paths?**

**Options:**

- Resume the same named session twice, ask Claude to ignore the other path, then merge both final answers.
- Start two fresh sessions, rerun all customer and order lookups separately, then compare their independent recommendations.
- **Use fork_session from the verified case baseline, explore each resolution path independently, then compare branch summaries before deciding.**  ✅
- Explore both paths in one conversation, separating them with headings and stopping after three turns each.

**Correct answer:** **Use fork_session from the verified case baseline, explore each resolution path independently, then compare branch summaries before deciding.**

**Explanation:**

Two resolution paths remain over a verified fact baseline; exploring both in one conversation contaminates assumptions, and fresh sessions create inconsistent facts and extra backend calls. Use fork_session from the verified case baseline, explore each path independently, then compare branch summaries before deciding. Resuming the same session twice doesn't create independent branches, fresh sessions rerun lookups and diverge, and headings or turn caps don't actually isolate context. Share the factual baseline while isolating each branch's reasoning.

---

## Q33  ·  Set 2 Question 42

*Domain: Agentic Architecture & Orchestration*

**During testing, a customer says they were charged twice and want a refund. The first model response contains a brief customer-facing sentence plus a request to call get_customer, but your loop displays the sentence and exits, so no tool runs. After a later patch, some conversations continue calling tools even after Claude has produced a complete customer response. Which implementation change best addresses both failure modes?**

**Options:**

- **Drive the loop from stop_reason, execute requested tools when it is tool_use, and return only when it is end_turn.**  ✅
- Predefine a fixed get_customer, lookup_order, process_refund sequence, stopping whenever a backend tool returns a successful response.
- Run at most three iterations for every request, returning the latest assistant text once the cap is reached.
- Stop the loop when the assistant text includes final answer language, then skip any remaining tool_use blocks.

**Correct answer:** **Drive the loop from stop_reason, execute requested tools when it is tool_use, and return only when it is end_turn.**

**Explanation:**

The loop stops on assistant text (skipping a needed get_customer), and after a patch it keeps calling tools past completion. Drive the loop from stop_reason: execute tools when it is tool_use, append the tool results, and return only when it is end_turn. Assistant text isn't a reliable completion signal because Claude may add a sentence before requesting a tool, and a fixed tool chain or iteration cap replaces model-driven reasoning. Let Claude decide the next action while the application provides deterministic control flow.

---

## Q34  ·  Set 2 Question 44

*Domain: Tool Design & MCP Integration*

**Production reviews show inconsistent tool choices when customers use colloquial requests such as "I was charged twice," "where is my replacement," and "I want my money back." The agent sometimes calls process_refund before confirming refund eligibility, uses lookup_order with emails that only get_customer accepts, and escalates duplicate-name matches without asking for order details. What is the most effective tool-interface change to improve selection reliability without hard-coding a decision tree?**

**Options:**

- Merge support tools into one execute_support_action tool that accepts freeform intent, identifiers, and requested outcome fields.
- Add a keyword router that maps phrases like "money back" and "charged twice" directly to specific tools.
- Instruct the agent to try get_customer, lookup_order, then process_refund in that fixed sequence for every request.
- **Revise each tool description to state accepted identifiers, example customer phrases, edge cases, and boundaries versus similar tools.**  ✅

**Correct answer:** **Revise each tool description to state accepted identifiers, example customer phrases, edge cases, and boundaries versus similar tools.**

**Explanation:**

Colloquial requests like "I was charged twice" or "I want my money back" cause misrouting — refund before eligibility, wrong identifier to lookup_order, escalating duplicate names. Revise each tool description to state accepted identifiers, example customer phrases, edge cases, and boundaries versus similar tools, without hard-coding a decision tree. Keyword routing is brittle for ambiguous language, one freeform action tool removes useful boundaries, and a fixed get_customer/lookup_order/process_refund sequence creates unnecessary or unsafe calls. Tool interfaces are part of the reasoning environment.

---

## Q35  ·  Set 2 Question 46

*Domain: Agentic Architecture & Orchestration*

**Production traces show that when customers provide photos and an order number, the agent sometimes calls process_refund immediately after get_customer succeeds, before lookup_order confirms item status, purchase date, and refundable amount. Several refunds were issued for final-sale items that backend policy would have rejected. What change would most effectively prevent this failure while preserving autonomous resolution for eligible cases?**

**Options:**

- Strengthen the system prompt to state that process_refund may run only after checking customer identity and order eligibility.
- Require the agent to search its prior assistant text for 'eligible refund' before allowing process_refund calls.
- Escalate every refund request involving photos or final-sale keywords to humans before any backend tools run.
- **Add a tool-call gate that rejects process_refund until get_customer and lookup_order return matching, refund-eligible records.**  ✅

**Correct answer:** **Add a tool-call gate that rejects process_refund until get_customer and lookup_order return matching, refund-eligible records.**

**Explanation:**

With photos and an order number, the agent calls process_refund right after get_customer, before lookup_order confirms status, date, and refundable amount, issuing refunds on final-sale items. Add a tool-call gate that rejects process_refund until get_customer and lookup_order return matching, refund-eligible records. Prompt reminders and few-shot examples stay probabilistic, parsing assistant text for "eligible refund" is fragile, and keyword-based broad escalation hurts first-contact resolution. Guarantee ordering for irreversible financial actions with a deterministic gate.

---

## Q36  ·  Set 2 Question 50

*Domain: Tool Design & MCP Integration*

**Production logs show inconsistent tool selection for billing-related messages. Routine refund requests are sometimes escalated, while requests requiring policy review are sometimes sent directly to process_refund. There are no backend errors, and the tool registry shows broad descriptions with little detail about side effects, eligible inputs, or boundaries between refund handling and human escalation. What is the best first change to improve reliability?**

**Options:**

- Merge process_refund and escalate_to_human into one handle_billing_case tool that internally decides the correct backend action.
- **Rewrite the affected tool descriptions to specify purposes, required inputs, side effects, examples, and boundaries between refund and escalation workflows.**  ✅
- Raise temperature slightly so the agent explores alternative tool choices instead of repeatedly choosing the same billing action.
- Add a keyword router that sends messages containing refund to process_refund and messages containing supervisor to escalate_to_human.

**Correct answer:** **Rewrite the affected tool descriptions to specify purposes, required inputs, side effects, examples, and boundaries between refund and escalation workflows.**

**Explanation:**

Billing messages misroute — routine refunds get escalated and policy-review cases go straight to process_refund — and the registry has broad descriptions with no side-effect or boundary detail. Rewrite the affected tool descriptions to specify purposes, required inputs, side effects, examples, and the boundary between refund and escalation workflows. Keyword routing is brittle, merging into one handler hides important boundaries, and raising temperature only adds randomness. For business-impact tools, descriptions must make consequences and eligibility explicit so the model can reason before acting.

---

## Q37  ·  Set 2 Question 51

*Domain: Context Management & Reliability*

**During a week-long investigation into regressions in billing dispute handling, the coordinator has already explored order lookup flows, refund policy files, and escalation handlers. It then launches subagents to inspect refund calculation and account-status branches. The subagents produce inconsistent findings, miss constraints discovered earlier, and repeat searches that were already completed. What change would most effectively improve reliability across the next exploration phase?**

**Options:**

- **Before launching each new investigation wave, create a structured findings brief and include it in every subagent’s initial prompt.**  ✅
- Increase the number of parallel subagents so repeated searches are diluted across more independent codebase exploration branches and files.
- Set a strict maximum of two tool calls per subagent to force concise exploration and reduce repeated context growth.
- Keep the full coordinator conversation open longer and rely on subagents to recover earlier discoveries through additional tool searches.

**Correct answer:** **Before launching each new investigation wave, create a structured findings brief and include it in every subagent’s initial prompt.**

**Explanation:**

Phased subagent waves produce inconsistent findings, miss earlier constraints, and repeat completed searches because subagents don't inherit prior context. Before launching each new wave, create a structured findings brief and include it in every subagent's initial prompt. Keeping the coordinator conversation open longer worsens degradation and still doesn't reach the subagents, more parallel subagents only help if each has the right starting context, and a strict tool-call cap is arbitrary and reduces evidence quality. Pass context explicitly across phases.

---

## Q38  ·  Set 2 Question 52

*Domain: Agentic Architecture & Orchestration*

**In production, escalated cases often bounce back because human support agents ask customers to repeat order numbers, refund amounts, and prior troubleshooting details. The escalation review console shows only fields submitted through the escalate_to_human tool, not the original chat transcript or tool results. What change best improves escalation handoff quality?**

**Options:**

- Escalate cases earlier whenever sentiment appears negative, so human agents can gather missing details directly from customers.
- Attach a transcript link to each escalation and instruct human agents to read it before contacting the customer.
- Send only the final customer-facing response in escalation notes, keeping internal reasoning and tool details out of the handoff.
- **Populate escalate_to_human with a structured handoff including customer ID, verified facts, root cause, amounts, attempted actions, and recommended next steps.**  ✅

**Correct answer:** **Populate escalate_to_human with a structured handoff including customer ID, verified facts, root cause, amounts, attempted actions, and recommended next steps.**

**Explanation:**

Escalated cases bounce back because the review console shows only the fields submitted through escalate_to_human, not the transcript or tool results. Populate escalate_to_human with a structured handoff: customer ID, verified facts, root cause, amounts, attempted actions, and recommended next steps. Sending only the customer-facing response loses operational context, a transcript link fails when reviewers can't access transcripts, and sentiment-triggered escalation doesn't preserve facts or improve routing. Handoff boundaries are context boundaries, so pass durable structured state.

---

## Q39  ·  Set 2 Question 53

*Domain: Agentic Architecture & Orchestration*

**You added AgentDefinition entries for billing-investigator and returns-investigator specialists, but production traces show the coordinator never starts them. The coordinator is configured with allowedTools containing only get_customer, lookup_order, process_refund, and escalate_to_human. What change best enables the intended delegation without unnecessarily broadening each specialist's permissions?**

**Options:**

- **Add Task to coordinator allowedTools and invoke specialists through it, while keeping backend MCP tools scoped to appropriate agents.**  ✅
- Instruct the coordinator to mention specialist names in prompts and treat their natural-language replies as delegated investigations.
- Grant every specialist all backend MCP tools so they can self-select capabilities without coordinator-mediated spawning.
- Run separate support-agent sessions for each specialty and paste their final summaries into the coordinator after completion.

**Correct answer:** **Add Task to coordinator allowedTools and invoke specialists through it, while keeping backend MCP tools scoped to appropriate agents.**

**Explanation:**

The specialist agents are defined but never start because the coordinator's allowedTools omits Task, the mechanism that spawns subagents. Add Task to the coordinator's allowedTools and invoke specialists through it, keeping backend MCP tools scoped to the appropriate agents. Mentioning specialist names in prompts is only natural-language guidance, not a real invocation; granting every specialist all backend tools increases misuse and still doesn't enable spawning; and running separate sessions manually loses controlled handoff and routing. The coordinator needs Task while specialists keep least privilege.

---

## Q40  ·  Set 2 Question 54

*Domain: Agentic Architecture & Orchestration*

**You added returns, billing, and account subagents. In test cases involving a damaged item plus a disputed late fee, the billing subagent asks the returns subagent about refund eligibility, the returns subagent replies directly, and the coordinator only sees the final billing summary. Audits now show missing rationale for why fees were waived, duplicate customer messages, and inconsistent escalation decisions. What orchestration change would best address this?**

**Options:**

- Give all subagents the full conversation history and complete tool access so they can independently resolve cross-cutting issues.
- **Route every subagent handoff and result through the coordinator, which aggregates state, applies escalation rules, and delegates follow-up work.**  ✅
- Have each subagent independently escalate whenever its confidence drops, then merge all escalations into the final customer response.
- Let specialized subagents call each other directly when they need context, reducing coordinator workload and shortening investigation paths.

**Correct answer:** **Route every subagent handoff and result through the coordinator, which aggregates state, applies escalation rules, and delegates follow-up work.**

**Explanation:**

The billing subagent asks returns directly and returns replies directly, so the coordinator only sees the final summary — losing the fee-waiver rationale and causing duplicate messages and inconsistent escalations. Route every subagent handoff and result through the coordinator, which aggregates state, applies escalation rules, and delegates follow-up work. Direct subagent calls create opaque side channels, full context plus all tools weakens specialization, and confidence-triggered independent escalation is uncalibrated. Hub-and-spoke gives the system one control point for observability and customer experience.

---

## Q41  ·  Set 2 Question 55

*Domain: Tool Design & MCP Integration*

**In the repository for this support agent, a regression appears only in test fixture files whose filenames end with `.policy-case.json`. These fixtures are scattered across multiple service packages, and you want Claude Code to identify the affected files before inspecting their contents. Which approach is most appropriate?**

**Options:**

- **Use Glob with `**/*.policy-case.json`, review the matched paths, then Read only the relevant fixture files.**  ✅
- Use Grep for `policy-case` across repository contents, then Read every file returned by the content search.
- Read all package directories recursively, then ask Claude to infer which filenames match the fixture naming convention.
- Use Bash to run recursive file listing commands, then paste the complete output into the conversation for filtering.

**Correct answer:** **Use Glob with `**/*.policy-case.json`, review the matched paths, then Read only the relevant fixture files.**

**Explanation:**

A regression lives in *.policy-case.json fixtures scattered across packages, and you want to find them before reading. Use Glob with **/*.policy-case.json, review the matched paths, then Read only the relevant fixture files. Grep for "policy-case" searches contents and can miss valid files or add unrelated matches, recursive Read consumes context before relevance is known, and Bash listings dump excessive output to filter. Match the tool to the criterion: Glob for filename and path patterns, then read the small set that matters.

---

## Q42  ·  Set 2 Question 60

*Domain: Agentic Architecture & Orchestration*

**During integration testing, a billing-dispute case starts well: Claude requests get_customer, your service executes it successfully, and the tool returns a verified customer record. The next user-facing message, however, is generated by your application from that raw tool payload, so no order lookup, refund decision, or escalation decision occurs. What change best fixes the control-flow design?**

**Options:**

- **Run an agentic loop that inspects stop_reason, executes requested tools, appends tool results, and repeats until end_turn.**  ✅
- Template a final customer response from the first completed tool result, using returned backend fields directly.
- Keep calling Claude while assistant text includes question marks, uncertainty phrases, or unresolved customer-facing language.
- Limit each request to three tool iterations, then summarize collected results and ask the customer to confirm.

**Correct answer:** **Run an agentic loop that inspects stop_reason, executes requested tools, appends tool results, and repeats until end_turn.**

**Explanation:**

get_customer succeeds, but the application templates the next user-facing message straight from the raw payload, so no order lookup, refund, or escalation decision happens. Run an agentic loop that inspects stop_reason, executes requested tools, appends tool_result blocks, and repeats until end_turn. A tool result isn't a final answer — the verified record is new context Claude needs before deciding the next call. Templating from the first payload short-circuits reasoning, parsing text for uncertainty is unreliable, and iteration caps are only safety guardrails.

---

## Q43  ·  Set 3 Question 4

*Domain: Agentic Architecture & Orchestration*

**A customer writes: "I need a refund for a damaged item, I was charged twice for another order, and I cannot access my account email." In testing, the agent often resolves only the first issue it investigates, then closes the case with an incomplete answer. When instructed to "handle everything," it sometimes mixes order details across issues or gives three disconnected replies. What workflow design best improves first-contact resolution for this pattern?**

**Options:**

- Process the customer's concerns strictly in message order, sending a separate final response after each tool result arrives.
- **Create separate issue records after customer verification, investigate independent concerns using shared case facts, then synthesize one customer-facing resolution.**  ✅
- Choose the most urgent-looking concern based on wording intensity, resolve it first, and defer remaining concerns to humans.
- Ask the customer to submit separate tickets for each concern before using backend tools or offering any resolution.

**Correct answer:** **Create separate issue records after customer verification, investigate independent concerns using shared case facts, then synthesize one customer-facing resolution.**

**Explanation:**

A three-issue message gets only the first concern resolved, or "handle everything" mixes order details and produces three disconnected replies. Create separate issue records after customer verification, investigate the independent concerns using shared case facts, then synthesize one customer-facing resolution. Strict message-order processing fragments the experience and adds latency, asking for separate tickets or deferring concerns by default undermines first-contact resolution, and choosing by "wording intensity" isn't a reliable priority signal. Separate the concerns, then unify the answer.

---

## Q44  ·  Set 3 Question 5

*Domain: Tool Design & MCP Integration*

**While updating refund-policy handling, you ask Claude Code to change a guard clause in a large tool adapter file. The attempted edit fails because the selected text appears in several similar handlers for returns, billing credits, and refunds. You need only the refund handler changed without altering adjacent cases. What should you do next?**

**Options:**

- Run Bash with a broad search-and-replace command targeting the repeated text throughout the support module.
- Use Grep to locate all duplicates, then ask Claude to modify every matching snippet for consistency.
- **Load the full file with Read, identify the intended refund block, then Write the complete corrected file.**  ✅
- Keep retrying Edit with the same replacement until Claude chooses the correct matching occurrence automatically.

**Correct answer:** **Load the full file with Read, identify the intended refund block, then Write the complete corrected file.**

**Explanation:**

The Edit fails because the guard-clause text appears in several similar handlers (returns, billing credits, refunds) and only the refund one should change. Load the full file with Read, identify the intended refund block, then Write the complete corrected file. A broad Bash search-and-replace changes unrelated handlers, modifying every Grep match violates the requirement to change only one handler, and retrying the same ambiguous Edit doesn't add the missing context. Use Read-then-Write when a targeted edit can't uniquely anchor the text.

---

## Q45  ·  Set 3 Question 16

*Domain: Tool Design & MCP Integration*

**During a production incident review, logs show the message "Refund approval token missing" appears only after escalation handoffs. You need Claude Code to inspect the repository and identify every code path that emits or handles this message before changing anything. Which approach should you take first?**

**Options:**

- **Use Grep to search repository contents for the exact error string and refund handler names, then Read matching files.**  ✅
- Use Glob to find refund-related filenames, then review only those files and skip content searches across unrelated paths.
- Use Edit to open likely refund modules one by one, searching manually before making targeted code changes.
- Read every support-agent source file into context, then ask Claude to identify where the error originates.

**Correct answer:** **Use Grep to search repository contents for the exact error string and refund handler names, then Read matching files.**

**Explanation:**

You need every code path that emits or handles "Refund approval token missing." Use Grep to search repository contents for the exact error string and refund handler names, then Read the matching files. Glob matches filenames, not where a string appears, so it can miss shared middleware, escalation adapters, or constants; Edit is for changes, not investigation; and reading every source file dilutes attention with irrelevant content. Do targeted content search first, contextual reading second, and modification last.

---

## Q46  ·  Set 3 Question 23

*Domain: Tool Design & MCP Integration*

**Production logs show two failure patterns in refund handling: intermittent gateway timeouts that often succeed on the next attempt, and permanent failures such as refund window expired or missing permission. Today the MCP tool sets `isError` and returns the same short failure message for both, so the agent sometimes repeats impossible operations and sometimes gives up on recoverable ones. What change best improves recovery behavior?**

**Options:**

- Configure the agent to retry every failed refund operation three times before showing the final error to the customer.
- Disable automatic retries for process_refund and escalate all failed refund attempts to avoid duplicate backend operations.
- **Add errorCategory and isRetryable fields to tool failures, retrying only failures marked retryable and preserving user-facing explanations.**  ✅
- Have the agent inspect failure message wording for timeout or permission keywords before deciding whether another attempt is useful.

**Correct answer:** **Add errorCategory and isRetryable fields to tool failures, retrying only failures marked retryable and preserving user-facing explanations.**

**Explanation:**

Refund handling has intermittent gateway timeouts that often succeed on retry and permanent failures like expired windows or missing permission, but the tool returns the same isError message for both. Add errorCategory and isRetryable fields, retrying only failures marked retryable and preserving user-facing explanations. Fixed retry counts waste attempts on permanent failures, parsing message wording is brittle when text changes, and escalating all failures undermines first-contact resolution. Base retry behavior on explicit semantics, not a generic failed status.

---

## Q47  ·  Set 3 Question 29

*Domain: Agentic Architecture & Orchestration*

**During a pilot, the coordinator verifies a customer, retrieves two recent orders, and then delegates separate billing-dispute and returns-policy checks. The delegated analyses frequently state that the customer ID or order status is unknown, even though those facts were available earlier in the coordinator's turn. The coordinator currently sends each delegated check only a brief task title such as "evaluate refund eligibility." What change would most reliably improve the delegated analyses?**

**Options:**

- **Include the relevant verified customer facts, order details, and prior tool outputs directly in every delegated Task prompt.**  ✅
- Have subagents select customer and order records heuristically from names when required identifiers are missing from their prompts.
- Add few-shot examples instructing subagents to remember earlier coordinator turns during billing and return eligibility analysis.
- Increase the coordinator's conversation token budget so earlier verification and order lookup results remain available in session.

**Correct answer:** **Include the relevant verified customer facts, order details, and prior tool outputs directly in every delegated Task prompt.**

**Explanation:**

get_customer and lookup_order succeed and are recorded in server-side logs, but the agent re-asks for identifiers and repeats lookups instead of deciding. Append each executed tool result to the conversation history using the matching tool_use_id before sending the next model request. Claude can't see backend logs or local application variables unless those results are in the messages you send back. Keeping results only in app state hides the facts, an assistant-text completion signal is unreliable, and a fixed tool sequence can't adapt. Each request must carry the relevant conversation state.

---

## Q48  ·  Set 3 Question 33

*Domain: Agentic Architecture & Orchestration*

**A customer support agent has MCP tools `get_customer`, `lookup_order`, `process_refund`, and `escalate_to_human`. During a billing-dispute pilot, `get_customer` correctly verifies the caller, and `lookup_order` sometimes returns an order tied to a different customer ID because family members share names. The required workflow says refunds must only be issued when the verified customer ID matches the order owner, otherwise the case goes to a human. Logs show Claude usually follows this, but occasionally calls `process_refund` after a persuasive customer message. What change best improves reliability?**

**Options:**

- Strengthen the system prompt to emphasize that ownership mismatches always require escalation before any refund is issued.
- **Add a stateful prerequisite gate that blocks process_refund unless verified customer and order owner IDs match, then escalates mismatches.**  ✅
- Add few-shot examples where persuasive customers with mismatched accounts receive apologies and are transferred without refunds.
- Parse the assistant response for phrases like verified owner before allowing process_refund to run in production.

**Correct answer:** **Add a stateful prerequisite gate that blocks process_refund unless verified customer and order owner IDs match, then escalates mismatches.**

**Explanation:**

Refunds must only issue when the verified customer ID matches the order owner, but a persuasive message occasionally gets process_refund called on a mismatch caused by shared family names. Add a stateful prerequisite gate that blocks process_refund unless verified customer and order owner IDs match, then escalates mismatches. Prompts and few-shot examples can't guarantee the check under persuasive wording, and parsing assistant text for "verified owner" isn't a stable interface. Enforce must-not-violate rules with structured state and gates, not guidance.

---

## Q49  ·  Set 3 Question 36

*Domain: Tool Design & MCP Integration*

**While updating the agent’s refund-policy behavior, you need to inspect only the files related to policy configuration and tests. The repository is large, and relevant files are spread across several packages with naming patterns such as return-policy.yaml, refund-policy.test.ts, and policy-overrides.json. What should you do first to locate the relevant files efficiently?**

**Options:**

- Use Grep for policy filename patterns across the repository, then Read every returned match before editing.
- Use Bash to recursively list the repository, then inspect unstructured terminal output for policy filenames.
- **Use Glob with targeted filename patterns, then Read only matching policy and test files before editing.**  ✅
- Use Read on each directory’s configuration files first, then manually decide which refund policy files matter.

**Correct answer:** **Use Glob with targeted filename patterns, then Read only matching policy and test files before editing.**

**Explanation:**

Policy and test files are spread across packages with names like return-policy.yaml, refund-policy.test.ts, and policy-overrides.json. Use Glob with targeted filename patterns, then Read only the matching policy and test files before editing. Grep searches contents and is the wrong primary tool when the selection criterion is the path itself, recursive Bash listings dump unstructured output, and reading broad directory contents pushes irrelevant material into context. Use the most constrained tool: Glob for path patterns, Grep for content, Read after narrowing.

---

## Q50  ·  Set 3 Question 38

*Domain: Agentic Architecture & Orchestration*

**Production review finds several billing dispute cases where the agent correctly verifies the customer and order, then attempts to call process_refund for amounts above your policy limit. Company policy allows autonomous refunds up to $500, but larger refunds require human approval before any financial action occurs. What change would most reliably prevent policy violations while preserving autonomous handling for allowed refunds?**

**Options:**

- Strengthen the system prompt with a mandatory refund limit rule and examples showing escalation for larger amounts.
- Scan the assistant’s final text for refund amounts above $500 and create an audit alert after completion.
- **Add a tool call interception hook that blocks process_refund above $500 and returns guidance to call escalate_to_human.**  ✅
- Update the process_refund tool description to warn that refunds above $500 are forbidden without human approval.

**Correct answer:** **Add a tool call interception hook that blocks process_refund above $500 and returns guidance to call escalate_to_human.**

**Explanation:**

The agent verifies correctly but tries process_refund above the $500 autonomous limit. Add a tool-call interception hook that blocks process_refund above $500 and returns guidance to call escalate_to_human, so compliant refunds still run autonomously. Prompt-only and description-only rules leave the model to remember and apply the limit every turn, and scanning the final assistant message is brittle and happens after the action may already be complete. Enforce financial policy boundaries deterministically at the tool boundary.

---

## Q51  ·  Set 3 Question 41

*Domain: Agentic Architecture & Orchestration*

**A coordinator delegates complex billing disputes to a case-investigation subagent. Logs show that when order data contains unusual combinations, such as a partial return plus a delayed replacement, the subagent follows the coordinator's embedded seven-step checklist exactly and returns incomplete conclusions instead of adapting. What change would most improve the delegation design?**

**Options:**

- Have the coordinator post-process incomplete subagent reports by guessing missing findings from customer tone and available message text.
- **Rewrite delegated Task prompts to state the support objective, constraints, case facts, and resolution quality criteria, leaving investigation paths flexible.**  ✅
- Keep the checklist but add instructions telling the subagent to ignore any step that seems irrelevant or outdated.
- Create separate subagents for every order status so the coordinator can route each case to a fixed procedure.

**Correct answer:** **Rewrite delegated Task prompts to state the support objective, constraints, case facts, and resolution quality criteria, leaving investigation paths flexible.**

**Explanation:**

An embedded seven-step checklist makes the investigation subagent follow steps rigidly and return incomplete conclusions on unusual order combinations like a partial return plus a delayed replacement. Rewrite delegated Task prompts to state the objective, constraints, case facts, and resolution quality criteria, leaving the investigation path flexible. Post-processing by guessing from customer tone fabricates findings, a checklist with "ignore irrelevant steps" creates contradictory instructions, and a subagent per order status is brittle and complex. The coordinator sets goals and context while the subagent adapts the path.

---

## Q52  ·  Set 3 Question 46

*Domain: Tool Design & MCP Integration*

**A newly connected returns-policy MCP server exposes a returns_helper tool. In production traces, the tool is discovered and works when manually forced, but the agent usually chains lookup_order, asks customers redundant policy questions, or escalates standard return cases. What is the best first change to improve adoption of this MCP capability?**

**Options:**

- **Rewrite returns_helper MCP tool description to specify eligibility inputs, returned fields, examples, and boundaries with refund tools.**  ✅
- Merge returns_helper into process_refund so every refund attempt automatically computes eligibility before performing backend actions.
- Add a keyword router that invokes returns_helper whenever users mention return, exchange, refund, damaged, or late delivery.
- Force returns_helper with tool_choice at the start of every return conversation, then let Claude continue after receiving results.

**Correct answer:** **Rewrite returns_helper MCP tool description to specify eligibility inputs, returned fields, examples, and boundaries with refund tools.**

**Explanation:**

The returns_helper MCP tool works when forced but is rarely chosen, so the agent chains lookup_order, asks redundant policy questions, or escalates standard returns. Rewrite its description to specify eligibility inputs, returned fields, examples, and boundaries with the refund tools. Merging it into process_refund weakens boundaries and adds side-effect risk, a keyword router is brittle for ambiguous return and refund language, and forcing it with tool_choice at the start of every return conversation over-constrains the agent and can misorder calls. Improve the description to preserve model-driven selection.

---

## Q53  ·  Set 3 Question 47

*Domain: Agentic Architecture & Orchestration*

**During a staging test, backend logs show that get_customer returns a verified customer record and lookup_order returns two eligible orders. On the next model request, the agent again asks the customer for the same identifiers and sometimes repeats the same lookup instead of deciding whether to refund or escalate. The tool executor is successfully calling the MCP tools and recording their outputs in server-side logs. What change most directly fixes this loop behavior?**

**Options:**

- Keep tool outputs in application state, then provide Claude a concise natural-language recap only after all tools finish.
- **Append each executed tool result to the conversation history using the matching tool_use_id before sending the next model request.**  ✅
- Run a predetermined get_customer, lookup_order, process_refund sequence and ignore intermediate model turns unless a tool fails.
- Continue the loop until the assistant text says the request is resolved, then suppress further tool calls.

**Correct answer:** **Append each executed tool result to the conversation history using the matching tool_use_id before sending the next model request.**

**Explanation:**

get_customer and lookup_order succeed and are recorded in server-side logs, but the agent re-asks for identifiers because the results were never returned to the model. Append each executed tool result to the conversation history using the matching tool_use_id before sending the next request. Claude cannot see backend logs or local variables unless the results are in the messages. Keeping results only in application state hides necessary facts, relying on assistant text as a completion signal is unreliable, and a fixed tool sequence can't adapt to case-specific outcomes. Every model request must include the new tool results.

---

## Q54  ·  Set 3 Question 52

*Domain: Context Management & Reliability*

**The QA process reviews 2% of auto-resolved tickets chosen uniformly each week. The dashboard shows 96% overall correctness, but refunds later reversed by human supervisors are concentrated in rare marketplace-seller warranty claims and older billing disputes that barely appear in the sample. You need to redesign review without sending every automated resolution to humans. What should you do?**

**Options:**

- Ask the agent to include a single global confidence score, then audit cases closest to the threshold.
- Increase the overall random sample from 2% to 5%, keeping selection uniform across all auto-resolved tickets.
- Stop sampling tickets above the confidence threshold, and review only low-confidence or customer-complaint cases going forward.
- **Use stratified random sampling across issue type, order age, seller channel, and resolution action for high-confidence auto-closures.**  ✅

**Correct answer:** **Use stratified random sampling across issue type, order age, seller channel, and resolution action for high-confidence auto-closures.**

**Explanation:**

Uniform 2% review shows 96% correctness, but reversed refunds concentrate in rare marketplace-seller warranty claims and older billing disputes that barely appear in the sample. Use stratified random sampling across issue type, order age, seller channel, and resolution action for high-confidence auto-closures. Bumping the uniform sample to 5% still under-covers the rare segments, dropping review of high-confidence cases is risky because confidence must be continuously validated, and complaint-driven review detects problems only after customer harm. Aggregate accuracy hides segment-level failures.

---

## Q55  ·  Set 3 Question 53

*Domain: Context Management & Reliability*

**Production review finds the agent routes many frustrated but straightforward damage-replacement cases to escalate_to_human. The tickets usually include phrases like "this is ridiculous" and photos matching your standard replacement policy, but not an explicit request for a human. Which change best improves escalation calibration while preserving customer preference handling?**

**Options:**

- Automatically escalate any message with angry language before investigating, because negative sentiment indicates the case is too complex.
- Require the agent to finish all available investigation steps before honoring any human escalation preference from the customer.
- **Update guidance to acknowledge frustration, proceed with supported resolution steps, and escalate only if the customer again asks for a human.**  ✅
- Have the agent request a self-rated confidence score from itself, escalating when the score falls below a threshold.

**Correct answer:** **Update guidance to acknowledge frustration, proceed with supported resolution steps, and escalate only if the customer again asks for a human.**

**Explanation:**

Frustrated but straightforward damage-replacement cases ("this is ridiculous" with policy-matching photos) get auto-escalated even without a request for a human. Update guidance to acknowledge the frustration, proceed with supported resolution steps, and escalate only if the customer again asks for a human. Auto-escalating on angry language treats tone as a proxy for complexity, forcing all investigation before honoring a human request ignores explicit preference, and a self-rated confidence threshold isn't calibrated. Separate emotional tone from the actual escalation criteria.

---

## Q56  ·  Set 3 Question 55

*Domain: Context Management & Reliability*

**A long-running billing dispute workflow delegates separate investigations for account status, order history, and refund eligibility. The service sometimes restarts after deploying updates. After restart, the coordinator resumes but cannot determine which subagent findings are current, re-runs completed investigations, and occasionally omits evidence needed for escalation handoffs. What design change best improves reliability?**

**Options:**

- Set a fixed limit of one retry per subagent after restarts, then continue with whichever findings return first.
- Store only the final customer response draft after each run, using it as the sole recovery checkpoint.
- Resume the prior coordinator session and ask Claude to reconstruct missing subagent progress from the conversation transcript.
- **Have each subagent export structured state to a known location; the coordinator reloads and injects it when resuming.**  ✅

**Correct answer:** **Have each subagent export structured state to a known location; the coordinator reloads and injects it when resuming.**

**Explanation:**

After restarts, the coordinator can't tell which subagent findings are current, re-runs completed investigations, and omits evidence needed for escalation. Have each subagent export structured state — findings, attempted actions, tool result references, open questions, completion status — to a known location, and have the coordinator reload and inject it when resuming. Session resumption or transcript reconstruction is fragile when contexts are incomplete, retry caps and partial findings manage control flow without preserving information, and saving only the final draft loses provenance. Persist durable structured state for crash recovery.

---

## Q57  ·  Set 3 Question 56

*Domain: Agentic Architecture & Orchestration*

**Production logs show that vague requests such as "my replacement and refund are both wrong" often require different investigation paths after the first backend lookup. Some turn out to be return-status issues, some are duplicate authorization holds, some involve account verification problems, and some combine multiple causes. A fixed workflow is producing unnecessary tool calls on simple cases and missing important branches on unusual cases. Which decomposition strategy should you use?**

**Options:**

- **Begin with a brief fact-gathering pass, then let the coordinator create targeted follow-up subtasks as tool findings reveal the dispute type.**  ✅
- Ask Claude to select one likely dispute category from the opening message, then execute only that category's standard workflow.
- Run every vague case through a fixed sequence covering billing, returns, account access, and refunds before generating the final response.
- Set a maximum of three investigation steps, escalating any case that still lacks a clear resolution after the cap.

**Correct answer:** **Begin with a brief fact-gathering pass, then let the coordinator create targeted follow-up subtasks as tool findings reveal the dispute type.**

**Explanation:**

Vague requests like "my replacement and refund are both wrong" need different paths after the first lookup, so a fixed workflow over-calls on simple cases and misses branches on unusual ones. Begin with a brief fact-gathering pass, then let the coordinator create targeted follow-up subtasks as tool findings reveal the dispute type. Running every case through all checks adds latency and noise, picking one category from the opening message narrows prematurely, and an arbitrary step cap can escalate solvable cases. Use fixed chains for predictable work and adaptive plans for open-ended investigations.

---

## Q58  ·  Set 3 Question 58

*Domain: Agentic Architecture & Orchestration*

**A new refunds policy allows autonomous refunds up to $150. Anything above that amount requires human approval, regardless of customer history, sentiment, or how obvious the case appears. In staging, the agent usually follows the policy but occasionally calls `process_refund` for $175 after reasoning that the customer clearly qualifies. What change best meets the policy requirement before launch?**

**Options:**

- Add few-shot examples where the agent declines refunds above $150 and apologizes before continuing the support conversation.
- **Add a tool call interception hook that blocks process_refund above $150 and redirects the case to human escalation.**  ✅
- Let the agent self-report confidence before each refund and escalate only when confidence falls below a fixed threshold.
- Strengthen the system prompt to state that refunds above $150 must always be escalated before process_refund is used.

**Correct answer:** **Add a tool call interception hook that blocks process_refund above $150 and redirects the case to human escalation.**

**Explanation:**

The agent usually follows the $150 autonomous refund limit but occasionally calls process_refund for $175 after reasoning the customer "clearly qualifies." Add a tool-call interception hook that blocks process_refund above $150 and redirects the case to human escalation. Few-shot examples and a stronger system prompt may reduce violations but can't make them impossible, and a self-reported confidence threshold isn't calibrated to a concrete dollar rule. For hard financial or compliance rules, hooks give deterministic guarantees while prompts and examples give only probabilistic guidance.

---
