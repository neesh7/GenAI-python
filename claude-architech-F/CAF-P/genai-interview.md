# GenAI Interview Questions — Based on Your Study

---

## Section 1: Claude API Fundamentals

**Conceptual**
1. What is the difference between a `user` role message and a `system` prompt in the Claude API? When would you use each?
2. Why does the Claude API require you to send the full conversation history on every request, rather than maintaining state server-side?
3. What does `stop_reason` tell you, and what are the possible values? When would you see `"end_turn"` vs `"tool_use"` vs `"max_tokens"`?
4. What is the structure of a `messages.create()` response object? Walk through the key fields.

**Practical**
5. Write a minimal Python snippet to make a basic API call to Claude and print only the text response.
6. How would you implement a chatbot with a 10-query hard limit? What state would you track?
7. How do you preserve conversation context across multiple turns without server-side sessions?

---

## Section 2: Streaming

**Conceptual**
8. What is the difference between standard streaming and fine-grained (beta) streaming in the Claude API?
9. In standard streaming mode, why does JSON in tool arguments always arrive as valid JSON fragments? What guarantee does the API provide?
10. Why might fine-grained streaming require a `try/except` around JSON parsing of tool arguments, while standard mode does not?
11. What event types do you listen for when streaming a tool call response? (`content_block_start`, `content_block_delta`, `input_json` etc.)

**Practical**
12. Implement streaming output that prints tokens to the console in real time using the `anthropic` SDK.
13. How would you detect mid-stream that the model is about to make a tool call, and capture the tool arguments incrementally?

---

## Section 3: Prompt Engineering

**Conceptual**
14. What is a "prefill" in the Claude API and what practical problems does it solve? Give two examples.
15. What are stop sequences? How would you use them to guarantee single-line responses or enforce specific output termination?
16. What is the difference between one-shot and multi-shot prompting? When does multi-shot outperform zero-shot?
17. What is "temperature" in LLM generation, and what is the behavioral difference between `temperature=0` and `temperature=1`?
18. What risks come from overly broad or vague system prompts? How do you test whether a system prompt is effective?

**Practical**
19. You want Claude to always respond with valid JSON. What two techniques would you combine (prefill + what else) to guarantee format compliance?
20. Design a system prompt for a math tutoring bot that refuses to give direct answers and instead guides students through steps.

---

## Section 4: Prompt Evaluation

**Conceptual**
21. Why can't you rely solely on human review to evaluate LLM outputs at scale? What does an automated evaluation pipeline look like?
22. What is "model-based grading" and what makes it better (or worse) than syntax/regex-based validation?
23. What is the difference between evaluating for **correctness** vs evaluating for **format compliance**? Give examples of each.
24. How do you generate a representative test dataset for evaluating a prompt? What properties should it have?

**Practical**
25. Your prompt evaluation scores drop from 0.85 to 0.70 after a model version update. Walk through how you'd diagnose the regression.
26. Design an evaluation rubric (with numeric scores) for assessing the quality of an AI code review assistant.

---

## Section 5: Tool Use

**Conceptual**
27. What is the difference between a tool *schema* and a tool *implementation*? Which does the LLM see, and which does your code execute?
28. Explain the multi-turn tool use loop. What sequence of API calls happens between the user asking a question and getting a final answer that required one tool call?
29. What does `is_error: true` in a tool result signal to the model? How should the model respond to it?
30. What is the risk of an infinite agentic loop in tool use, and how do you prevent it?
31. When a model returns multiple tool calls in a single response, what is the correct way to handle them before sending back results?
32. What is the difference between the built-in `text_editor` tool and a custom tool you define yourself? When would you use each?

**Practical**
33. Write the JSON schema for a `get_stock_price` tool that accepts a stock ticker symbol (string, required) and an optional exchange (string, e.g. "NYSE").
34. Implement a `run_tools()` function that takes a list of `tool_use` content blocks and returns a list of `tool_result` messages.
35. You have a weather tool and a calendar tool. A user asks "Do I need an umbrella for my 3pm meeting tomorrow?" — describe the complete multi-turn flow your agent would execute.
36. How does `tool_choice` work? What are the three modes (`auto`, `any`, `tool`) and when would you force a specific tool?

---

## Section 6: Streaming + Tool Use

**Conceptual**
37. In fine-grained streaming mode, why might you receive an `input_json` delta chunk that contains syntactically invalid JSON?
38. How do you reconstruct tool call arguments from incremental streaming chunks?
39. What is the performance trade-off between standard and fine-grained streaming when tools are involved?

---

## Section 7: RAG (Retrieval Augmented Generation)

