# Features of Claude — Personal Revision Notes

## Contents

1. [Extended Thinking](#extended-thinking) — Advanced reasoning with visible thought process
2. [Vision Capabilities](#vision-capabilities) — Image analysis and understanding
3. [PDF Document Processing](#pdf-document-processing) — Direct PDF analysis and multi-document handling
4. [Direct PDF vs RAG](#direct-pdf-vs-rag-when-to-use-which) — Comparing direct analysis with RAG approach
5. [Citations](#citations-show-your-work) — Source attribution and transparency
6. [Prompt Caching](#prompt-caching) — Speed and cost optimization through preprocessing reuse
7. [Files API & Code Execution](#files-api--code-execution) — Execute Python code and process files

---

## Extended Thinking

### What it is
- Claude's advanced reasoning feature — gives the model "scratch paper" time to work through problems before giving the final answer
- Response changes from a plain text block → **two parts**: a thinking block + a text block
- You can literally see Claude's reasoning process, which improves transparency and accuracy

### When to use it
- **Don't reach for it first.** Run prompts without thinking, optimize the prompt, and only enable thinking if accuracy still isn't meeting requirements
- Best for: complex multi-step reasoning, hard math/logic problems, tasks where you need to audit the reasoning chain

### Trade-offs to remember
| Pro | Con |
|-----|-----|
| Better reasoning on hard tasks | Costs more (thinking tokens are billed) |
| Higher accuracy | Higher latency |
| Transparent thought process | More complex response parsing in code |

---

## Response Structure

When thinking is enabled, the response content list has two blocks:
1. `ThinkingBlock` (or `RedactedThinkingBlock`) — the reasoning
2. `TextBlock` — the final answer

To extract only the final answer:
```python
def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])
```

---

## Redacted Thinking

- Sometimes the thinking block comes back **encrypted/redacted** instead of readable text
- Happens when Claude's internal safety systems flag the thinking content
- The redacted block still holds the full thinking in encrypted form — you can pass it back in future messages and Claude retains full context
- Use the magic trigger string to **test** that your app handles redacted blocks without crashing:
```python
thinking_test_str = "ANTHROPIC_MAGIC_STRING_TRIGGER_REDACTED_THINKING_46C9A13E193C177646C7398A98432ECCCE4C1253D5E2D82641AC0E52CC2876CB"
```

---

## Signature System (Security)

- Every thinking block includes a **cryptographic signature**
- Prevents you (or anyone) from tampering with the thinking text before passing it back to Claude
- Modified thinking → signature check fails → model won't trust the reasoning chain
- This is a safety guardrail: stops malicious steering of Claude through fake reasoning

---

## Implementation

### Chat function parameters to add
```python
def chat(
    messages,
    system=None,
    temperature=1.0,
    stop_sequences=[],
    tools=None,
    thinking=False,        # toggle thinking on/off
    thinking_budget=1024,  # min 1024 tokens
):
```

### Enabling thinking in API params
```python
if thinking:
    params["thinking"] = {
        "type": "enabled",
        "budget_tokens": thinking_budget,  # note: key is "budget_tokens", not "budget"
    }
```

### Calling with thinking on
```python
chat(messages, thinking=True)
chat(messages, thinking=True, thinking_budget=5000)  # increase budget for harder tasks
```

### Rules for `max_tokens` and `budget_tokens`
- `max_tokens` **must be greater than** `thinking_budget`
- Minimum `thinking_budget` = **1024**

---

## Incompatibilities — Important!

Extended thinking does **NOT** work with:
- Message **pre-filling** (assistant prefills)
- **Temperature** control

> Full list: https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#feature-compatibility

---

## Quick Mental Model

```
Standard call:   [user msg] → Claude → TextBlock
Thinking call:   [user msg] → Claude thinks... → ThinkingBlock + TextBlock
                                                   (may be redacted)
```

---

## Key Things to Not Mix Up

- `budget_tokens` ≠ `budget` — the API key is `budget_tokens`
- Redacted ≠ broken — redacted thinking is expected, not an error
- Thinking tokens are **billed separately** — don't leave high budgets on by default
- Thinking is a **last resort** optimization tool, not a default setting

---

# Vision Capabilities

## What it is
- Claude can analyze images in your messages
- Use cases: describe images, compare images, count objects, perform complex visual analysis
- Images can be sent as **base64-encoded data** or as **URLs**

## Limitations (Hard Caps)
| Limit | Spec |
|-------|------|
| Images per request | Max 100 across all messages |
| Size per image | Max 5MB |
| Single image dimensions | Max 8000px × 8000px |
| Multiple images dimensions | Max 2000px × 2000px each |
| Token cost | `(width × height) / 750` tokens per image |

## Message Structure

Images go in the **user message** as blocks alongside text:

```python
import base64

with open("image.png", "rb") as f:
    image_bytes = base64.standard_b64encode(f.read()).decode("utf-8")

add_user_message(messages, [
    {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/png",  # or image/jpeg, image/gif, image/webp
            "data": image_bytes,
        }
    },
    {
        "type": "text",
        "text": "What do you see in this image?"
    }
])
```

Or using a URL:
```python
add_user_message(messages, [
    {
        "type": "image",
        "source": {
            "type": "url",
            "url": "https://example.com/image.png",
        }
    },
    {
        "type": "text",
        "text": "Analyze this satellite image."
    }
])
```

## Prompting Strategy

**Simple questions often fail.** Just asking "How many objects?" won't give accurate results. Instead:

### Technique 1: Step-by-Step Analysis
Break down the task into explicit steps:
```
Analyze this image of marbles using this methodology:
1. Identify each unique marble one at a time and assign it a number
2. Verify by counting a different way (e.g., row by row from bottom-left)
What is the exact, verified count?
```

### Technique 2: One-Shot Examples
Include an example image with a known answer, then ask about your target:
```
Here's an example: [image of 15 marbles] The answer is 15.
Now, how many marbles are in this image? [target image]
```

### Technique 3: Detailed Guidelines
Provide Claude with a structured checklist:
```
Analyze for:
- Presence of X (yes/no)
- Estimate Y (0-25%, 25-50%, etc.)
- Rate Z on scale 1-4
```

## Real-World Example: Fire Risk Assessment

Automate fire risk assessment from satellite imagery:

**Analysis steps:**
1. **Residence identification**: Find the main house (largest roofed structure, driveway, regular geometry)
2. **Tree overhang**: Identify trees whose canopy extends over the roof; estimate % coverage
3. **Fire risk**: Evaluate wildfire vulnerability (ember catch, fuel paths, chimneys exposed)
4. **Defensible space**: Check for continuous canopy and fuel ladders (ground → tree → roof)
5. **Fire rating**: Assign 1-4 based on:
   - **1 (Low)**: No overhang, good defensible space
   - **2 (Moderate)**: <25% overhang, some tree separation
   - **3 (High)**: 25-50% overhang, connected canopies
   - **4 (Severe)**: >50% overhang, dense vegetation touching structure

The detailed, step-by-step prompt produces **far more accurate** results than "rate the fire risk."

## Key Takeaway

**Same rules apply:** Just like with text, investment in crafting detailed, structured prompts beats simple questions. Vision is powerful when paired with good prompt engineering.

---

# PDF Document Processing

## What it is
- Claude can read and analyze PDF files directly — similar to image processing, but for documents
- One-stop solution for extracting ANY type of information from PDFs
- No need for pre-conversion to text or images — Claude handles it all

## What Claude Extracts
Claude understands:
- **Text content** throughout the document
- **Embedded images and charts** within the PDF
- **Tables** and their data relationships
- **Document structure** and formatting
- **Metadata** and document properties

## Code Structure

Nearly identical to image processing, with these key changes:

```python
import base64

with open("earth.pdf", "rb") as f:
    file_bytes = base64.standard_b64encode(f.read()).decode("utf-8")

messages = []

add_user_message(messages, [
    {
        "type": "document",    # NOT "image"
        "source": {
            "type": "base64",
            "media_type": "application/pdf",  # NOT image/png
            "data": file_bytes,
        },
    },
    {"type": "text", "text": "Summarize this document"},
])

chat(messages)
```

## Key Differences from Image Processing

| Aspect | Images | PDFs |
|--------|--------|------|
| `type` | `"image"` | `"document"` |
| `media_type` | `"image/png"`, `"image/jpeg"` | `"application/pdf"` |
| Variable name | `image_bytes` | `file_bytes` (for clarity) |
| File extension | `.png`, `.jpg` | `.pdf` |
| Use case | Visual analysis | Document analysis, data extraction |

## Use Cases

1. **Document Summarization** — Extract key points from long PDFs
2. **Data Extraction** — Pull tables, figures, and structured data
3. **Compliance Review** — Check documents against standards
4. **Q&A over Documents** — Answer questions about PDF content
5. **Document Comparison** — Compare multiple PDFs
6. **Information Retrieval** — Find specific information in archives

## API Limits

Same as images in most respects, but PDFs can be longer:
- Files are converted to tokens based on page count and content complexity
- No strict file size limit, but very large PDFs will consume more tokens
- Claude can handle multi-page documents efficiently

## Prompting Strategy

Use the same techniques as vision:
- **Detailed step-by-step prompts** beat simple "summarize" requests
- **Structured extraction prompts** ensure consistent output format
- **Multi-turn conversations** work great for exploring document content
- **One-shot examples** can guide the extraction format

## Example: Extract Data from a Report

Instead of: `"Extract the financial data"`

Better: `"Extract financial data into a table with columns: Year | Revenue | Expenses | Net Profit. Only include years 2020-2024."`

---

## Quick Mental Model

```
PDF Processing Pipeline:
[PDF file] → base64 encode → send as "document" type → Claude → extracted data/summary/analysis
```

PDFs are treated as first-class document objects, not converted to images or text. This allows Claude to understand document structure, tables, and embedded visuals all at once.

---

## Direct PDF vs RAG: When to Use Which

**Direct PDF Analysis** works great, but it's not always the best choice. Here's when to use each:

### Use Direct PDF Analysis When:
- PDF is small-medium (< 50 pages)
- One-off analysis ("summarize this contract")
- You need full document context
- Budget is not a constraint

### Use RAG Instead When:
- PDF is large (100+ pages)
- Multiple queries over same document
- You're building a searchable document library
- Specific information retrieval ("find all mentions of X")
- Cost matters (repeated queries)
- You have 10+ PDFs to manage

### Cost Comparison
```
Direct PDF: Send entire 100-page PDF for every query = $$$ per query
RAG:        Setup once, then cheap retrievals = $ per query (10x cheaper)

For 50 questions:
Direct PDF: 50 × expensive = VERY expensive
RAG:        1 × setup + 50 × cheap = Much cheaper
```

---

# Citations: Show Your Work

## What it is
- Claude references specific parts of documents it's analyzing
- Shows users exactly WHERE information came from
- Creates transparency: "This came from page 15 of earth.pdf"
- Builds trust by showing Claude isn't making things up

## Why Citations Matter
Without citations, users assume Claude is drawing from training data. Citations prove Claude is actually referencing YOUR document:
- Users can **verify** information by checking the source
- Users can **explore** broader context around facts
- Builds **trust** through transparency
- Creates an **audit trail** for regulatory/compliance needs

## Enabling Citations

Add two fields to your document block:

```python
{
    "type": "document",
    "source": {
        "type": "base64",
        "media_type": "application/pdf",
        "data": file_bytes,
    },
    "title": "earth.pdf",              # Readable name for document
    "citations": {"enabled": True}    # Enable citation tracking
}
```

## Citation Data Structure

When citations are enabled, Claude's response includes citation objects:

```python
{
    "cited_text": "The atmosphere formed from...",  # Exact text from document
    "document_index": 0,                         # Which document (if multiple)
    "document_title": "earth.pdf",               # Your assigned title
    "start_page_number": 3,                      # Where citation starts
    "end_page_number": 5,                        # Where citation ends
}
```

## Using Citations with Plain Text

Citations work with text sources too:

```python
{
    "type": "document",
    "source": {
        "type": "text",
        "media_type": "text/plain",
        "data": article_text,
    },
    "title": "earth_article",
    "citations": {"enabled": True}
}
```

With text, instead of page numbers, you get **character positions** pinpointing exact location.

## Building UIs with Citations

Citations are most powerful when integrated into user interfaces:

```
User reads: "Earth's atmosphere formed from..."
            ↓ [Hover over citation marker]
User sees:  "Page 3 of earth.pdf"
            ↓ [Click to view]
User views: Full context around that quote
```

This creates a transparent research experience where users can:
- See answers are grounded in source material
- Verify information independently
- Understand context around facts
- Trust the analysis

## When to Use Citations

| Scenario | Use Citations? |
|----------|---|
| Legal/compliance document review | ✅ **Must** |
| Academic research | ✅ **Highly recommended** |
| Financial reports | ✅ **Highly recommended** |
| Internal knowledge lookup | ❌ Not critical |
| Quick document summary | ❌ Optional |

---

## Key Points

- **Citations ≠ RAG** — Citations show sources; RAG manages large documents
- **Both are complementary** — Use RAG for large doc management + citations for transparency
- **Trust builder** — Citations transform Claude from "black box" to "transparent researcher"
- **Multi-document friendly** — `document_index` lets you cite from specific documents when analyzing multiple PDFs

---

# Prompt Caching

## What it is
- Reuse preprocessing work from previous requests instead of discarding it
- Speeds up Claude's responses and reduces costs
- Works like a lookup table: "I've processed this content before, reuse that work"
- Automatic optimization: first request writes cache, follow-ups read from it

## How Claude Normally Works (Without Caching)

```
[Your message] → Tokenize → Embeddings → Context Analysis → Generate Response → Discard all work
```

For each request, Claude:
1. Tokenizes the prompt into smaller pieces
2. Creates embeddings for each token
3. Adds context based on surrounding text
4. **Then** generates the actual response
5. **Throws away** all preprocessing work

## The Problem

When you make follow-up requests with the same content, Claude **repeats all the same preprocessing work**:

```
Request 1: Preprocess document (10 seconds) → Generate answer → Throw away preprocessing
Request 2: Preprocess SAME document (10 seconds) → Generate answer → Throw away preprocessing
Request 3: Preprocess SAME document (10 seconds) → Generate answer → Throw away preprocessing
```

This is wasteful when analyzing the same document multiple times.

## How Prompt Caching Solves This

```
Request 1: Preprocess document (10 sec) → SAVE to cache → Generate answer
Request 2: Reuse cached preprocessing (instant) → Generate answer (faster)
Request 3: Reuse cached preprocessing (instant) → Generate answer (faster)
```

Cache acts as a lookup table: "If I see this content again, reuse this preprocessing."

## Key Benefits

| Benefit | Impact |
|---------|--------|
| **Faster responses** | Cached requests execute much quicker |
| **Lower costs** | Pay less for cached portions of requests |
| **Automatic** | No manual cache management needed |
| **Transparent** | Works seamlessly in the background |

## Important Limitations

| Limitation | Details |
|-----------|---------|
| **Cache duration** | Only lives for **1 hour** |
| **Limited use cases** | Only beneficial with **repeated same content** |
| **High frequency** | Most effective when same content appears **very frequently** |
| **Cost threshold** | Only worthwhile for large, repeated content |

## When Caching Helps

✅ **Good use cases:**
- Asking multiple questions about the same 100-page document
- Iterative refinement of content (keep base, change specific parts)
- Document analysis workflows with many variations
- Code review across multiple files (same codebase analyzed many times)

❌ **Poor use cases:**
- One-off document analysis
- Conversations with constantly changing content
- Small documents (less than ~1000 tokens)
- Rare, one-time requests

## Real-World Example

**Scenario:** Legal contract review with 5 follow-up questions

Without caching:
```
Q1: Read contract (10s preprocessing) + answer (2s) = 12s
Q2: Read contract (10s preprocessing) + answer (2s) = 12s
Q3: Read contract (10s preprocessing) + answer (2s) = 12s
Q4: Read contract (10s preprocessing) + answer (2s) = 12s
Q5: Read contract (10s preprocessing) + answer (2s) = 12s
Total: 60 seconds, 50 seconds wasted on duplicate preprocessing
```

With caching:
```
Q1: Read contract (10s preprocessing) + CACHE IT + answer (2s) = 12s
Q2: Reuse cache (instant) + answer (2s) = 2s ✨ (10s faster)
Q3: Reuse cache (instant) + answer (2s) = 2s ✨ (10s faster)
Q4: Reuse cache (instant) + answer (2s) = 2s ✨ (10s faster)
Q5: Reuse cache (instant) + answer (2s) = 2s ✨ (10s faster)
Total: 20 seconds, 40 seconds saved
```

## Cost Impact

Cached tokens typically cost **10% of uncached tokens**:
- Uncached token: 1¢ per 1M tokens
- Cached token: 0.1¢ per 1M tokens (10x cheaper)

For 100K token document with 5 queries:
- **Without cache:** 100K × 5 = 500K tokens @ standard rate
- **With cache:** 100K @ standard + (100K × 4) @ 10% = 140K token equivalents (72% savings)

## Quick Mental Model

```
Prompt Caching = "Don't reprocess content I just processed"
                 = Faster responses + lower costs
                 = Best for multi-query document analysis
```

## Cache Breakpoints (Implementation)

Caching is **NOT automatic** — you must manually add cache breakpoints to specific blocks.

### How Cache Breakpoints Work

```
Request 1:
├─ System prompt
├─ [CACHE BREAKPOINT] ← All work up to here gets cached
├─ Document content (100KB)
├─ Initial question
└─ Generate answer

Request 2 (identical content up to breakpoint):
├─ System prompt (identical)
├─ [CACHE BREAKPOINT] ← Reuse cached work instantly
├─ Document content (identical)
├─ Different follow-up question ← Process only this part
└─ Generate answer (much faster)
```

### Adding a Cache Breakpoint

Use the **longhand form** with `cache_control` field (shorthand form doesn't support caching):

```python
# Shorthand (NO caching possible)
"text": "Your content here"

# Longhand (supports caching)
{
    "type": "text",
    "text": "Your content here",
    "cache_control": {"type": "ephemeral"}
}
```

### Cache Invalidation Rules

**Cache is ONLY reused if content is identical up to breakpoint:**
- Adding "please" = cache miss
- Changing one word = cache miss
- Reordering content = cache miss
- Even minor changes force full reprocessing

### What Can Be Cached

Not just text blocks — cache breakpoints work on:
- **System prompts** (excellent candidates — rarely change)
- **Tool definitions** (excellent candidates — constant across requests)
- **Image blocks**
- **Tool use and tool result blocks**
- **Messages** (entire message history up to a point)

### Cross-Message Caching

Cache breakpoints span **multiple messages**:

```python
messages = [
    {"role": "user", "content": [{"type": "text", "text": "Context A..."}]},
    {"role": "assistant", "content": [{"type": "text", "text": "Response A..."}]},
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Follow-up context...",
                "cache_control": {"type": "ephemeral"}  # Caches ALL previous + this
            }
        ]
    }
]
```

## Effective Cache Placement Strategy

### Cache Ordering

Claude processes requests in this order:
1. **Tools** (first) — cache tool definitions here
2. **System prompt** (next) — cache system prompt here
3. **Messages** (last) — cache message history here

### Strategic Placement

**Best practice:** Cache what stays constant, leave what changes uncached

```python
# System prompt + tools (constant) → Cache these
# Document content (constant) → Cache this
# User question (changes) → DON'T cache this

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": system_prompt_100KB, "cache_control": {...}},
            {"type": "text", "text": document_content_100KB, "cache_control": {...}},
            # No cache control on the question ↓
            {"type": "text", "text": "What is X?"}
        ]
    }
]
```

### Up to 4 Breakpoints

You can add **maximum 4 cache breakpoints** per request:

```python
# Example: Cache tools, system, context, then message history
1. Cache breakpoint on tools
2. Cache breakpoint on system prompt
3. Cache breakpoint on context (document)
4. Cache breakpoint on message history
→ New question processes without caching
```

## Minimum Content Threshold

**Critical:** Content must be **≥ 1024 tokens** to be cached

```
✅ 100KB document → easily over 1024 tokens → cacheable
✅ 50 similar paragraphs → likely over 1024 tokens → cacheable
❌ "Hi there!" → ~2 tokens → NOT cacheable
❌ Single short message → <1024 tokens total → NOT cacheable
```

The 1024 token minimum applies to the **total content up to the breakpoint**, not individual blocks.

## Implementation Pattern

**Optimal setup for document Q&A:**

```python
# Request 1: Write to cache
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Context: [100KB document]\n\nQuestion: What is X?",
                "cache_control": {"type": "ephemeral"}
            }
        ]
    }
]
response = client.messages.create(..., messages=messages)  # Caches document

# Request 2: Reuse cache (100% identical content up to breakpoint)
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Context: [100KB document]\n\nQuestion: What is Y?",  # DIFFERENT question
                "cache_control": {"type": "ephemeral"}  # Still gets cache hit!
            }
        ]
    }
]
response = client.messages.create(..., messages=messages)  # Reuses cache, MUCH faster
```

## Key Insights

- **Not automatic** — explicit `cache_control` required
- **Content must match** — byte-for-byte identical up to breakpoint
- **System + tools** — best ROI for caching (constant, rarely change)
- **1-hour TTL** — cache expires, must reprocess after 1 hour
- **1024 token minimum** — tiny requests won't benefit
- **Up to 4 breakpoints** — flexibility in granular caching

---

## Cache vs No Cache: When to Use

| Scenario | Use Caching? |
|----------|---|
| Document Q&A with multiple questions | ✅ **YES** (document + system cached) |
| Analyzing same code/document repeatedly | ✅ **YES** (constant context) |
| Iterative refinement (same base, changing request) | ✅ **YES** (base cached) |
| One-off analysis | ❌ No (no follow-ups) |
| Small requests (<1024 tokens) | ❌ No (minimum threshold) |
| Rapidly changing content | ❌ No (invalidates cache constantly) |

---

## Implementation: Tool Schema Caching

Tool schemas are excellent candidates for caching (typically 1.7K tokens for multiple tools).

**Safe approach** (avoid modifying original tools):

```python
if tools:
    tools_clone = tools.copy()  # Copy the list
    last_tool = tools_clone[-1].copy()  # Copy the last tool dict
    last_tool["cache_control"] = {"type": "ephemeral"}  # Add cache control
    tools_clone[-1] = last_tool  # Replace in copy
    params["tools"] = tools_clone  # Use copy, not original
```

This preserves your original tools and prevents issues if you reorder them later.

## Implementation: System Prompt Caching

System prompts need to be converted from strings to structured text blocks:

```python
# Before (no caching):
params["system"] = "You are a helpful assistant..."

# After (with caching):
if system:
    params["system"] = [
        {
            "type": "text",
            "text": system,
            "cache_control": {"type": "ephemeral"}
        }
    ]
```

This allows Claude to cache your system prompt (typically 1K-6K tokens).

## Understanding Cache Behavior

### Cache Usage Patterns

When caching is enabled, the response's `usage` field shows:

```python
response.usage
# First request:
# - cache_creation_input_tokens=1772  # Writing to cache
# - input_tokens=500                  # Uncached content
# Total cost: 1772 + 500 = 2272 tokens

# Follow-up request (identical tools + system):
# - cache_read_input_tokens=1772      # Reading from cache ✨
# - input_tokens=50                   # Uncached content (e.g., new question)
# Total cost: 1772 × 0.1 + 50 = 227 tokens (90% savings!)
```

### Cache Sensitivity

The cache is **extremely sensitive**:
- Changing 1 character in tools → invalidates tool cache
- Changing 1 character in system prompt → invalidates system cache
- Reordering message order → invalidates message cache
- Even whitespace differences → cache miss

```python
# These are DIFFERENT and will NOT reuse cache:
"You are a helpful assistant"
"You are a helpful assistant."  # Added period!

# Cache will be invalidated for both
```

## Cache Ordering and Breakpoints

Claude processes request components in a specific order:

```
Processing order (critical for understanding cache):

1. TOOLS (processed first)
   - If you cache tools here, they're available for all messages

2. SYSTEM PROMPT (processed next)
   - Tools already cached if identical
   - System prompt caching is independent

3. MESSAGES (processed last)
   - Can cache message history separately
   - New messages invalidate message cache only
```

### Partial Cache Hits

You can have partial cache reuse:

```python
# Scenario: Keep tools same, change system prompt

Request 1:
├─ Tools → Cache write (1.7K tokens)
├─ System prompt → Cache write (5K tokens)
└─ Message → Cache write (500 tokens)
Total: 7.2K tokens

Request 2 (same tools, different system):
├─ Tools → Cache read ✨ (1.7K @ 10% = 170 tokens)
├─ System prompt → Cache write (5.2K tokens)  # Changed, new cache
└─ Message → Same message? Cache read ✨ (500 @ 10% = 50 tokens)
Total: 170 + 5200 + 50 = 5.42K tokens

Savings: 7.2K → 5.42K (25% savings despite system change)
```

## When Cache Hits Occur

Cache is reused when:
- ✅ **Tools identical** → tools cache hit
- ✅ **System prompt identical** → system cache hit  
- ✅ **Message history identical** → message cache hit
- ❌ **Any change** → that component's cache invalidated (others may still hit)

## Real-World Implementation Pattern

```python
def query_with_caching(tools, system, messages, question):
    """Helper that enables caching on stable components."""
    
    params = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 2000,
        "messages": messages + [{"role": "user", "content": question}]
    }
    
    # Cache tools (rarely change)
    if tools:
        tools_clone = tools.copy()
        last_tool = tools_clone[-1].copy()
        last_tool["cache_control"] = {"type": "ephemeral"}
        tools_clone[-1] = last_tool
        params["tools"] = tools_clone
    
    # Cache system prompt (rarely change)
    if system:
        params["system"] = [
            {
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral"}
            }
        ]
    
    return client.messages.create(**params)

# Usage:
# Q1: Full cost (all cached)
result1 = query_with_caching(tools, system, [], "Question 1?")

# Q2: Cheap cost (reuses cache)
result2 = query_with_caching(tools, system, [], "Question 2?")

# Q3: Partial cost (new system, reuses tools)
different_system = "Different prompt"
result3 = query_with_caching(tools, different_system, [], "Question 3?")
```

## Practical Considerations

### Best Practices

1. **Cache stable content**
   - ✅ Tool schemas (same across all requests)
   - ✅ System prompts (same for a session)
   - ✅ Large documents (don't change per query)
   - ❌ User questions (change every request)

2. **Don't cache frequently changing content**
   - ❌ Real-time data that updates every second
   - ❌ User session variables
   - ❌ Any per-request customizations

3. **Monitor cache effectiveness**
   ```python
   # Check cache hit rate
   if response.usage.cache_read_input_tokens > 0:
       cache_hit_rate = response.usage.cache_read_input_tokens / (
           response.usage.cache_read_input_tokens + response.usage.cache_creation_input_tokens
       ) * 100
       print(f"Cache hit rate: {cache_hit_rate:.1f}%")
   ```

### Optimal Use Cases

| Scenario | Effectiveness | Why |
|----------|---|---|
| Multi-turn Q&A on same document | **Excellent** 🌟🌟🌟 | Document cached, questions change |
| Coding assistant with stable instructions | **Excellent** 🌟🌟🌟 | System + tools cached, code changes |
| Research with tool library | **Very Good** 🌟🌟 | Tools cached, each search different |
| Rapid iteration on same problem | **Very Good** 🌟🌟 | Context cached, prompts vary |
| One-off requests | **Poor** 🌟 | No follow-ups to benefit from cache |
| Highly dynamic content | **Poor** 🌟 | Everything changes each request |

### Cost Savings Calculation

```
Example: Legal document analyzer

Setup:
- System prompt: 5K tokens
- Tool definitions: 1.7K tokens  
- Document: 20K tokens (constant)
- Total cached: 26.7K tokens

Request pattern: 50 questions in one session

Without caching:
- 50 requests × (26.7K + 500 tokens/question) = 1.36M tokens

With caching:
- 1st request: 26.7K (cache write)
- 49 follow-ups: 49 × (26.7K × 0.1 + 500) = 131K tokens
- Total: 157.7K tokens

Savings: 1.36M → 157.7K = 88% reduction! 🚀
```

## Key Points

- **Manual opt-in** — Must add `cache_control: {"type": "ephemeral"}` to blocks
- **Identity-based** — Content must be identical up to breakpoint to reuse cache
- **Threshold:** Minimum 1024 tokens for a block to be cacheable
- **Scope:** System, tools, documents, message history all cacheable
- **Breakpoints:** Up to 4 per request for fine-grained control
- **TTL:** 1 hour — cache expires and must be regenerated (designed for session-length use)
- **ROI:** Highest on system prompts and tool definitions (stable, reused often)
- **Sensitivity:** Single character change invalidates that component's cache
- **Cost savings:** 10x cheaper for cached reads (10% of standard token cost)
- **Best for:** Applications making multiple requests with stable context

---

# Files API & Code Execution

## What They Are

Two complementary features that unlock powerful delegated computation:

- **Files API** — Upload files once, reference them by ID in future messages (instead of encoding as base64)
- **Code Execution** — Claude writes and executes Python code in isolated Docker containers

Individually useful; together they're transformative for data analysis and complex tasks.

## Files API

### How It Works

```
Traditional approach:
File → Base64 encode → Include in every message ❌ (wasteful)

Files API approach:
File → Upload once → Get file ID → Reference by ID in messages ✅ (efficient)
```

### Upload Pattern

```python
# Step 1: Upload file once
file_metadata = client.beta.files.upload(
    file=("streaming.csv", open("streaming.csv", "rb")),
)
file_id = file_metadata.id

# Step 2: Reference file ID in messages (can reuse)
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Analyze this data"},
            {"type": "document", "source": {"type": "file", "file_id": file_id}}
        ]
    }
]

# Step 3: Use the same file_id in multiple requests
response1 = client.messages.create(model=model, messages=messages)
response2 = client.messages.create(model=model, messages=messages)  # Reuse same file
```

### Benefits

- ✅ **Efficiency** — Upload once, use many times
- ✅ **Bandwidth** — Don't resend file data per request
- ✅ **Large files** — Practical for large datasets, not bound by message size
- ✅ **Cost** — Files cached after first use

## Code Execution Tool

### What It Is

A built-in tool Claude can use to execute Python code in an isolated environment:

```
Claude writes Python → Submits to code execution → Runs in Docker → Returns output
```

### Key Characteristics

| Aspect | Details |
|--------|---------|
| **Environment** | Isolated Docker container |
| **Network** | No access (can't call external APIs) |
| **Duration** | Execution within single request |
| **Multiple runs** | Claude can execute code multiple times in one conversation |
| **Input/Output** | Data goes through Files API (no network) |
| **Libraries** | Standard Python + data science stack (pandas, numpy, matplotlib, etc.) |

### Using Code Execution

```python
# Include code_execution tool in your request
messages = [{"role": "user", "content": "Analyze the CSV and create visualizations"}]

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4000,
    messages=messages,
    tools=[{"type": "code_execution_20250522", "name": "code_execution"}]
)
```

### Response Structure

When Claude uses code execution, the response contains:

1. **Text blocks** — Claude's analysis and explanations
2. **Server tool use blocks** — The actual code Claude wrote
3. **Code execution result blocks** — Output from running the code

```
Response:
├─ TextBlock: "I'll analyze the churn drivers..."
├─ ToolUseBlock: "import pandas as pd; df = pd.read_csv(...)"
├─ ToolResultBlock: Output and visualizations
├─ TextBlock: "The analysis shows that..."
└─ (Claude may iterate: more code → more results)
```

## Combining Files API + Code Execution

This is where the magic happens. Since Docker has no network access, Files API is the primary way to move data in/out:

### Complete Workflow

```
1. Upload file (CSV, dataset, etc.)
   ↓
2. Send message with:
   - Text request for analysis
   - File reference (using file_id)
   - Code execution tool enabled
   ↓
3. Claude:
   - Reads file from container
   - Writes Python code
   - Executes code
   - Generates visualizations
   - Produces output files
   ↓
4. Download results
   - Claude's analysis text
   - Generated visualizations
   - Output files
```

### Practical Example: Churn Analysis

```python
# Step 1: Upload streaming service data
file_metadata = client.beta.files.upload(
    file=("streaming.csv", open("streaming.csv", "rb")),
)

# Step 2: Request analysis with code execution
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Run detailed analysis to determine major drivers of churn. Generate at least one detailed plot summarizing findings."
            },
            {
                "type": "document",
                "source": {"type": "file", "file_id": file_metadata.id}
            }
        ]
    }
]

# Step 3: Call Claude with code execution enabled
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4000,
    messages=messages,
    tools=[{"type": "code_execution_20250522", "name": "code_execution"}]
)

# Step 4: Extract results
for block in response.content:
    if hasattr(block, "type") and block.type == "text":
        print(block.text)  # Claude's analysis
    elif hasattr(block, "type") and block.type == "code_execution_output":
        # Download generated visualization/file
        download_file(block.file_id)
```

## What You Can Do

With Files API + Code Execution:

✅ **Data Analysis**
- Load CSV files
- Generate plots and visualizations
- Perform statistical analysis
- Create reports with charts

✅ **Document Processing**
- Extract and transform data
- Parse structured/unstructured text
- Generate summaries
- Convert between formats

✅ **Image Processing**
- Manipulate and analyze images
- Generate thumbnails
- Apply filters and transformations

✅ **Mathematical Computation**
- Solve complex equations
- Run simulations
- Build models
- Optimize parameters

✅ **Report Generation**
- Combine analysis with formatting
- Create custom visualizations
- Generate PDFs or documents

## Limitations to Know

| Limitation | Impact |
|-----------|--------|
| **No network** | Can't fetch live data or call APIs |
| **Isolated** | Can't access local system files (except uploaded) |
| **Timeout** | Code must complete within request timeout |
| **Memory** | Limited RAM for large datasets |
| **Library gaps** | Only standard data science libraries available |

## Key Differences from Direct Code Execution

| Aspect | Files API + Code Execution | Direct API Call |
|--------|---------------------------|-----------------|
| **Setup** | Upload file once | Include file each request |
| **Reuse** | Reference by ID | Re-send base64 |
| **Execution** | Claude-controlled | You write the code |
| **Iteration** | Claude iterates naturally | You orchestrate loops |
| **Output** | Files available to download | Returned as data |

## Real-World Use Case Example

**Scenario:** Analyze streaming service churn

```
Input: streaming.csv (100MB file, 500K rows)
↓
1. Upload CSV using Files API
   - One-time operation
   - Get file_id back
↓
2. Ask Claude to analyze:
   "What are the churn drivers?"
↓
3. Claude:
   - Reads file with pandas
   - Analyzes subscriptions
   - Creates visualizations
   - Identifies patterns
↓
Output:
✓ Analysis text (churn drivers identified)
✓ Visualization (plot of key factors)
✓ Statistical summary
✓ Recommendations
```

## Best Practices

1. **Upload files early** — Do it once, reference many times
2. **Use code execution for computational tasks** — Let Claude handle the Python
3. **Trust Claude's iteration** — It will refine code if first attempt fails
4. **Check for file outputs** — Look for `code_execution_output` blocks with file IDs
5. **Download and verify** — Always check generated files before using

## Key Points

- **Two separate features** — Files API for efficient file handling, Code Execution for computation
- **Designed to work together** — No network in Docker means Files API is essential for I/O
- **Claude does the coding** — You ask, Claude writes and executes Python
- **Professional output** — Generates publication-quality visualizations and reports
- **Automated iteration** — Claude can refactor and improve code within one request
- **Best for:** Data analysis, document processing, complex computations
- **Not suitable for:** Real-time data, external API integration, network-dependent tasks
