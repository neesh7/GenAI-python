# Write a proompt that will assist users in writing python code, json config or Regular expressions focused on AWS-specific use cases
# Input: User will request for a specific task
# Output: Python, JSON, or a regular expression without any explanation

# Step1: write a draft prompt
# Step2: assemble a dataset Eval Dataset

import dotenv
from anthropic import Anthropic
import json
from statistics import mean
import re, ast

# 
dotenv.load_dotenv()
client = Anthropic()
model = "claude-haiku-4-5-20251001"

# Helper Functions
def add_user_messege(messages, text):
    user_messege = {"role": "user", "content": text}
    messages.append(user_messege)

def add_assistant_messege(messages, text):
    assistant_messege = {"role": "assistant", "content": text}
    messages.append(assistant_messege)

def chat(messages, system_prompt=None, temperature=0.5, stop_sequence=[]):
    # Note temp close to 0 is deterministic and close to 1 is creative use case
    params = {
        "model": model,
        "max_tokens": 500,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequence
            }
    if system_prompt:
        params["system"] = system_prompt

    message = client.messages.create(**params)
    return message.content[0].text

# # declare an message list to maintain conversation history
# messages = []

def generate_dataset():
    prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
  {
    "task": "Create a JSON configuration for an AWS Lambda function that sets up a basic Python runtime with a memory allocation of 512MB and a timeout of 10 seconds",
    "format": "json",
    "solution_criteria": "Must include runtime, memory size, timeout, and basic structure for AWS Lambda configuration"
  },
  ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
* Focus on tasks that do not require writing much code
* Each task must include a "solution_criteria" field describing what a good solution must contain

Please generate 3 objects.
"""
    messages = []
    add_user_messege(messages, prompt)
    add_assistant_messege(messages, "```json")
    text = chat(messages, stop_sequence=["```"])
    return json.loads(text)


def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""
    prompt = f"""
Please solve the following task:

{test_case["task"]}

* Respond only with Python, JSON, or a plain REGEX
* Do not add any commentary or explanation
"""

    messages = []
    add_user_messege(messages, prompt)
    add_assistant_messege(messages,"```code")
    output = chat(messages, stop_sequence=["```"])
    return output

def grade_by_model(test_case, output):
    # Create evaluation prompt
    eval_prompt = f"""
You are an expert code reviewer. Evaluate this AI-generated solution against the provided solution criteria.

Task:
<task>
{test_case["task"]}
</task>

Solution to Evaluate:
<solution>
{output}
</solution>

Solution Criteria (what a good solution MUST contain):
<solution_criteria>
{test_case.get("solution_criteria", "No specific criteria provided")}
</solution_criteria>

Evaluate how well the solution meets the criteria above. Respond with ONLY a valid JSON object (no markdown, no code blocks):
{{
  "strengths": ["strength1", "strength2"],
  "weaknesses": ["weakness1", "weakness2"],
  "reasoning": "brief explanation referencing the solution_criteria",
  "score": 7
}}
"""

    messages = []
    add_user_messege(messages, eval_prompt)

    eval_text = chat(messages, temperature=0.3)

    # Try to parse JSON with error handling
    try:
        # First try direct parsing
        return json.loads(eval_text)
    except json.JSONDecodeError:
        # Try to extract JSON from the response
        try:
            json_start = eval_text.find('{')
            json_end = eval_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = eval_text[json_start:json_end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        # Fallback response if parsing fails
        return {
            "strengths": ["Unable to parse response"],
            "weaknesses": ["Response parsing failed"],
            "reasoning": eval_text[:500],
            "score": 5
        }


def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0

def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0

def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0


def grade_syntax(output, test_case):
    """Validates the syntax of the output based on the test case format"""
    fmt = test_case.get("format", "").lower()

    if fmt == "json":
        return validate_json(output)
    elif fmt == "python":
        return validate_python(output)
    elif fmt == "regex":
        return validate_regex(output)
    else:
        # Try all validators and return the highest score
        return max(
            validate_json(output),
            validate_python(output),
            validate_regex(output)
        )


def run_test_case(test_case):
    """Calls run_prompt, then grades the result"""
    output = run_prompt(test_case)

    model_grade = grade_by_model(test_case, output)
    model_score = model_grade["score"]
    reasoning = model_grade["reasoning"]

    syntax_score = grade_syntax(output, test_case)
    score = (model_score + syntax_score) / 2

    return {
        "output": output,
        "test_case": test_case,
        "model_score": model_score,
        "syntax_score": syntax_score,
        "score": score,
        "reasoning": reasoning,
    }


def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    average_score = mean([result["score"] for result in results])
    print(f"Average Score:{average_score}")
    return results


if __name__ == "__main__":
    # Check if dataset exists, if not generate it
    try:
        with open("dataset.json", "r") as f:
            dataset = json.load(f)
        print("Loaded existing dataset from dataset.json")
    except FileNotFoundError:
        print("Generating new dataset...")
        dataset = generate_dataset()
        with open('dataset.json', 'w') as f:
            json.dump(dataset, f, indent=2)
        print("Dataset saved to dataset.json")

    print(f"\nRunning evaluation on {len(dataset)} test cases...\n")

    # Run evaluation
    results = run_eval(dataset)

    # Display results
    print("=" * 80)
    print("EVALUATION RESULTS")
    print("=" * 80)
    print(json.dumps(results, indent=2))

    # Save results
    with open('eval_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\n✓ Results saved to eval_results.json")
