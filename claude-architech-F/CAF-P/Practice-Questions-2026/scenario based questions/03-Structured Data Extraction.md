# Scenario: Structured Data Extraction

> You are building a structured data extraction system using Claude. The system extracts information from unstructured documents, validates output using JSON schemas, and maintains high accuracy. It must handle edge cases gracefully and integrate with downstream systems.

Questions for this scenario, collected from Practice Tests 1-3 (Claude Certified Architect - Foundations, v2.0).

**Total questions: 33**

---

## Q1  ·  Set 1 Question 1

*Domain: Prompt Engineering & Structured Output*

**Your extraction QA pass produces JSON records that validate successfully, but reviewers report the findings are hard to act on. Some records describe vague problems like "date issue," others omit where the problem appears, and suggested fixes vary between full sentences, fragments, and empty strings. The downstream ticketing system accepts the records, but reviewers spend significant time interpreting them. What change would most effectively improve consistency?**

**Options:**

- **Add targeted examples showing complete actionable findings with document location, affected field, issue description, severity, and suggested correction.**  ✅
- Add a general instruction requiring concise, high-confidence findings and asking Claude to avoid vague or incomplete reviewer notes.
- Post-process each finding with regular expressions to infer missing locations, severities, and suggested fixes from the text.
- Make every finding field non-null in the schema so validation fails whenever Claude leaves any reviewer detail empty.

**Correct answer:** **Add targeted examples showing complete actionable findings with document location, affected field, issue description, severity, and suggested correction.**

**Explanation:**

The outputs are valid but inconsistent in specificity and format, which is exactly when few-shot examples help. Show targeted examples of a complete finding — document location, affected field, issue description, severity, suggested fix — so Claude generalizes that shape to new documents. A schema can enforce that fields exist but can't show what a useful description looks like, "be concise" is too vague, regex post-processing can't reliably rebuild meaning from inconsistent text, and forcing every field non-null invites fabrication when evidence is genuinely missing.

---

## Q2  ·  Set 1 Question 3

*Domain: Prompt Engineering & Structured Output*

**You are about to process 80,000 archived vendor contracts overnight. A new extraction prompt and schema passed a few hand-picked examples, but historical documents vary by template, scanned OCR quality, and contract addenda. Reprocessing failures delays a downstream migration. What should you do next?**

**Options:**

- Submit the entire workload immediately, then resubmit every failed document after inspecting aggregate completion and error counts.
- Split documents randomly into equal daily batches and tune the prompt only after all batches finish processing.
- Increase max_tokens for all batch requests so longer outputs can handle templates, addenda, and OCR noise more reliably.
- **Run a representative pilot batch, analyze validation failures and null patterns, refine the prompt, then submit the full workload.**  ✅

**Correct answer:** **Run a representative pilot batch, analyze validation failures and null patterns, refine the prompt, then submit the full workload.**

**Explanation:**

A new prompt and schema that only passed a few hand-picked examples will meet real template, OCR, and addenda variation at scale. Run a representative pilot batch first, analyze the validation failures and null patterns, refine the prompt, then submit all 80,000. Submitting everything immediately turns prompt defects into mass cleanup, random daily batches still defer learning and repeat failures, and raising max_tokens only addresses truncation, not extraction quality. Validate at representative scale before the full run.

---

## Q3  ·  Set 1 Question 10

*Domain: Context Management & Reliability*

**A coordinator splits each document into sections and sends them to extraction subagents for fields such as parties, dates, totals, and obligations. During testing, one subagent sometimes loses access to a section-level source system for a few minutes. The current implementation either returns an empty section extraction marked as successful or aborts the entire document extraction, causing downstream systems to misinterpret the document state. What should you change?**

**Options:**

- **Have subagents report unresolved failures with attempted section, failure type, partial fields, and recovery suggestions for coordinator handling.**  ✅
- Return an empty extraction object for the failed section so downstream validators can treat missing fields consistently.
- Terminate the entire document workflow whenever any subagent cannot access its assigned source section.
- Retry the failed section until it succeeds, withholding all partial extractions from downstream systems until completion.

**Correct answer:** **Have subagents report unresolved failures with attempted section, failure type, partial fields, and recovery suggestions for coordinator handling.**

**Explanation:**

A few-minute section-level access failure is currently reported either as a successful empty result or by aborting the whole document. Have subagents report unresolved failures with the attempted section, failure type, partial fields, and recovery suggestions, so the coordinator can retry, use an alternate path, proceed with gaps, or route just that section to review. Empty-as-success creates false completeness, aborting discards good partial work, and blind retry-until-success can stall and hide state. Distinguish a valid empty result from an access failure.

---

## Q4  ·  Set 1 Question 12

*Domain: Prompt Engineering & Structured Output*

**Your extraction QA pass reviews Claude's JSON outputs before downstream ingestion. Reviewers dismiss many findings because the QA prompt flags harmless differences: inferred date formats, optional fields absent from the source, and wording variations that do not change extracted values. The current prompt says, "Check the extraction for accuracy and report any problems." What change would most effectively improve precision?**

**Options:**

- Increase the validation sample size and ask reviewers to manually ignore findings that are not actionable.
- **Rewrite the QA prompt to define reportable errors, acceptable variations, and skip conditions with concrete examples for each category.**  ✅
- Require the QA pass to flag every schema field that is null, even when the source document omits it.
- Add instructions that Claude should be conservative and report only findings where it feels highly confident.

**Correct answer:** **Rewrite the QA prompt to define reportable errors, acceptable variations, and skip conditions with concrete examples for each category.**

**Explanation:**

"Check the extraction for accuracy and report any problems" makes Claude flag harmless formatting and valid nulls. Rewrite the QA prompt to define reportable errors, acceptable variations, and skip conditions, with concrete examples for each category. "Be conservative" or "high-confidence only" don't create real decision boundaries, and flagging every null treats valid absence as an error and can pressure fabrication. Precision comes from concrete decision rules and examples, not broad quality goals.

