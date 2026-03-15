# RepoMind AI Backend

This repository contains a FastAPI backend for code repository analysis and LLM-based code question answering.


# workflow 

User enters GitHub repository
        ↓
Repository cloned
        ↓
Files scanned
        ↓
Tree-sitter parses code
        ↓
Dependency graph created
        ↓
Code chunks embedded
        ↓
FAISS vector index built
        ↓
User asks question
        ↓
Vector search + keyword search retrieve code
        ↓
Relevant code passed to LLM
        ↓
LLM generates explanation


## Setup

1. Create and activate Python virtual environment:
   ```bash
   cd /Users/jahanvi/Documents/repomind\ 2\ copy/backend
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env`:
   ```ini
   OPENAI_API_KEY=your_openai_key(optional )
   ANTHROPIC_API_KEY=your_anthropic_key9(optional)
   ```

4. Install Ollama (required for local LLM).
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull llama3.2
   ollama serve
   ```

## Run

Start the API server:
```bash
venv/bin/python -m uvicorn app.main:app --reload --port 8001
```

Open:
- `http://127.0.0.1:8001` (UI)
- `http://127.0.0.1:8001/docs` (Swagger)

## Endpoints

- `POST /analyze` (body: repo URL as raw JSON string)
- `POST /ask` (body: `{ "question": "..." }`)

## Notes

- Must call `/analyze` first.
- `/ask` uses a code search context and an LLM via `app/llm/llm_service.py`.
- If Ollama isn't running, the LLM call will fail.

## Detailed Architecture

### Flow diagram

```mermaid
flowchart TD
    A[Browser / Client] -->|POST /analyze| B[FastAPI /app/main.py]
    B --> C[clone_repository + scan_repository]
    C --> D[TreeSitterParser analyzer]
    D --> E[build_dependency_graph]
    E --> F[vector_search.build_index]
    F --> B
    B -->|returns analysis result| A

    A -->|POST /ask| B2[FastAPI /app/main.py ask_repo]
    B2 --> G[code_search.search]
    G --> H[collect context from top 5 files]
    H --> I[LLM call via ask_llm]
    I --> J[Ollama (local) or Anthropic/OpenAI]
    J --> I
    I --> B2
    B2 -->|answer + snippets| A
```

### Component details

- `app/main.py`
  - Main HTTP endpoints: `/`, `/analyze`, `/ask`.
  - `/analyze` does repo clone + scan + parser + graph + index.
  - `/ask` does code search and context assembly, then passes to LLM.

- `app/repo/cloner.py`
  - `clone_repository(repo_url)`: clones remotely stored repo, returns local path.

- `app/repo/scanner.py`
  - `scan_repository(path)`: finds supported files and returns file list.

- `app/parser/treesitter_parser.py`
  - Uses tree-sitter to parse code into AST, extract functions/classes/imports.

- `app/graph/dependency_graph.py`
  - Converts parser output into a directional dependency graph for the repository.

- `app/search/vector_search.py`
  - Builds vector index from repository text for semantic search.

- `app/search/code_search.py`
  - Simple keyword search over Python files + snippet extraction.

- `app/llm/llm_service.py`
  - `ask_llm(question, context)` uses a local Ollama model (Llama 3.2), fallback to remote provider if needed.

- `.env`
  - `OPENAI_API_KEY` (optional)
  - `ANTHROPIC_API_KEY` (optional)
  - `OLLAMA` is local and does not require API key; make sure `ollama serve` is running.

## Full operation sequence

1. Start Ollama server:
   - `ollama serve` (or `ollama serve --port 11435` if port conflict)

2. Start API app:
   - `venv/bin/python -m uvicorn app.main:app --reload --port 8001`

3. Browser UI:
   - `http://127.0.0.1:8001`
   - Enter repo URL and click Analyze.
   - Ask questions after analyze completes.

4. Internally `/ask` in app:
   - `code_search.search` finds a small result set with code snippets.
   - `ask_llm` creates a prompt (question + context).
   - Ollama returns AI generated answer.

5. Debugging tips:
   - If `readthedocs` cross-service path is not working, curl endpoints directly with Postman.
   - Monitor logs for parser errors and `tree_sitter` parse failures.
     