**Conceptual**
40. What is the core problem RAG solves that "prompt stuffing" (putting the whole document in context) cannot scale to solve?
41. Explain the four-stage RAG pipeline: preprocessing → chunking → retrieval → prompting.
42. Compare these four chunking strategies — when would you prefer each?
   - Size-based (fixed char count with overlap)
   - Structure-based (Markdown headers)
   - Sentence-based (NLP groupings)
   - Semantic-based (embedding similarity)
43. Why is chunk overlap important? What problem does it solve at chunk boundaries?
44. What is a text embedding? What does it mean for two chunks to be "close" in embedding space?
45. What is the difference between semantic search and keyword search for retrieval? When does semantic search outperform keyword search?
46. Why does VoyageAI (and similar APIs) distinguish between `"document"` and `"query"` input types when generating embeddings?
47. What is cosine similarity, and why is it preferred over Euclidean distance for comparing embeddings?
48. What are the failure modes of RAG? (e.g., retrieval misses, chunking artifacts, context window limits)

**Practical**
49. You have a 200-page PDF. Walk through, step by step, how you'd build a Q&A system over it using RAG.
50. A user asks a question that spans two sections of a document, but your chunks split them apart. How would you mitigate this?
51. Your RAG system returns relevant chunks but the model still gives wrong answers. What would you investigate first?
52. How would you evaluate the quality of your retrieval step independently from the generation step?

---

## Section 7b: Hybrid Search — BM25 + Semantic + RRF

**Conceptual**
53. What is the key failure mode of semantic-only search that motivates adding lexical search to a RAG pipeline? Give a concrete example.
54. How does BM25 (Best Match 25) rank documents? Walk through its four steps: tokenize → count → weight → rank.
55. Why do rare, specific terms (like incident IDs or product codes) get higher BM25 weight than common words like "the" or "a"?
56. What is Reciprocal Rank Fusion (RRF)? Write the formula and explain what each variable represents.
57. Why is RRF preferred over averaging raw scores when merging semantic and BM25 results?
58. In RRF, what does the constant `k` (default 60) control? What happens to results if you set `k=1` vs `k=60`?
59. A document ranks #1 in semantic search and #3 in BM25. Another ranks #4 in both. Which gets the higher RRF score and why?
60. What does the `SearchIndex` protocol enable in a hybrid retriever architecture? Why is interface consistency important here?
61. What is the difference between `input_type="query"` and `input_type="document"` in VoyageAI's embedding API, and why does it matter?

**Practical**
62. Your search for `"INC-2023-Q4-011"` using semantic-only retrieval returns a financial section that doesn't mention the ID. How would hybrid search fix this, and why?
63. Implement the RRF score calculation for three documents given their ranks in two indexes. Which document wins and why?
64. You're building a retriever that combines VectorIndex and BM25Index. Walk through how `add_documents` and `search` are coordinated across both indexes.
65. When would you add a third index to the Retriever (e.g., a keyword index or graph-based index)? What interface must it implement to plug in cleanly?
66. A user searches for a product name that is semantically related to many things but must exact-match. How would you weight BM25 vs semantic in your hybrid system?

---

## Section 8: MCP (Model Context Protocol)


**Conceptual**
53. What is MCP and what problem does it solve compared to defining tools inline in every API call?
54. How does the `@mcp.tool()` decorator work? What does it expose to the model?
55. What is the role of Pydantic `Field` descriptions in MCP tool definitions?
56. How does an MCP server differ architecturally from a direct API integration?

---

## Section 9: Systems Design & Architecture

**Conceptual**
57. You're building an AI assistant that can search the web, query a database, and write files. Design the agent loop — how does control flow between the LLM and tool execution?
58. How would you add observability (logging, tracing, latency tracking) to a production multi-turn agent?
59. What are the trade-offs between a single large system prompt vs dynamically constructing the prompt per request?
60. How do you handle secrets (API keys, DB credentials) in an agentic system that calls multiple external services?
61. A production RAG system's response quality degrades over time. What monitoring would you put in place, and what could cause this?

---

## Section 10: Behavioral / Scenario

62. You deployed a prompt and it works well on test cases but fails in production on edge cases users find. What's your process?
63. A product manager asks you to "make the AI more creative." How would you translate that into a concrete technical change, and how would you measure whether it worked?
64. Your tool-use agent is getting stuck in loops — the model keeps calling the same tool with the same arguments. How do you debug and fix this?
65. Explain the difference between a **chatbot**, an **agent**, and a **RAG system** to a non-technical stakeholder in one paragraph each.

---

## Section 11: Extended Thinking