---

## Q5  ·  Set 1 Question 16

*Domain: Prompt Engineering & Structured Output*

**Reviewers are dismissing many extraction warnings after checking the source documents. Your logs capture the final JSON output, confidence score, document type, and reviewer disposition, but your team cannot tell whether false positives cluster around handwritten totals, scanned tables, ambiguous dates, or other recurring source patterns. What change would best support systematic improvement of the extraction workflow?**

**Options:**

- Retry every dismissed extraction with the reviewer decision appended, then accept the second extraction when confidence increases.
- **Add a detected_pattern field to each structured finding, then analyze dismissal rates by pattern during feedback review.**  ✅
- Raise the minimum confidence threshold for all extraction warnings until reviewer dismissal rates fall below the target.
- Ask reviewers to enter free-text explanations for every dismissal, then manually read comments during quarterly audits.

**Correct answer:** **Add a detected_pattern field to each structured finding, then analyze dismissal rates by pattern during feedback review.**

**Explanation:**

The logs capture outcomes but not the source construct behind each false positive, so the team can't tell whether handwritten totals or scanned tables drive dismissals. Add a detected_pattern field to each finding and analyze dismissal rates by pattern. Blind retries repeat the same mistake without revealing the cause, a global confidence threshold hides the problem and cuts recall in well-performing segments, and free-text notes are too unstructured and slow to aggregate. Capture machine-analyzable metadata at the moment a finding is produced.

---

## Q6  ·  Set 1 Question 19

*Domain: Prompt Engineering & Structured Output*

**Your extraction pipeline uses tool use with a strict schema, so outputs are syntactically valid. However, downstream semantic validators reject some invoices because the extracted line-item totals do not match the stated invoice total, and because a due date was placed in the invoice_date field. The current retry simply sends the document again with "fix the extraction," and the same fields often remain wrong. What change would most effectively improve recoverable correction quality?**

**Options:**

- Loosen the downstream validators so line-item total mismatches and date-field swaps become warnings instead of failures.
- Ask Claude to provide a confidence score for each field and retry only fields below a chosen threshold.
- **Send a follow-up request containing the document, failed extraction, and exact validation errors for targeted self-correction.**  ✅
- Retry the original extraction prompt with a lower temperature and discard the failed output before revalidating.

**Correct answer:** **Send a follow-up request containing the document, failed extraction, and exact validation errors for targeted self-correction.**

**Explanation:**

