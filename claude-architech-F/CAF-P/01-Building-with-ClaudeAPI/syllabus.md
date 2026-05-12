# Building with Claude API — Complete Curriculum

## Course Overview

### Introduction
- Welcome to the course
- What you'll learn in this course
- How to get the most out of this material

### Anthropic Overview
- What is Anthropic?
- Overview of Claude models (Opus, Sonnet, Haiku)
- Claude capabilities and use cases
- Comparison with other LLMs

---

## Module 1: Accessing Claude with the API

### Accessing the API
- Creating an Anthropic client
- Authentication and API keys
- Environment variable management (.env)
- API endpoints and versioning

### Getting an API Key
- Signing up for Anthropic API
- Managing API keys
- Rate limits and quotas

### Making a Request
- Basic API call structure
- Request parameters
- Response structure
- Understanding message objects

**Code**: `01_requests.py`

### Multi-Turn Conversations
- Message history management
- Adding user and assistant messages
- Maintaining conversation context
- Context preservation across turns

**Code**: `02_Multi-turn-conversation.py`

### Chat Exercise
- Build an interactive chatbot
- Handle user input
- Implement conversation limits

**Code**: `03_chat_bot.py`, `04_Math-tutor-bot.py`

### System Prompts
- Defining assistant behavior
- System vs user messages
- Role-based prompting
- Prompt injection prevention

### System Prompts Exercise
- Create domain-specific assistants
- Test prompt effectiveness

### Temperature
- Understanding randomness in generation
- Temperature values (0.0 to 1.0)
- When to use deterministic (0) vs creative (1)
- Impact on output consistency

### Response Streaming
- Real-time token streaming
- Using `client.messages.stream()`
- Standard vs fine-grained streaming modes
- Handling stream events
- Reconstructing complete responses

**Code**: `05_streaming.py`

### Structured Data
- Prefills for output guidance
- Stop sequences for response control
- JSON format enforcement
- Code format guidance

**Code**: `06_prefills-and-stopsequences.py`

### Structured Data Exercise
- Guarantee JSON output
- Control response termination
- Enforce specific formats

### Quiz on Accessing Claude with the API
- Fundamentals assessment
- Multi-turn conversation understanding
- API parameter knowledge

---

## Module 2: Prompt Evaluation

### Prompt Evaluation
- Introduction to systematic evaluation
- Why prompt evaluation matters
- Automating quality assessment

### A Typical Eval Workflow
- Dataset preparation
- Prompt execution
- Result collection
- Performance analysis

### Generating Test Datasets
- Creating representative test cases
- Edge case identification
- Expected output definition
- Dataset structure

### Running the Eval
- Executing prompts against test cases
- Batch processing
- Collecting outputs
- Tracking metrics

**Code**: `01_prompt_evaluation.py`

### Model Based Grading
- Using Claude to grade responses
- Semantic evaluation
- Scoring frameworks
- Automatic assessment

### Code Based Grading
- Syntax validation (JSON, Python, regex)
- Format checking
- Error detection
- Regex-based grading

### Exercise on Prompt Evals
- Design an evaluation rubric
- Create test datasets
- Run evaluation pipeline
- Interpret results

**Files**: `dataset.json`, `eval_results.json`

### Quiz on Prompt Evaluation
- Evaluation methodology
- Grading approaches
- Dataset generation

---

## Module 3: Prompt Engineering Techniques

### Prompt Engineering
- Introduction to prompt engineering
- Why good prompts matter
- Iterative improvement

### Being Clear and Direct
- Avoiding ambiguity
- Explicit instructions
- Simple language
- Direct requests

### Being Specific
- Providing context
- Detailed requirements
- Example specifications
- Output format details

### Structure with XML Tags
- Using XML for clarity
- Hierarchical organization
- Section separation
- Complex instruction formatting

### Providing Examples
- One-shot prompting (1 example)
- Multi-shot prompting (multiple examples)
- Few-shot learning
- Format demonstration

### Exercise on Prompting
- Optimize prompts for accuracy
- Test different approaches
- Compare results

**Code**: `01_prompt_evaluator.py`

### Quiz on Prompt Engineering Techniques
- Best practices
- Prompting strategies
- Optimization methods

---

## Module 4: Tool Use with Claude

### Introducing Tool Use
- What are tools?
- Why use tools with Claude?
- Tool vs function implementations
- Real-world applications

### Project Overview
- Weather API integration
- Multi-tool agent system
- Tool orchestration

