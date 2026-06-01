# Structured Data Extraction — Answering Strategy

> A study cheat sheet for the **Structured Data Extraction** scenario, built from the 33 questions in [03-Structured Data Extraction.md](../03-Structured%20Data%20Extraction.md).
> Goal: read any scenario the right way so your answers stay accurate — even under exam time pressure (3 sets × ~20 questions).

---

## Architecture & Scope Note (read this first)

**Don't reflexively apply the Customer Support hub-and-spoke model here.** This scenario's backbone is a **linear pipeline**, not a coordinator hub:

```
Documents → Extraction (Claude + tool_use/schema) → Validation (schema + semantic) → QA review → Downstream
```

- **Hub-and-spoke is a guest pattern, not the host.** A coordinator + subagents appears in only a few questions (Q3 splits a document into per-section extraction subagents; Q29 delegates subagents to inspect parsers/schemas/validators). If a question doesn't mention a coordinator, **don't invent one** — most questions are about a single extraction/QA step.
- **No fixed subagent roster and no named MCP tool catalog.** Unlike Customer Support (intake/billing/returns/risk + `get_customer`/`process_refund`…), the only "tools" revealed are generic: the **extraction tool-use call + JSON schema** (Q8), backend **OCR / table-parsing / validation** tools whose raw output floods context (Q17), a **separate QA/review instance** (Q11, Q12), and the **Message Batches API + `custom_id`** for bulk runs (Q14, Q21).
- **What it actually tests:** the two domain tags are **Prompt Engineering & Structured Output** (majority) and **Context Management & Reliability** — i.e. schema design, few-shot judgment, semantic validation, anti-fabrication, provenance, calibration, and batch processing. It is **not** an orchestration/governance scenario (no gates, no escalation, no least-privilege tool ownership).

> **Rule of thumb:** Customer Support → *agent orchestration & governance*. Structured Data Extraction → *prompt engineering & extraction reliability*. Carry over only the genuinely shared mechanisms (isolated reviewer, structured failure reports, segment-level confidence, durable state).

---

## Step 1: Build the Mental Model Before Reading Any Question

Every question is set in the **same system**, so hold this pipeline and its goal in your head:

```
Unstructured documents (contracts, invoices, NDAs, insurance packets, journal articles)
        │
        ▼
Extraction (Claude + tool_use with a JSON schema)   → structured records
        │
        ▼
Validation                                          → schema check  (is the JSON well-formed?)
        │                                           → semantic check (do totals sum? dates sane? line exists?)
        ▼
QA / review pass (often a SECOND Claude instance)   → flags problems for human reviewers
        │
        ▼
Downstream systems (ticketing, procurement, analytics, dashboards)

TARGET: high accuracy at scale, graceful edge-case handling, machine-actionable output.
```

Two simple ideas explain most answers:

1. **Passing the schema doesn't mean the answer is right.** A schema only checks the *shape* — are the field types correct, are required fields present. It can't check *meaning*. So it will happily accept line-item totals that don't add up, a due date dropped into the `invoice_date` field, or a value the model just made up. When the question says something like "it validates fine but the output is wrong, inconsistent, or misleading," the fix is almost always **show examples** (when the issue is judgment or formatting) or **add a meaning-check and re-ask with the error** (when numbers or dates are wrong) — *not* a sternly-worded instruction.
2. **Don't turn a missing thing into a confident answer.** Treating a failed lookup as "found nothing" hides real outages. Forcing a value into the nearest enum looks precise but is wrong. Telling the model to "guess the missing date" or making a field required just pushes it to **make data up**. Instead: leave real blanks as null, report real failures honestly, and ask for the missing source.

The classic exam trade-off is **examples vs schema escape-hatches vs prose**:
- **Examples** show the model where the evidence usually hides and what a good answer looks like.
- **Schema escape-hatches** (a fallback `other` category, nullable fields) let the model say "I'm not sure" or "it's not here" truthfully.
- **Prose instructions** like "be conservative," "be exhaustive," or "never make things up" sound right but rarely work — they're usually the trap answer.

---

## Step 2: The 9 Patterns (Quick Reference)

All 33 questions collapse into **9 patterns**. Read the symptom, match the row, pick the structural fix.

