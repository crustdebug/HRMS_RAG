# HRMS RAG

A **HR Management System chatbot** powered by **Retrieval-Augmented Generation (RAG)**. Ask HR-related questions in natural language and get answers grounded in your company's HR data.

Built with **FastAPI**, **LangChain**, **FAISS**, and **Google Gemini** (free tier).

---

## Features

- **RAG pipeline** — retrieves relevant HR context from a FAISS vector store before generating an answer
- **Gemini free-tier LLM** with automatic model fallback (flash-lite → flash → pro)
- **FastAPI** backend with an HTML/JS frontend
- **Docker support** for containerized deployment
- Environment-variable based API key management

---

## Project Structure

```
Simple_HRMS_RAG/
├── app/                    # Core application logic (routes, RAG chain, etc.)
├── data/                   # Source HR documents / knowledge base
├── static/                 # Frontend HTML, CSS, JS assets
├── backups/                # Backup files
├── database.JSON           # Structured HR data store
├── check_embeddings.py     # Utility to inspect FAISS embeddings
├── remove_space_textkey.py # Data-cleaning helper
├── setup_fix.py            # Setup / repair utility
├── test_chatbot.py         # Chatbot test script
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container definition
├── .env .example           # Environment variable template
├── MODEL_INFO.md           # Gemini model & rate-limit details
└── EXAONE_hardware_requirements.md  # Hardware notes for EXAONE models
```

---

## How It Works

1. HR documents are chunked, embedded with `sentence-transformers`, and indexed in a **FAISS** vector store.
2. On each user query, the most relevant chunks are retrieved from FAISS.
3. The retrieved context + the user's question are passed to **Google Gemini** to generate a grounded answer.
4. The FastAPI server exposes the chatbot as a REST API, served alongside an HTML frontend.

---

## LLM — Google Gemini (Free Tier)

The system uses a **three-model fallback chain** so it stays within free-tier rate limits:

| Priority | Model | RPM | RPD |
|----------|-------|-----|-----|
| 1st | `gemini-2.5-flash-lite` | 15 | 1,000 |
| 2nd | `gemini-2.5-flash` | 10 | 250 |
| 3rd | `gemini-2.5-pro` | 2 | 50–100 |

If a model is rate-limited or errors, the next one is tried automatically. An error is only returned if all three fail.

> See [`MODEL_INFO.md`](MODEL_INFO.md) for full details.

---

## Getting Started

### Prerequisites

- Python 3.10+
- A [Google AI Studio](https://aistudio.google.com/) API key (free)

### 1. Clone the repository

```bash
git clone https://github.com/crustdebug/Simple_HRMS_RAG.git
cd Simple_HRMS_RAG
```

### 2. Set up environment variables

```bash
cp ".env .example" .env
```

Edit `.env` and add your Google Gemini API key:

```
GOOGLE_API_KEY=your_api_key_here
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
uvicorn app.main:app --reload
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

---

## Docker

```bash
docker build -t hrms-rag .
docker run -p 8000:8000 --env-file .env hrms-rag
```

---

## Utility Scripts

| Script | Purpose |
|--------|---------|
| `check_embeddings.py` | Inspect the contents of the FAISS vector store |
| `remove_space_textkey.py` | Clean whitespace issues in the data keys |
| `setup_fix.py` | Fix common setup/configuration issues |
| `test_chatbot.py` | Run test queries against the chatbot |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, Uvicorn |
| LLM | Google Gemini (via `langchain-google-genai`) |
| Embeddings | `sentence-transformers` (HuggingFace) |
| Vector Store | FAISS (`faiss-cpu`) |
| RAG Framework | LangChain 0.3 |
| Frontend | HTML / CSS / JS |
| Containerization | Docker |

---

## License

This project is open source. Feel free to fork, extend, and adapt it for your own HR use cases.
