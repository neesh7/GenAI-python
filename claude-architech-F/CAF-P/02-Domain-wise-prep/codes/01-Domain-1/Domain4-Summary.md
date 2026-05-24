# Domain 4: Prompt Engineering & Structured Output (20%)

Master prompt engineering techniques for production systems. Covers explicit criteria, few-shot prompting, tool_use for structured output, JSON schema design, validation-retry loops, and multi-pass review strategies.

---

## d4.1 — Explicit Criteria & Instruction Design

### Core Concepts

Production prompts require **explicit, measurable criteria** instead of vague instructions. Vagueness leads to false positives and eroded developer trust.

**Key Understanding:**
- **Explicit criteria over vague instructions** — "Flag functions over 50 lines" not "Flag long functions"
- **False positive impact** — Too many false positives = alert fatigue = developers ignore all flags
- **Specificity reduces ambiguity** — Measurable criteria enable consistent results across runs
- **Measurable criteria enable validation** — You can verify flagged items actually meet the criteria
- **Trust erosion** — When developers stop trusting the system, no flag gets attention (including real issues)

### Why Vagueness Fails in Production

| Vague Instruction | Problem | Measurable Alternative |
|---|---|---|
| "Make it better" | Better how? Faster? Cleaner? | "Reduce cyclomatic complexity to <10 per function" |
| "Find issues" | What counts as an issue? | "Flag SQL queries using string concatenation only" |
| "Be thorough" | Over-flags, creates alert fatigue | "Flag only: >50 lines, missing error handling, hardcoded secrets" |

### Code Pattern

```markdown
# VAGUE: Inconsistent, high false positives
Review this code for quality issues.
Be thorough and flag anything suspicious.

---

# EXPLICIT: Consistent, actionable, low false positives
Review this code and flag ONLY the following:
1. Functions exceeding 50 lines of code
2. Async operations missing try-catch error handling
3. Hardcoded strings matching API key patterns (sk-, pk-, key-)
4. Public functions missing JSDoc documentation
5. SQL queries constructed with string concatenation

For each issue found, provide:
- File path and line number
- Which rule (1-5) was violated
- Severity: critical (3,5) | warning (1,2) | info (4)
- One-line fix suggestion
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Vague instructions** like "make it better" or "find issues" | Results are inconsistent; developers can't trust the system |
| **Not considering false positive impact** | Alert fatigue erodes trust; developers ignore ALL flags |
| **Unmeasurable criteria** | Can't validate the output; can't verify consistency |
| **Over-flagging for perfection** | Developers tune out the system |

### Exam Tip 🎯
**Every time the exam asks about prompt design for production systems, the correct answer uses specific, measurable criteria.** If an option says "be thorough" or "find all issues," it's wrong.

---

## d4.2 — Few-Shot Prompting

### Core Concepts

Few-shot prompting provides **2-4 examples** that establish expected output format, reasoning pattern, and edge case handling.

**Key Understanding:**
- **2-4 examples is optimal** — Fewer than 2 doesn't establish pattern; more than 4-6 bloats without proportional benefit
- **Format consistency** — All examples must follow identical output structure
- **Edge case coverage** — At least one example should demonstrate an ambiguous/edge case
- **Diversity matters** — Cover different categories (positive/negative, simple/complex)
- **Most valuable for ambiguous tasks** — Classification with fuzzy boundaries, sarcasm, mixed sentiment

### When Few-Shot is Valuable ✅

- Ambiguous classification tasks (sentiment with sarcasm, mixed reviews)
- Custom output formats that aren't standard
- Domain-specific reasoning patterns
- Tasks where boundary between categories is fuzzy

### When Few-Shot is Unnecessary ❌

- Simple, well-defined tasks (e.g., "extract the email address")
- Tasks with clear, objective criteria
- Standard output formats (JSON, XML) that Claude handles natively

### Code Pattern

```python
few_shot_prompt = """
Classify customer reviews. Provide sentiment and reasoning.

Example 1 (Clear positive):
Input: "Absolutely love this product! Best purchase this year."
Output: {"sentiment": "positive", "confidence": "high",
         "reasoning": "Strong positive language, superlative"}

Example 2 (Clear negative):
Input: "Terrible experience. Product broke after 2 days."
Output: {"sentiment": "negative", "confidence": "high",
         "reasoning": "Explicit negative + product failure"}

Example 3 (Ambiguous — mixed sentiment):
Input: "Great features but the battery life is disappointing."
Output: {"sentiment": "mixed", "confidence": "medium",
         "reasoning": "Positive on features, negative on battery"}

Example 4 (Edge case — sarcasm):
Input: "Oh wonderful, another update that breaks everything."
Output: {"sentiment": "negative", "confidence": "medium",
         "reasoning": "Sarcastic positive masking frustration"}

Now classify this review:
Input: "{user_review}"
"""
```

### Few-Shot Best Practices

| Practice | Why It Matters |
|---|---|
| **2-4 examples** | Sweet spot; fewer doesn't establish pattern, more bloats |
| **Include edge case** | At least 1 example with ambiguity or sarcasm |
| **Format consistency** | All examples follow identical structure |
| **Diverse examples** | Cover positive, negative, neutral, complex cases |

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Too many examples (>6)** | Bloats prompt without proportional benefit |
| **Inconsistent formatting** | Confuses the model about expected output structure |
| **No edge case coverage** | Model doesn't learn how to handle ambiguous cases |
| **Using few-shot for simple tasks** | Wastes tokens; Claude handles simple extraction natively |

### Exam Tip 🎯
**The exam tests whether you know the optimal number of few-shot examples (2-4) and that at least one should cover an edge case.** More than 6 examples is always wrong.

---

## d4.2.5 — Chain-of-Thought Prompting

### Core Concepts

**Chain-of-Thought (CoT)** = Ask Claude to **explain its reasoning step-by-step** before giving the answer. This improves accuracy on complex reasoning tasks.

**Key Understanding:**
- **Forces step-by-step reasoning** — Model explains BEFORE concluding
- **Reduces errors on complex tasks** — Catches mistakes mid-reasoning, not just at the end
- **Best for multi-step logic** — Decision trees, complex debugging, security analysis
- **Not needed for simple extraction** — "Extract email" doesn't need CoT
- **Combines well with few-shot** — Few-shot examples + CoT = strongest approach
- **Improves transparency** — You see the reasoning, not just the answer

### When CoT is Valuable ✅

- Complex logic puzzles or debugging
- Security audits (multiple threat vectors)
- Code review (multi-step analysis)
- Decision-making with conditions
- Tasks requiring verification at each step

### When CoT is Unnecessary ❌

- Simple extraction ("Extract email address")
- Straightforward classification with clear boundaries
- Direct lookups or transformations

### Code Pattern: Without vs With CoT

**Without CoT (Direct Answer):**
```
Prompt: "Is this code vulnerable to SQL injection?
Code: db.query('SELECT * FROM users WHERE id=' + req.params.id)"

