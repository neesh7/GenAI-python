# Domain 5: Context & Reliability (15%)

Manage context effectively in production systems. Covers progressive summarization risks, context positioning, escalation patterns, error propagation, context degradation, human review, and information provenance.

---

## d5.1 — Context Optimization & Positioning

### Core Concepts

Context management is about making the most of the limited context window while **preserving critical information**. Two key risks dominate this domain.

**Key Understanding:**
- **Progressive summarization risks** — Repeated compression silently destroys critical details
- **"Lost in the middle" effect** — Information in the middle of contexts is less likely to be recalled
- **Case facts blocks** — Immutable structured reference sections that preserve critical info (never summarized)
- **Trimming verbose outputs** — Remove noise while retaining essential data
- **Position-aware ordering** — Important info at beginning/end (high-recall); less critical in middle

### Progressive Summarization Risk

**The Problem:** Each summarization removes detail:

```
Original: 
"Customer John Smith (ACC-12345) called about order #98765. 
Charged $150.00 instead of promotional $99.99."

After 1st summary: 
"Customer called about billing issue with promotion."

After 2nd summary: 
"Customer has a billing issue."

Result: Lost customer name, account ID, order number, exact amounts, promotion code ❌
```

### The "Lost in the Middle" Effect

Research shows **middle context is forgotten**:
- **Beginning** → High recall ✅
- **Middle** → Low recall ❌
- **End** → High recall ✅

**Solution:** Position critical info at start/end, less critical info in middle.

### Case Facts Blocks (The Fix) ✅

**Immutable structured reference block placed at the beginning** — never summarized or compressed.

```markdown
## CASE FACTS (Do not summarize — reference directly)
| Field          | Value                                  |
|---|---|
| Customer       | John Smith                             |
| Account ID     | ACC-12345                              |
| Order          | #98765                                 |
| Expected Price | $99.99 (promotion SUMMER2026)          |
| Charged Price  | $150.00                                |
| Overcharge     | $50.01                                 |
| Customer Since | 2019 (7-year tenure)                   |
| Priority       | High (overcharge + loyal customer)     |

## RULES
- Always address customer as "Mr. Smith"
- This case qualifies for immediate resolution
- Refund amount ($50.01) is within $500 limit
```

### Code Pattern

```markdown
# WRONG: Progressive summarization loses critical details
Turn 1: "John Smith (ACC-12345) order #98765..."
Turn 5: [Summary] "Customer billing issue"
Turn 10: [Summary] "Billing issue being handled"
# By turn 10: lost name, account, order, amounts ❌

---

# CORRECT: Case facts block — always available, never summarized
## CASE FACTS (immutable)
- Customer: John Smith (ACC-12345)
- Order: #98765
- Issue: Overcharged $50.01 (promo SUMMER2026)
- This block stays intact regardless of length ✅
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Progressive summarization of critical details** | Silent detail loss; can't be recovered |
| **Ignoring "lost in the middle" effect** | Important info buried in middle gets forgotten |
| **No case facts block** | Critical data gets lost as conversation grows |
| **Verbose tool outputs without trimming** | Noise fills context window, pushing out important info |

### Exam Tip 🎯
**If the exam asks how to preserve critical customer details in a long conversation, the answer is ALWAYS "case facts" blocks, never progressive summarization.**

---

## d5.2 — Escalation & Error Propagation

### Core Concepts

Escalation and error propagation determine how failures flow through a system. Getting this wrong means either **overwhelming humans with trivial issues** or **silently dropping critical failures**.

**Key Understanding:**
- **Valid escalation triggers** — Customer request, policy gap, capability limit, business threshold, repeated failures
- **Invalid escalation triggers** — Sentiment (angry ≠ complex), self-reported confidence
- **Structured error context** — Always include what was attempted and why it failed
- **Access failure vs empty result** — "Could not check DB" ≠ "Checked, found nothing"
- **Local recovery first** — Try to fix locally before escalating to coordinator
- **Partial results with context** — Report progress even on failure

### Valid Escalation Triggers ✅

| Trigger | Example |
|---|---|
| **Customer explicit request** | "I want to speak to a human" |
| **Policy gap detected** | Situation not covered by existing rules |
| **Capability limit** | Agent lacks required access/permissions |
| **Business threshold exceeded** | Refund > $500 agent limit |
| **Repeated failures** | After 3 retry attempts still failing |

### Invalid Escalation Triggers ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Negative sentiment** | Angry customer asking to change address ≠ needs escalation |
| **Low self-reported confidence** | Model confidence is unreliable; sentiment ≠ complexity |

### Code Pattern

```python
# WRONG: Escalate based on sentiment
if customer_sentiment == "angry":
    escalate_to_human()
# An angry customer with a simple task does NOT need escalation ❌

# WRONG: Escalate based on confidence
if model_confidence < 0.7:
    escalate_to_human()
# Model's own confidence is unreliable ❌

---

# CORRECT: Escalate based on objective criteria
if customer.requested_human:
    escalate("Customer explicitly requested human")
