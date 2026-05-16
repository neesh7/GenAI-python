# Agents and Workflows

Agents and workflows are strategies for handling user tasks that Claude can't complete in a single request. Throughout this course, you've been creating both—when you used tools and let Claude figure out how to complete tasks, that was an agent.

---

## Workflows vs Agents

The decision comes down to how well you understand the task:

| Aspect | Workflow | Agent |
|--------|----------|--------|
| **Use when** | Task steps are clear and predetermined | Task parameters and steps are uncertain |
| **Structure** | Fixed series of calls to Claude | Goal + tools, Claude figures out how |
| **Control** | You define the exact flow | Claude decides the approach |
| **Best for** | Well-defined processes | Exploratory or variable tasks |

**Quick Rule:**
- **Workflow** — You can picture the exact flow
- **Agent** — You're not sure what Claude will need to do

---

## Agents: When Flexibility Matters

Agents represent a shift from structured workflows. While workflows are perfect when you know the exact steps, agents shine when you don't. Instead of defining a rigid sequence, you give Claude a goal and tools, then let it figure out how to combine them to achieve the objective.

This flexibility allows you to create one agent and deploy it to solve a wide range of unpredictable problems—but this comes with trade-offs in reliability and cost.

### How Tools Make the Agent

Tools are the building blocks. Claude's power comes from combining simple tools in unexpected ways.

**Example: Datetime Tools**
```
Tools available:
- get_current_datetime()
- add_duration_to_datetime(date, duration)
- set_reminder(content, timestamp)
```

Claude chains them creatively:
- **"What's the time?"** → Calls get_current_datetime
- **"What day is it in 11 days?"** → Calls get_current_datetime, then add_duration_to_datetime
- **"Set gym reminder next Wednesday"** → Uses all three tools in sequence
- **"When does my warranty expire?"** → Asks for purchase date first, then calculates

Claude even recognizes when it needs more information before proceeding.

### Tools Should Be Abstract, Not Specialized

**Key principle:** Provide reasonably abstract tools that Claude can combine creatively, not hyper-specialized ones.

**Claude Code example:**
```
Generic tools available:
- bash (run any command)
- read (read any file)
- write (create file)
- edit (modify files)
- glob (find files)
- grep (search contents)

NOT specialized tools like:
- refactor_code ✗
- install_dependencies ✗
```

Claude figures out how to use basic tools to accomplish complex tasks—refactoring code, installing dependencies, running tests—without explicit specialized tools. This abstraction handles countless scenarios developers never planned for.

### Best Practice: Design Combinable Tools

Provide tools that Claude can mix and match:

**Social Media Video Agent Example:**
```
Tools:
- bash (FFMPEG for video processing)
- generate_image (create images from prompts)
- text_to_speech (convert text to audio)
- post_media (upload to social platforms)
```

This enables:
- Simple workflows (create → post)
- Interactive experiences (generate sample → get approval → proceed)
- Adaptive approaches based on user feedback

The flexibility allows agents to respond dynamically—something rigid workflows struggle with. This is what makes agents powerful for user-responsive, unpredictable applications.

### Environment Inspection: The Critical Missing Piece

Claude operates blindly—it needs to observe and understand the results of its actions to work effectively.

#### Why Inspection Matters

**Computer Use Example:**
Every time Claude clicks a button or types text, it immediately receives a screenshot. Without seeing results, Claude can't know if:
- The action succeeded
- A menu opened or page navigated
- The environment changed as expected

**Without inspection:** Claude is guessing blindly  
**With inspection:** Claude understands the current state and can adapt

#### Reading Before Writing

Before modifying files, Claude must inspect current contents:

```
User: "Add a new route to this Python file"

Claude's approach:
1. Read the file (inspect environment)
2. Understand existing structure
3. Safely add new route without breaking code
4. Verify the changes
```

Skipping step 1 risks breaking existing functionality.

#### System Prompts for Inspection

Guide Claude to inspect through system prompts:

