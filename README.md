# ai-act-tutor

An interactive Streamlit-based educational tool to study and explore the European Union AI Act (Regulation 2024/1689) using Retrieval-Augmented Generation (RAG), quizzes, and guided modules.

## Goals
- Top-tier RAG pipeline (LangChain v0.2+, LangSmith)
- Modular, extensible codebase
- Streamlit frontend: chat, study, quiz
- ChromaDB/FAISS for local vectorstore
- Secure, token-efficient, and citation-friendly

## Directory Structure
```
app/
  main.py         # Streamlit entry point
  chat.py         # Chat interface (RAG)
  study.py        # Guided study modules
  quiz.py         # Quiz interface
core/
  loader.py       # Document loader & chunker
  rag_chain.py    # RAG chain builder
  quiz_generator.py # MCQ generation (future)
data/             # Raw source documents
vectorstore/      # Chroma/FAISS index
langsmith/        # LangSmith config
requirements.txt  # Dependencies
```

## Setup
1. `pip install -r requirements.txt`
2. Add your OpenAI API key to a `.env` file: `OPENAI_API_KEY=sk-...`
3. Place the EU AI Act PDF/HTML in `data/`
4. Run: `streamlit run app/main.py`

## Security & Performance
- Uses environment variables for API keys
- Optimized for token usage and context length
- Logging and exception handling for ingestion/retrieval

## Audience
AI practitioners, lawyers, and policy students studying the EU AI Act.

---
*Work in progress. See TODOs in code for next steps.* 