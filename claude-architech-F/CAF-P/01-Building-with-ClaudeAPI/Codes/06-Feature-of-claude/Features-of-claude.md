# Features of Claude — Personal Revision Notes

## Contents

1. [Extended Thinking](#extended-thinking) — Advanced reasoning with visible thought process
2. [Vision Capabilities](#vision-capabilities) — Image analysis and understanding
3. [PDF Document Processing](#pdf-document-processing) — Direct PDF analysis and multi-document handling
4. [Direct PDF vs RAG](#direct-pdf-vs-rag-when-to-use-which) — Comparing direct analysis with RAG approach
5. [Citations](#citations-show-your-work) — Source attribution and transparency

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