Response: "Yes, vulnerable"
(No reasoning shown; hard to verify or debug)
```

**With CoT (Step-by-Step):**
```
Prompt: "Is this code vulnerable to SQL injection?
Think step-by-step:
1. Identify all user inputs
2. Check if inputs are validated
3. Check if SQL query uses parameterized queries or string concatenation
4. Assess risk

Code: db.query('SELECT * FROM users WHERE id=' + req.params.id)"

Response: 
"Step 1: User input is req.params.id
Step 2: No validation visible
Step 3: Query uses string concatenation: 'SELECT * FROM users WHERE id=' + req.params.id
Step 4: VULNERABLE - attacker can inject SQL via id parameter (e.g., ?id=1 OR 1=1)"

(Clear reasoning; you can verify each step)
```

### Few-Shot + Chain-of-Thought (Combined - Strongest)

```
Example 1 (Vulnerable):
Code: "db.query('SELECT * FROM users WHERE id=' + req.params.id)"
Reasoning: 
  1. User input: req.params.id
  2. No validation
  3. Uses string concatenation (not parameterized)
  4. Conclusion: SQL injection vulnerability
Output: "CRITICAL: SQL injection vulnerability"

Example 2 (Secure):
Code: "db.query('SELECT * FROM users WHERE id = ?', [req.params.id])"
Reasoning:
  1. User input: req.params.id
  2. Uses parameterized query (? placeholder)
  3. Input separated from SQL query
  4. Conclusion: Safe from SQL injection
Output: "OK: Safe from SQL injection"

Now analyze this code:
Code: [CODE HERE]
Think step-by-step before concluding
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Using CoT for simple tasks** | "Extract email from text" doesn't need step-by-step reasoning; wastes tokens |
| **No verification steps** | If you ask for reasoning but don't verify it, defeats the purpose |
| **Too vague reasoning prompt** | "Explain your thinking" is weaker than "Check: (1) inputs, (2) validation, (3) output handling" |
| **Combining with poor examples** | Few-shot + CoT without good examples = poor quality |

### When to Combine Techniques

| Task | Best Approach | Why |
|---|---|---|
| Simple extraction | Zero-Shot | Straightforward, no reasoning needed |
| Sentiment classification with sarcasm | Few-Shot (2-4 examples) | Ambiguity needs examples, not explanation |
| Complex security audit | Few-Shot + CoT | Ambiguity + multi-step reasoning |
| Debugging logic errors | CoT only | Step-by-step reasoning required |
| Structured data extraction | tool_use + validation | Format guarantee needed |

