from openai import OpenAI
import os
import json
import re

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)

# ------------------ JSON PARSER ------------------

def safe_parse_json_evaluate_answer(data):
    # Already parsed
    if isinstance(data, dict):
        return data

    # If string → try parsing
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            pass

        # Try extracting JSON block safely (non-greedy)
        try:
            match = re.search(r'\{[\s\S]*?\}', data)
            if match:
                return json.loads(match.group())
        except:
            pass

    return {
        "score": None,
        "feedback": "Could not parse response",
        "improvement": "Ensure LLM returns valid JSON"
    }


# ------------------ SKILL EXTRACTION ------------------

def extract_skills(resume_text):
    prompt = f"""
    Extract all technical skills from this resume.
    Return ONLY a JSON array of skill names.

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model= "nvidia/nemotron-3-nano-30b-a3b:free",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

def generate_question(skill, difficulty):
    prompt = f"""
    Ask a {difficulty} level backend interview question on {skill}.

    Rules:
    - real-world scenario
    - no theory definitions
    - one clear question only
    - Only ask one-liners (questions which could be answered in one line)
    """

    response = client.chat.completions.create(
        model= "nvidia/nemotron-3-nano-30b-a3b:free",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# ------------------ ANSWER EVALUATION ------------------

def evaluate_answer(skill, question, answer, difficulty):

    # -------- Difficulty Rules --------
    if difficulty == "easy":
        difficulty_rules = """
This is an EASY question:
- Focus ONLY on correctness and basic implementation
- Do NOT penalize for missing production-level concerns
- Do NOT expect scalability or architecture
- Simpler solutions are preferred
- Over-engineering should slightly reduce score

Typical score range:
- Correct simple solution → 7–9
- Over-engineered but correct → 6–8
- Incorrect → below 5
"""
        criteria = """
EVALUATION CRITERIA:
1. Correctness (MOST IMPORTANT)
2. Basic completeness
3. Simplicity and clarity

Ignore:
- scalability
- architecture
- advanced optimizations
"""

    elif difficulty == "medium":
        difficulty_rules = """
This is a MEDIUM question:
- Expect correct and reasonably complete answer
- Some real-world thinking should be present
- Missing edge cases should reduce score slightly
"""
        criteria = """
EVALUATION CRITERIA:
1. Correctness
2. Completeness
3. Code quality
4. Some real-world thinking
"""

    else:
        difficulty_rules = """
This is a HARD question:
- Expect production-ready thinking
- Must include scalability, edge cases, and trade-offs
- Penalize heavily for incomplete or shallow answers
"""
        criteria = """
EVALUATION CRITERIA:
1. Correctness
2. Completeness
3. Production readiness
4. Scalability & edge cases
5. System design thinking
"""

    # -------- Prompt --------
    prompt = f"""
You are a senior backend engineer conducting a real interview.

Skill: {skill}

Question:
{question}

Candidate Answer:
```
{answer}
```

Difficulty: {difficulty}

{difficulty_rules}

{criteria}

SCORING RUBRIC:
0–3 → Poor
4–5 → Basic
6–7 → Good
8–9 → Strong
10 → Exceptional

IMPORTANT RULES:
- Follow difficulty strictly
- For EASY: prioritize correctness over everything
- Do NOT penalize missing advanced concepts in easy questions
- If code is present, evaluate structure and best practices
- Be consistent with scoring rubric

Return STRICT JSON ONLY:
{{
"score": number,
"feedback": "clear strengths + weaknesses",
"improvement": "specific actionable steps"
}}
"""

    # -------- LLM Call --------
    response = client.chat.completions.create(
        model="nvidia/nemotron-3-nano-30b-a3b:free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    raw_output = response.choices[0].message.content

    # Debug (keep for now)
    print("RAW OUTPUT TYPE:", type(raw_output))
    print("RAW OUTPUT:", raw_output)

    return safe_parse_json_evaluate_answer(raw_output)