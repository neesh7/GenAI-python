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

## Why These Patterns Matter

Understanding workflows gives you repeatable recipes for your own features. The evaluator-optimizer is one proven pattern—consider applying it to:
- Code review automation
- Document quality checking
- Image/content validation
- Data processing pipelines

Remember: identifying patterns doesn't implement anything—you still write the code. But these proven patterns help you design better multi-step systems.