**Video Generation Agent Example:**
```
For video creation, you must:
- Use bash to run whisper.cpp and verify dialogue placement
- Use FFmpeg to extract screenshots at intervals
- Visually inspect output matches requirements
- Compare generated content against original spec
```

This ensures Claude verifies each step rather than assuming success.

#### Benefits of Environment Inspection

| Benefit | Impact |
|---------|--------|
| **Progress tracking** | Claude gauges how close to completion |
| **Error handling** | Unexpected results detected and corrected |
| **Quality assurance** | Output verified before task completion |
| **Adaptive behavior** | Claude adjusts approach based on observations |

#### Practical Implementation

Always ask: **"How will Claude know if this action worked?"**

Provide tools and instructions for Claude to observe:
- **File operations** — Read before modifications
- **UI interactions** — Take screenshots after actions
- **API calls** — Check responses for expected data
- **Content generation** — Validate against requirements

**Environment inspection transforms Claude from a blind executor into an agent that truly understands and adapts to its working environment.**

---

## Example: Image to CAD Workflow

Imagine a web app where users drag and drop an image of a metal part, and you create a STEP file (3D model) from it.

Since the task is clear and has defined steps, this is a perfect workflow candidate:

1. **Analyze** — Feed image to Claude, ask it to describe the object
2. **Model** — Claude uses CadQuery library to create a 3D model
3. **Render** — Generate a rendering of the model
4. **Grade** — Claude compares rendering to original image
5. **Iterate** — If issues found, fix them and repeat steps 3-4

---

## The Evaluator-Optimizer Pattern

This CAD workflow demonstrates the evaluator-optimizer pattern:

```
Input
  ↓
Producer: Creates output (Claude generates model/rendering)
  ↓
Grader: Evaluates output against criteria
  ↓
Does it meet criteria?
  ├─ Yes → Return result
  └─ No → Feedback to Producer
          Loop back with improvements
```

**Three components:**
1. **Producer** — Takes input and creates output
2. **Grader** — Evaluates output against criteria
3. **Feedback Loop** — Sends evaluation back for improvement

This pattern repeats until the grader accepts the output.

---

## Parallelization Workflows

Complex decisions often look simple but become problematic when implemented. Parallelization breaks these into parallel sub-tasks that Claude evaluates independently.

### The Problem with Complex Single Prompts

Asking Claude to evaluate multiple criteria at once creates cognitive overload:
- Material designer: Choose between metal, polymer, ceramic, composite, elastomer, wood
- Adding detailed criteria for each type → One massive prompt → Confusion and inconsistency

### The Parallelization Solution

Instead of one complex prompt, send **multiple focused requests simultaneously**:

```
Image of part
├─ Request 1: "Evaluate for METAL with [metal criteria]" → Metal analysis
├─ Request 2: "Evaluate for POLYMER with [polymer criteria]" → Polymer analysis
├─ Request 3: "Evaluate for CERAMIC with [ceramic criteria]" → Ceramic analysis
├─ Request 4: "Evaluate for COMPOSITE with [composite criteria]" → Composite analysis
└─ Final Step: "Compare all analyses → Best material recommendation"
```

**Pattern structure:**
1. **Split** — Break complex decision into independent sub-tasks
2. **Run in parallel** — Execute all sub-tasks simultaneously
3. **Aggregate** — Combine all results into final decision

### Why Parallelization Works

| Benefit | Impact |
|---------|--------|
| **Focused attention** | Claude concentrates on one aspect instead of juggling multiple criteria |
| **Easier optimization** | Improve individual prompts independently |
| **Better scalability** | Add new options without rewriting existing prompts |
| **Improved reliability** | Reduced cognitive load = more consistent results |

### When to Use Parallelization

Perfect for tasks with:
- Multiple independent evaluations (material types, design options, review categories)
- Different domains of expertise required
- Criteria that don't naturally combine into one question
- Complex decisions broken into simpler pieces

**Key insight:** Each parallel sub-task must be independent and contribute a distinct piece of analysis to the final decision.

---

## Chaining Workflows

Chaining breaks large complex tasks into smaller sequential subtasks that build on each other, with optional non-LLM processing between steps.

### What is Workflow Chaining?