### Tool Functions
- Implementing tool logic
- Input validation
- Error handling
- Return value formatting

**Code**: `01-weather-api.py`

### Tool Schemas
- JSON schema definition
- Parameter specification
- Type definitions
- Required vs optional parameters

### Handling Message Blocks
- Detecting tool calls in responses
- Extracting tool use information
- Tool call structure
- Content block types

### Sending Tool Results
- Formatting tool results
- Error reporting with `is_error` flag
- Result structure
- Tool result integration

### Multi-Turn Conversations with Tools
- Tool use loop pattern
- Maintaining conversation context
- Tool call chains
- Managing state

### Implementing Multiple Turns
- Loop until `stop_reason != "tool_use"`
- Tool execution flow
- Result aggregation
- Conversation management

**Code**: `02-multiTool.py` (PRIMARY EXAMPLE)

### Using Multiple Tools
- Tool routing
- Multiple tool calls per response
- Tool batching
- Sequential execution

### Fine Grained Tool Calling
- Standard streaming mode (always-valid JSON)
- Fine-grained streaming mode (incremental)
- JSON parsing robustness
- Error handling in streams

**Code**: `03-Toolcall-and-streaming.py`

### The Text Edit Tool
- Built-in text editor tool
- File operations
- Edit capabilities

**Code**: `04-textEditor-tool.py`

### The Web Search Tool
- Built-in web search
- Search integration
- Result processing

**Code**: `05-webSearch-Tool.py`

### Documentation
- `TOOL_USE_COMPLETE_GUIDE.md` — Comprehensive tool use guide
- `STREAMING_GUIDE.md` — Streaming with tools

### Quiz on Tool Use with Claude
- Tool definition understanding
- Multi-turn agent loops
- Tool execution patterns

---

## Module 5: RAG and Agentic Search

### Introducing Retrieval Augmented Generation
- RAG problem statement
- Context window limitations
- Prompt stuffing vs RAG
- RAG architecture

### Text Chunking Strategies
- Size-based chunking (fixed character count with overlap)
- Structure-based chunking (markdown headers)
- Sentence-based chunking (NLP groupings)
- Semantic-based chunking (embedding similarity)
- Overlap for context preservation

**Code**: `01-Rag-ways-to-chunk.py`

### Text Embeddings
- Vector representations
- VoyageAI integration
- Document vs query embeddings
- Embedding dimensions
- Cosine similarity

**Code**: `02-SemanticSearch.py`

### The Full RAG Flow
- Document preprocessing
- Chunk generation
- Embedding computation
- Query embedding
- Similarity search
- Context assembly
- Prompt generation

### Implementing the RAG Flow
- End-to-end pipeline
- Storage and retrieval
- Integration with Claude

**Code**: Interactive notebooks

### BM25 Lexical Search
- Keyword-based retrieval
- Term frequency weighting
- Rare term boosting
- BM25 algorithm

### Hybrid Search Approaches
- Combining semantic and lexical search
- Reciprocal Rank Fusion (RRF)
- Score merging strategies
- Result ranking

### A Multi-Index RAG Pipeline
- Managing multiple document collections
- Index strategies
- Scalable retrieval

**Files**: `RAG.md` — Complete RAG guide

---

## Module 6: Features of Claude

### Extended Thinking
- What is extended thinking?
- Thinking blocks vs text blocks
- Reasoning process transparency
- Trade-offs: cost vs accuracy

**Implementation**:
- `thinking=True` parameter
- `thinking_budget` (minimum 1024 tokens)
- ThinkingBlock structure
- RedactedThinkingBlock handling
- Cryptographic signatures

**Incompatibilities**: 
- Cannot use with prefills
- Cannot use with temperature control

**Code**: `06-Extended-thinking.py`

### Image Support (Vision Capabilities)
- Image analysis and description
- Supported formats (PNG, JPG, GIF, WebP)
- Image limits:
  - 100 images per request
  - 5MB max per image
  - 8000px single / 2000px multi-image
  - Token cost: (width × height) / 750

**Prompting Strategies**:
- Step-by-step analysis
- One-shot examples
- Detailed guidelines
- Real-world: Fire risk assessment

**Code**: `02-vision-capability-of-claude.py`

### PDF Support (Document Processing)
- Analyzing PDF documents
- Document blocks (different from image blocks)
- Media type: `application/pdf`
- Multi-page document handling
- Extracting text, tables, images from PDFs

**Direct PDF vs RAG**:
- Direct analysis: small PDFs, one-off queries
- RAG approach: large PDFs, multiple queries
- Cost comparison and trade-offs
- Multi-turn PDF conversations

