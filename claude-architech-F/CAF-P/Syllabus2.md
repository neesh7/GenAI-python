# Claude Certified Architect - Video Series Supplement
## "Peace of Code" YouTube Full Course (Ep 01-15)

---

## 📺 Complete Video Series (All 15 Episodes)

| Episode | Topic | Duration | Domain |
|---------|-------|----------|--------|
| **Ep 01** | Agentic Loops & stop_reason Explained | 49:27 | Domain 1 |
| **Ep 02** | Multi-Agent Systems & Coordinator Patterns Explained | 32:36 | Domain 1 |
| **Ep 03** | Subagent Context Passing & Session Management | 33:36 | Domain 1, 5 |
| **Ep 04** | Multi-Agent System in Python & Claude SDK (Hands On) | 12:48 | Domain 1 |
| **Ep 05** | PreToolUse, PostToolUse Hooks & Task Decomposition | 45:23 | Domain 1 |
| **Ep 06** | Tool Descriptions & Tool Misrouting Explained | 24:50 | Domain 2 |
| **Ep 07** | Agent Error Handling & tool_choice Explained | 38:06 | Domain 1, 2 |
| **Ep 08** | MCP Servers, Config, Cline & More | 1:29:09 | Domain 2 |
| **Ep 09** | Claude Built-in Tools Explained | 35:39 | Domain 3 |
| **Ep 10** | CLAUDE.md Hierarchy & Config Rules | 31:37 | Domain 3 |
| **Ep 11** | Custom Slash Commands & Skills | 39:17 | Domain 3 |
| **Ep 12** | Plan Mode vs Execute (Claude Code) | 51:42 | Domain 3 |
| **Ep 13** | Claude Code CI/CD Pipelines | 31:22 | Domain 3 |
| **Ep 14** | Prompt Engineering — Explicit Criteria & False Positives | 34:25 | Domain 4 |
| **Ep 15** | Few-Shot Prompting Explained | 27:42 | Domain 4 |

---

## 📊 Total Series Duration

| Segment | Episodes | Total Duration |
|---------|----------|-----------------|
| **Part 1: Agentic & MCP** | 01-07 | ~4h 56m |
| **Part 2: Claude Code & Prompts** | 08-15 | ~6h 1m |
| **COMPLETE SERIES** | **01-15** | **~11 hours** |

**Channel:** Peace Of Code  
**Certification:** Claude Certified Architect

---

## 🎯 Domain Coverage Analysis

### Domain 1: Agentic Architecture & Orchestration (25%)

| Sub-Domain | Syllabus Topic | Video Coverage | Status |
|------------|---|---|---|
| **d1.1** | Agentic Loops & Core API | Ep 01, 05, 07 | ✅ **COVERED** |
| **d1.2** | Multi-Agent Orchestration (Hub-and-Spoke) | Ep 02, 04 | ✅ **COVERED** |
| **d1.3** | Hooks & Programmatic Enforcement | Ep 05 | ✅ **COVERED** |
| **d1.4** | Session Management & Context Isolation | Ep 03, 04 | ⚠️ **PARTIAL** |

**Coverage:** ~85% ✅  
**What's Missing:**
- Deep dive on session isolation patterns
- Multi-agent error propagation strategies

---

### Domain 2: Tool Design & MCP Integration (20%)

| Sub-Domain | Syllabus Topic | Video Coverage | Status |
|------------|---|---|---|
| **d2.1** | Tool Description Quality | Ep 06 | ⚠️ **PARTIAL** |
| **d2.2** | Structured Error Responses | Ep 07 | ⚠️ **PARTIAL** |
| **d2.3** | MCP Architecture & Concepts | Ep 08 | ⚠️ **PARTIAL** |
| **d2.4** | MCP Server Implementation | Ep 08 | ⚠️ **PARTIAL** |
| **d2.5** | Transport Layers (stdio vs SSE) | ❌ **NOT COVERED** | ❌ **MISSING** |

**Coverage:** ~60% ⚠️  
**What's Missing:**
- Detailed structured error field patterns (`isError`, `errorCategory`, `isRetryable`)
- Transport layer deep dive (stdio vs SSE vs WebSocket)
- Error categorization (auth, not_found, rate_limit, timeout, validation)
- Empty result vs access failure distinction
- MCP resource and prompt implementations