| Symptom in the scenario | Fix category | Questions |
|---|---|---|
| Outputs are schema-valid but **inconsistent / vague / wrong-located / mis-formatted**; prose guidance hasn't helped | **Targeted few-shot examples** showing the ideal output, evidence boundaries, and unusual source locations | Q1, Q4, Q13, Q28, Q32, Q33 |
| **Semantic** failures (totals don't sum, date in wrong field, currency in amount) on otherwise valid JSON | **Targeted retry** with source document + failed extraction + exact validator messages | Q6, Q15, Q18 |
| Model is asked to "return JSON" but emits markdown fences / prose / malformed commas | **Define an extraction tool with a JSON schema**; consume `tool_use` input directly | Q8 |
| Closed enum forces novel/ambiguous values into the nearest category → misleading analytics | **Add fallback enum values (`unclear`/`other`) + required detail field**; keep nulls genuine | Q19, Q27, Q30 |
| Required value missing because the **source is absent** or evidence is genuinely gone | **Detect source absence, stop retries, mark incomplete, request the source** | Q24, Q30(extract), Q33(nullable) |
| Subagent loses access mid-extraction → returns empty-success or aborts whole doc | **Structured failure reports** (attempted section, failure type, partial fields, recovery suggestion) | Q3 |
| QA findings are noisy / a category is mostly dismissed → reviewers ignore the whole feed | **Separate by category & severity, suppress/refine noisy categories, prioritize high-precision** | Q20, Q22 |
| Can't tell *why* findings fail / aggregate accuracy hides clustered errors | **Capture structured metadata at generation** (`detected_pattern`) + **segment-level analysis** before reducing review | Q5, Q7, Q9 |
| State lost across long runs / restarts; provenance lost after summarization | **Durable external state** — scratchpad, external tool-output store, exported resume manifest, source excerpts carried as data | Q10, Q16, Q17, Q23, Q25, Q26, Q29 |

Plus three "single-instance" structural calls that don't need a row of their own:

- **Review architecture:** isolate the reviewer (separate instance, no original reasoning) and **decompose long reviews** — focused per-section passes + a cross-section consistency pass. (Q11, Q12, Q31)
- **Scale & cost:** **pilot a representative batch** before the full run (Q2); keep **synchronous** for latency-bound queues, use the **Message Batches API** for latency-tolerant bulk (Q14).
- **Correlation:** join batch results on a **stable `custom_id`**, never on array/line order or model-generated filenames (Q21).

**The one rule behind all nine:** *fix the system itself — teach judgment with examples, give the schema honest ways to express uncertainty, validate meaning not just shape, and move durable state out of the transient conversation.*

---

## Detailed Symptom → Fix Reference (all 33)

| Symptom in the scenario | Fix | Questions |
|---|---|---|
| Findings validate but are vague ("date issue"), miss location, inconsistent fix wording | Few-shot examples of a complete finding (location, field, issue, severity, correction) | Q1 |
| New prompt/schema passed a few hand-picked cases; 80k docs vary by template/OCR/addenda | Run a representative **pilot batch**, analyze failures & null patterns, refine, then submit all | Q2 |
| Subagent loses section access → empty-success or full abort | Report unresolved failure: attempted section, failure type, partial fields, recovery suggestion | Q3 |
| QA flags harmless format diffs and valid nulls ("report any problems") | Rewrite QA prompt with **reportable errors, acceptable variations, skip conditions + examples** | Q4 |
| Logs capture outcomes but not the source construct behind false positives | Add `detected_pattern` field; analyze dismissal rates by pattern | Q5, Q9 |
| Semantic rejects (totals don't sum, due date in `invoice_date`); "fix the extraction" loops | Follow-up with source + failed extraction + **exact validation errors** for targeted self-correction | Q6, Q15 |
| 97.2% aggregate; leadership wants to drop review on high confidence | Analyze accuracy **by document type & field**; automate only validated segments, route the rest | Q7 |
| "Return valid JSON" still yields markdown fences / prose / bad commas | **Extraction tool + JSON schema**, consume `tool_use` input directly | Q8 |
| Same conversation infers extraction rules *and* reviews them → inherits its own mistakes | **Separate review instance** with source + fields + rubric, **excluding** the original reasoning | Q11 |
| One call reviews a 90-page packet → early errors caught, middle missed, self-contradiction | **Focused per-section passes + separate cross-section consistency pass** | Q12, Q31 |
| 18% null for fields that exist but sit in cover letters/footnotes/table captions | Targeted **few-shot from those unusual locations**; preserve genuine nulls | Q13, Q33 |
| Two queues: latency-bound onboarding vs 40k archived contracts | **Sync for onboarding, Message Batches API for the archive** | Q14 |
| Findings degrade & teammates can't recover discoveries over a month | **Repository scratchpad** of schemas, validators, edge cases, file paths | Q16 |
| Raw OCR/table/validator payloads dominate context → clause bleed, dropped pages | **Preprocess: store full output externally, append only schema-relevant fields + provenance** | Q17 |
| Nightly retry says only "fix the invalid fields" | Retry with source + rejected extraction + **exact validator messages**, return corrected record only | Q18 |
| Closed enum forces unusual clauses; ambiguous ones labeled inconsistently | **Fallback category (`other`) + required free-text detail**; add enum values for ambiguity | Q19, Q27, Q30 |
| One noisy finding category dismissed → reviewers skim & miss real ones | **Separate by category & severity, tighten the noisy check, prioritize high-precision** | Q20 |
| Result-file line order causes mismatches after retries/partial failures | **Stable `custom_id`** persisted with metadata; reconcile on that identifier | Q21 |
| "ambiguous payment terms" dismissed 68% → whole feed ignored | **Temporarily suppress** that category, refine criteria/examples, re-enable | Q22 |
| Consolidated obligations lack row-level evidence; auditors reopen every file | Each obligation **carries source IDs + excerpts**; merge duplicates **retaining every reference** | Q23, Q26 |
| Required approval date missing because the approval letter was never in the input | **Detect source absence, stop retries, mark incomplete, request the missing source** | Q24 |
| Mid-pipeline summarization flattens evidence; can't trace exclusions to a passage | Intermediate handoffs carry **source doc + location + excerpt** into final synthesis | Q25 |
| Long audit interrupted → repeats work, loses edge cases on restart | Subagents **export structured state to fixed paths**; load a **resume manifest** | Q29 |
| Detailed field defs + length rules still give uneven summaries/owner wording | Add **2–4 representative input/ideal-output examples** | Q28 |
| Valid unit variants flagged, ambiguous ones accepted; prose lists don't help | Few-shot of acceptable variants **and** genuinely ambiguous entries, with reasoning | Q32 |

---

## Step 3: The "North Star" Principles

Every correct answer follows one of these. When two options look plausible, the one matching a north star wins:

1. **Examples teach judgment that prose and schema can't.** For inconsistent specificity/format, unusual evidence locations, or ambiguity boundaries, add targeted few-shot — not "be concise/thorough" or longer instructions. (Q1, Q4, Q13, Q28, Q32, Q33)
2. **Schema-valid is not correct — validate meaning, then retry with the evidence.** Add semantic checks; send the source + failed extraction + exact validator messages for targeted self-correction. (Q6, Q15, Q18; Q1/Q7 CI parallels)
3. **Generate machine-readable output at the source.** Use an extraction tool with a JSON schema and consume `tool_use` input; don't scrape/regex prose. (Q8)
4. **Give the schema honest escape hatches.** Fallback enum values + detail fields for novel/ambiguous categories; nullable for genuinely absent data — never force a value or make it required to "force completeness." (Q19, Q27, Q30, Q24)
5. **Distinguish "found nothing" from "couldn't access," and a gap from a correctable error.** Structured failure reports; stop retries when the source is absent; classify missing-baseline vs format errors. (Q3, Q24, Q30)
6. **Provenance is part of the data contract.** Each fact carries source ID + location + excerpt through every handoff and summarization step; consolidation keeps all references. (Q23, Q25, Q26, Q17)
7. **Capture structured diagnostic metadata at generation time, and analyze by segment.** `detected_pattern` fields beat free-text notes; segment-level accuracy beats a flattering aggregate before you cut review. (Q5, Q7, Q9)
8. **Persist durable state outside the conversation.** Scratchpads, external tool-output stores, exported resume manifests survive long runs and restarts. (Q16, Q29, Q17)
9. **Isolate and decompose review.** A separate reviewer without the original reasoning; focused per-section passes plus a cross-section consistency pass. (Q11, Q12, Q31)
10. **Match the processing mode and correlation to the requirement.** Pilot before full scale; sync for latency-bound, batches for bulk; reconcile on stable `custom_id`. (Q2, Q14, Q21)

---

## Step 4: Eliminate the Recurring Wrong-Answer Traps

These distractors appear in nearly every question. **Cross them out on sight** — they're correct answers ~0% of the time in this scenario:

- ❌ "Make the field **required / non-null** so validation forces completeness" → pressures fabrication when evidence is genuinely absent (Q13, Q24, Q33, Q30, Q14-CI)
- ❌ "Tell Claude **null is unacceptable** / infer the value from nearby fields" → invents plausible but unsupported data (Q13, Q24)
- ❌ "Add a general instruction to be **concise / conservative / exhaustive / careful**" → no decision boundary; examples or criteria are the fix (Q1, Q4, Q28, Q20, Q22)
- ❌ "**Regex / post-process** the text to rebuild missing fields" or "strip markdown fences with regex" → brittle repair layer; can silently corrupt data (Q1, Q8)
- ❌ "Convert failures to **empty successful results**" → hides outages as no-matches (Q3)
- ❌ "**Retry until** all fields populate / until it passes / N blind retries" → wastes attempts and launders hallucinations (Q18, Q24, Q15, Q30, Q13)
- ❌ "Replace the enum with an **unrestricted string**" → loses normalization, causes label drift (Q19, Q27, Q30)
- ❌ "Force the **closest enum value** / keep the closed enum and instruct to pick closest" → schema-valid but misleading analytics (Q19, Q27, Q30)
- ❌ "Raise a **single global confidence threshold**" → hides clustered errors, cuts recall in good segments (Q5, Q7, Q10, Q20, Q22)
- ❌ "Trust the **aggregate accuracy** and monitor complaints" → makes downstream users the error detector (Q7)
- ❌ "**Same instance self-critiques** / extended thinking / 3 self-review turns" → inherits the original assumptions (Q11)
- ❌ "**Majority vote** — accept only issues found by ≥2 reviews" → filters out valid findings that appear inconsistently (Q12, Q31)
- ❌ "Increase **max_tokens** / give more context to fix long-input attention" → doesn't fix uneven attention or extraction quality (Q2, Q12, Q17)
- ❌ "Rely on **array/line order** or a **model-generated filename** to correlate batch results" → breaks after retries/partial failures (Q21)
- ❌ "**Reconstruct citations after** synthesis / packet-level bibliography / store whole docs for auditors" → fabricated or too-coarse provenance (Q23, Q25, Q26)
- ❌ "Rely on **/compact** or **rereading the whole codebase** to preserve findings" → not a durable record (Q16, Q29)
- ❌ "**Free-text** notes / natural-language summaries for analysis" → too unstructured and slow to aggregate (Q5, Q9)

---

## Step 5: The Decision Test (when down to two options)

1. **Is the output schema-valid but semantically/judgment wrong?** → **Examples** (judgment/format/location) or **semantic validation + targeted retry** (relational errors). Reject prose and "make it required." (Q1, Q4, Q6, Q13, Q15)
2. **Is a value missing?** → Ask *why*: genuine absence/absent source → **nullable / stop-and-request**; misplaced/misformatted → **targeted retry**; novel category → **fallback enum + detail**. Never force or infer. (Q24, Q19, Q27, Q30)
3. **Does it preserve information, provenance, and operational meaning?** → Reject empty-success, generic failures, dropped excerpts, reconstructed citations. (Q3, Q23, Q25, Q26)
4. **Does it diagnose at the right granularity?** → Structured metadata + segment-level analysis beat aggregates, global thresholds, and free-text. (Q5, Q7, Q9)
5. **Is the reviewer independent and the review decomposed?** → Separate instance, no original reasoning; per-section + consistency pass. Reject self-critique and majority vote. (Q11, Q12, Q31)

---

## Exam-Specific Tactics

- **"Schema vs semantic" is the signature distinction.** Almost every "validates successfully but…" stem wants either **examples** (the value is judgment/format/location-dependent) or **semantic validation + targeted retry** (the value breaks a relationship like a sum or date order). Stronger schema constraints are the trap.
- **"Examples vs prose vs schema constraint" decides most prompt questions.** When prose ("be conservative," length rules, longer field defs) has *already failed* in the stem, the answer is almost always **targeted few-shot examples**, not more prose (Q1, Q4, Q13, Q28, Q32, Q33).
- **Enum edge cases → fallback + detail field.** Five-way pattern: closed enum forces wrong values, unrestricted string loses normalization, "pick closest" misleads, "retry until valid" optimizes the wrong thing → **add `unclear`/`other` + required detail** (Q19, Q27, Q30).
- **"Missing value" forks three ways.** Misplaced/misformatted → retry with validator messages; genuinely absent in a present source → preserve null + examples; **source not in the input at all** → stop retries and request it (Q24, Q30). Spot which before answering.
- **Provenance must be carried, never reconstructed.** Any option that *regenerates* citations after summarization, or offers a packet-level bibliography, or stores whole docs for manual search, is wrong; carry source ID + location + excerpt as structured data (Q23, Q25, Q26).
- **Scale questions reward calibration, not optimism.** Pilot before the full run (Q2), analyze by segment before reducing review (Q7), correlate on stable IDs (Q21), and split sync vs batch by latency (Q14).
- **The longer, mechanism-rich answer usually wins.** Correct answers name concrete mechanisms ("`detected_pattern` field analyzed by segment," "follow-up with exact validator messages"); traps are vague ("be exhaustive," "be conservative," "infer from nearby fields").

---

**Bottom line:** internalize that **schema-valid is not correct**. Classify each scenario by **(1)** whether the failure is *judgment/format* (→ examples), *relational/semantic* (→ validation + targeted retry), *category/uncertainty* (→ fallback enum + detail / nullable), *missing-source* (→ stop & request), *provenance/state* (→ carry it as data / persist externally), or *diagnosis* (→ structured metadata + segment analysis). The mechanism-rich option that teaches judgment, represents uncertainty honestly, and never fabricates is almost always correct.
