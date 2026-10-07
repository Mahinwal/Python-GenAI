# GenAI Prompting — Learning Notes

A practical guide to learning prompt engineering with the **OpenAI Python SDK**.

The goal is to understand prompting as an application-development skill rather than memorizing "magic prompts".

---

## 1. What is Prompting?

Prompting is the process of giving an LLM clear instructions, context, constraints, examples, and an expected output format so that it can perform a task reliably.

A useful mental model is:

```text
Instructions / System Behavior
            ↓
         Context
            ↓
       User Request
            ↓
          LLM
            ↓
      Structured Output
```

A production prompt is often a contract between your application and the model.

---

# 2. Prompting Learning Roadmap

## Level 1 — Prompting Foundations

1. System Prompting
2. Instruction Prompting
3. Zero-Shot Prompting
4. One-Shot Prompting
5. Few-Shot Prompting
6. Persona / Role Prompting
7. Contextual Prompting
8. Delimiter-Based Prompting
9. Constraint Prompting
10. Output Format Prompting
11. Structured Output / JSON

## Level 2 — Reasoning and Reliability

12. Step-by-Step Prompting
13. Chain-of-Thought Concepts
14. Problem Decomposition
15. Self-Consistency
16. Reflection / Critique Prompting
17. Prompt Chaining

> Note: Do not design applications around requesting or exposing a model's private chain-of-thought. Prefer concise reasoning summaries, intermediate results, or structured outputs when appropriate.

## Level 3 — Application-Oriented Prompting

18. Tool / Function Calling
19. ReAct-style workflows
20. RAG Prompting
21. Agent Prompting
22. Multi-step Workflows
23. Prompt Evaluation
24. Prompt Optimization

---

# 3. OpenAI SDK Setup

Install the OpenAI Python SDK:

```bash
pip install openai
```

Set your API key as an environment variable.

Linux/macOS:

```bash
export OPENAI_API_KEY="your-api-key"
```

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your-api-key"
```

Then:

```python
from openai import OpenAI

client = OpenAI()
```

The SDK reads `OPENAI_API_KEY` from the environment.

---

# 4. Your First LLM Request

Start with the simplest possible request.

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="YOUR_MODEL",
    input="What is FastAPI?"
)

print(response.output_text)
```

Conceptually:

```text
User Input
    ↓
OpenAI API
    ↓
LLM
    ↓
Response
```

There is no special behavior instruction yet.

This is your baseline.

---

# 5. System Prompting

## What is System Prompting?

A system prompt defines the model's high-level behavior, role, rules, constraints, and communication style.

Instead of only asking:

```text
What is FastAPI?
```

we can tell the model how to answer:

```text
You are an experienced Python backend tutor.
Explain technical concepts clearly.
Use practical examples.
Keep explanations concise.
```

With the OpenAI Responses API, high-level behavior can be provided using `instructions`.

Example:

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="YOUR_MODEL",
    instructions="""
    You are an experienced Python backend tutor.

    Explain technical concepts clearly.
    Assume the learner already knows Python basics.
    Use practical examples.
    Keep explanations concise.
    """,
    input="What is FastAPI?"
)

print(response.output_text)
```

---

# 6. System Prompt Structure

A useful structure is:

```text
ROLE
    ↓
OBJECTIVE
    ↓
CONTEXT
    ↓
RULES
    ↓
CONSTRAINTS
    ↓
OUTPUT REQUIREMENTS
```

Example:

```text
ROLE:
You are a senior Python backend engineer and technical tutor.

AUDIENCE:
The learner has several years of Python backend experience.

OBJECTIVE:
Help the learner understand backend and GenAI concepts.

BEHAVIOR:
- Explain concepts practically.
- Prefer real-world examples.
- Explain why something is used.
- Mention common mistakes.

CONSTRAINTS:
- Avoid unnecessary theory.
- Keep answers concise.
- Do not use unnecessarily complex terminology.

OUTPUT:
- Start with a simple explanation.
- Give a practical Python example.
- Explain the example.
- Mention one common mistake.
```

---

# 7. Why System Prompting Matters

Compare these two requests.

## Without instructions

```python
response = client.responses.create(
    model="YOUR_MODEL",
    input="Explain dependency injection in FastAPI."
)
```

The model decides how to explain the concept.

## With instructions

```python
response = client.responses.create(
    model="YOUR_MODEL",
    instructions="""
    You are a senior Python backend engineer.

    The learner already knows Python and FastAPI.

    Explain concepts using practical production examples.
    Avoid beginner-level explanations.
    Explain why the concept is useful.
    Mention one common mistake.
    Keep the answer concise.
    """,
    input="Explain dependency injection in FastAPI."
)
```

The question is identical.

The desired behavior is different.

That is the core idea of system prompting.

---

# 8. Role / Persona Prompting

Persona prompting defines the role or expertise the model should use.

Example:

```text
You are a senior Python backend engineer.
```

Or:

```text
You are a technical interviewer specializing in Python and FastAPI.
```

Or:

```text
You are a code reviewer focused on production-quality Python.
```

Example:

```python
response = client.responses.create(
    model="YOUR_MODEL",
    instructions="""
    You are a senior Python backend engineer
    reviewing production code.

    Focus on:
    - correctness
    - maintainability
    - performance
    - security
    - Python best practices
    """,
    input="Review this FastAPI endpoint: ..."
)
```

Persona is useful, but remember:

> A persona does not magically give the model new knowledge. It mainly influences behavior, focus, vocabulary, and response style.

---

# 9. Zero-Shot Prompting

Zero-shot means asking the model to perform a task without providing examples.

Example:

```text
Classify the following customer message as:
- complaint
- question
- feedback