Sending the document again with "fix the extraction" keeps producing the same errors. Send a follow-up that includes the source, the failed extraction, and the exact validation errors (totals don't sum, due date placed in invoice_date) so Claude can target the recoverable problems. A strict schema prevents syntax errors but not semantic ones, lower temperature or per-field confidence scores don't communicate what failed, and loosening the validators just lets bad data reach downstream systems. Turn validator failures into actionable feedback.

---

## Q7  ·  Set 1 Question 21

*Domain: Context Management & Reliability*

**A labeled validation run reports 97.2% aggregate extraction accuracy across NDAs, invoices, insurance forms, and purchase orders. Leadership wants to bypass human review for any record where Claude returns high confidence, but pilot complaints suggest errors cluster in specific document families and fields. What should you do before reducing reviewer coverage?**

**Options:**

- **Analyze accuracy by document type and extracted field, then automate only segments meeting validated thresholds while routing others to review.**  ✅
- Raise the global confidence threshold until the aggregate validation accuracy reaches 99%, then disable review for remaining outputs.
- Randomly review a fixed percentage of every extraction category, regardless of document type, field, or prior validation performance.
- Use the 97.2% aggregate accuracy to auto-approve all high-confidence outputs, monitoring user complaints for emerging regressions.

**Correct answer:** **Analyze accuracy by document type and extracted field, then automate only segments meeting validated thresholds while routing others to review.**

**Explanation:**

A 97.2% aggregate hides clusters of errors in specific document families and fields. Analyze accuracy by document type and field, automate only the segments that meet validated thresholds, and keep routing the rest to review. A higher global confidence threshold doesn't prove each segment is reliable, uniform random review ignores known risk differences, and trusting the aggregate while watching for complaints makes customers the error detector. Confidence must be calibrated at the segment level before review is reduced.

---

## Q8  ·  Set 1 Question 33

*Domain: Prompt Engineering & Structured Output*

**Your invoice extractor currently asks Claude to "return valid JSON" with fields for vendor, invoice_date, line_items, and total_amount. In production, a small but persistent share of responses include markdown fences, explanatory text, or malformed commas, causing downstream parsers to reject otherwise correct extractions. What change would most effectively improve structured output reliability?**

**Options:**

- **Define an extraction tool with a JSON schema for target fields, then consume the structured tool_use input directly.**  ✅
- Keep requesting JSON only, then strip markdown fences and trailing prose with regular expressions before parsing.
- Use assistant prefill with an opening brace and stop sequences, then parse the generated text as JSON.
- Add stronger prompt wording that forbids explanations, examples, markdown, comments, and any non-JSON characters in every response.

**Correct answer:** **Define an extraction tool with a JSON schema for target fields, then consume the structured tool_use input directly.**

**Explanation:**

Asking for "valid JSON" still yields occasional markdown fences, stray prose, and malformed commas that break parsers. Define an extraction tool with a JSON schema and consume the structured tool_use input directly, so the app reads structured arguments instead of scraping text. Regex cleanup is a brittle repair layer that can silently corrupt data, prefill plus stop sequences still produces text to parse, and stronger wording can't guarantee syntax or schema compliance. Don't treat machine-readable output as ordinary prose.

---

## Q9  ·  Set 1 Question 34

*Domain: Prompt Engineering & Structured Output*

**Your extraction pipeline includes a QA pass that flags possible mistakes in supplier contract records before they enter the downstream procurement system. Over the last month, procurement analysts accepted many findings about missing renewal clauses but overturned most findings involving informal pricing language. Current logs store only document ID, field name, confidence, and finding text, making it difficult to prioritize prompt and validator improvements. What change should you make first?**

**Options:**

- Add a system prompt instruction telling Claude to report only findings that procurement analysts would likely accept.
- Store only analyst accept or reject decisions per document, then randomly sample overturned findings for manual discussion.
- **Add a structured detected_pattern field to each QA finding, then analyze acceptance rates by pattern and document type.**  ✅
- Increase the QA confidence threshold globally, suppressing all lower-confidence findings before analysts review extracted contract records.

**Correct answer:** **Add a structured detected_pattern field to each QA finding, then analyze acceptance rates by pattern and document type.**

**Explanation:**

The logs store only document ID, field, confidence, and text, so the team can't tell why informal-pricing findings get overturned while renewal-clause findings are accepted. Add a structured detected_pattern field and analyze acceptance rates by pattern and document type. A "report only likely-accepted findings" instruction relies on Claude predicting reviewers, a global threshold cuts signal without explaining failures, and accept/reject labels alone lack the cause. Record why a finding was produced, not just whether it was accepted.

---

## Q10  ·  Set 1 Question 35

*Domain: Context Management & Reliability*

**Production review shows inconsistent routing: documents with unreadable required values and unfamiliar layouts sometimes flow into downstream systems, while routine invoices missing optional purchase-order numbers are sent for manual review. The extraction schema already permits nullable fields for data that is absent from the source. What change would most effectively improve routing decisions?**

**Options:**

- Escalate documents based on frustrated wording, urgent language, or negative sentiment detected in the source text.
- Require retries until all schema fields are populated, then escalate only documents still containing null values.
- Route documents to reviewers whenever the model reports confidence below a single global threshold after extraction.
- **Add explicit human-review criteria with few-shot examples distinguishing absent optional fields, unreadable required fields, and unsupported document types.**  ✅

**Correct answer:** **Add explicit human-review criteria with few-shot examples distinguishing absent optional fields, unreadable required fields, and unsupported document types.**

**Explanation:**

Routing is inconsistent — unreadable required values flow downstream while routine invoices missing an optional PO number go to review. Add explicit human-review criteria with few-shot examples distinguishing absent optional fields, unreadable required fields, and unsupported document types. Sentiment-based escalation and a single global confidence threshold don't measure extraction risk, and retrying until every field is populated pressures the model to invent values. Use specific decision boundaries; nullable optional fields can be passed downstream.

---

## Q11  ·  Set 1 Question 41

*Domain: Prompt Engineering & Structured Output*

**During evaluation, the extraction pipeline handles supplier contracts by first asking Claude to infer document-specific extraction rules, then asking the same conversation to review the resulting field values. Human auditors find that the review step often misses subtle errors introduced by the inferred rules, such as treating renewal notice dates as contract end dates. You need to improve review effectiveness without changing the extraction schema. What architecture should you use?**

**Options:**

- **Run a separate Claude review instance with the source document, extracted fields, and rubric, excluding the original extraction reasoning.**  ✅
- Ask the same conversation to self-critique its extraction using extended thinking and a stricter instruction to find mistakes.
- Append the extraction rationale to the review prompt so Claude can verify whether each reasoning step was internally consistent.
- Run three self-review turns in the original conversation and accept fields only when all turns report high confidence.

**Correct answer:** **Run a separate Claude review instance with the source document, extracted fields, and rubric, excluding the original extraction reasoning.**

**Explanation:**

The same conversation that inferred the extraction rules also reviews them, so it inherits its own mistakes, like treating a renewal notice date as the contract end date. Run a separate Claude review instance given only the source document, extracted fields, and rubric, excluding the original reasoning. Self-critique, extended thinking, or repeated self-review turns keep the original assumptions, and appending the rationale pushes the reviewer toward checking internal consistency instead of source-grounded correctness. Isolate the review context.

---

## Q12  ·  Set 1 Question 50

*Domain: Prompt Engineering & Structured Output*

**Your QA prompt reviews a 90-page vendor onboarding packet and its extracted records in one call. It catches detailed field errors in the first few forms, but misses mismatched tax IDs in middle attachments and contradicts itself about required signatures. Which review architecture would best improve reliability?**

**Options:**

- Run three full-packet reviews and accept only issues reported by at least two reviewers.
- Increase max_tokens and add stronger instructions to be exhaustive while reviewing the entire packet once.
- Ask the same extraction instance to critique its own output using extended thinking before returning final records.
- **Run focused review passes on each packet section, then run a separate consistency pass across cross-section fields.**  ✅

**Correct answer:** **Run focused review passes on each packet section, then run a separate consistency pass across cross-section fields.**

**Explanation:**

One call reviewing a 90-page packet catches early errors but misses middle ones and contradicts itself. Run focused review passes per section, then a separate consistency pass across cross-section fields such as tax IDs, signatures, and dates. Self-review by the same instance preserves its original assumptions, more max_tokens doesn't fix uneven attention over long inputs, and majority voting filters out valid findings that appear inconsistently. Separate local validation from global consistency analysis.

---

## Q13  ·  Set 1 Question 52

*Domain: Prompt Engineering & Structured Output*

**In validation runs, 18% of supplier contracts return null for effective_date and renewal_terms even though human reviewers find the information present. The misses cluster in documents where dates and renewal language appear in cover letters, footnotes, or table captions rather than standard contract header sections. Outputs are otherwise schema-valid, and downstream systems can accept null only when the source truly omits the field. What change would most improve extraction accuracy?**

**Options:**

- Append a rule telling Claude that null values are unacceptable whenever the document is classified as a supplier contract.
- Retry every extraction with null fields until the model returns populated values for all contract metadata fields.
- Change the schema to make effective_date and renewal_terms required non-null fields, rejecting outputs that leave either value empty.
- **Add targeted few-shot examples showing the fields extracted from cover-letter text, footnotes, and table captions with brief rationale.**  ✅

**Correct answer:** **Add targeted few-shot examples showing the fields extracted from cover-letter text, footnotes, and table captions with brief rationale.**

**Explanation:**

18% of contracts return null for fields that actually exist but appear in cover letters, footnotes, or table captions instead of standard headers. Add targeted few-shot examples showing those fields extracted from those unusual locations, with brief rationale, while preserving genuine nulls. Making the fields non-null, banning nulls by instruction, or retrying until values appear all convert uncertainty into hallucinated data. The problem is recognizing facts outside conventional sections, which examples teach better than schema constraints.

---

## Q14  ·  Set 1 Question 53

*Domain: Prompt Engineering & Structured Output*

**Your product has two document queues: customer onboarding forms that must populate an eligibility screen while an operations specialist is waiting, and 40,000 archived contracts used for a dashboard due next week. Finance asks whether the lower-cost processing path should replace the current real-time calls for both queues. What should you recommend?**

**Options:**

- Move both queues to the Message Batches API, polling frequently so urgent onboarding jobs usually finish quickly.
- Keep both queues on synchronous calls, since batch responses cannot be reliably matched back to submitted documents.
- Route onboarding forms to batches first, then fall back to synchronous calls whenever pending jobs exceed a threshold.
- **Keep synchronous calls for onboarding forms, and use the Message Batches API for historical contracts with latency-tolerant processing.**  ✅

**Correct answer:** **Keep synchronous calls for onboarding forms, and use the Message Batches API for historical contracts with latency-tolerant processing.**

**Explanation:**

Match the processing mode to the latency requirement. The onboarding queue blocks a waiting specialist, so keep synchronous calls; the 40,000 archived contracts are latency-tolerant, so use the Message Batches API to cut cost. Polling batches frequently doesn't make them interactive since they can take up to 24 hours, a threshold fallback still sends urgent items into a path with no latency guarantee, and avoiding batches over correlation fears is a false premise — custom_id matches each result back to its document.

---

## Q15  ·  Set 1 Question 54

*Domain: Prompt Engineering & Structured Output*

**Your invoice extraction pipeline already returns syntactically valid structured objects, but semantic validators reject about 7% of documents because line-item totals do not sum to the stated total or normalized dates fail business rules. Most rejected documents contain the needed values, but the model placed or formatted them incorrectly. What should you change to recover these cases while preserving validation rigor?**

**Options:**

- **Send a follow-up request containing the source document, failed extraction, and precise validator messages for targeted correction.**  ✅
- Retry the original extraction prompt up to three times, accepting the first response that passes schema validation.
- Ask Claude to explain likely extraction mistakes in natural language, then parse that explanation to update records.
- Loosen the JSON schema by making rejected fields nullable, then route missing values to downstream reconciliation jobs.

**Correct answer:** **Send a follow-up request containing the source document, failed extraction, and precise validator messages for targeted correction.**

**Explanation:**

About 7% fail because the values exist but were misplaced or misformatted. Send a follow-up request with the source document, the failed extraction, and the precise validator messages for targeted correction. Blind retries with an arbitrary cap give no actionable information, loosening the schema to nullable weakens data-quality guarantees, and parsing a natural-language explanation is a brittle integration. Keep validation strict while giving the model a precise opportunity to repair recoverable errors.

---

## Q16  ·  Set 2 Question 9

*Domain: Context Management & Reliability*

**During a month-long effort to improve your extraction pipeline, Claude Code has explored parsers, JSON schema definitions, validation utilities, fixture documents, and downstream mapping code. After several long sessions, it starts giving answers based on generic extraction patterns rather than specific files it already inspected, and teammates joining later cannot reliably recover the earlier discoveries. What should you do to make later exploration and follow-up changes more reliable?**

**Options:**

- **Have Claude maintain a repository scratchpad file recording discovered schemas, validators, edge cases, and file paths for future reference.**  ✅
- Rely on /compact whenever context grows, trusting the compressed conversation to preserve every schema detail and exception.
- Continue the same session indefinitely, adding reminders in chat whenever Claude overlooks a previously discovered mapping.
- Ask Claude to reread the entire extractor codebase before each new change to refresh all implementation details.

**Correct answer:** **Have Claude maintain a repository scratchpad file recording discovered schemas, validators, edge cases, and file paths for future reference.**

**Explanation:**

After a month of exploration, findings buried in long sessions degrade and teammates can't recover the earlier discoveries. Have Claude maintain a repository scratchpad file recording discovered schemas, validators, edge cases, and file paths for future reference. /compact isn't a reliable record of detailed findings, rereading the entire codebase before each change wastes context and dilutes attention, and continuing one session indefinitely makes the degradation worse. Move critical state out of the transient conversation into a persistent artifact.

---

## Q17  ·  Set 2 Question 25

*Domain: Context Management & Reliability*

**A pilot processes 30 contracts per run. Accuracy is high on early documents but declines later: clauses copied from earlier contracts appear in later extractions, and page references from middle documents are dropped. Trace logs show raw outputs from OCR, table parsing, and validation tools dominate the request history, including coordinates, styling data, alternate OCR hypotheses, debug IDs, and validator traces. Downstream extraction only uses clause text, page number, document ID, confidence, and validation status. The operations team also needs original tool responses available for traceability. What change best addresses the reliability problem?**

**Options:**

- Replace accumulated tool results with brief prose summaries after every fixed batch of five processed documents.
- Increase max_tokens and reduce each request to fewer documents while leaving the tool result payloads unchanged.
- Keep all raw tool outputs in conversation history so Claude can independently determine which details remain important.
- **Add a preprocessing layer that stores full tool outputs externally and appends only schema-relevant fields and provenance to conversation history.**  ✅

**Correct answer:** **Add a preprocessing layer that stores full tool outputs externally and appends only schema-relevant fields and provenance to conversation history.**

**Explanation:**

Raw OCR, table, and validator payloads (coordinates, styling, alternate hypotheses, debug IDs) dominate the request history, causing clause bleed and dropped page references, but operations still needs the raw outputs for traceability. Add a preprocessing layer that stores full tool outputs externally and appends only schema-relevant fields plus provenance to the conversation. Prose summaries blur exact numbers, dates, and confidence values, and raising max_tokens or shrinking batches only treats symptoms. Manage what enters the context rather than hoping the model ignores noise.

---

## Q18  ·  Set 2 Question 28

*Domain: Prompt Engineering & Structured Output*

**A nightly extraction job processes supplier contracts into a structured record for downstream procurement systems. Validation now rejects many records because renewal dates are earlier than start dates, currency codes are copied into amount fields, and a required payment_terms field is filled with plausible but unsupported values. The current retry prompt says only, "Fix the invalid fields and return the corrected record." Which change would most effectively improve recoverable retry quality?**

**Options:**

- Apply deterministic post-processing rules that swap invalid dates and blank unsupported fields before sending records downstream.
- **Retry with the source document, rejected extraction, and exact validator messages, instructing Claude to produce a corrected record only.**  ✅
- Increase the retry count and ask Claude to be more careful until the record passes all procurement validations.
- Retry with only the validator messages, omitting the contract text to reduce context size and focus correction effort.

**Correct answer:** **Retry with the source document, rejected extraction, and exact validator messages, instructing Claude to produce a corrected record only.**

**Explanation:**

"Fix the invalid fields and return the corrected record" keeps repeating the same errors. Retry with the source document, the rejected extraction, and the exact validator messages, instructing Claude to return only the corrected record, so it can fix date relationships and remove unsupported values. Sending only the validator messages removes the source evidence, deterministic patching produces superficially valid but incorrect records, and more retries with "be careful" rely on repetition rather than feedback. Retries work for recoverable errors when the evidence is present.

---

## Q19  ·  Set 2 Question 30

*Domain: Prompt Engineering & Structured Output*

**Your extraction schema classifies vendor contract clauses using a required enum: termination, indemnity, liability, confidentiality, payment. In validation logs, unusual clauses are being forced into the nearest allowed category, while genuinely ambiguous clauses are returned with confident but inconsistent labels. Downstream analytics need stable categories without losing information from unexpected clause types. What schema adjustment best handles these edge cases?**

**Options:**

- Make category a required unrestricted string so Claude can invent precise labels for every unexpected clause type.
- **Add enum values for ambiguous cases and a fallback category paired with a required free-text detail field.**  ✅
- Remove the category field and rely on downstream systems to infer classifications from extracted clause text.
- Keep the closed enum and instruct Claude to choose the closest category whenever the source is unclear.

**Correct answer:** **Add enum values for ambiguous cases and a fallback category paired with a required free-text detail field.**

**Explanation:**

A closed enum forces unusual clauses into the nearest category and labels genuinely ambiguous ones inconsistently. Add enum values for ambiguous cases and a fallback category (other) paired with a required free-text detail field, so the model can represent uncertainty and taxonomy gaps. An unrestricted string loses normalization and causes label drift, forcing the closest value creates schema-valid but misleading data, and removing the field eliminates the structured signal analytics need. Keep normalized categories but add safe escape hatches.

---

## Q20  ·  Set 2 Question 31

*Domain: Prompt Engineering & Structured Output*

**A QA prompt flags extraction problems before records reach reviewers. In pilot results, most total-mismatch and missing-signature findings are confirmed, but a new "possible payment-term ambiguity" category is usually dismissed. Reviewers now skim the entire finding feed and miss confirmed total mismatches. What should you change first?**

**Options:**

- Increase the sample size in aggregate accuracy reports and reassure reviewers that overall precision remains above launch targets.
- **Separate findings by category and severity, tighten criteria for noisy checks, and prioritize high-precision issues in reviewer queues.**  ✅
- Combine all findings into one confidence-sorted queue, instructing reviewers to ignore any item that appears low impact.
- Add a global "be conservative" instruction and suppress findings whenever Claude reports confidence below a fixed threshold.

**Correct answer:** **Separate findings by category and severity, tighten criteria for noisy checks, and prioritize high-precision issues in reviewer queues.**

**Explanation:**

One noisy "payment-term ambiguity" category is usually dismissed, so reviewers now skim the whole feed and miss confirmed total mismatches. Separate findings by category and severity, tighten the criteria for the noisy check, and prioritize high-precision issues in the queue. Reviewer trust is category-sensitive — visible false positives in one category contaminate trust in accurate ones. A larger aggregate report, a single confidence-sorted queue, or a vague "be conservative" threshold don't address that root cause.

---

## Q21  ·  Set 2 Question 40

*Domain: Prompt Engineering & Structured Output*

**Your nightly run submits 30,000 document extraction requests. The result processing job must update the correct downstream record for each successful extraction and resubmit only the documents that failed validation or exceeded context limits. During testing, engineers notice that relying on the result file's line order creates occasional mismatches after retries and partial failure handling. What design should you use?**

**Options:**

- Submit one combined request containing all documents, so every extraction and failure appears in a single ordered output.
- Assume batch results preserve submission order, then join each response to the original manifest by its array position.
- **Assign a stable custom_id derived from each document record, persist it with request metadata, and reconcile results using that identifier.**  ✅
- Ask Claude to include the source filename in every extraction, then parse that field when processing failures.

**Correct answer:** **Assign a stable custom_id derived from each document record, persist it with request metadata, and reconcile results using that identifier.**

**Explanation:**

Relying on the result file's line order causes mismatches after retries and partial-failure handling. Assign a stable custom_id derived from each document record, persist it with the request metadata, and reconcile results using that identifier. Array-position joins become fragile when batches are retried, filtered, or partially reprocessed; parsing a model-generated filename is unreliable, especially for failed responses; and combining all documents into one request weakens per-document failure handling. Correlate on stable metadata, not output order or generated text.

---

## Q22  ·  Set 2 Question 45

*Domain: Prompt Engineering & Structured Output*

**Reviewers receive structured QA findings about extracted contract fields before downstream loading. After two weeks, audits show that most categories are useful, but findings labeled "ambiguous payment terms" are dismissed in 68% of reviews because the source wording is often acceptable. Reviewers have started ignoring the entire QA feed, including accurate findings about unsupported totals and missing effective dates. What should you do next?**

**Options:**

- Keep all finding categories active and ask reviewers to dismiss incorrect items until enough data accumulates.
- **Temporarily suppress the ambiguous payment terms category while refining its criteria and examples before re-enabling it.**  ✅
- Raise the global confidence threshold for all QA findings until the overall volume drops to an acceptable level.
- Add a general instruction telling Claude to be conservative and report only findings it is highly confident about.

**Correct answer:** **Temporarily suppress the ambiguous payment terms category while refining its criteria and examples before re-enabling it.**

**Explanation:**

The "ambiguous payment terms" category is dismissed in 68% of reviews and is destroying trust in otherwise accurate findings. Temporarily suppress that category while you refine its criteria and examples, then re-enable it, preserving reviewer attention for the categories that already work. Raising a global threshold cuts useful findings across all categories, a broad "be conservative" instruction doesn't define the decision boundary, and leaving the noisy category active teaches reviewers to ignore the entire feed. A high-false-positive category contaminates trust in the whole system.

---

## Q23  ·  Set 2 Question 56

*Domain: Context Management & Reliability*

**During consolidation of extracted obligations from 60 supplier contracts, the final dataset correctly groups duplicate obligations across documents. However, auditors cannot determine which contract clauses support each normalized obligation, and reviewers must reopen every source file to verify disputed entries. What change would best improve reliability without preventing consolidation?**

**Options:**

- Concatenate all document summaries before consolidation and ask Claude to regenerate citations for the final normalized obligations.
- Keep only the highest-confidence extraction for each obligation and discard lower-confidence duplicates during the consolidation step.
- Store source document names at the batch level only, then rely on reviewers to infer relevant clauses when needed.
- **Require each extracted obligation to carry source identifiers and excerpts, then merge duplicates while retaining every supporting reference.**  ✅

**Correct answer:** **Require each extracted obligation to carry source identifiers and excerpts, then merge duplicates while retaining every supporting reference.**

**Explanation:**

Consolidation groups duplicate obligations correctly, but auditors can't tell which clauses support each one and must reopen every file. Require each extracted obligation to carry source identifiers and excerpts, then merge duplicates while retaining every supporting reference. Keeping only the highest-confidence extraction discards corroboration and treats confidence as proof, regenerating citations from summaries risks fabricated references, and batch-level source names are too coarse for obligation-level verification. Consolidation and traceability are not opposites.

---

## Q24  ·  Set 2 Question 58

*Domain: Prompt Engineering & Structured Output*

**In a pilot, 6% of procurement packet extractions fail semantic validation because the required approval date is missing. Reviewer audit shows the provided PDFs say "approval letter on file," but the approval letters were not included in the model input. Retrying the same documents often produces plausible but unsupported dates. Which adjustment best improves extraction reliability?**

**Options:**

- Require the approval_date field and instruct Claude to infer it from nearby signature dates when no explicit date exists.
- **Detect source absence after validation, stop automated retries, mark extraction incomplete, and request the missing approval letter.**  ✅
- Add examples of varied approval letter layouts and rerun extraction unchanged against the same uploaded procurement PDFs.
- Retry failed documents up to five times with increasingly explicit prompts, then accept the most frequent date returned.

**Correct answer:** **Detect source absence after validation, stop automated retries, mark extraction incomplete, and request the missing approval letter.**

**Explanation:**

The approval letters were never in the model input ("approval letter on file"), so retries invent plausible but unsupported dates. Detect the source-absence condition after validation, stop automated retries, mark the extraction incomplete with a reason like missing_source, and request the missing letter. Required fields or "infer from nearby signature dates" pressure the model to fabricate, and retry caps with majority-vote selection launder hallucinated values into stable-looking outputs. Retry helps only when the evidence exists; otherwise request the source.

---

## Q25  ·  Set 3 Question 7

*Domain: Context Management & Reliability*

**A pipeline extracts insurance policy exclusions from packets containing the policy, riders, emails, and broker notes. The first pass captures detailed snippets, but a middle step condenses each packet into a short narrative before final JSON extraction. Audit reviewers find accurate-looking exclusions in final records, but they cannot determine which document or passage supports each exclusion, especially when riders override earlier policy language. What change best addresses this failure mode?**

**Options:**

- Ask Claude to include citations only for exclusions it considers uncertain, keeping straightforward final records easier to read.
- Increase the final synthesis context budget so Claude can reread all original packet documents before producing each JSON record.
- Append a packet-level bibliography to every final JSON record so reviewers can manually search likely source documents.
- **Change intermediate handoffs so each extracted fact carries its source document, location, and supporting excerpt into final synthesis.**  ✅

**Correct answer:** **Change intermediate handoffs so each extracted fact carries its source document, location, and supporting excerpt into final synthesis.**

**Explanation:**

A middle summarization step flattens evidence, so final exclusions can't be traced to a document or passage, especially when riders override earlier policy language. Change the intermediate handoffs so each extracted fact carries its source document, location, and supporting excerpt into final synthesis. A packet-level bibliography lists possible sources without linking specific fields to evidence, more final-step context doesn't restore provenance the summary already dropped, and citing only uncertain exclusions is unreliable. Make provenance part of the data contract, not a later add-on.

---

## Q26  ·  Set 3 Question 13

*Domain: Context Management & Reliability*

**Your pipeline extracts obligations from vendor contracts, policy memos, and meeting notes into a consolidated compliance matrix. Reviewers find that when two sources support the same obligation with slightly different wording, final rows contain a polished obligation statement and a bibliography list, but no row-level evidence trail. Auditors reject several rows because they cannot verify which excerpts were merged into each statement. What should you change?**

**Options:**

- Store the full input documents alongside the final matrix and instruct auditors to search them when evidence is needed.
- Choose the highest-confidence source for each obligation during deduplication and discard lower-confidence supporting excerpts before synthesis.
- **Require each extracted obligation to carry source excerpts and locations, then preserve and merge that evidence into each synthesized matrix row.**  ✅
- Add a final verification prompt asking Claude to reconstruct citations for each matrix row after synthesis is complete.

**Correct answer:** **Require each extracted obligation to carry source excerpts and locations, then preserve and merge that evidence into each synthesized matrix row.**

**Explanation:**

Final rows have a polished statement and a bibliography but no row-level evidence trail, so auditors reject them. Require each extracted obligation to carry source excerpts and locations, then preserve and merge that evidence into each synthesized matrix row. Reconstructing citations after synthesis risks plausible but incorrect attribution, storing whole documents pushes verification work onto auditors, and keeping only the highest-confidence source discards corroboration and hides source diversity. Maintain attribution as structured data, not recreated from memory.

---

## Q27  ·  Set 3 Question 15

*Domain: Prompt Engineering & Structured Output*

**Your extraction tool captures payment_method using a JSON Schema enum of credit_card, ach, wire, and check. In validation logs, documents with wording like "paid through marketplace balance" or no stated payment method either fail enum validation or get coerced into one of the existing categories, which misleads downstream reporting. What schema change best handles these edge cases while preserving structured categories?**

**Options:**

- **Extend the enum with unclear and other, plus a required detail field when other is selected.**  ✅
- Replace the enum with an unrestricted string so novel payment descriptions pass validation without schema changes.
- Reject any document containing unfamiliar payment wording and route it directly to human review before extraction.
- Force Claude to choose the closest existing enum value and add a confidence score for downstream filtering.

**Correct answer:** **Extend the enum with unclear and other, plus a required detail field when other is selected.**

**Explanation:**

The payment_method enum either fails validation or coerces wording like "paid through marketplace balance" into a wrong category. Extend the enum with unclear and other, plus a required detail field when other is selected, so the schema can represent missing, ambiguous, and novel values. An unrestricted string weakens validation and aggregation, rejecting all unfamiliar wording wastes reviewer capacity, and forcing the closest value creates false precision that corrupts analytics. Keep structured categories but admit ambiguity and extensibility.

---

## Q28  ·  Set 3 Question 22

*Domain: Prompt Engineering & Structured Output*

**Your extractor processes vendor contracts and outputs schema-valid records, but downstream reviewers report that obligation summaries vary from terse fragments to long paraphrases, evidence snippets sometimes include irrelevant surrounding text, and action_owner wording is inconsistent. The prompt already contains detailed field definitions and length guidance, but changes have not stabilized outputs. What should you do next?**

**Options:**

- Set temperature to zero and rely on deterministic decoding to standardize all reviewer-facing extraction wording across documents.
- Expand the field descriptions with stricter prose rules for every obligation type, then ask Claude to be more consistent.
- Reject any record whose summaries exceed a fixed word limit, then rerun the full document automatically.
- **Add 2 to 4 representative input and ideal output examples showing concise obligations, evidence boundaries, and owner wording.**  ✅

**Correct answer:** **Add 2 to 4 representative input and ideal output examples showing concise obligations, evidence boundaries, and owner wording.**

**Explanation:**

Detailed field definitions and length guidance haven't stabilized the summary wording, evidence boundaries, or owner labels. Add 2 to 4 representative input and ideal-output examples showing concise obligations, bounded evidence snippets, and consistent owner wording. More prose repeats the approach that already failed, fixed word limits treat symptoms without teaching the behavior, and temperature changes can't supply the missing demonstrations. Examples communicate judgment-dependent formatting more reliably than additional instructions, especially a small targeted set.

---

## Q29  ·  Set 3 Question 27

*Domain: Context Management & Reliability*

**A long-running audit of your extraction pipeline delegates separate Claude Code subagents to inspect parser modules, schema definitions, validation failures, and downstream mapping logic. Twice this week, the process was interrupted after hours of exploration. When restarted, the coordinator repeated completed investigations, missed several previously discovered edge cases, and gave subagents incomplete background about which document formats had already been analyzed. What design change would most improve reliability after interruptions?**

**Options:**

- Restart the audit from the beginning whenever an interruption occurs, discarding partial subagent findings to avoid inconsistency.
- Resume the prior named session and ask Claude to infer unfinished work from the accumulated conversation history.
- **Have each subagent export structured state to fixed paths, then load a resume manifest into restarted coordinator prompts.**  ✅
- Keep a single freeform scratchpad summary updated manually, then tell new subagents to continue from that summary.

**Correct answer:** **Have each subagent export structured state to fixed paths, then load a resume manifest into restarted coordinator prompts.**

**Explanation:**

Interruptions cause repeated investigations and lost edge cases because the work lives only in conversation history. Have each subagent export structured state — completed files, discovered edge cases, open questions, source paths, partial results — to fixed paths, then load a resume manifest into the restarted coordinator's prompts. Restarting from scratch wastes completed work, resuming a named session and inferring unfinished work from history risks stale results and missing handoffs, and a single freeform summary lacks the structure for coverage tracking. Use a durable external source of truth.

---

## Q30  ·  Set 3 Question 31

*Domain: Prompt Engineering & Structured Output*

**Production evaluation shows your extraction tool validates successfully, but downstream analytics are unreliable. New vendor industries and uncertain contract classifications are being squeezed into the closest allowed enum value, causing misleading dashboards even though no JSON schema errors occur. What schema change would best improve reliability while preserving machine-readable output?**

**Options:**

- Keep the closed enum unchanged and retry extractions until the model selects one of the approved category values.
- **Add explicit fallback enum values with companion detail fields so uncertain or novel categories are captured without forced misclassification.**  ✅
- Expand the enum with every observed category and reject documents whose categories are not already listed.
- Replace the enum with a free-text string field and let downstream systems normalize categories after extraction.

**Correct answer:** **Add explicit fallback enum values with companion detail fields so uncertain or novel categories are captured without forced misclassification.**

**Explanation:**

New industries and uncertain classifications get squeezed into the closest enum value, producing misleading dashboards even though no schema error occurs. Add explicit fallback enum values (unclear, other) with companion detail fields so uncertain or novel categories are captured without forced misclassification. Retrying until an approved value appears optimizes validation success over truthfulness, free text loses consistency, and endlessly expanding a closed enum still fails on future or ambiguous cases. Schema enforcement guarantees structure, not meaning, so give the model valid ways to express what the evidence supports.

---

## Q31  ·  Set 3 Question 35

*Domain: Prompt Engineering & Structured Output*

**A release candidate updates 18 extraction assets, including prompts, JSON schemas, validators, and few-shot examples across invoices, contracts, and intake forms. A single review request produces uneven results: detailed feedback on early files, superficial comments on later files, and missed mismatches between schema fields and validator assumptions. What review architecture should you use before approving the release?**

**Options:**

- Ask contributors to limit extraction pull requests to five changed files, postponing larger schema updates until later releases.
- Run three full-repository reviews and report only defects that at least two reviews identify independently.
- **Review each changed file separately for local prompt and schema defects, then run a final pass checking cross-file consistency.**  ✅
- Increase the context budget and review all changed prompts, schemas, validators, and examples together in one request.

**Correct answer:** **Review each changed file separately for local prompt and schema defects, then run a final pass checking cross-file consistency.**

**Explanation:**

One review request over 18 changed assets gives detailed feedback early, superficial comments later, and misses schema-validator mismatches. Review each changed file separately for local prompt and schema defects, then run a final pass checking cross-file consistency (validators vs schemas, examples vs format, conflicting instructions). More context is not better attention, broad repeated reviews reproduce the same blind spots while adding cost, and arbitrary file limits fragment related changes. Decompose large reviews by concern.

---

## Q32  ·  Set 3 Question 50

*Domain: Prompt Engineering & Structured Output*

**In pilot runs, quantity fields from several vendors use shorthand like "approx. 12 kg", "12kg net", and "12 kilograms". The extractor often flags valid variants as defects while accepting truly ambiguous entries like "12 units" without unit context. The schema and validation logic are stable, and prose instructions listing allowed unit formats have not improved consistency. What change would most effectively improve judgment across new vendor layouts?**

**Options:**

- **Add a small set of labeled examples showing acceptable unit variants and genuinely ambiguous entries, including expected fields and reasoning.**  ✅
- Increase the minimum confidence threshold so borderline extractions are routed to human review before downstream validation occurs.
- Instruct the model to return null for any measurement containing informal wording, unusual spacing, or missing punctuation.
- Expand the prompt with a comprehensive list of every vendor-specific unit spelling and abbreviation observed so far.

**Correct answer:** **Add a small set of labeled examples showing acceptable unit variants and genuinely ambiguous entries, including expected fields and reasoning.**

**Explanation:**

Prose lists of allowed unit formats haven't worked — valid variants like "12kg net" get flagged while ambiguous "12 units" passes. Add a small set of labeled examples showing acceptable unit variants and genuinely ambiguous entries, including the expected fields and reasoning, so Claude learns the decision boundary and generalizes to new vendor layouts. Raising the confidence threshold only changes downstream routing, and returning null for all informal wording discards valid shorthand that real documents contain. Examples define the boundary better than an exhaustive spelling list.

---

## Q33  ·  Set 3 Question 54

*Domain: Prompt Engineering & Structured Output*

**Your extractor captures `sample_size`, `study_design`, and `citation_source` from journal articles. It works on papers with explicit Methods and References sections, but misses the same fields when sample details appear in an abstract footnote, study design appears in an appendix table, or citations are inline only. Validation passes because those fields are nullable, but downstream analytics show systematic under-extraction. What change would most effectively improve extraction quality?**

**Options:**

- Make sample_size, study_design, and citation_source required in the schema so validation failures force complete outputs.
- **Add targeted examples showing correct extraction from multiple document layouts, including inline citations, appendix tables, and embedded methodology details.**  ✅
- Preprocess documents with keyword rules that discard content outside Methods, Results, References, and Appendix headings before extraction.
- Expand the instructions with a longer list of possible section names and tell Claude to search them exhaustively.

**Correct answer:** **Add targeted examples showing correct extraction from multiple document layouts, including inline citations, appendix tables, and embedded methodology details.**

**Explanation:**

Fields are missed when sample details, study design, or citations appear in abstract footnotes, appendix tables, or inline text; validation passes because the fields are nullable, but analytics show systematic under-extraction. Add targeted examples showing correct extraction from those varied layouts so Claude maps differently-placed evidence into the same schema fields. Making the fields required rewards fabrication, keyword preprocessing discards evidence on brittle assumptions about where it appears, and longer heading lists don't demonstrate the ambiguous cases. Examples teach the transformation while preserving real nulls.

---