---

### Domain 3: Claude Code Configuration (20%)

| Sub-Domain | Syllabus Topic | Video Coverage | Status |
|------------|---|---|---|
| **d3.1** | CLAUDE.md Hierarchy (User → Project → Directory) | Ep 10 | ✅ **COVERED** |
| **d3.2** | Commands vs Skills (Context Forking) | Ep 11 | ✅ **COVERED** |
| **d3.3** | Plan Mode Triggers & Usage | Ep 12 | ✅ **COVERED** |
| **d3.4** | CI/CD Integration & Batch Processing | Ep 13 | ✅ **COVERED** |

**Coverage:** ~90% ✅  
**What's Missing:**
- Advanced CLI flags (`-p`, `--output-format json`, `--json-schema`)
- Batch API integration details
- Plan mode decision matrix (45+ files rule)

---

### Domain 4: Prompt Engineering (20%)

| Sub-Domain | Syllabus Topic | Video Coverage | Status |
|------------|---|---|---|
| **d4.1** | Explicit Measurable Criteria | Ep 14 | ✅ **COVERED** |
| **d4.2** | Few-Shot Prompting (2-4 examples) | Ep 15 | ✅ **COVERED** |
| **d4.3** | Structured Output via tool_use | ❌ **NOT COVERED** | ❌ **MISSING** |
| **d4.4** | Validation-Retry Loops & Multi-Pass Review | ❌ **NOT COVERED** | ❌ **MISSING** |

**Coverage:** ~50% ⚠️  
**What's Missing:**
- JSON schema validation patterns
- Validation-retry loop implementation
- Multi-pass review (separate sessions to avoid same-session bias)
- Field-level confidence patterns
- False positive reduction strategies

---

### Domain 5: Context Management (15%)

| Sub-Domain | Syllabus Topic | Video Coverage | Status |
|------------|---|---|---|
| **d5.1** | Case Facts Blocks Pattern | ❌ **NOT COVERED** | ❌ **MISSING** |
| **d5.2** | Progressive Summarization Risks | ❌ **NOT COVERED** | ❌ **MISSING** |
| **d5.3** | Lost-in-the-Middle Effect | ❌ **NOT COVERED** | ❌ **MISSING** |
| **d5.4** | Escalation Triggers & Reliability | ❌ **NOT COVERED** | ❌ **MISSING** |

**Coverage:** 0% ❌  
**What's Missing (CRITICAL):**
- Case facts block implementation
- Prompt caching for context preservation
- Token budgeting strategies
- "Lost in the middle" position effects
- Valid vs invalid escalation criteria
- Progressive summarization problems
- Context window management
- Human escalation logic

---

## 📋 Overall Coverage Summary

| Domain | Weight | Video Coverage | Status | Gap |
|--------|--------|---|---|---|
| Domain 1: Agentic | 25% | ~85% | ✅ Strong | Minor gaps |
| Domain 2: Tool Design & MCP | 20% | ~60% | ⚠️ Partial | Significant gaps |
| Domain 3: Claude Code | 20% | ~90% | ✅ Strong | Minor gaps |
| Domain 4: Prompt Engineering | 20% | ~50% | ⚠️ Weak | Major gaps |
| Domain 5: Context Mgmt | 15% | **0%** | ❌ **MISSING** | **CRITICAL** |
| **TOTAL** | **100%** | **~65%** | ⚠️ **INCOMPLETE** | **~35% GAP** |

---

## ⚠️ Critical Gaps (MUST Study Separately)

### 🔴 Domain 5: Context Management (15% of exam) - COMPLETELY MISSING
- [ ] Case facts blocks pattern
- [ ] Progressive summarization risks
- [ ] Lost-in-the-middle effect
- [ ] Escalation triggers (policy gaps, NOT sentiment)
- [ ] Prompt caching (1024 token minimum, 4 breakpoints max)
- [ ] Token budgeting
- [ ] Valid escalation criteria vs invalid

### 🟠 Domain 4: Prompt Engineering - MAJOR GAPS
- [ ] JSON schema validation patterns
- [ ] Validation-retry loops (implementation)
- [ ] Multi-pass review (separate sessions)
- [ ] Same-session bias problem
- [ ] Field-level confidence scoring
- [ ] False positive reduction