Message:
"The application keeps timing out."
```

No examples are provided.

Python:

```python
response = client.responses.create(
    model="YOUR_MODEL",
    input="""
    Classify the following customer message as:
    - complaint
    - question
    - feedback

    Message:
    "The application keeps timing out."
    """
)

print(response.output_text)
```

Use zero-shot when the task is simple and the desired behavior is easy to describe.

---

# 10. One-Shot Prompting

One-shot prompting provides one example.

```text
Classify messages as complaint or question.

Example:
Message: "Why can't I log in?"
Classification: question

Now classify:
Message: "The application keeps crashing."
```

The example demonstrates the desired pattern.

---

# 11. Few-Shot Prompting

Few-shot prompting provides multiple examples.

```text
Classify the message.

Examples:

Message: "Why can't I log in?"
Classification: question

Message: "The application crashes every time."
Classification: complaint

Message: "The new dashboard is much easier to use."
Classification: feedback

Now classify:
Message: "Can you explain why my report failed?"
```

Few-shot prompting is particularly useful when:

- The task has a specific output pattern.
- The classification rules are difficult to explain.
- You need the model to imitate a particular style.
- Examples communicate the desired behavior better than instructions.

---

# 12. Contextual Prompting

Give the model the information it needs to perform the task.

Example:

```text
You are a customer-support assistant.

Use the following product information:

Product:
FastAPI Training Course

Duration:
30 days

Level:
Intermediate

Now answer:

How long is the course?
```

The model can answer using the supplied context.

This concept becomes extremely important in **RAG**.

---

# 13. Delimiter-Based Prompting

Use clear delimiters to separate instructions from data.

Example:

```text
SYSTEM:
You are a text classifier.

USER DATA:
<customer_message>
The application is not working.
</customer_message>

TASK:
Classify the message.
```

In Python:

```python
message = "The application is not working."

response = client.responses.create(
    model="YOUR_MODEL",
    instructions="""
    You are a customer-support classifier.
    Classify the customer message.
    """,
    input=f"""
    <customer_message>
    {message}
    </customer_message>

    Return the classification.
    """
)
```

Delimiters become especially important when your application inserts user-generated or retrieved content into prompts.

Common delimiters include:

```text
<document>
</document>

<context>
</context>

<customer_message>
</customer_message>
```

---

# 14. Constraint Prompting

Constraints tell the model what it must or must not do.

Example:

```text
Rules:
- Answer only using the supplied context.
- Do not invent information.
- If the answer is unavailable, say "I don't know."
- Keep the answer under 100 words.
```

Python:

```python
response = client.responses.create(
    model="YOUR_MODEL",
    instructions="""
    You are a documentation assistant.

    Rules:
    - Answer only using the supplied context.
    - Do not invent information.
    - If the answer is unavailable, say "I don't know."
    - Keep the answer concise.
    """,
    input="..."
)
```

Constraints are extremely important for production systems.

---

# 15. Output Format Prompting

Tell the model exactly how you want the answer structured.

Example:

```text
Return the answer using this format:

Definition:
...

Example:
...

Common mistake:
...
```

Another example:

```text
Return:

Summary:
...

Advantages:
...

Disadvantages:
...
```

This is useful when another part of your application will consume the output.

---

# 16. Structured Output

For applications, free-form text is often not enough.

You may want:

```json
{
  "category": "complaint",
  "priority": "high",
  "summary": "Application timeout"
}
```

Conceptually:

```text
User Input
    ↓
LLM
    ↓
Structured Output
    ↓
Python Application
    ↓
Database / API / Workflow
```

Structured output is particularly important when integrating LLMs into FastAPI services.

---

# 17. Prompt Chaining

Instead of asking the model to perform a large task in one prompt, break it into smaller steps.

Example:

```text
Step 1:
Extract the customer's problem.

        ↓

Step 2:
Classify the problem.

        ↓

Step 3:
Generate a response.

        ↓