if not policy_covers(situation):
    escalate("Policy gap detected")
if refund_amount > AGENT_REFUND_LIMIT:
    escalate(f"Amount ${refund_amount} exceeds ${AGENT_REFUND_LIMIT} limit")
if retry_count >= MAX_RETRIES:
    escalate("Exhausted retry attempts")
```

### Error Propagation in Multi-Agent Systems

When a subagent fails, report **structured context** to coordinator:

```json
{
  "isError": true,
  "errorCategory": "database_unavailable",
  "isRetryable": true,
  "context": {
    "attempted": "Lookup customer by email",
    "service": "customer-database",
    "timeout_ms": 5000,
    "why_it_matters": "Without customer lookup, can't determine account status"
  }
}
```

**Critical:** Never silently drop failures. Coordinator must know data is missing.

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Sentiment-based escalation** | Sentiment doesn't indicate task complexity |
| **Generic error propagation** | Loses original error context; can't diagnose |
| **Silent error suppression** | Coordinator assumes data exists when it doesn't |
| **Confidence-based escalation** | Model self-confidence is unreliable |

### Exam Tip 🎯
**Sentiment-based and confidence-based escalation are ALWAYS wrong on the exam.** Valid triggers: explicit customer request, policy gaps, capability limits, business thresholds.

---

## d5.3 — Context Degradation & Extended Sessions

### Core Concepts

Long-running agent sessions suffer from **context degradation** — quality decreases as conversation fills context window.

**Key Understanding:**
- **Context degradation symptoms** — Agent forgets instructions, responses become generic, tool accuracy drops
- **Scratchpad files** — External files persist important state across context resets
- **/compact** — Compress conversation history to reclaim context space
- **Subagent delegation** — Delegate verbose exploration to subagents (keeps coordinator clean)
- **Stratified metrics** — Track accuracy per document type, not just aggregate
- **Information provenance** — Preserve source and confidence level of each data point

### Symptoms of Context Degradation ❌

- Agent forgets earlier instructions or constraints
- Responses become less focused, more generic
- Tool selection accuracy decreases
- Agent repeats work it already did
- Quality noticeably drops after 50+ turns

### Mitigation Strategies ✅

| Strategy | When to Use | Why |
|---|---|---|
| **/compact** | Context getting long but task ongoing | Reclaim space; keep conversation flowing |
| **Scratchpad files** | Multi-step tasks; need persistent state | Survives context compression & resets |
| **Subagent delegation** | Verbose exploration needed | Subagent absorbs exploration noise |
| **Position-aware ordering** | Long context | Critical info at beginning/end |

### Code Pattern

```python
# Strategy 1: Scratchpad files for persistent state
agent.run("""
Before starting complex analysis:
1. Create scratchpad file: progress.md
2. Record key findings as you discover them
3. Update progress.md after each major step
4. If context gets long, use /compact
5. After /compact, re-read progress.md to restore context
""")

# Strategy 2: Subagent delegation for verbose tasks
coordinator = Agent(tools=[Task, read_scratchpad, summarize])
coordinator.run("""
For this codebase analysis:
1. Delegate file-by-file analysis to subagent
   (keeps exploration out of coordinator context)
2. Subagent writes findings to scratchpad
3. Coordinator reads summarized findings
4. Coordinator synthesizes final report
""")

# Strategy 3: Stratified metrics (per-document-type accuracy)
def track_accuracy(results):
    by_type = {}
    for r in results:
        doc_type = r["document_type"]
        if doc_type not in by_type:
            by_type[doc_type] = {"correct": 0, "total": 0}
        by_type[doc_type]["total"] += 1
        if r["is_correct"]:
            by_type[doc_type]["correct"] += 1
    
    # Reveals hidden failures per category
    for doc_type, stats in by_type.items():
        accuracy = stats["correct"] / stats["total"] * 100
        print(f"{doc_type}: {accuracy:.1f}%")
```

### Stratified Metrics: Aggregate vs Per-Type

```
WRONG: Aggregate metrics only
Total correct: 950 / 1000 = 95.0% accuracy
"Looks great!" ✅

BUT actually:
- Invoices:  70/100  = 70%  ❌ FAILING!
- Receipts: 880/900 = 97.8% ✅
- Aggregate HIDES the invoice problem!

---

CORRECT: Per-document-type metrics
- Invoice accuracy:   70.0% ❌ ALERT: Below threshold!
- Receipt accuracy:   97.8% ✅ OK
- Contract accuracy: 100.0% ✅ OK
Now we can see and FIX the invoice problem ✅
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Extended sessions without monitoring** | Quality degradation goes unnoticed |
| **No scratchpad files for state** | Important state lost on context compression |
| **Aggregate metrics only** | Masks per-category failures |
| **No subagent delegation** | Coordinator context polluted with exploration noise |

### Exam Tip 🎯
**Aggregate metrics masking per-category failures is a KEY exam concept.** Correct answer always tracks accuracy per document type (stratified metrics), not just overall accuracy.

---

## d5.4 — Human Review & Information Provenance

