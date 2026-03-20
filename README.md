# PostGen AI — The Viral LinkedIn Content Engine

> **RAG-powered content generation** that analyzes real viral LinkedIn posts and crafts high-performing originals — instantly.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-orange?logo=google)](https://ai.google.dev)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-red)](https://qdrant.tech)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-ff4b4b?logo=streamlit)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://docker.com)

---

## 🎯 What Is PostGen AI?

PostGen AI is a production-grade **Retrieval-Augmented Generation (RAG)** system built specifically for LinkedIn content creators, growth marketers, and personal brand builders.

Instead of hallucinating "viral" styles, PostGen AI:
1. **Retrieves** semantically similar posts from a curated database of real, high-performing LinkedIn content
2. **Filters** results by tone, industry, and metadata for hyper-targeted generation
3. **Generates** a fully original post using **Gemini 2.5 Flash**, trained on those viral patterns
4. **Learns** from the performance of generated posts over time via an analytics feedback loop

---

## ✨ Core Features

| Feature | Description |
|---|---|
| 🔀 **Hybrid Search** | Combines Dense Vector Search (semantic) + Sparse BM25 (keyword) for precision retrieval |
| 🎯 **Cross-Encoder Reranking** | A dedicated reranker model scores retrieved posts for relevance before generation |
| 🏷️ **Metadata Filtering** | Filter by **Tone** (Storytelling, Controversial, Professional) and **Industry** |
| 🧠 **Few-Shot RAG Generation** | Gemini 2.5 Flash mimics structure & energy of top-performing posts |
| 📊 **Analytics Feedback Loop** | Post performance data (reactions, comments) flows back into Qdrant to keep the knowledge base fresh |
| 🖥️ **Dual Interface** | Rich Streamlit Web UI + CLI for automation workflows |
| 🐳 **Docker-Ready** | Qdrant runs as a containerized service out of the box |

---

## 🏗️ Architecture

```
User Input (Topic + Filters)
        │
        ▼
┌─────────────────────────┐
│   Hybrid Retrieval       │  Dense (all-MiniLM-L6-v2) + Sparse (BM25)
│   Qdrant Vector DB       │  Metadata filter: Tone / Industry
└────────────┬────────────┘
             │  Top-K Candidates
             ▼
┌─────────────────────────┐
│  Cross-Encoder Reranker  │  Scores & re-orders candidates for max relevance
└────────────┬────────────┘
             │  Top-3 Viral Examples
             ▼
┌─────────────────────────┐
│  Gemini 2.5 Flash (Gen)  │  Few-Shot Prompted: Initial Draft
└────────────┬────────────┘
             │  Draft
             ▼
┌─────────────────────────┐
│   Critic Agent (SME)    │  Scores & Critiques Hook, Format, CTA
└────────────┬────────────┘
             │  Feedback
             ▼
┌─────────────────────────┐
│  Refinement Agent (AI)   │  Applies critique to craft final post
└────────────┬────────────┘
             │  Refined Post
             ▼
      📋 Ready to Publish
             │
             ▼
┌─────────────────────────┐
│   Analytics Feedback     │  Post reactions/comments re-ingested into Qdrant
│   Loop                   │  Vector DB stays current with trending content
└─────────────────────────┘
```

---

## 🗂️ Project Structure

```
PostGen_AI_demo/
├── data/
│   └── viral_posts.csv         # Curated high-engagement LinkedIn dataset
├── src/
│   ├── agents/
│   │   └── critic.py           # Critic Agent for post evaluation
│   ├── ingestion/
│   │   └── ingest.py           # Data cleaning, embedding, & Qdrant upload pipeline
│   ├── retrieval/
│   │   └── search.py           # Hybrid search + cross-encoder reranking
│   ├── generation/
│   │   └── generation.py       # Gemini 2.5 Flash prompt engineering & generation
│   ├── app.py                  # Streamlit Web UI
│   └── main.py                 # CLI entry point
├── config/                     # Configuration & prompt templates
├── docker-compose.yml          # Qdrant container setup
├── requirements.txt
└── .env                        # API keys (not committed)
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Docker Desktop
- A [Google AI Studio](https://aistudio.google.com) API key

### 1. Clone & Install
```bash
git clone https://github.com/your-username/PostGen_AI_demo.git
cd PostGen_AI_demo
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Create a .env file in the project root
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Start the Vector Database
```bash
docker-compose up -d
```

### 4. Ingest Viral Posts Dataset
```bash
python src/ingestion/ingest.py
```

### 5. Launch the App

**Web UI (Recommended):**
```bash
streamlit run src/app.py
```

**CLI Mode:**
```bash
python src/main.py
```

---

## 🧩 How the RAG Pipeline Works

### Step 1 — Hybrid Retrieval
The user's topic is encoded into a 384-dimensional vector using `all-MiniLM-L6-v2`. Qdrant performs a **hybrid search** — combining semantic similarity (dense vectors) with keyword relevance (BM25 sparse index) — against the viral posts dataset. Metadata filters narrow results by **Tone** or **Industry** if specified.

### Step 2 — Cross-Encoder Reranking
The initial top-K candidates are passed through a **Cross-Encoder model** that jointly encodes query + document pairs to produce fine-grained relevance scores. Only the top 3 posts make it into the generation context.

### Step 3 — Multi-Agent Multi-Cycle Generation
The system executes a **Generate-Critique-Refine** loop:
1. **Generator Agent**: Creates an initial draft using few-shot retrieval examples.
2. **Critic Agent**: Reviews the draft against viral standards (Hook, Format, CTA, Authenticity) and outputs scores + actionable feedback.
3. **Refinement Agent**: Consumes the initial draft + criticism and crafts the final polished output automatically.

### Step 4 — Analytics Feedback Loop
After a post is published and performance data is collected, the engagement metrics (reactions, comments, reposts) are written back into Qdrant. This keeps the knowledge base biased toward content that is **performing well right now**, not just historically.

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Google Gemini 2.5 Flash |
| **Vector DB** | Qdrant (local Docker) |
| **Embeddings** | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| **Reranker** | Cross-Encoder (`ms-marco-MiniLM`) |
| **Backend** | Python with FastAPI-ready structure |
| **Frontend** | Streamlit |
| **Data** | Pandas, viral LinkedIn CSV dataset |
| **Infra** | Docker Compose |

---

## 🔮 Roadmap

- [ ] REST API layer (FastAPI) for third-party integrations
- [ ] LinkedIn OAuth integration for one-click publish
- [x] Multi-Agent evaluation loop (Critic → Rewriter → Publisher)
- [ ] Tone and Industry auto-detection from user input
- [ ] Engagement prediction score before publishing

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with ❤️ using <strong>Gemini 2.5 Flash</strong>, <strong>Qdrant</strong>, and <strong>Sentence Transformers</strong>
</p>