### Exam Tip 🎯
**Chain-of-Thought is NOT explicitly tested on the architect exam**, but understanding it helps you design better prompts. The exam focuses on few-shot, explicit criteria, and tool_use. However, CoT strengthens production prompts by forcing transparent reasoning.

---

## d4.3 — Tool Use for Structured Output

### Core Concepts

**tool_use guarantees JSON schema compliance,** but NOT semantic correctness. The structure is valid, but the content may be wrong.

**Key Understanding:**
- **tool_use guarantees STRUCTURE** — All required fields present, correct types, valid enum values
- **tool_use does NOT guarantee SEMANTICS** — Values might be wrong (wrong name extracted, wrong date, etc.)
- **tool_choice parameter** controls invocation: 'auto' (decides), 'any' (must use tool), or forced specific tool
- **Schema design matters** — required fields, enums with 'other', nullable fields
- **Validation still required** — Check extracted values for correctness after tool_use

### Critical Distinction

| Aspect | Guaranteed | NOT Guaranteed |
|---|---|---|
| **Structure** | ✅ JSON matches schema | ❌ Values are correct |
| **Required fields** | ✅ All present | ❌ Content accuracy |
| **Data types** | ✅ Correct types | ❌ Semantic meaning |
| **Enum values** | ✅ Valid enums only | ❌ Chosen value is right |

### tool_choice Parameter

```python
# "auto" — Claude decides whether to use tool
client.messages.create(
    tools=[extract_tool],
    tool_choice="auto",  # May or may not use the tool
)

# "any" — Claude must use a tool (but chooses which)
client.messages.create(
    tools=[extract_tool, other_tool],
    tool_choice="any",  # Must use one of them
)

# Forced specific tool — Guarantees structure
client.messages.create(
    tools=[extract_tool],
    tool_choice={"type": "tool", "name": "extract_invoice"},  # Always uses this
)
```

### Schema Design Best Practices

```json
{
  "type": "object",
  "properties": {
    "vendor_name": {
      "type": "string",
      "description": "Name of the vendor"
    },
    "document_type": {
      "type": "string",
      "enum": ["standard_invoice", "credit_note", "proforma", "other"],
      "description": "Document category"
    },
    "document_type_detail": {
      "type": "string",
      "description": "Required if document_type is 'other'"
    },
    "optional_field": {
      "type": ["string", "null"],
      "description": "Field that can be missing"
    }
  },
  "required": ["vendor_name", "document_type"]
}
```

### Code Pattern

```python
# Force tool_use for guaranteed structure
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    tools=[extract_tool],
    tool_choice={"type": "tool", "name": "extract_invoice"},
    messages=[{"role": "user", "content": f"Extract: {invoice}"}]
)

# Parse structured output
data = parse_tool_response(response)

# CRITICAL: Validate semantics (not just structure!)
errors = []
if not re.match(r"\d{4}-\d{2}-\d{2}", data["date"]):
    errors.append("Invalid date format")
if data["total"] <= 0:
    errors.append("Total must be positive")
if not data["vendor_name"]:
    errors.append("Vendor name cannot be empty")
```

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Assuming tool_use catches all errors** | It only guarantees structure, not semantic correctness |
| **No validation after tool_use** | Content might be wrong even though structure is valid |
| **Not using enums with 'other'** | Unexpected values break schema |
| **Not marking optional fields as nullable** | Missing optional data fails validation |

### Exam Tip 🎯
**tool_use guarantees STRUCTURE, not SEMANTICS.** The exam will present options claiming tool_use eliminates all errors — that's always wrong. You still need to validate extracted values.

---

## d4.4 — Validation-Retry Loops & Multi-Pass Review

### Core Concepts

**Validation-retry loops** append specific errors and retry for self-correction. **Multi-pass review** uses local analysis + cross-file integration for reliability.

**Key Understanding:**
- **Validation-retry loop** — Extract → Validate → Append specific errors → Retry (self-correct)
- **Specific error feedback** — "Date field is 2 days in future (2024-05-25)" not "Date is wrong"
- **tracked patterns** — Identify systematic failures across documents
- **Multi-pass review** — Pass 1 (local analysis), Pass 2 (cross-file integration)
- **Same-session self-review is limited** — Reviewer retains generator's reasoning → blind spots
- **Batch processing strategy** — Sync for blocking tasks, Batch API for non-urgent (50% savings)

### Validation-Retry Loop Pattern

```
Step 1: Extract data using tool_use
    ↓
Step 2: Validate against business rules
    ↓
Step 3: If invalid, append SPECIFIC error details
    ↓
Step 4: Retry with explicit feedback
    ↓
Step 5: Model self-corrects based on feedback
    ↓
Step 6: Track systematic failures (detected_pattern)
```

### Specific Error Feedback