Instead of asking Claude to do everything at once, split the work into focused steps:

**Example: Automated Video Marketing Tool**
```
1. Find trending topics on Twitter
2. Select most interesting topic (Claude)
3. Research the topic (Claude)
4. Write video script (Claude)
5. Create video (AI avatar + text-to-speech)
6. Post to social media
```

### The Long Prompt Problem

Combining all constraints into one massive prompt leads to inconsistency:

**Single Prompt Request:**
```
Write a technical article that:
- Doesn't mention AI authorship
- Avoids emojis
- No clichéd language
- Professional, technical tone
```

**Result:** Claude might still include emojis, mention AI, or sound unprofessional. Too many constraints to juggle simultaneously.

### The Chaining Solution

Break into two sequential steps:

**Step 1:** Generate initial content (accept it won't be perfect)
```
Claude: Writes article with some constraint violations
```

**Step 2:** Focused revision (Claude concentrates only on fixing)
```
User: "Revise this article:
1. Remove any AI authorship mentions
2. Delete all emojis
3. Replace cringey writing with technical language"

Claude: Fixes specific issues with full focus
```

### Why Chaining Works Better

| Single Prompt | Chaining |
|---------------|----------|
| Claude juggles many constraints | Claude focuses on one step at a time |
| Often ignores some rules | Revision step catches violations |
| Harder to debug failures | Each step isolated and testable |
| Complex and long | Simpler, more focused requests |

### When to Use Chaining

Perfect for:
- Complex tasks with multiple requirements
- Claude consistently ignores constraints in long prompts
- Need to validate/process outputs between steps
- Multi-stage transformations (generate → revise → format → validate)

**Key insight:** Chaining reduces cognitive load by letting Claude focus on one aspect sequentially rather than balancing everything simultaneously.

---

## Routing Workflows

Routing categorizes incoming requests and directs them to specialized processing pipelines instead of using one generic prompt for all request types.

### The Problem with Generic Prompts

A single prompt can't handle diverse request types effectively:

**Example: Video Script Generator**
- Topic: "Python functions" → needs educational content (clear explanations, examples)
- Topic: "Surfing" → needs entertainment content (high-energy, visual appeal)

One generic prompt fails because different topics require fundamentally different approaches.

### Setting Up Content Categories

Define specialized categories for your application:

| Category | Purpose | Style |
|----------|---------|-------|
| **Educational** | Clear explanations | Engaging, relatable examples |
| **Entertainment** | High-energy content | Trendy language, cultural relevance |
| **Comedy** | Humor-focused | Sharp observations, unexpected twists |
| **Personal Vlog** | Authentic storytelling | Conversational, intimate tone |
| **Reviews** | Experience-based | Strengths/weaknesses focus |
| **Storytelling** | Immersive content | Vivid details, emotional connection |

Each category gets its own specialized prompt template optimized for that style.

### How Routing Works

**Two-step process:**

**Step 1: Categorization**
```
User input: "Python functions"
↓
Claude categorizes: "Educational"
```

**Step 2: Specialized Processing**
```
Use educational prompt template
↓
Generate script with educational style
```

### Routing Workflow Architecture

```
User input
    ↓
Router (Claude categorizes request)
    ↓
Select specialized pipeline based on category
    ↓
Process through optimized workflow for that category
    ↓
Return specialized output
```

**Key insight:** Input goes to ONE specialized pipeline, not all. Each pipeline is highly optimized for its specific use case.

### When to Use Routing

Perfect for:
- Applications handling diverse request types
- Clear, definable categories covering your use cases
- Reliable categorization by Claude
- Benefit of specialization outweighs routing overhead

**Common use cases:** Customer service bots, content generation tools, multi-domain question answering, request classification systems.

---

---

## Workflows vs Agents: The Decision Framework

When building AI applications, choose between workflows and agents based on your problem domain and reliability requirements.

### What Are Workflows?

Predefined series of Claude calls to solve **known problems**. You use workflows when:
- You can picture the exact sequence of steps
- The task is well-defined and specific
- You know what inputs the system will receive

**Example:** Image → Analyze → Model → Grade → Iterate

### What Are Agents?

Claude gets tools and formulates its own plan to complete tasks. You use agents when:
- You don't know what exact tasks will arrive
- The system must handle novel, unpredictable situations
- Tasks require creative tool combinations

**Example:** "Plan my entire trip" (agent decides: weather → flights → hotels → itinerary)

### Side-by-Side Comparison

| Aspect | Workflows | Agents |
|--------|-----------|--------|
| **Accuracy** | ✅ Higher—Claude focuses on one task | ⚠️ Lower—more moving parts |
| **Flexibility** | ✗ Low—dedicated to specific task types | ✅ High—handles varied requests |
| **Testing** | ✅ Easy—you know each exact step | ⚠️ Hard—steps are unpredictable |
| **Predictability** | ✅ High—consistent behavior | ⚠️ Low—Claude decides the path |
| **User Experience** | ⚠️ Constrained—specific inputs required | ✅ Flexible—natural conversation |
| **Planning Required** | ⚠️ High upfront design work | ✅ Lower—more adaptive |

### Benefits of Workflows

- ✅ Claude focuses on one subtask at a time → higher accuracy
- ✅ Easy to evaluate and test (known steps)
- ✅ Predictable and reliable execution
- ✅ Perfect for specific, well-defined problems

### Benefits of Agents

- ✅ Flexible user experience
- ✅ Claude combines tools creatively for varied tasks
- ✅ Handles novel situations not anticipated during development
- ✅ Can ask users for additional input when needed

### When to Use Each

**Use Workflows when:**
- You have well-defined processes
- Reliability is critical
- Task steps are predetermined
- You need consistent, predictable behavior

**Examples:** Content analysis, document processing, image-to-CAD conversion, customer inquiry routing

**Use Agents when:**
- Handling unpredictable, varied user requests
- Creative problem-solving is required
- Task parameters are unknown upfront
- Flexibility matters more than perfect reliability

**Examples:** General-purpose coding assistant, research helper, trip planner, customer service

### The Engineering Principle

**Users care about reliability, not fancy architecture.**

Your primary goal: solve problems reliably. The recommendation is **always implement workflows where possible** and resort to agents only when truly required.

Workflows provide the reliability and predictability production applications need. Agents offer flexibility for scenarios where exact requirements can't be predetermined.

**In most cases, start with workflows—they're more maintainable, testable, and reliable.**

---

## Advanced Topics to Investigate

As you build more sophisticated AI applications, these advanced topics become important:

### Agent Orchestration
Managing multiple agents working together, coordinating their actions, and handling communication between agents. This includes designing systems where agents can delegate tasks to other agents and combine their results.

### Agent Evaluation and Instrumentation
Measuring agent performance beyond simple accuracy metrics. Includes tracking decision paths, evaluating tool selection choices, monitoring cost-per-task, and understanding agent behavior patterns over time.

### Agentic RAG
Combining agent capabilities with retrieval-augmented generation. Agents autonomously decide when to retrieve information, what queries to make, and how to synthesize retrieval results into final answers.

### RAG Evaluation
Evaluating retrieval and generation components separately. Includes measuring retrieval quality (precision, recall, relevance) independently from generation quality, and understanding where RAG systems fail.

### Tool Evaluation
Assessing whether your tool definitions are effective for agent use. Questions include: Are tools abstract enough? Do agents use them creatively? Are certain tools never called? Do agents struggle with any particular tool?

---

## Why These Patterns Matter

Understanding workflows and agents gives you repeatable recipes for your own features:

**Workflow Patterns:**
- **Evaluator-Optimizer** — Iterative improvement through feedback loops
- **Parallelization** — Independent multi-criteria evaluations
- **Chaining** — Sequential tasks with constraint focus
- **Routing** — Categorization and specialized processing pipelines

**Agent Design:**
- Abstract, combinable tools (not specialized)
- Environment inspection for adaptive behavior
- Flexible task handling for unpredictable scenarios

These patterns help you design better multi-step systems with the right trade-offs between reliability and flexibility.
