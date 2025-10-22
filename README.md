
# 🎬 MovieRAG — Getting Started (External Users)

This guide explains **exactly** how to run the MovieRAG project on a fresh machine — no prior context required.

> TL;DR  
> 1) Install Python 3.10–3.12  
> 2) `python -m venv .venv && source .venv/bin/activate`  
> 3) `pip install -r requirements.txt`  
> 4) Create `.env` with your `OPENAI_API_KEY`  
> 5) Put your `movies.csv` in `data/`  
> 6) Run CLI: `python main.py` **or** Web UI: `streamlit run chatbot_view.py`

---
<img width="877" height="785" alt="Screenshot 2025-10-23 at 00 49 56" src="https://github.com/user-attachments/assets/2dd9f883-d7d6-4491-9fcd-54abdd2531a4" />

## 1) What is MovieRAG?

MovieRAG is a **RAG (Retrieval-Augmented Generation)** chatbot that recommends movies from a local CSV file.  
It indexes your CSV into a **Chroma** vector database using a **HuggingFace embedding model**, and uses an LLM (OpenAI) via **LangChain + LangGraph** for tool-using retrieval.

- **Data source:** `data/movies.csv`
- **Vector DB:** `vector_db/` (auto-created; persisted Chroma index)
- **Embedding:** `sentence-transformers/all-MiniLM-L6-v2` (fast) — configurable
- **LLM provider:** OpenAI via `langchain-openai` (configure your API key)
- **Agent:** LangGraph ReAct agent with a single tool: `retrieve_movie_context`

---

## 2) Project Layout

```
movieRecommendation/
│
├── app/
│   ├── __init__.py
│   ├── config.py           # absolute paths, model & embedding, env
│   ├── vector_store.py     # CSV -> document -> Chroma (persist) -> retriever
│   ├── tools.py            # retrieve_movie_context (uses retriever)
│   ├── create_agent.py     # LangGraph ReAct agent
│   └── run_chat.py         # CLI chat loop (used by main.py)
│
├── data/
│   └── movies.csv          # your dataset (REQUIRED)
│
├── vector_db/              # persisted Chroma index (auto-created)
│
├── main.py                 # CLI entrypoint
├── chatbot_view.py         # Web UI (recommended)
└── requirements.txt
```

> All internal imports inside `app/` are **relative** (e.g., `from .config import model`).  
> Top-level scripts (`main.py`, `chatbot_view.py`) import **absolutely** (e.g., `from app.create_agent import create_agent`).

---

## 3) Requirements & Installation

### A) Python & Virtualenv

- Install **Python 3.10–3.12**
- Create & activate a virtualenv:

**macOS / Linux**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### B) Install dependencies

```
pip install -r requirements.txt
```

> If PyTorch installation fails on Apple Silicon or CPU-only machines, try:
> ```bash
> pip install torch --index-url https://download.pytorch.org/whl/cpu
> ```

---

## 4) Configure your OpenAI API key

Create a **.env** file at the project root:

```
OPENAI_API_KEY=sk-your_key_here
```

The app automatically loads this via `python-dotenv` in `app/config.py`.

---

## 5) Provide your data (movies.csv)

Place your CSV at: `data/movies.csv`

**Expected columns** (adjust `app/vector_store.py:createFilmDocument` if you need to rename fields):
```
title, genre, director, actors_1, actors_2, description,
year, duration, country, language, writer,
desc35, avg_imdb, budget, worldwide_gross_income
```

> Each row = one movie. The script concatenates fields into a single textual document for embedding.

---

## 6) Run the app

### Option A — CLI (terminal chat)

From the project root:
```bash
python main.py
```
- Type your question, **type `çıkış`** to exit.
- The first run will build the Chroma index in `vector_db/`.

### Option B — Web UI (Streamlit)

From the project root:
```bash
streamlit run chatbot_view.py
```
- Opens in your browser (usually http://localhost:8501)
- **Enter** sends message; **Shift+Enter** adds newline
- Uses the same backend agent and retriever

> In PyCharm: Run/Debug → “Module name” = `streamlit`, Parameters = `run chatbot_view.py`, Working directory = project root.

---

## 7) How it works

1. **vector_store.py**
   - Reads `data/movies.csv`
   - Builds a formatted text per movie (`createFilmDocument`)
   - Embeds texts using HuggingFace (`sentence-transformers/all-MiniLM-L6-v2` by default)
   - Persists vectors into Chroma at `vector_db/` (auto-created)
   - Exposes `retriever = vectorstore.as_retriever()`

2. **tools.py**
   - Defines `retrieve_movie_context(query)` — a LangChain tool that calls the retriever

3. **create_agent.py**
   - Builds a LangGraph **ReAct** agent with the tool
   - System prompt enforces “use the tool; do not hallucinate; answer in Turkish”

4. **main.py / chatbot_view.py**
   - Provide **CLI** or **Web** UI frontends streaming responses

---

## 8) Configuration (tuning)

Open `app/config.py` to change:
- **Embedding model** (speed vs. quality)
  - Fast: `sentence-transformers/all-MiniLM-L6-v2`
  - Multilingual: `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`
- **LLM model** (OpenAI; e.g., `gpt-3.5-turbo`)
- **Paths** (already absolute and robust)

After changing embedding model or the dataset, you may want to **rebuild Chroma**:
```bash
rm -rf vector_db
python main.py
```

---

## 9) Troubleshooting

- **FileNotFoundError: ../data/movies.csv**  
  You moved files into `app/` or changed the working directory. This project uses **absolute paths** in `config.py`. Ensure your CSV exists at `data/movies.csv` (project root).

- **attempted relative import with no known parent package**  
  Don’t run modules inside `app/` directly with `python app/xxx.py`.  
  Use top-level scripts (e.g., `python main.py`), or use module mode: `python -m app.chatbot_view` (if you keep the NiceGUI example).

- **ModuleNotFoundError: app**  
  Run from the **project root**. In PyCharm, set Working directory to the project root.

- **Model suggests films not in CSV**  
  Tighten the system prompt and/or post-filter results against CSV titles. The default system prompt already instructs the agent not to go beyond retrieved context.

- **Torch installation issues**  
  Install the CPU wheel:  
  `pip install torch --index-url https://download.pytorch.org/whl/cpu`

---

## 10) FAQ

**Q: Can I use a different UI (Gradio, NiceGUI)?**  
A: Yes. Streamlit is included by default. NiceGUI and Gradio are optional; see `requirements.txt` comments.

**Q: How to add more tools (e.g., filter by IMDb score)?**  
A: Add a new function tool in `app/tools.py` and include it when creating the agent in `app/create_agent.py`.

**Q: How to switch to another LLM (Azure, etc.)?**  
A: Replace `langchain-openai` config in `app/config.py` and provide the corresponding API keys.

---

## 11) Minimal Commands Recap

```bash
# create & enter venv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1

# install deps
pip install -r requirements.txt

# set key
echo "OPENAI_API_KEY=sk-your_key" > .env

# put your CSV
# ./data/movies.csv

# run CLI OR Web UI
python main.py
# OR
streamlit run chatbot_view.py
```

Happy hacking! 🎬
