# Gen AI Roadmap

## Phase 0 : Foundation of GenAI
  Goal: Setup environment, Understand the basics

1. **Intro to GenAI & LLms**
-  What is Generative AI ? LLms? Rags? - understanding the terminolgies ( tokens, embeddings, transformer, logits and response)
-  Understanding Transformer Architechture and History
-  Overview of OpenAI, Hugging Face, GPT
-  Tools: VsCode, UV, Python

2. **Project1** : Your First chatbot with OpenAI API
-  use OpenAI `Chat Completion` API
-  Simple CLI Based Chatbot
-  Intro to **Prompt Engineering**
  
## Phase 1: Prompt Engineering and Token Management

  Goal: Learn the art and science of interacting with LLms
1. **Prompt Engineering Deep Dive**
-  Zero-shot, Few-shot, chain-of-thought, Self-consistency( Multiple response generated then sampled then returned)
-  **Multi Modal Prompting:** Multimodal system prompting is when you define the AI’s behavior using more than one mode of input—not just text, but also images, audio, or video. This allows the model to understand context more deeply and respond with greater nuance.

Think of it as giving the AI multiple senses to interpret your intent.
-  parameters like temperature, top-p/top-k, tokens, max_lenght

2. **Project2**: Smart Email Generator
   - Take a subject and generate email copy
   - use prompt templates and roles

## Phase 2: Langchain Essentials
Goal: Understand how to build production apps using Langchain

1. **Langchain Basics**
-  Components: chains, tools, agents, memory, prompt templates

2. **Project3**: Ai-Powered PDF Q&A Bot
- upload PDF -> Chunk it -> Embed -> Query using OpenAI
- Tools: Langchain, FAISS, PyPDF, OpenAIEmbeddings

## Phase 3: RAG (Retrievel - Augmented Generation)
Goal: Build RAG-based systems from scratch

1. Intro to Embeddings & Vector stores
   - ChromaDB, PineCone
   - Cosine similarity, chunking, indexing
2. **Project4**: Resume Analyzer Bot
   - Upload resume, analyze it and suggest job matches
   - **RAG Pipeline using chroma + Langchain**
3. **Project5**: Youtube video Q&A Bot
   - use `yt-dlp` to extract transcripts
   - create embeddings, and answer questions based on video

## Phase 4 : Agent & Tools
Goal: Use LLms with tools and create autonomous workflows

1. Langchain Agents Explained
   - ReACT, MRKL, Tool Usage

2. **Project6**: Multi-tool Research Assistant
   - Toolset: SerpAPI, Calculator, Websearch, DocsReader

3.  **Project7**: AI Travel Planner
   - Input: Dates + preferences -> **Output:** Itinerary
   - Uses tools like Maps, Flights, Weather, Budget Planner
## Phase 5: LangGraph and Multi Agent System
Goal: Master LangGraph for dynamics multi-agent orchestration
1. LangGraph Intro
   - Graph-based reasoning
   - Building agent workflows
2. **Project8**: Autnomous Startup Ideation bot
   - One agent ideates, one critiques, one validates market fit
## Phase 6: API Deployment + Web App Integration
Goal: serve models via PAI and build full-stack app
1. Serving LLM Apps with FastAPI
   - API routing, auth, json I/o
2. **Project9**: AI Code Review API
   - INPUT: PR diff -> outputs: Comment suggestions
3. Frontend Integration(Option react/firebase)
   - Connecting FASTAPI backend with fronend
   - Deploy on Vercel/Render

## Phase 6: MCP (Model Context Protocol)
Goal: Personalize LLM behaviour per user, domain or app context

## Phase 7: Deployment and Production ready API
Goal: Take Apps to production
1. Caching, Rate Limiting and Logging
   - Redis, Pinecone persistance
   - Tracing with LangSmith/OpenTelemetry
2. **Project10**: Full stack AI Feedback APP
   - INPUT: student project uploads
   - Output: Instant AI Feedback, stored in database
   - Dashboard View with ranking/score

## Some Advance topics
    - Fine-tunning vs RAG
    - open-soruces LLMs: LLaMA, Mistral, Ollama
    - Local Vector DBs and embeddings models (e.g.., Instructor-XL)
    - Cost Optimization techniques (token counting, streaming)
    - use Hugging face transformers Directly