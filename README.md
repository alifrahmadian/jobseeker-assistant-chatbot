# 🔭 CareerLens — AI-Powered Jobseeker Assistant Chatbot

**CareerLens** is an intelligent career advisor chatbot built for jobseekers. Powered by a multi-agent AI architecture, it helps users navigate the job market by analyzing resume data, identifying skill gaps, and providing personalized career insights.

> Built as Capstone Project 3 — AI Engineering Bootcamp, Purwadhika  
> **Mohamad Alif Rahmadian**

---

## 🌐 Live Demo

🚀 **[Try CareerLens on Streamlit Cloud](https://jobseeker-assistant-chatbot-8xwqrewv2mketgmrxacd6j.streamlit.app/)**

📂 **[GitHub Repository](https://github.com/alifrahmadian/jobseeker-assistant-chatbot)**

---

## 🎯 Problem Statement

In today's competitive job market, jobseekers face two core challenges:

1. **Lack of self-awareness** — Many applicants don't know why they're not getting callbacks. Is it a skill gap? A weak CV? Misaligned job targeting?
2. **Information overload** — With thousands of job postings across platforms, it's hard to know which roles genuinely fit your background.

CareerLens solves this by providing a conversational AI that can analyze your CV, benchmark you against real candidate data, and give actionable insights — all powered by a dataset of 2,400+ real-world resumes.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Job Recommendation** | Find roles that match your background or uploaded CV |
| 📊 **Personal Career Insight** | Understand how your profile compares to candidates in the dataset |
| 🧩 **Skill Gap Analysis** | Identify missing skills for your target role |
| 📝 **Resume Improvement Hints** | Get actionable suggestions to strengthen your CV |
| 📈 **Job Market Insight** | Explore trending skills and categories in the job market |
| 🏆 **Benchmark** | See what a typical resume looks like in your target field |
| ⭐ **CV Scoring** | Get a 0–100 score with breakdown and improvement tips |
| 🔗 **Job Description Analysis** | Paste a LinkedIn job posting and get a fit analysis against your CV |
| 📄 **CV Upload** | Upload your PDF CV for automatic parsing and personalized analysis |

---

## 🏗️ Architecture

CareerLens uses a **multi-agent supervisor architecture** built with LangGraph.

```
User Input
    │
    ▼
┌─────────────┐
│  Supervisor  │  ← Routes based on intent
└──────┬──────┘
       │
  ┌────┴────┐─────────────┐
  ▼         ▼             ▼
RAG        SQL        CV Analysis
Agent      Agent        Agent
  │         │             │
  ▼         ▼             ▼
Qdrant    MySQL      RAG + SQL + CV Parser
(Semantic) (Structured)  (Multi-tool)
```

**State flows through all agents** via LangGraph's `StateGraph`, carrying conversation history, user background, and intermediate results.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | OpenAI GPT-4o-mini (chat), GPT-4o (CV parsing) |
| **Agent Framework** | LangChain + LangGraph |
| **Vector Database** | Qdrant Cloud |
| **Relational Database** | MySQL (Railway) |
| **Observability** | Langfuse |
| **UI** | Streamlit |
| **Language** | Python 3.14 |

---

## 📊 Dataset

- **Source**: [Kaggle Resume Dataset](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset)
- **Size**: 2,400+ resumes
- **Categories**: 24 job categories (IT, Finance, Engineering, Healthcare, etc.)
- **Format**: CSV with raw resume text (`Resume_str`) and category labels

### Data Pipeline

```
Raw CSV (Resume_str)
    │
    ├──→ LLM Extraction → MySQL
    │     (job_title, skills,
    │      experiences, educations)
    │
    └──→ OpenAI Embedding → Qdrant
          (semantic vectors for RAG)
```

---

## 🤖 Agents

### Supervisor Agent
Routes user queries to the appropriate specialist agent based on intent detection.

### RAG Agent
Handles semantic search queries using Qdrant vector database. Best for finding similar profiles, qualitative insights, and contextual job recommendations.

### SQL Agent
Handles structured data queries using Text-to-SQL against MySQL. Best for statistics, counts, aggregations, and filtering by category or skills.

### CV Analysis Agent
Multi-tool agent (using `create_agent`) that orchestrates RAG, SQL, and CV Parser tools for deep CV analysis, scoring, and personalized insights.

---

## 🗂️ Project Structure

```
jobseeker-assistant-chatbot/
├── main.py                    # Streamlit entry point
├── requirements.txt
├── packages.txt               # System dependencies (poppler)
├── pyproject.toml
├── .env.example
├── data/
│   ├── raw/                   # Original dataset
│   └── processed/             # Cleaned dataset
├── notebooks/
│   └── exploration.ipynb      # Data exploration
├── scripts/
│   └── run_pipeline.py        # One-time data pipeline
└── app/
    ├── agents/                # Supervisor, RAG, SQL, CV Analysis agents
    ├── database/              # MySQL & Qdrant clients
    ├── graphs/                # LangGraph StateGraph
    ├── pipelines/             # Data ingestion, extraction, embedding
    ├── prompts/               # All prompt templates
    ├── schemas/               # Pydantic schemas
    ├── tools/                 # RAG, SQL, CV Parser tools
    └── utils/                 # Config, logger, utilities
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- MySQL (local)
- Qdrant Cloud account
- OpenAI API key
- Langfuse account

### Installation

```bash
# Clone the repository
git clone https://github.com/alifrahmadian/jobseeker-assistant-chatbot.git
cd jobseeker-assistant-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
make install

# Install system dependencies (Mac)
brew install poppler
```

### Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```env
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL_NAME=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CV_MODEL=gpt-4o

QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key
QDRANT_COLLECTION_NAME=resumes

MYSQL_DB_HOST=localhost
MYSQL_DB_USER=root
MYSQL_DB_PASSWORD=your_password
MYSQL_DB_DATABASE=jobseeker_assistant_chatbot_db
MYSQL_DB_PORT=3306

LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

### Run Data Pipeline (One-time)

```bash
make run_pipeline
```

### Run Application

```bash
make run
```

---

## 📋 Requirements

See `requirements.txt` for full list. Key dependencies:

- `langchain`, `langchain-openai`, `langchain-community`
- `langgraph`
- `langfuse`
- `qdrant-client`, `langchain-qdrant`
- `mysql-connector-python`
- `streamlit`
- `pdf2image`, `pillow`
- `pandas`, `pydantic`

---

## 🎓 About

This project was built as **Capstone Project 3** for the **AI Engineering Bootcamp at Purwadhika Digital Technology School**.

**Author**: Mohamad Alif Rahmadian  
**Bootcamp**: AI Engineering Bootcamp — Purwadhika  
**Topic**: NLP & LLMs Mastery: Advanced & Custom AI