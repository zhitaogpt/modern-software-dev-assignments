# Action Item Extractor

A minimal FastAPI application that uses both rule-based heuristics and Large Language Models (Ollama) to extract action items from free-form notes.

## Features

- **Rule-based Extraction**: Fast, deterministic extraction using regex and keyword matching.
- **LLM-powered Extraction**: Semantic extraction using Ollama (Llama 3.1) to understand natural language requests.
- **Note Management**: Save and list historical notes.
- **Action Item Tracking**: Mark extracted tasks as done.
- **Modern API**: Built with FastAPI and Pydantic for robust type validation and automatic documentation.

## Setup & Running

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/)
- [Ollama](https://ollama.com/) with `llama3.1:8b` model pulled (`ollama pull llama3.1:8b`)

### Installation

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Start the FastAPI server:
   ```bash
   poetry run uvicorn week2.app.main:app --reload
   ```

3. Open your browser at `http://127.0.0.1:8000`.

## API Endpoints

- `GET /`: Serves the frontend.
- `POST /notes`: Create a new note.
- `GET /notes`: List all saved notes.
- `POST /action-items/extract`: Extract items using regex rules.
- `POST /action-items/extract-llm`: Extract items using the LLM.
- `GET /action-items`: List all action items.
- `POST /action-items/{id}/done`: Mark a specific item as done/undone.

## Testing

The project uses `pytest` for testing, covering both traditional logic and LLM outputs.

Run tests:
```bash
poetry run pytest week2/tests/test_extract.py
```

*Note: LLM tests require Ollama to be running locally.*