**Code**: `03-pdf-analysis.py`

### Citations
- Why citations matter (transparency, trust)
- Citation structure and metadata:
  - `cited_text` — exact quoted text
  - `document_title` — source document
  - `start_page_number` / `end_page_number` — location
  - `document_index` — for multiple documents
- Enabling citations: `"citations": {"enabled": True}`
- Plain text support (character positions)
- Building citation-aware UIs
- Use cases: legal, compliance, academic

**Code**: `04-citations.py`

### Prompt Caching
- Reducing costs and latency
- Caching strategy
- Cache key management
- Token usage with caching

### Rules of Prompt Caching
- When caching applies
- Cache efficiency
- Context window management

### Prompt Caching in Action
- Implementation patterns
- Monitoring cache hits
- Performance optimization

### Code Execution and the Files API
- File operations
- Executing code
- Managing file context

### Quiz on Features of Claude
- Feature understanding
- Implementation details
- Trade-offs and limitations

**Documentation**: `Features-of-claude.md` — Complete feature reference

---

## Module 7: Model Context Protocol

### Introducing MCP
- What is MCP?
- MCP architecture
- Server-client model
- Tool standardization

### MCP Clients
- Client implementation
- Server communication
- Tool discovery

### Project Setup
- Project structure
- Dependencies
- Configuration

**Code**: `app/main.py`

### Defining Tools with MCP
- `@mcp.tool()` decorator
- Pydantic Field documentation
- Parameter definition
- Type annotations

### The Server Inspector
- Tool inspection
- Capability discovery
- Metadata examination

### Implementing a Client
- Client creation
- Tool registration
- Tool execution

### Defining Resources
- Resource types
- Resource definition
- Metadata

### Accessing Resources
- Resource retrieval
- Access patterns
- Error handling

### Defining Prompts
- Custom prompts
- Prompt templates
- Parameterized prompts

### Prompts in the Client
- Using defined prompts
- Prompt execution
- Result handling

### MCP Review
- Architecture summary
- Best practices
- Common patterns

### Quiz on Model Context Protocol
- MCP fundamentals
- Tool definition
- Client-server communication

**Code**: 
- `app/tools/document.py` — Document processing
- `app/tools/math.py` — Math operations
- `tests/test_document.py` — Testing
- `pyproject.toml` — Project config

---

## Module 8: Anthropic Apps - Claude Code and Computer Use

### Anthropic Apps
- Overview of Anthropic applications
- Claude Code capabilities
- Computer use agent

### Claude Code Setup
- Installation
- Configuration
- Environment setup

### Claude Code in Action
- Building applications
- Real-time development
- Interactive coding

### Enhancements with MCP Servers
- Integrating MCP tools
- Tool availability
- Enhanced capabilities

---

## Module 9: Agents and Workflows

### Agents and Workflows
- Difference between agents and workflows
- When to use each
- Architecture patterns

### Parallelization Workflows
- Running independent tasks in parallel
- Concurrent execution
- Result aggregation

### Chaining Workflows
- Sequential task execution
- Passing context between steps
- Dependency management

### Routing Workflows
- Decision-based routing
- Conditional execution
- Multi-path flows

### Agents and Tools
- Agent design
- Tool integration
- Control flow

### Environment Inspection
- System information
- Available resources
- Configuration discovery

### Workflows vs Agents
- Architectural comparison
- Use case selection
- Trade-offs

### Quiz on Agents and Workflows
- Design patterns
- Implementation strategies
- Best practices

---

## Module 10: Interview Preparation & Assessment

### Interview Questions Bank
- **113 Total Questions** across all topics:
  - Claude API Fundamentals (7 questions)
  - Streaming (6 questions)
  - Prompt Engineering (7 questions)
  - Prompt Evaluation (6 questions)
  - Tool Use (10 questions)
  - Streaming + Tool Use (3 questions)
  - RAG (13 questions)
  - MCP (4 questions)
  - Systems Design (5 questions)
  - Behavioral Scenarios (4 questions)
  - Extended Thinking (9 questions)
  - Vision Capabilities (8 questions)
  - PDF Processing (7 questions)
  - Direct PDF vs RAG (6 questions)
  - Citations (9 questions)
  - Multi-Turn Document Conversations (3 questions)
  - PDF Comparison & Batch Analysis (4 questions)

**File**: `genai-interview.md`