### 🟡 Domain 2: Tool Design & MCP - SIGNIFICANT GAPS
- [ ] Structured error response fields
- [ ] Transport layers (stdio vs SSE detailed comparison)
- [ ] Error categorization patterns
- [ ] Empty result vs access failure (CRITICAL distinction)
- [ ] MCP resources and prompts implementation

---

## 📌 Anti-Patterns Coverage

**Videos Touch On:** 
- ✅ stop_reason vs text parsing
- ✅ Hooks vs prompts for enforcement
- ✅ Tool descriptions quality

**Videos MISS:**
- ❌ Same-session self-review
- ❌ Prompt-based business rules
- ❌ Sentiment-based escalation
- ❌ Generic error messages
- ❌ 18+ tools per agent (partially)
- ❌ Progressive summarization pitfalls
- ❌ All 18 anti-patterns NOT explicitly covered

---

## 🎯 Scenarios Coverage

| Scenario | Topic | Domains | Video Coverage | Status |
|----------|-------|---------|---|---|
| **Scenario 1** | Customer Support Resolution Agent | Domain 1, 2, 5 | Ep 01-07 | ⚠️ Partial |
| **Scenario 2** | Code Generation with Claude Code | Domain 3, 4 | Ep 09-13 | ✅ Good |
| **Scenario 3** | Multi-Agent Research System | Domain 1, 2 | Ep 02-04 | ✅ Good |
| **Scenario 4** | Developer Productivity | Domain 3, 4 | Ep 09-13 | ✅ Good |
| **Scenario 5** | Claude Code for CI/CD | Domain 3 | Ep 13 | ✅ Covered |
| **Scenario 6** | Structured Data Extraction | Domain 2, 4, 5 | ❌ Not Covered | ❌ Missing |

---

## 📚 What You MUST Supplement With

