# CCAF 12-Day Sprint Plan
## Target: Pass exam by May 17th, 2026

**Your advantages:** DevOps + Python + Azure = You're starting at Week 2, not Week 0

---
# CCAF 12-Day Sprint Plan v3.0 — Exam-Focused Edition
## Target: Pass exam by May 17th, 2026 with 800+ score

> **Strategy:** Anthropic/Udemy/YouTube for foundation + claudecertifications.com for exam-critical prep
> **Coverage:** 95%+ of all exam topics
> **Pass Probability:** 80-85% with disciplined execution

---

## 🎯 RESOURCE STRATEGY (Two-Track Approach)

### **Track A: Foundation Building** (Days 1-8)
Use any of these for general understanding:
- 🎓 **Anthropic Academy** (Skilljar) — Free official courses
- 📺 **YouTube** — Andrew Brown, freeCodeCamp
- 💰 **Udemy** — Frank Kane, Vanderbilt courses

### **Track B: Exam-Critical Prep** ⭐ MUST USE
**https://claudecertifications.com/claude-certified-architect**

This is the **PRIMARY exam prep resource** because it:
- ✅ Maps directly to all 5 exam domains
- ✅ Includes anti-patterns (heavily tested)
- ✅ Provides 6 scenario walkthroughs
- ✅ Has 25 free practice questions
- ✅ Shows exact code patterns the exam tests

---

## 📊 EXAM STRUCTURE

