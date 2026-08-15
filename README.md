# 🤖 Autonomous Customer Support Agent

A multi-agent AI system built with **LangGraph-style orchestration** that autonomously answers customer support queries using RAG (Retrieval-Augmented Generation), with confidence-based escalation to a human when the AI isn't sure.

🔗 **Live Demo:** [Coming soon]

---

## Overview

This system simulates a real-world customer support automation pipeline:

1. **Classifies** incoming queries by category (technical/billing/general) and urgency
2. **Retrieves** relevant context from a knowledge base using semantic search (RAG)
3. **Drafts** an answer using an LLM, grounded strictly in retrieved context
4. **Decides** whether to auto-resolve or escalate to a human, based on the model's own confidence

For this demo, the knowledge base is built from public **FastAPI documentation**, but the architecture is designed to plug into any company's internal docs, ticket history, or knowledge base with minimal changes.

---

## Features

- 🧠 Multi-agent pipeline: Classifier → Retriever → Drafter → Escalation Handler
- 📚 RAG-based retrieval using ChromaDB + sentence-transformer embeddings
- 🎯 Confidence-aware responses — the system escalates rather than hallucinating when unsure
- 🎫 Ticket logging and an escalation dashboard (SQLite-backed)
- 💬 Simple chat interface built with Streamlit

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM | Groq (Llama 3.3 70B) |
| Orchestration | Custom agent pipeline (LangChain primitives) |
| Vector DB | ChromaDB |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Ticket Storage | SQLite |
| Frontend | Streamlit |

---

## Architecture

```
User Query
     │
     ▼
Query Classifier Agent ──► Category + Urgency
     │
     ▼
Knowledge Retriever Agent ──► Top-k relevant chunks (ChromaDB)
     │
     ▼
Response Drafter Agent ──► Answer + Confidence (high/medium/low)
     │
     ▼
   Confidence Check
     │
  ┌──┴──┐
  ▼     ▼
High   Low/Medium
  │     │
Auto-  Escalated
Resolved  (logged for human review)
```

---

## Why Confidence-Based Escalation Matters

A key design decision in this project: the system is intentionally **conservative**. Rather than always producing a confident-sounding answer (a common failure mode of naive LLM support bots), it self-assesses confidence based on how well the retrieved context actually covers the question, and escalates when it doesn't. This mirrors how production support systems balance automation with reliability — an honest "I'm not sure" beats a fluent but wrong answer.

---

## Project Structure

```
support-agents/
├── app.py                    # Streamlit app (chat + escalation dashboard)
├── src/
│   ├── knowledge_base.py     # Scrapes docs, builds ChromaDB knowledge base
│   ├── agents.py             # Classifier, Retriever, Drafter agents
│   ├── ticket_store.py       # SQLite ticket logging
│   └── orchestrator.py       # Full pipeline: classify → retrieve → draft → escalate
├── data/                     # SQLite ticket database
├── requirements.txt
└── README.md
```

---

## Running Locally

```bash
# Clone the repo
git clone https://github.com/Radhana123/support-agents.git
cd support-agents

# Create virtual environment
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key to a .env file
echo GROQ_API_KEY=your_key_here > .env

# Build the knowledge base (first time only)
python src/knowledge_base.py

# Run the app
streamlit run app.py
```

---

## Example Queries to Try

- "What is a path parameter in FastAPI?" (usually auto-resolved)
- "How do I connect FastAPI to a PostgreSQL database?" (usually escalated — outside knowledge base scope)

---

## Author

**Radhana** — Dual Degree student, Mechanical Engineering & Manufacturing Science, IIT Kharagpur