Step 4:
Validate the response.
```

This can improve reliability and makes debugging easier.

---

# 18. Decomposition Prompting

Break a complex problem into smaller tasks.

Instead of:

```text
Analyze this entire software architecture.
```

Use:

```text
1. Identify the components.
2. Identify communication between components.
3. Identify potential bottlenecks.
4. Identify security risks.
5. Recommend improvements.
```

The model now has a clearer task structure.

---

# 19. Reflection / Critique Prompting

Ask the model to evaluate an answer against explicit criteria.

Example:

```text
Review the proposed solution.

Check:
1. Correctness
2. Security
3. Performance
4. Maintainability

List problems first, then provide an improved solution.
```

This is useful for:

- Code review
- Writing
- Requirements analysis
- Generated SQL
- Architecture review

---

# 20. Chain-of-Thought: Important Note

Chain-of-thought refers to intermediate reasoning used to solve complex problems.

You may encounter prompts such as:

```text
Think step by step.
```

For modern application design, avoid making your application depend on receiving the model's private chain-of-thought.

Instead, request useful, observable artifacts:

```text
Provide the key steps used to reach the answer.
```

or:

```text
Show the calculation steps.
```

or:

```text
Return the assumptions and final result.
```

This gives you useful reasoning information without requiring hidden internal reasoning.

---

# 21. A Production-Oriented Prompt Template

A useful starting template:

```text
ROLE:
You are [role].

OBJECTIVE:
Your task is to [objective].

CONTEXT:
<context>
[relevant information]
</context>

RULES:
- [rule 1]
- [rule 2]
- [rule 3]

CONSTRAINTS:
- [constraint 1]
- [constraint 2]

TASK:
[user task]

OUTPUT:
Return the response in the following format:
[format]
```

Example:

```text
ROLE:
You are a senior Python backend engineer.

OBJECTIVE:
Help developers understand Python backend concepts.

CONTEXT:
The developer has several years of Python experience.

RULES:
- Prefer practical examples.
- Explain why a technique is used.
- Mention common mistakes.

CONSTRAINTS:
- Avoid unnecessary theory.
- Keep explanations concise.

TASK:
Explain dependency injection in FastAPI.

OUTPUT:
1. Definition
2. Practical example
3. Explanation
4. Common mistake
```

---

# 22. Prompting Experiments

The best way to learn prompting is to keep the user question unchanged and modify the instructions.

Use:

```text
Question:
Explain dependency injection in FastAPI.
```

### Experiment 1

```text
You are a teacher.
```

### Experiment 2

```text
You are a senior backend engineer.
```

### Experiment 3

```text
You are a senior backend engineer.

Use practical FastAPI examples.
```

### Experiment 4

```text
You are a senior backend engineer.

The learner already knows Python and FastAPI.
Avoid beginner-level explanations.
Use practical examples.
```

### Experiment 5

```text
You are a senior backend engineer.

The learner already knows Python and FastAPI.

For every answer:
1. Explain the concept.
2. Give a practical example.
3. Explain the example.
4. Mention one common mistake.

Keep the answer concise.
```

Compare the outputs.

This experiment demonstrates how instructions change model behavior.

---

# 23. Recommended Learning Order

Follow this sequence:

```text
System Prompting
       ↓
Instruction Prompting
       ↓
Zero-Shot
       ↓
One-Shot
       ↓
Few-Shot
       ↓
Persona / Role
       ↓
Context
       ↓
Delimiters
       ↓
Constraints
       ↓
Output Formatting
       ↓
Structured Output
       ↓
Decomposition
       ↓
Prompt Chaining
       ↓
Reflection
       ↓
Tool Calling
       ↓
RAG Prompting
       ↓
Agents
```

---

# 24. First Practice Project — AI Python Tutor

Build a simple Python application:

```text
                User
                  |
                  | Question
                  ↓
             Python App
                  |
                  ↓
            OpenAI SDK
                  |
        +---------+---------+
        |                   |
 Instructions            User Input
        |                   |
        +---------+---------+
                  ↓
                 LLM
                  |
                  ↓
               Answer
```

Requirements:

- Use the OpenAI Python SDK.
- Use the Responses API.
- Use an instruction/system-style prompt.
- Accept a Python question from the user.
- Return the answer.
- Experiment with different system prompts.
- Compare the outputs.

Start with a CLI application before adding FastAPI.

---

# 25. Key Takeaways

### Prompting is not about magic words.

Good prompts generally provide:

```text
Clear role
+
Clear objective
+
Relevant context
+
Explicit rules
+
Useful constraints
+
Expected output
```

### Start simple.

Do not immediately jump to:

```text
LangChain
RAG
Agents
Vector databases
MCP
Fine-tuning
```

First understand:

```text
Python
  ↓
OpenAI SDK
  ↓
LLM
  ↓
Instructions
  ↓
User Input
  ↓
Output
```

Once this mental model is clear, the advanced GenAI architecture becomes much easier to understand.

---

## Suggested Next Topic

After completing the System Prompting exercises, continue with:

**Instruction Prompting → Zero-Shot → One-Shot → Few-Shot Prompting**

Then build the same application using all three techniques and compare the results.