| Wrong (Generic) | Right (Specific) |
|---|---|
| "There were errors, try again" | "Invoice total ($500) doesn't match line items sum ($450); tax is percentage (10%) instead of dollar amount ($50)" |
| "Validation failed" | "Date 2024-05-25 is 2 days in the future; invoice date must be ≤ today" |
| "Please correct the data" | "Vendor name is blank; must be non-empty string matching [A-Za-z0-9 ]" |

### Code Pattern

```python
def extract_with_validation(document, max_retries=3):
    messages = [{"role": "user", "content": f"Extract: {document}"}]
    
    for attempt in range(max_retries):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            tools=[extract_tool],
            tool_choice={"type": "tool", "name": "extract_invoice"},
            messages=messages,
        )
        
        data = parse_tool_response(response)
        errors = validate(data)
        
        if not errors:
            return data  # Valid — success!
        
        # CRITICAL: Append SPECIFIC errors for retry
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": f"Validation failed. Fix these errors:\n"
                + "\n".join(f"- {e}" for e in errors)
                + "\nRe-extract with corrections."
        })
    
    raise ExtractionError(f"Failed after {max_retries} attempts")

def validate(data):
    errors = []
    if data["total"] <= 0:
        errors.append(f"Total must be positive, got {data['total']}")
    if sum(i["total"] for i in data["line_items"]) != data["subtotal"]:
        errors.append(f"Line items sum (${sum(...)}) doesn't match subtotal (${data['subtotal']})")
    if not re.match(r"\d{4}-\d{2}-\d{2}", data["date"]):
        errors.append(f"Date must be ISO 8601 format (YYYY-MM-DD), got {data['date']}")
    return errors
```

### Multi-Pass Review Strategy

```
Pass 1 (Local Analysis):
├── Per-file syntax checking
├── Naming conventions
├── Missing error handling
└── Documentation completeness

    ↓ (Results from Pass 1)

Pass 2 (Cross-File Integration):
├── Import path validation
├── Interface compatibility
├── Data flow consistency
└── Integration points
```

### Same-Session Self-Review Limitation

| Pattern | Effectiveness | Why |
|---|---|---|
| **Same session generate + review** | ❌ Low | Reviewer retains generator's reasoning → confirmation bias |
| **Separate sessions** | ✅ High | Reviewer has fresh perspective, no generator context |

### Batch Processing Strategy

| Scenario | Approach | Why |
|---|---|---|
| Blocking PR review | Synchronous (-p) | Need immediate feedback before merge |
| Real-time feedback | Synchronous (-p) | Can't wait 24 hours |
| Nightly code audit | Batch API | Time-flexible, saves 50% cost |
| Weekly compliance scan | Batch API | Time-flexible, saves 50% cost |

### Anti-Patterns to Avoid ❌

| Anti-Pattern | Why It's Wrong |
|---|---|
| **Same-session self-review** | Confirmation bias; reviewer sees through generator's eyes |
| **Generic retry without error details** | Model has no specific feedback to correct on |
| **Aggregate accuracy masking per-type failures** | 95% accuracy hides that extraction fails 50% for complex invoices |
| **Assuming all retries help** | After 2-3 retries, model often repeats same error |

### Exam Tip 🎯
**Three must-know facts:** 
1. **Retry with SPECIFIC error details**, not generic messages
2. **Same-session self-review is an anti-pattern** — use separate sessions
3. **Use Batch API for non-urgent tasks (50% cost savings)**

---

## Key Exam Tips for Domain 4

1. **Explicit, measurable criteria > vague instructions** — Always specific
2. **2-4 few-shot examples is the sweet spot** — Include at least one edge case
3. **tool_use = structural compliance, NOT semantic correctness** — Always validate
4. **Specific error feedback for retries** — Not generic "try again"
5. **Same-session self-review is an anti-pattern** — Use separate sessions
6. **Batch API for non-urgent work** — 50% cost savings with 24-hour window

---

## Related Exam Scenarios

- **Scenario 2**: Code Generation with Claude Code — Tests prompt design, few-shot patterns, and iterative refinement
- **Scenario 5**: Claude Code for CI/CD — Tests multi-pass review, validation-retry loops, batch processing
- **Scenario 6**: Structured Data Extraction — Tests JSON schemas, tool_use, validation-retry, few-shot prompting

---

## Summary Table

| Sub-Domain | Focus | Critical Concept | Exam Weight |
|---|---|---|---|
| **d4.1** | Explicit Criteria | Measurable criteria eliminate false positives; avoid vague instructions | 25% of Domain 4 |
| **d4.2** | Few-Shot Prompting | 2-4 examples optimal; include edge case coverage | 20% of Domain 4 |
| **d4.3** | Tool Use Output | tool_use guarantees structure, not semantics; always validate | 30% of Domain 4 |
| **d4.4** | Validation-Retry | Specific error feedback; separate sessions; Batch API for cost savings | 25% of Domain 4 |