### Core Concepts

**Information provenance** = Tracking where each piece of data came from and how reliable the source is. Critical for multi-agent systems with conflicting information.

**Key Understanding:**
- **Stratified sampling** — Review samples across categories, not just random
- **Field-level confidence** — Provide confidence for individual fields
- **Claim-source mappings** — Link each output to its source for traceability
- **Temporal data** — Preserve timestamps and version info
- **Conflict annotation** — Explicitly mark conflicting sources (don't silently choose)
- **Human-in-the-loop checkpoints** — Pause for critical decisions

### Provenance Metadata to Track

| Metadata | Example |
|---|---|
| **Source** | "customer-db", "invoice-pdf", "web-scrape" |
| **Confidence** | "verified", "extracted", "inferred", "estimated" |
| **Timestamp** | When was this data retrieved? |
| **Agent ID** | Which subagent provided this? |

### Confidence Levels (Reliability Ranking)

```
"verified"   (4) — From authoritative source (database, API)
"extracted"  (3) — Parsed from structured document
"inferred"   (2) — Derived from context
"estimated"  (1) — Best guess
```

### Code Pattern: Conflict Resolution with Provenance

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DataWithProvenance:
    value: str | float | dict
    source: str                 # "customer-db", "invoice-pdf", etc
    confidence: str             # "verified", "extracted", "inferred"
    retrieved_at: datetime
    agent_id: str              # Which subagent provided this

def resolve_conflict(data_points: list[DataWithProvenance]):
    """When subagents disagree, use provenance to decide."""
    
    confidence_rank = {
        "verified": 4,
        "extracted": 3,
        "inferred": 2,
        "estimated": 1,
    }
    
    # Pick the most reliable source
    best = max(data_points, key=lambda d: confidence_rank[d.confidence])
    
    # Log the conflict for audit trail
    log_conflict(
        chosen=best,
        alternatives=data_points,
        reason=f"Selected {best.source} (confidence: {best.confidence})"
    )
    
    return best
```

### Human-in-the-Loop Checkpoints

Present humans with:
- The decision to be made
- Data supporting each option (with provenance)
- Recommended action and why
- Way to approve, modify, or reject

**Use for:**
- Financial decisions above thresholds
- Legal/compliance operations
- Irreversible actions
- Conflicting information detected

### Code Pattern: With vs Without Provenance

```python
# WRONG: No provenance tracking
revenue = subagent_1.get_revenue()      # From where?
revenue_2 = subagent_2.get_revenue()    # Conflicts!
# Which one do we trust? We don't know!
final_revenue = revenue  # Arbitrary choice ❌

---

# CORRECT: With provenance tracking
rev_1 = DataWithProvenance(
    value=1_500_000, source="financial-db",
    confidence="verified", agent_id="finance-agent"
)
rev_2 = DataWithProvenance(
    value=1_480_000, source="quarterly-pdf",
    confidence="extracted", agent_id="doc-agent"
)
# Trust verified database over extracted PDF ✅
final = resolve_conflict([rev_1, rev_2])
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Aggregate accuracy only** | Masks per-document-type failures |
| **No claim-source mappings** | Can't trace data back to origin |
| **Silent conflict resolution** | No audit trail; can't explain decision |
| **No temporal data** | Can't determine if data is stale |
| **Field-level confidence missing** | Can't assess reliability of individual fields |

### Exam Tip 🎯
**When subagents provide conflicting data, the correct answer ALWAYS involves tracking information provenance (source, confidence, timestamp) and using it to resolve conflicts.** Arbitrary selection without provenance is always wrong.

---

## Key Exam Tips for Domain 5

1. **Case facts blocks > progressive summarization** — Never lose critical details
2. **Sentiment ≠ complexity** for escalation — Only escalate on objective criteria
3. **Always distinguish access failures from empty results** — Different error types
4. **Track accuracy per document type** — Stratified metrics, not aggregate
5. **Maintain information provenance** — Source, confidence, timestamp for all data
6. **Use /compact for extended sessions** — Prevent context degradation
7. **Scratchpad files for persistent state** — Survive context compression

---

## Related Exam Scenarios

- **Scenario 1**: Customer Support Resolution Agent — Tests escalation logic and error propagation
- **Scenario 3**: Multi-Agent Research System — Tests context passing, error handling, provenance
- **Scenario 6**: Structured Data Extraction — Tests accuracy tracking per document type

---

## Summary Table

| Sub-Domain | Focus | Critical Concept | Exam Weight |
|---|---|---|---|
| **d5.1** | Context Optimization | Case facts blocks; position-aware; lost-in-middle effect | 25% of Domain 5 |
| **d5.2** | Escalation & Errors | Valid triggers; error propagation; sentiment ≠ complexity | 30% of Domain 5 |
| **d5.3** | Context Degradation | /compact, scratchpad files, stratified metrics | 25% of Domain 5 |
| **d5.4** | Provenance & Review | Claim-source mappings, conflict resolution, human-in-loop | 20% of Domain 5 |