### Final Assessment
- Comprehensive exam covering all modules
- Practical implementation tasks
- Real-world scenario problem-solving
- Code review and optimization

---

## Course Resources

### Code Implementations
- Complete, runnable examples for each module
- Real-world patterns and best practices
- Integration examples

### Documentation
- Feature guides (`Features-of-claude.md`)
- Tool use guide (`TOOL_USE_COMPLETE_GUIDE.md`)
- RAG guide (`RAG.md`)
- Streaming guide (`STREAMING_GUIDE.md`)

### Data Files
- Sample datasets for evaluation
- Test PDFs (`earth.pdf`)
- Property images for vision testing
- Evaluation results examples

---

## Learning Outcomes

By completing this course, you will be able to:

1. **Build Production Claude Applications**
   - Make API requests and handle responses
   - Implement multi-turn conversations
   - Control output format and behavior

2. **Engineer Effective Prompts**
   - Apply prompt engineering best practices
   - Evaluate and iterate on prompts
   - Optimize for accuracy

3. **Implement Tool Use Patterns**
   - Design and register tools
   - Create agentic loops
   - Handle multiple tools and streaming

4. **Build RAG Systems**
   - Implement various chunking strategies
   - Create semantic and hybrid search
   - Manage large document collections

5. **Leverage Advanced Features**
   - Enable extended thinking for complex reasoning
   - Analyze images and PDFs
   - Implement citation-aware systems
   - Enable prompt caching for efficiency

6. **Design Production Systems**
   - Implement MCP servers and clients
   - Build agent and workflow systems
   - Create scalable architectures
   - Handle error cases gracefully

---

## Technologies & Tools

- **Python 3.8+**
- **Anthropic SDK** (anthropic library)
- **Libraries**: dotenv, requests, voyageai, pydantic, pytest, uv
- **External APIs**: wttr.in (weather), waqi.info (air quality), VoyageAI (embeddings)
- **Protocols**: MCP (Model Context Protocol)

---

## Prerequisites

- Python programming proficiency
- Basic understanding of APIs and HTTP requests
- Familiarity with JSON format
- Command line basics
- Optional: Basic NLP/ML concepts

---

## Course Structure

```
Codes/
├── 01-Accessing-Claude-with-api/
│   ├── 01_requests.py
│   ├── 02_Multi-turn-conversation.py
│   ├── 03_chat_bot.py
│   ├── 04_Math-tutor-bot.py
│   ├── 05_streaming.py
│   └── 06_prefills-and-stopsequences.py
├── 02-Prompt-evaluation/
│   ├── 01_prompt_evaluation.py
│   ├── dataset.json
│   └── eval_results.json
├── 03-Prompt-engineering-techniques/
│   ├── 01_prompt_evaluator.py
│   └── [guides and examples]
├── 04-Tools-use/
│   ├── 01-weather-api.py
│   ├── 02-multiTool.py
│   ├── 03-Toolcall-and-streaming.py
│   ├── TOOL_USE_COMPLETE_GUIDE.md
│   └── STREAMING_GUIDE.md
├── 05-RAG/
│   ├── 01-Rag-ways-to-chunk.py
│   ├── 02-SemanticSearch.py
│   ├── RAG.md
│   └── [data files]
├── 06-Feature-of-claude/
│   ├── 01-Extended-thinking.py
│   ├── 02-vision-capability-of-claude.py
│   ├── 03-pdf-analysis.py
│   ├── 04-citations.py
│   ├── Features-of-claude.md
│   ├── earth.pdf
│   └── images/
├── 08-ClaudeCodeinAction/
│   └── [MCP implementation]
└── genai-interview.md
```

---

## Suggested Learning Path

1. Start with Module 1: Accessing Claude with the API (fundamentals)
2. Move to Module 2: Prompt Evaluation (testing mindset)
3. Learn Module 3: Prompt Engineering (optimization)
4. Implement Module 4: Tool Use (advanced interaction)
5. Build with Module 5: RAG (scale to documents)
6. Explore Module 6: Features (extend capabilities)
7. Study Module 7: MCP (production patterns)
8. Design Module 8 & 9: Apps and Agents (architecture)
9. Review Module 10: Interview Prep (assessment)

---

## Getting Started

1. Clone/download the course materials
2. Set up Python environment (`python -m venv venv`)
3. Install dependencies (`pip install -r requirements.txt`)
4. Create `.env` file with `ANTHROPIC_API_KEY`
5. Start with Module 1 code examples
6. Follow along with exercises
7. Test with provided datasets
8. Practice interview questions

---