### 1. **claudecertifications.com (PRIORITY)**
- [ ] [Domain 5: Context Management](https://claudecertifications.com/claude-certified-architect/domains/context-management) — **15% of exam, 0% video coverage**
- [ ] [Anti-Patterns Cheatsheet](https://claudecertifications.com/claude-certified-architect/anti-patterns) — 18 patterns to memorize
- [ ] [Domain 4: Prompt Engineering](https://claudecertifications.com/claude-certified-architect/domains/prompt-engineering) — Validation-retry loops
- [ ] [Domain 2: Tool Design](https://claudecertifications.com/claude-certified-architect/domains/tool-design-mcp) — Structured errors
- [ ] [6 Scenario Walkthroughs](https://claudecertifications.com/claude-certified-architect/scenarios)
- [ ] [25 Free Practice Questions](https://claudecertifications.com/claude-certified-architect/practice-questions)

### 2. **Anthropic Official Docs**
- [ ] Prompt caching documentation
- [ ] Context window management
- [ ] Token budgeting
- [ ] MCP detailed specifications

### 3. **Practice & Testing**
- [ ] Official practice exam (60 questions, 120 mins)
- [ ] Free 25 practice questions on claudecertifications.com
- [ ] Timed practice tests

---

---

# ⚡ 4-Day Accelerated Video Completion Plan

## Overview
**Complete all 15 episodes in 4 days** (~10 hours with optimizations)

**Daily breakdown:** ~2.5-3 hours per day  
**Speed hacks:** Selective 1.25x playback on non-critical episodes  
**Total time:** ~10 hours (vs 11 hours normal pace)

---

## Day-by-Day Schedule

### Day 1: Agentic Foundations (Domain 1 - Part 1)
**⏱️ Total: 2h 8m watching + 15m breaks = 2h 23m**

| Episode | Duration | Domain | Speed | Key Focus |
|---------|----------|--------|-------|-----------|
| Ep 01 | 49:27 | Domain 1 | 1.0x | Agentic loops, stop_reason |
| Ep 02 | 32:36 | Domain 1 | 1.0x | Multi-agent patterns |
| Ep 03 | 33:36 | Domain 1, 5 | 1.0x | Context passing |
| Ep 04 | 12:48 | Domain 1 | 1.0x | Hands-on (quick) |

**Activities:**
- [ ] Watch continuously with 15-min break after Ep 02
- [ ] Take notes on `stop_reason` patterns
- [ ] Review loop termination logic
- [ ] 10-min recap of key concepts

**Why this group:** Foundation concepts must stick before advanced patterns

---

### Day 2: Agentic Advanced + Tool Design (Domain 1 Part 2 + Domain 2 Part 1)
**⏱️ Total: 1h 48m watching + 10m breaks = 1h 58m**

| Episode | Duration | Domain | Speed | Key Focus |
|---------|----------|--------|-------|-----------|
| Ep 05 | 45:23 | Domain 1 | 1.0x | Hooks (CRITICAL!) |
| Ep 06 | 24:50 | Domain 2 | 1.0x | Tool descriptions |
| Ep 07 | 38:06 | Domain 1, 2 | 1.0x | Error handling |

**Activities:**
- [ ] Watch Ep 05-07 continuously
- [ ] 10-min break after Ep 05
- [ ] **MEMO:** Hooks > Prompts for enforcement
- [ ] Note tool description quality markers
- [ ] Screenshot error handling patterns
- [ ] Code exercise: Write a tool schema locally

**Why this group:** Transitions from agentic to tool-focused content

---

### Day 3: MCP Deep Dive + Claude Code Intro (Domain 2 Part 2 + Domain 3 Part 1)
**⏱️ Total: 2h 18m watching + 30m breaks = 2h 48m**

| Episode | Duration | Domain | Speed | Key Focus |
|---------|----------|--------|-------|-----------|
| Ep 08 | 1:29:09 | Domain 2 | **1.25x** | MCP servers ⭐ |
| Ep 09 | 35:39 | Domain 3 | 1.0x | Built-in tools |
| Ep 10 | 31:37 | Domain 3 | 1.0x | CLAUDE.md hierarchy |

**Time Savings:** Ep 08 @ 1.25x = saves ~18 mins (drops from 89m to 71m)

**Activities:**
- [ ] Watch Ep 08 at 1.25x speed (~71m)
- [ ] 20-min break (EARNED! Ep 08 is long)
- [ ] Watch Ep 09-10 normally (~67m)
- [ ] 10-min stretch/walk
- [ ] **MEMO:** MCP architecture patterns
- [ ] Note CLAUDE.md hierarchy: User → Project → Directory
- [ ] Create CLAUDE.md file locally

**Why this group:** Ep 08 is long, pair with shorter content. Logical progression MCP→Claude Code

**💡 Speed rationale:** Ep 08 is technical but slow-paced, 1.25x still comprehensible

---

### Day 4: Claude Code + Prompt Engineering (Domain 3 Part 2 + Domain 4)
**⏱️ Total: 2h 39m watching + 25m breaks = 3h 4m (Heaviest day)**

| Episode | Duration | Domain | Speed | Key Focus |
|---------|----------|--------|-------|-----------|
| Ep 11 | 39:17 | Domain 3 | **1.25x** | Slash commands |
| Ep 12 | 51:42 | Domain 3 | 1.0x | Plan mode (critical!) |
| Ep 13 | 31:22 | Domain 3 | **1.25x** | CI/CD pipelines |
| Ep 14 | 34:25 | Domain 4 | 1.0x | Prompt engineering |
| Ep 15 | 27:42 | Domain 4 | **1.25x** | Few-shot prompting |

**Time Savings:** 3 episodes @ 1.25x = saves ~25 minutes total

**Activities:**
- [ ] Watch Ep 11 @ 1.25x (~31m)
- [ ] Watch Ep 12 @ 1.0x (~52m) — Important, full speed
- [ ] 15-min break
- [ ] Watch Ep 13 @ 1.25x (~25m)
- [ ] Watch Ep 14 @ 1.0x (~34m) — Dense content, full speed
- [ ] 10-min break
- [ ] Watch Ep 15 @ 1.25x (~22m)
- [ ] **MEMO:** Plan mode decision criteria
- [ ] Note explicit criteria patterns
- [ ] Code exercise: Write multi-pass review prompt

**Why this group:** Ep 12 is substantial but critical, pairs well with 13-15

---

## Optimized 4-Day Schedule (Summary Table)

| Day | Episodes | Duration (Normal) | Duration (Optimized) | Breaks | Total Time |
|-----|----------|---|---|---|---|
| **Day 1** | Ep 01-04 | 2h 8m | 2h 8m | 15m | **2h 23m** |
| **Day 2** | Ep 05-07 | 1h 48m | 1h 48m | 10m | **1h 58m** |
| **Day 3** | Ep 08-10 | 2h 36m | 2h 18m (Ep 08 @ 1.25x) | 30m | **2h 48m** |
| **Day 4** | Ep 11-15 | 3h 4m | 2h 39m (3 eps @ 1.25x) | 25m | **3h 4m** |
| **TOTAL** | **15 eps** | **11h 0m** | **~10h 0m** | **1h 20m** | **~10h 20m** |

✅ **Saves 1 hour vs normal pace**  
✅ **All content covered completely**  
✅ **Maintains comprehension with strategic 1.25x**

---

## Daily Checklist & Activities

### Day 1 Checklist — **Domain 1: Agentic Architecture**
- [ ] Watch Ep 01-04 (2h 8m + 15m break)
- [ ] Take notes on `stop_reason` pattern
- [ ] Understand hub-and-spoke model
- [ ] 10-min recap: Explain agentic loop to yourself

### Day 2 Checklist — **Domain 1 → Domain 2: Tool Design**
- [ ] Watch Ep 05-07 (1h 48m + 10m break)
- [ ] **Memo key point:** Hooks > Prompts for business rules
- [ ] Note tool description quality markers
- [ ] Hands-on: Write a tool schema locally
- [ ] Screenshot error handling patterns

### Day 3 Checklist — **Domain 2 → Domain 3: Claude Code**
- [ ] Watch Ep 08 @ 1.25x + Ep 09-10 normal (2h 18m + 30m break)
- [ ] Take 20-min break after Ep 08 (you earned it!)
- [ ] Sketch MCP architecture on paper
- [ ] Hands-on: Create CLAUDE.md hierarchy locally
- [ ] Note: CLAUDE.md inheritance rules

### Day 4 Checklist — **Domain 3 → Domain 4: Prompt Engineering**
- [ ] Watch Ep 11-15 with selective 1.25x (2h 39m + 25m breaks)
- [ ] Understand Plan Mode decision criteria
- [ ] Note: When to use Plan Mode (45+ files rule)
- [ ] Hands-on: Write few-shot example prompt
- [ ] **DONE!** 🎉 Review key concepts from all 4 days

---

## Pro Tips for 4-Day Success

### ✅ DO THIS:

| Strategy | Why It Works | Time Saved |
|----------|---|---|
| **1.25x on non-critical episodes** | Technical but slow-paced content | ~25 mins |
| **Smart note-taking** | Only write decisions, patterns, exceptions | Retention + speed |
| **Take breaks strategically** | After long episodes + every 45-50 mins | Mental clarity |
| **Pair watching with coding** | Hands-on reinforces concepts | Deep learning |
| **Day-end 10-min recap** | Recite concepts from memory | Retention |

### ❌ DON'T DO THIS:

| Mistake | Why It Fails |
|---------|---|
| **Watch at 2x speed** | Lose comprehension on technical content |
| **Skip breaks** | Burnout hits on Day 4, retention crashes |
| **Multitask** | These are dense technical videos |
| **Binge all 11 hours Day 1** | Impossible to retain, brain overload |
| **Skip hands-on coding** | Passive watching != learning |

---

## Post-4-Day Plan (What's Next)

After completing all 15 videos in 4 days:

### Remaining 5-Hour Supplement (Days 5-7)
| Task | Domain | Duration | Priority | Notes |
|------|--------|----------|----------|-------|
| Study Domain 5 (claudecertifications.com) | Domain 5 | 2-3h | 🔴 CRITICAL | 15% of exam, 0% video coverage |
| Memorize 18 Anti-Patterns | All Domains | 1-2h | 🔴 CRITICAL | Exam has trick questions |
| Free 25 Practice Questions | All Domains | 1-2h | 🟡 IMPORTANT | Understand format |
| Official Practice Exam | All Domains | 2h | 🟡 IMPORTANT | Full simulation |

### Total Certification Prep Path
```
✅ Days 1-4: Watch all 15 videos (10h)
✅ Days 5-7: Supplement study (5h)
✅ Day 8: Practice exam + review (3h)
━━━━━━━━━━━━━━━━━
📊 Total: 8 days, 18 hours
🎯 Target: 80-85% pass probability
```

---

## Readiness Checkpoint

After 4 days of videos, you should be able to:

| Skill | Domain | Can Demonstrate? |
|-------|--------|---|
| Write agentic loop with proper stop_reason handling | Domain 1 | ✅ |
| Explain hub-and-spoke multi-agent pattern | Domain 1 | ✅ |
| Distinguish hooks from prompts for enforcement | Domain 1 | ✅ |
| Write quality tool description | Domain 2 | ✅ |
| Explain MCP architecture basics | Domain 2 | ⚠️ Partial |
| Create CLAUDE.md hierarchy | Domain 3 | ✅ |
| Decide when to use Plan Mode | Domain 3 | ✅ |
| Write explicit criteria prompt | Domain 4 | ✅ |
| Provide few-shot examples | Domain 4 | ✅ |
| Explain case facts blocks (after supplement) | Domain 5 | ❌ Not yet |

---

## 🎓 Recommended Study Path
1. **Ep 01-07** — Agentic Architecture & MCP Basics (5 hours)
2. **Ep 08** — MCP Servers Deep Dive (1.5 hours)
3. **Ep 09-13** — Claude Code (3 hours)
4. **Ep 14-15** — Prompt Engineering Intro (1.5 hours)

### Phase 2: Supplement Missing Content (15-20 hours)
1. **Domain 5 (Critical)** — Study claudecertifications.com (5 hours)
2. **Anti-Patterns** — Memorize all 18 (3 hours)
3. **Domain 4 Deep Dive** — Validation-retry loops (3 hours)
4. **Domain 2 Deep Dive** — Structured errors (3 hours)
5. **6 Scenarios** — Study walkthroughs (2 hours)

### Phase 3: Practice & Review (5-8 hours)
1. **Free 25 Questions** (1 hour)
2. **Official Practice Exam** (2 hours)
3. **Weak Domain Review** (2-3 hours)
4. **Anti-Patterns Flash Cards** (1-2 hours)

---

## ✅ Study Checklist

### Videos (Complete)
- [ ] Ep 01-15 watched (11 hours)
- [ ] Notes taken on key concepts
- [ ] Hands-on projects built (agentic loops, MCP, Claude Code)

### Supplementary (Required)
- [ ] Domain 5 complete on claudecertifications.com
- [ ] All 18 anti-patterns memorized
- [ ] All 6 scenarios understood
- [ ] Structured error patterns learned
- [ ] Validation-retry loops implemented

### Practice (Essential)
- [ ] 25 free practice questions completed
- [ ] Official practice exam taken (70%+ target)
- [ ] Weak domains identified and reviewed

### Final Prep
- [ ] Anti-patterns flashcard review
- [ ] Scenario quick reference created
- [ ] Sleep 8+ hours before exam
- [ ] Clear desk, test camera/mic

---

## 📊 Final Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| **Video Quality** | ⭐⭐⭐⭐⭐ | Excellent, hands-on, covers 65% |
| **Completeness** | ⚠️ 65% | Misses Domain 5 entirely |
| **Exam Readiness (Videos Only)** | ❌ ~50% | Need supplementary study |
| **Time Investment** | ✅ 11 hours | Well-produced, engaging |
| **Hands-On Value** | ✅ High | Python examples, real code |
| **Exam Pass Probability (Videos Only)** | ❌ 30-40% | Too many gaps |
| **Exam Pass Probability (Videos + Supplement)** | ✅ 80-85% | With full supplementary study |

---

## 🎯 Bottom Line

**Videos are EXCELLENT foundation but NOT sufficient for exam.**

**Video series: 65% coverage**  
**Missing: 35% (including 15% from Domain 5 alone)**

### To Pass the Exam:
1. ✅ Watch all 15 videos (11 hours)
2. ✅ Study claudecertifications.com for missing domains (15-20 hours)
3. ✅ Memorize anti-patterns & scenarios (5 hours)
4. ✅ Practice with exam questions (3-5 hours)

**Total Study Time:** ~35-40 hours  
**Pass Probability with this plan:** 80-85%

---

**Last Updated:** May 2026  
**Status:** Ready for supplementary study planning