**Conceptual**
66. What is extended thinking and how is it different from standard Claude generation?
67. Extended thinking has a cost trade-off. What are you paying for, and when is it worth the cost?
68. What does a `ThinkingBlock` contain versus a `TextBlock` in an extended thinking response?
69. What is "redacted thinking" and when does it occur? Is it an error or expected behavior?
70. Why does extended thinking include a cryptographic signature system? What problem does it solve?

**Practical**
71. What are the two incompatible features with extended thinking? Why can't they work together?
72. Write code to enable extended thinking with a `thinking_budget` of 5000 tokens and extract both the thinking and text from the response.
73. How would you test that your application gracefully handles redacted thinking blocks without crashing?
74. When should you enable extended thinking: before or after optimizing your prompt? Why?

---

## Section 12: Vision Capabilities

**Conceptual**
75. What types of content can Claude analyze in images beyond text? (Give at least three examples)
76. Why can't you send 100 images each at 8000px resolution in a single request, but you can send multiple images at 2000px resolution?
77. How are image tokens calculated? What's the formula for token cost?
78. Prompting with images: why does a simple question like "How many objects?" often fail, while a step-by-step methodology succeeds?

**Practical**
79. Write the code structure to include a satellite image (base64 encoded) with a text prompt in a single user message.
80. Design a one-shot prompting example for marble counting: show the expected format and what makes it effective.
81. You're building a fire risk assessment system using satellite imagery. What are the five key analysis steps you'd structure into your prompt?
82. Implement code to compare two satellite images with the prompt: "Which has higher fire risk and why?"

---

## Section 13: PDF Document Processing

**Conceptual**
83. Why does processing PDFs with Claude (as documents) work differently from converting PDFs to images first?
84. What can Claude extract from PDFs that goes beyond simple text extraction?
85. How do you structure a PDF document block differently from an image block in the message API?
86. What is the key difference between processing a PDF with base64 encoding vs a URL source?

**Practical**
87. Write the code to encode a PDF file to base64 and send it to Claude with a summarization prompt.
88. What media type should you use when sending a PDF as a document block? Why does it matter?
89. Design a prompt to extract financial data from a 50-page annual report. What structure would you use to ensure consistent output?

---

## Section 14: Direct PDF Analysis vs RAG

**Conceptual**
90. When should you use direct PDF analysis instead of RAG? Give specific document sizes/use cases.
91. What is the main cost difference between directly analyzing a PDF vs using RAG for repeated queries?
92. Why is RAG better for a searchable document library with 100+ PDFs?
93. For a single question about a 500-page legal contract, which approach is better and why?

**Practical**
94. Calculate the cost comparison: You have 10 PDFs (50 pages each) and 100 queries. Should you use direct analysis or RAG? Show the reasoning.
95. When would you use both approaches together in the same system? Describe the architecture.

---

## Section 15: Citations

**Conceptual**
96. What problem do citations solve that regular document analysis doesn't address?
97. How does enabling citations change the structure of Claude's response?
98. What information is included in a citation object? List all the fields.
99. Why does a citation include a cryptographic signature, and what does it protect against?
100. When are citations NOT necessary? Give three use cases where you can skip them.

**Practical**
101. Write the code to enable citations in a PDF document block. What two fields must you add?
102. How would you build a UI that shows citation markers and lets users click to see the source page?
103. A user asks Claude about information in a document. Claude cites pages 5-7. The user claims the info isn't on page 5. How would you debug this?
104. Implement code to extract and display all citations from a Claude response about a PDF, showing the cited text and page numbers.

---

## Section 16: Multi-Turn Document Conversations

**Conceptual**
105. Why is multi-turn conversation more useful than single queries for document analysis?
106. In a multi-turn PDF conversation, how does Claude maintain context about which document it's analyzing?
107. What are the benefits of citation-enabled multi-turn conversations vs standard conversations?

**Practical**
108. Design a multi-turn conversation flow for a research assistant analyzing a 100-page research paper. What would the first 5 turns look like?
109. Implement code that sends a PDF once, then asks 5 follow-up questions without re-sending the document.

---

## Section 17: PDF Comparison & Batch Analysis

**Conceptual**
110. Can Claude analyze multiple PDFs in a single API call? What are the limits?
111. Why would you compare two PDFs instead of analyzing them separately?

**Practical**
112. Write code to send two PDFs and ask: "Which document has more risk factors and why?"
113. Design a batch analysis pipeline that processes 10 PDFs with the same prompt. What would the structure be?

---

*113 questions across fundamentals, streaming, prompt engineering, evaluation, tool use, RAG, extended thinking, vision, PDF processing, citations, multi-turn conversations, and document comparison — directly tied to the implementations in this repo.*