## Assessment

- **Quizzes**: End-of-module knowledge checks
- **Exercises**: Hands-on implementation practice
- **Interview Questions**: Comprehensive question bank (113 questions)
- **Final Assessment**: Capstone project and exam

---

*Last Updated: May 2026*  
*Total Modules: 10 | Total Code Examples: 20+ | Interview Questions: 113*

---

## Quick Reference: Course Topics Table

| Module | Topics | Key Code Files |
|--------|--------|-----------------|
| **1. Accessing Claude with API** | Accessing API • API Keys • Making Requests • Multi-Turn Conversations • Chat Exercise • System Prompts • Temperature • Response Streaming • Structured Data • Quiz | `01_requests.py` `02_Multi-turn-conversation.py` `03_chat_bot.py` `05_streaming.py` `06_prefills.py` |
| **2. Prompt Evaluation** | Prompt Evaluation • Eval Workflow • Generating Datasets • Running Eval • Model-Based Grading • Code-Based Grading • Exercise • Quiz | `01_prompt_evaluation.py` `dataset.json` `eval_results.json` |
| **3. Prompt Engineering** | Prompt Engineering • Being Clear & Direct • Being Specific • XML Tags • Providing Examples • Exercise • Quiz | `01_prompt_evaluator.py` |
| **4. Tool Use with Claude** | Introducing Tools • Tool Functions • Tool Schemas • Message Handling • Tool Results • Multi-Turn with Tools • Multiple Tools • Fine-Grained Calling • Text Editor Tool • Web Search Tool • Quiz | `01-weather-api.py` `02-multiTool.py` `03-Toolcall-and-streaming.py` `04-textEditor.py` `05-webSearch.py` `TOOL_USE_COMPLETE_GUIDE.md` |
| **5. RAG & Agentic Search** | Introducing RAG • Text Chunking • Text Embeddings • Full RAG Flow • Implementing RAG • BM25 Search • Multi-Index Pipeline | `01-Rag-ways-to-chunk.py` `02-SemanticSearch.py` `RAG.md` |
| **6. Features of Claude** | Extended Thinking • Image Support • PDF Support • Citations • Prompt Caching • Rules of Caching • Caching in Action • Code Execution • Files API • Quiz | `06-Extended-thinking.py` `02-vision-capability.py` `03-pdf-analysis.py` `04-citations.py` `Features-of-claude.md` |
| **7. Model Context Protocol** | Introducing MCP • MCP Clients • Project Setup • Defining Tools • Server Inspector • Implementing Client • Resources • Prompts • MCP Review • Quiz | `app/main.py` `app/tools/document.py` `app/tools/math.py` `tests/test_document.py` |
| **8. Anthropic Apps** | Anthropic Apps • Claude Code Setup • Claude Code in Action • MCP Enhancements | `08-ClaudeCodeinAction/` |
| **9. Agents & Workflows** | Agents & Workflows • Parallelization • Chaining • Routing • Agents with Tools • Environment Inspection • Workflows vs Agents • Quiz | - |
| **10. Interview & Assessment** | 113 Interview Questions • Behavioral Scenarios • Final Assessment | `genai-interview.md` |

---

## Quick Topic Checklist

### Core Concepts
- ✅ API Fundamentals & Authentication
- ✅ Multi-turn Conversations
- ✅ System Prompts & Temperature Control
- ✅ Response Streaming (Standard & Fine-grained)
- ✅ Prefills & Stop Sequences

### Optimization & Evaluation
- ✅ Prompt Engineering Best Practices
- ✅ Prompt Evaluation Framework
- ✅ Model-based & Code-based Grading
- ✅ Dataset Generation & Testing

### Advanced Patterns
- ✅ Tool Use (Single & Multi-turn)
- ✅ Tool Schemas & Agentic Loops
- ✅ RAG Systems (Chunking, Embeddings, Search)
- ✅ Hybrid Search (BM25 + Semantic + RRF)

### Features
- ✅ Extended Thinking (Advanced Reasoning)
- ✅ Vision Capabilities (Image Analysis)
- ✅ PDF Processing (Documents & Analysis)
- ✅ Citations (Source Attribution)
- ✅ Prompt Caching (Cost Optimization)

### Production Ready
- ✅ MCP (Model Context Protocol)
- ✅ Claude Code Implementation
- ✅ Agent & Workflow Design
- ✅ Scalable System Architecture

---

## At a Glance

**10 Modules | 10 Major Topics | 20+ Code Examples | 113 Interview Questions**