| Domain | Weight | Direct Link |
|---|---|---|
| 1. Agentic Architecture & Orchestration | ~25% | [Domain 1](https://claudecertifications.com/claude-certified-architect/domains/agentic-architecture) |
| 2. Tool Design & MCP Integration | ~20% | [Domain 2](https://claudecertifications.com/claude-certified-architect/domains/tool-design-mcp) |
| 3. Claude Code Configuration | ~20% | [Domain 3](https://claudecertifications.com/claude-certified-architect/domains/claude-code-config) |
| 4. Prompt Engineering | ~20% | [Domain 4](https://claudecertifications.com/claude-certified-architect/domains/prompt-engineering) |
| 5. Context Management | ~15% | [Domain 5](https://claudecertifications.com/claude-certified-architect/domains/context-management) |

**Critical Resources:**
- 📋 [Exam Guide](https://claudecertifications.com/claude-certified-architect/exam-guide)
- 🎯 [6 Scenarios](https://claudecertifications.com/claude-certified-architect/scenarios)
- ❌ [Anti-Patterns Cheatsheet](https://claudecertifications.com/claude-certified-architect/anti-patterns)
- ✅ [Practice Questions](https://claudecertifications.com/claude-certified-architect/practice-questions)

---

## 🎯 PHASE 1: FOUNDATION (Days 1-4)
### Focus: Domain 4 (Prompt Engineering 20%)

---

### **DAY 1 — Wednesday, May 6** ⏰ 4-5 hours
**Goal:** Foundation setup + first API calls

**🎓 Track A — Foundation (Morning, 2 hours):**
- [ ] Sign up at https://anthropic.skilljar.com
- [ ] Complete "Claude 101" course (1 hour)
- [ ] Start "Building with Claude API" — modules 1-2

**🎯 Track B — Exam Prep (Afternoon, 1 hour):**
- [ ] **READ:** [Exam Guide Overview](https://claudecertifications.com/claude-certified-architect/exam-guide)
- [ ] Understand exam format, 5 domains, 6 scenarios, anti-patterns
- [ ] Bookmark all domain pages

**Hands-on (1-2 hours):**
- [ ] Sign up at https://console.anthropic.com (claim $5 credits)
- [ ] Install: `pip install anthropic`
- [ ] First API call (hello world)
- [ ] Test streaming response

**Evening (30 mins):**
- [ ] Read: https://docs.anthropic.com/en/api/getting-started

**✅ Success Check:** API call working + understand exam structure

---

### **DAY 2 — Thursday, May 7** ⏰ 4-5 hours
**Goal:** Master tool use + agentic loop fundamentals

**🎓 Track A — Foundation (Morning, 2 hours):**
- [ ] Continue "Building with Claude API" — tool use modules
- [ ] Watch any Andrew Brown YouTube clips on tool use (optional)

**🎯 Track B — Exam Prep (Afternoon, 2 hours):**
- [ ] **STUDY:** [Domain 1: Agentic Architecture](https://claudecertifications.com/claude-certified-architect/domains/agentic-architecture)
- [ ] Focus on subdomain **d1.1: Agentic Loops & Core API**
- [ ] **MEMORIZE:** `stop_reason` patterns (`tool_use` vs `end_turn`)
- [ ] Note the anti-patterns listed

**Hands-on (1 hour):**
- [ ] Build agentic loop script using `stop_reason` pattern
- [ ] Implement weather/calculator tool calling
- [ ] **CRITICAL:** Use the EXACT pattern from claudecertifications.com

**🔑 Pattern to Master:**
```python
while True:
    response = client.messages.create(...)
    if response.stop_reason == "end_turn":
        break  # Done
    if response.stop_reason == "tool_use":
        # Execute tool, append result, continue
```

**✅ Success Check:** Agentic loop working with `stop_reason`

---

### **DAY 3 — Friday, May 8** ⏰ 4-5 hours
**Goal:** Structured output + few-shot prompting

**🎓 Track A — Foundation (Morning, 2 hours):**
- [ ] Finish "Building with Claude API" course
- [ ] Watch Frank Kane Udemy modules (if you bought it)

**🎯 Track B — Exam Prep (Afternoon, 2 hours):**
- [ ] **STUDY:** [Domain 4: Prompt Engineering](https://claudecertifications.com/claude-certified-architect/domains/prompt-engineering)
- [ ] All subdomains (d4.1 to d4.4)
- [ ] **MEMORIZE:** 
  - Explicit criteria patterns
  - Few-shot rules (2-4 examples)
  - tool_use for structured output
  - Validation-retry loops

**Hands-on (1 hour):**
- [ ] Build a code review prompt with explicit measurable criteria
- [ ] Implement validation-retry loop pattern
- [ ] Practice JSON schema with nullable fields

**🔑 Critical Distinction:**
- ❌ "Be thorough, find issues"
- ✅ "Flag functions exceeding 50 lines"

**✅ Success Check:** Domain 4 fully understood

---

### **DAY 4 — Saturday, May 9** ⏰ 4-5 hours
**Goal:** Multi-pass review + Domain 4 mastery

**🎓 Track A — Foundation (Morning, 1 hour):**
- [ ] Quick review of API course concepts
- [ ] Read Anthropic docs on prompt engineering

**🎯 Track B — Exam Prep (Afternoon, 3 hours):**
- [ ] **DEEP DIVE:** [Domain 4 — Multi-Pass Review](https://claudecertifications.com/claude-certified-architect/domains/prompt-engineering)
- [ ] Subdomain d4.4: Validation-Retry Loops
- [ ] Study same-session bias problem
- [ ] **PRACTICE QUESTIONS:** Take any Domain 4 questions from [Practice Questions page](https://claudecertifications.com/claude-certified-architect/practice-questions)

**Hands-on (1 hour):**
- [ ] Build multi-pass review system:
  - Generator session (creates code)
  - Reviewer session (reviews independently — different context)
- [ ] Test field-level confidence pattern

**❌ Anti-Patterns to Memorize:**
- Same-session self-review (model retains bias)
- Vague "be careful" instructions
- Too many examples (>6)

**✅ Success Check:** Domain 4 (20% of exam) feels solid

---

## 🔥 PHASE 2: DEEP TECHNICAL (Days 5-8)
### Focus: Domains 2, 3, 1 (65% of exam)

---

### **DAY 5 — Sunday, May 10** ⏰ 6-8 hours (BIG DAY!)
**Goal:** Master Claude Code Configuration

**🎓 Track A — Foundation (Morning, 2 hours):**
- [ ] Anthropic Academy: "Claude Code in Action"
- [ ] OR: Andrew Brown freeCodeCamp video (specific sections only)

**🎯 Track B — Exam Prep (Afternoon, 3 hours):**
- [ ] **STUDY:** [Domain 3: Claude Code Configuration](https://claudecertifications.com/claude-certified-architect/domains/claude-code-config)
- [ ] All subdomains (d3.1 to d3.4)
- [ ] **MEMORIZE the hierarchy:**
  - User: `~/.claude/CLAUDE.md` (personal)
  - Project: `.claude/CLAUDE.md` (team-shared)
  - Directory: `src/api/CLAUDE.md` (scoped)
- [ ] Study `@import` syntax and `.claude/rules/` directory

**Hands-on (3 hours):**
- [ ] Install Claude Code: `irm https://claude.ai/install.ps1 | iex`
- [ ] Create test project with full hierarchy
- [ ] Practice CLAUDE.md inheritance
- [ ] Test custom slash commands in `.claude/commands/`
- [ ] Build a SKILL.md with frontmatter

**🔑 SKILL.md Frontmatter (Memorize):**
```yaml
context: fork              # Isolated context
allowed-tools: [Read, Edit, Grep]
argument-hint: "<filename>"
paths: ["src/**/*.ts"]
```

**❌ Anti-Pattern:** Personal prefs (vim) in PROJECT config

**✅ Success Check:** Can configure full Claude Code hierarchy

---

### **DAY 6 — Monday, May 11** ⏰ 6-8 hours (BIG DAY!)
**Goal:** CI/CD integration + plan mode mastery

**🎓 Track A — Foundation (Morning, 2 hours):**
- [ ] Anthropic Academy: Claude Code 101 (if not done)
- [ ] Watch GitHub Actions integration tutorials

**🎯 Track B — Exam Prep (Afternoon, 2 hours):**
- [ ] **STUDY:** [Domain 3 — CI/CD Integration](https://claudecertifications.com/claude-certified-architect/domains/claude-code-config)
- [ ] Subdomain d3.4: CI/CD & Batch Processing
- [ ] Master flag combinations:
  - `-p` or `--print`: non-interactive
  - `--output-format json`: structured output
  - `--json-schema`: validated output
- [ ] Study Plan Mode triggers

**Hands-on (4 hours):**
- [ ] Build CI/CD integration:
  ```yaml
  - run: claude -p "review PR" --output-format json
  ```
- [ ] Test `.mcp.json` (project-level)
- [ ] Test `~/.claude.json` (user-level)
- [ ] Practice Batch API (Message Batches)
- [ ] Build Azure DevOps automation example

**🎯 Plan Mode Decision:**
- ✅ USE: 45+ files, library migration, microservice restructure
- ❌ SKIP: Single-file bug fix, clear stack trace, simple validation

**🎯 Scenario Coverage:**
- Scenario 2: Code Generation
- Scenario 5: Claude Code for CI/CD

**✅ Success Check:** Working CI/CD + understand Plan Mode

---

### **DAY 7 — Tuesday, May 12** ⏰ 5-6 hours
**Goal:** MCP + Tool Design (Domain 2 - 20%)

**🎓 Track A — Foundation (Morning, 3 hours):**
- [ ] Anthropic Academy: "Introduction to MCP"
- [ ] Anthropic Academy: "MCP Advanced Topics"
- [ ] Read MCP Python SDK docs

**🎯 Track B — Exam Prep (Afternoon, 2-3 hours):**
- [ ] **STUDY:** [Domain 2: Tool Design & MCP](https://claudecertifications.com/claude-certified-architect/domains/tool-design-mcp)
- [ ] All subdomains (d2.1 to d2.5)
- [ ] **MEMORIZE:**
  - Tool description quality patterns
  - Structured error fields
  - Transport layers (stdio vs SSE)

**🔑 Tool Description Quality:**
```json
{
  "description": "Search by email, phone (E.164), or account ID (ACC-XXXXX). Returns customer object or empty array. Empty result is NOT an error.",
  "input_schema": {...detailed types...}
}
```

**🔑 Structured Error Response:**
```json
{
  "isError": true,
  "errorCategory": "auth | not_found | rate_limit | timeout | validation",
  "isRetryable": true,
  "context": { "what_was_attempted": "...", "what_failed": "..." }
}
```

**🔑 CRITICAL DISTINCTION:**
- **Access Failure:** "Couldn't check DB" → `isError: true`
- **Empty Result:** "Checked DB, no matches" → `isError: false`

**🔑 Transport Selection:**
- **stdio:** Local subprocess only (same machine)
- **SSE:** Remote, cloud, streaming (HTTP across networks)
- **WebSocket:** Bidirectional (rarely needed)

**✅ Success Check:** Domain 2 fully understood

---

### **DAY 8 — Wednesday, May 13** ⏰ 5-6 hours
**Goal:** Build MCP server + Master Agentic (Domain 1 - 25%)

**Hands-on Morning (3 hours):**
- [ ] Build MCP server in Python (kubectl/Azure CLI wrapper)
- [ ] Apply tool description best practices
- [ ] Implement structured error responses
- [ ] Test with Claude Code

**🎯 Track B — Exam Prep (Afternoon, 3 hours):**
- [ ] **DEEP STUDY:** [Domain 1: Agentic Architecture](https://claudecertifications.com/claude-certified-architect/domains/agentic-architecture)
- [ ] ALL subdomains (d1.1 to d1.4)
- [ ] **CRITICAL TOPICS:**
  - Agentic loops (reviewed)
  - Multi-Agent Orchestration (Hub-and-Spoke)
  - Hooks & Programmatic Enforcement
  - Session Management

**🔑 Hub-and-Spoke Pattern:**
```python
coordinator = Agent(
    tools=[Task, summarize_results, format_report]
    # Task tool REQUIRED for spawning subagents
)

market_researcher = Agent(
    tools=[web_search, read_doc, extract_data]
    # 4-5 tools per agent (NOT 18+)
)
```

**🔑 Hooks vs Prompts (HIGHLY TESTED):**
- **Hooks** = Deterministic (100% reliable)
- **Prompts** = Probabilistic (model may ignore)

**Example: $500 Refund Limit**
- ❌ WRONG: System prompt rule
- ✅ RIGHT: PostToolUse hook blocks programmatically

**Hands-on Evening (1 hour):**
- [ ] Build 2-agent system (coordinator + subagent)
- [ ] Test context isolation
- [ ] Pass ONLY relevant context (not full coordinator history)

**🎯 Scenario Coverage:**
- Scenario 1: Customer Support Agent
- Scenario 3: Multi-Agent Research

**✅ Success Check:** MCP server works + understand hooks vs prompts

---

## 🎯 PHASE 3: FINAL PUSH (Days 9-12)
### Focus: Domain 5 + Anti-patterns + Practice

---

### **DAY 9 — Thursday, May 14** ⏰ 4-5 hours
**Goal:** Context Management + Reliability (Domain 5)

**🎓 Track A — Foundation (Morning, 1 hour):**
- [ ] Read Anthropic docs on prompt caching
- [ ] Review token budgeting concepts

**🎯 Track B — Exam Prep (Afternoon, 3 hours):**
- [ ] **STUDY:** [Domain 5: Context Management](https://claudecertifications.com/claude-certified-architect/domains/context-management)
- [ ] All subdomains (d5.1 to d5.4)
- [ ] **MEMORIZE:**
  - Progressive Summarization risks
  - "Lost in the Middle" effect
  - Case Facts Blocks pattern
  - Valid vs Invalid escalation

**🔑 Case Facts Block:**
```markdown
## CASE FACTS (Do not summarize — reference directly)
| Field | Value |
|-------|-------|
| Customer | John Smith |
| Account ID | ACC-12345 |
| Order | #98765 |
| Overcharge | $50.01 |
```

**🔑 Escalation Triggers:**

| ✅ VALID | ❌ INVALID |
|---|---|
| Customer requests human | Negative sentiment |
| Policy gap detected | Self-reported confidence |
| Capability exceeded | Aggregate metrics only |
| Threshold exceeded ($500+) | |

**Hands-on (1 hour):**
- [ ] Build escalation logic with structured criteria
- [ ] Implement case facts pattern in code
- [ ] Test long conversation context preservation

**✅ Success Check:** Domain 5 (15%) covered

---

### **DAY 10 — Friday, May 15** ⏰ 5-6 hours
**Goal:** Practice exam + Anti-patterns mastery ⭐ CRITICAL DAY

**🎯 Track B — Exam Prep (Morning, 3 hours):**
- [ ] **TAKE: Anthropic Official Practice Exam** (60 questions, 120 mins)
- [ ] Time yourself strictly
- [ ] Don't skip — pick best guess

**Afternoon (2 hours):**
- [ ] **CRITICAL:** Study [Anti-Patterns Cheatsheet](https://claudecertifications.com/claude-certified-architect/anti-patterns)
- [ ] **MEMORIZE all 18 anti-patterns** with severity ratings
- [ ] Take the [Free 25 Practice Questions](https://claudecertifications.com/claude-certified-architect/practice-questions)
- [ ] Read explanations for each

**🔑 The 10 Most Critical Anti-Patterns:**

| ❌ WRONG | ✅ RIGHT |
|---|---|
| Parsing text for loop termination | Check `stop_reason` |
| Iteration caps as primary stop | Let loop terminate naturally |
| Prompt-based business rules | Programmatic hooks |
| Self-reported confidence | Structured criteria |
| Sentiment-based escalation | Task complexity + policy gaps |
| Generic "Operation failed" | Structured: isError, errorCategory |
| Suppressing errors silently | Distinguish access vs empty |
| 18+ tools per agent | 4-5 tools per agent |
| Same-session self-review | Separate sessions |
| Aggregate accuracy only | Per-document-type metrics |

**Evening (1 hour):**
- [ ] Identify weakest domain
- [ ] Re-read that domain's claudecertifications.com page

**✅ Success Check:** 70%+ on practice exam + memorized anti-patterns

---

### **DAY 11 — Saturday, May 16** ⏰ 4-5 hours
**Goal:** Scenario walkthroughs + final review

**🎯 Track B — Exam Prep (Morning, 3 hours):**
- [ ] **CRITICAL:** Study [All 6 Scenarios](https://claudecertifications.com/claude-certified-architect/scenarios)
- [ ] Walk through each scenario's key skills

**🎯 The 6 Scenarios (Memorize Each):**

**1. Customer Support Resolution Agent**
- Skills: Agent SDK, MCP tools, escalation, structured errors
- Key: Hook-based compliance, NOT prompt-based

**2. Code Generation with Claude Code**
- Skills: CLAUDE.md hierarchy, plan mode, slash commands
- Key: TDD iteration pattern

**3. Multi-Agent Research System**
- Skills: Hub-and-spoke, context isolation, error propagation
- Key: Explicit context per subagent (NOT full history)

**4. Developer Productivity with Claude**
- Skills: Built-in tools (Read, Write, Bash, Grep, Glob), MCP
- Key: Tool distribution across agents (4-5 each)

**5. Claude Code for CI/CD**
- Skills: `-p` flag, `--output-format json`, Batch API
- Key: Session isolation between generator and reviewer

**6. Structured Data Extraction**
- Skills: JSON schemas, tool_use, validation-retry, few-shot
- Key: Field-level confidence + human review for low confidence

**Afternoon (2 hours):**
- [ ] Take Practice Exam #2 if available
- [ ] Quiz yourself: For each anti-pattern, name the correct alternative
- [ ] Review weak areas one more time

**Evening:**
- [ ] LIGHT review only — NO new content
- [ ] Sleep 8+ hours tonight!

**✅ Success Check:** Can recite all 10 anti-patterns + 6 scenarios

---

### **DAY 12 — Sunday, May 17** 🎯 EXAM DAY!
**Goal:** PASS WITH 800+ SCORE!

**Morning (1 hour max):**
- [ ] Light review only — DON'T cram!
- [ ] Quick anti-patterns flash review
- [ ] Quick scenarios checklist

**Pre-exam (2 hours before):**
- [ ] Eat balanced meal
- [ ] Stay hydrated
- [ ] Take short walk

**30 mins before:**
- [ ] Test camera/mic for ProctorFree
- [ ] Bathroom break
- [ ] Clear desk
- [ ] Close all apps

**EXAM TIME (120 mins):**
- [ ] Read EACH question twice
- [ ] Identify which scenario it belongs to
- [ ] **ALWAYS** look for anti-pattern distractors
- [ ] Flag uncertain questions
- [ ] Use ALL 120 minutes

**🎯 Exam Strategy:**
1. Pass 1: Easy questions (45 mins)
2. Pass 2: Medium questions (45 mins)
3. Pass 3: Hard + flagged review (30 mins)

**Results in 2 business days! 🏆**

---

## 🔑 EXAM-CRITICAL CHEAT SHEET

### **Domain 1 (25%)**
- Loop: Check `stop_reason`
- Multi-agent: Hub-and-spoke + context isolation
- Hooks: Deterministic > Prompts
- Tools: 4-5 per agent (NOT 18+)

### **Domain 2 (20%)**
- Tool descriptions: Detailed + examples + edge cases
- Errors: `isError`, `errorCategory`, `isRetryable`
- Access failure ≠ Empty result
- Transport: stdio (local) vs SSE (cloud)

### **Domain 3 (20%)**
- Hierarchy: User > Project > Directory
- Commands (same context) vs Skills (forked)
- CI/CD: `-p` + `--output-format json`
- Plan mode: 45+ files only

### **Domain 4 (20%)**
- Explicit measurable criteria
- Few-shot: 2-4 examples
- tool_use for structured output
- Multi-pass review (separate sessions)

### **Domain 5 (15%)**
- Case facts blocks (immutable)
- NO progressive summarization of critical data
- Escalate: policy gaps, NOT sentiment
- Lost-in-middle: critical info at start/end

---

## 📚 DAILY RESOURCE QUICK ACCESS

**Bookmark these 8 URLs:**

```
PRIMARY EXAM PREP (claudecertifications.com):
1. Exam Guide: /claude-certified-architect/exam-guide
2. Domain 1: /claude-certified-architect/domains/agentic-architecture
3. Domain 2: /claude-certified-architect/domains/tool-design-mcp
4. Domain 3: /claude-certified-architect/domains/claude-code-config
5. Domain 4: /claude-certified-architect/domains/prompt-engineering
6. Domain 5: /claude-certified-architect/domains/context-management
7. Anti-Patterns: /claude-certified-architect/anti-patterns
8. Practice Questions: /claude-certified-architect/practice-questions

FOUNDATION LEARNING:
- https://anthropic.skilljar.com (free official courses)
- https://docs.anthropic.com (reference docs)

OPTIONAL:
- YouTube: Andrew Brown / freeCodeCamp
- Udemy: Frank Kane Claude Code course
```

---

## ⚠️ IMPORTANT DISCLAIMER

**claudecertifications.com is a third-party study site** — not officially endorsed by Anthropic. While excellent for exam-specific patterns, the official source is **Anthropic's documentation and courses**.

**Strategy:** Use claudecertifications.com to know **WHAT to study** for the exam, then verify with Anthropic docs for **accurate technical details**.

---

## 📊 SUCCESS METRICS

**Daily checkpoints:**
- Day 1-4: ✅ Domain 4 covered (Prompt Engineering)
- Day 5-6: ✅ Domain 3 covered (Claude Code)
- Day 7-8: ✅ Domains 1+2 covered (Agentic + MCP)
- Day 9: ✅ Domain 5 covered (Context)
- Day 10: ✅ 70%+ on practice exam
- Day 11: ✅ All anti-patterns + scenarios memorized
- Day 12: ✅ PASS WITH 800+! 🏆

**Total study time:** ~60-65 hours over 12 days
**Pass probability:** 80-85%

---

## 🥋 FINAL WISDOM

This v3 plan integrates:
- ✅ **Foundation learning** from Anthropic/YouTube/Udemy (general knowledge)
- ✅ **Exam-critical prep** from claudecertifications.com (specific to test)
- ✅ **Hands-on projects** for retention
- ✅ **Anti-patterns mastery** (the trap questions)
- ✅ **All 6 scenarios** walkthrough

The two-track approach ensures you:
1. **Understand WHY** things work (Anthropic courses)
2. **Know WHAT the exam tests** (claudecertifications.com)
3. **Can BUILD it** (hands-on projects)

That's the trifecta for passing.

---

**Now stop planning and START EXECUTING!**

GO GET IT! 🥋🔥🐼

---

**Version:** 3.0 — Exam-Focused Edition
**Updated:** May 2026
**Coverage:** 95%+ of CCAF exam topics
**Strategy:** Foundation (any source) + Exam Prep (claudecertifications.com)