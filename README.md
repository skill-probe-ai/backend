# 🚀 **SkillProbeAI — Backend**

> Help developers become interview-ready — not just resume-ready.

AI-powered backend that converts resumes into **realistic interview practice sessions** and evaluates answers using LLMs with structured feedback.

---

## 🎯 Why I Built This

Preparing for technical interviews is hard.

Most candidates:

- don’t know if they are actually ready
- rely on theory or memorization
- lack real interview-style practice

At the same time, resumes often list skills that are not fully validated.

**SkillProbeAI is built to bridge this gap.**

It helps candidates:

- understand their actual skill level
- practice real interview-style questions
- receive structured, actionable feedback
- improve through iterative evaluation

👉 The goal is not just evaluation, but **guided interview preparation through realistic practice**.

---

## 🧠 What This System Does

1. Ingest resume
2. Extract skills using LLM
3. Start interview session per skill
4. Generate questions dynamically
5. Evaluate answers with structured scoring
6. Track performance across sessions

---

## ⚙️ Core Capabilities

### 📄 Resume → Structured Skills

- Converts unstructured resume text into structured skill entities
- Reduces manual input and bias

---

### 🎯 Dynamic Question Engine

- Generates questions per skill + difficulty
- Avoids static question banks
- Produces unique interview sessions per user

---

### 🧪 LLM-Based Evaluation

- Scores answers based on:
  - correctness
  - completeness
  - clarity
  - real-world thinking

- Returns structured output:

```json
{
  "score": 0-10,
  "feedback": "...",
  "improvement": "..."
}
```

---

### 🔁 Stateful Interview Sessions

Maintains:

- session_id
- question progression
- answer history

Enables multi-step evaluation and future adaptivity.

---

### 🧠 Skill Verification (Core Idea)

A skill is not “known” unless it is demonstrated.

✔ correct answers
✔ across multiple questions
✔ with consistency

👉 This lays the foundation for a **skill verification system**, not just a quiz engine.

---

## 🏗️ System Architecture

```
Frontend (React)
        ↓
Django REST API
        ↓
LLM Service Layer (OpenRouter)
        ↓
Database (SQLite / PostgreSQL)
```

---

## 🧩 Backend Design

### 🔹 API Layer (Django REST Framework)

- clean separation of concerns
- stateless endpoints
- easy frontend integration

---

### 🔹 LLM Layer

Handles:

- skill extraction
- question generation
- answer evaluation

**Design choice:**
LLM logic is isolated → makes model replacement easy.

---

### 🔹 Data Models (Conceptual)

- Resume
- Skill
- UserSkill
- InterviewSession
- Question
- Answer

This enables:

- traceability
- analytics
- future personalization

---

## ⚖️ Engineering Decisions

### 1. Why LLM for evaluation?

Rule-based evaluation:

- rigid
- hard to scale
- cannot evaluate reasoning

LLMs:

- understand context
- handle open-ended answers
- simulate interview-style feedback

---

### 2. Difficulty-Aware Scoring

Evaluation adapts based on difficulty:

| Level  | Focus               |
| ------ | ------------------- |
| Easy   | correctness         |
| Medium | completeness        |
| Hard   | production thinking |

👉 Ensures fair and realistic scoring.

---

### 3. Structured JSON Enforcement

- Forces predictable responses from LLM
- Reduces parsing failures
- Improves API reliability

---

### 4. Session-Based Flow

Tracks state to:

- maintain continuity
- evaluate progression
- support adaptive questioning (future)

---

### 5. Over-Engineering Detection

Penalizes unnecessary complexity in simple problems.

👉 Reflects real interview expectations.

---

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **LLM Gateway**: OpenRouter
- **LLM Models**: OpenRouter-compatible (e.g., Nemotron)
- **Database**: SQLite (dev), PostgreSQL (production-ready)
- **Language**: Python

---

## 🚀 Running Locally

```bash
git clone https://github.com/skill-probe-ai/backend.git
cd backend

python -m venv job_ready_env
job_ready_env\Scripts\activate

pip install -r requirements.txt

# create .env
OPENAI_API_KEY=your_key

python manage.py migrate
python manage.py runserver
```

---

## 📡 API Overview

```
POST /api/resume/
GET  /api/skills/
POST /api/interview/start/
POST /api/answer/submit/
```

---

## 🧪 Example Output

```json
{
  "score": 7,
  "feedback": "Correct implementation but slightly over-engineered for the problem scope",
  "improvement": "Simplify logic and avoid unnecessary middleware for easy-level questions"
}
```

---

## 📈 Future Work

### Near-term

- multi-question adaptive flow
- skill confidence scoring
- frontend (React)

### Mid-term

- async processing (Celery + Redis)
- caching LLM responses
- rate limiting

### Long-term

- skill graph per user
- recruiter dashboard
- analytics & insights
- coding sandbox execution

---

## 🔐 Security Considerations

- API keys via environment variables
- no secrets in repository
- input validation before LLM calls

Planned:

- authentication (JWT)
- rate limiting
- abuse protection

---

## 🧠 What This Project Demonstrates

- practical LLM integration
- backend system design
- API-first architecture
- prompt engineering
- handling unstructured data
- building evaluation workflows

---

## 👨‍💻 Author

**Vishal Singh**
Full-Stack Developer (Backend + AI Systems)

---

# ⭐ Final Thought

> Anyone can list skills.
> Very few can demonstrate them.

SkillProbeAI helps bridge that gap through structured, realistic interview practice.

---
