# Minimal RAG System

This project is a **Minimal Retrieval-Augmented Generation (RAG) System** built with FastAPI, FAISS, and a lightweight NLP model. The system enables document ingestion and querying to retrieve relevant documents and generate answers using a Transformer model.

## Features
- **Document Ingestion**: Store text documents and their embeddings in FAISS.
- **Querying**: Retrieve relevant documents and generate answers.
- **FastAPI with Swagger UI**: Easily test APIs with an interactive UI.
- **Dockerized Deployment**: Run the entire system in a containerized environment.

## Installation & Running

### Using Docker (Recommended)

1. **Pull the Docker Image:**
   ```bash
   docker pull shaistashabbir/rag
   ```

2. **Run the Container:**
   ```bash
   docker run -p 8000:8000 shaistashabbir/rag
   ```

3. **Access the Swagger UI:**
   Open your browser and visit:
   ```
   http://localhost:8000/docs
   ```

## API Endpoints

### 1. Root Endpoint
- **`GET /`**
- Returns a welcome message.

### 2. Ingest Document
- **`POST /ingest`**
- **Request Body:** `{ "text": "your document text" }`
- **Response:** `{ "message": "Document ingested" }`

### 3. Query System
- **`POST /query`**
- **Request Body:** `{ "question": "your question" }`
- **Response:** `{ "answer": "generated answer" }`

## Development Setup (Without Docker)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ShaistaShabbir-prog/rag-system-fastapi.git
   cd RAG_Shabbir
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Notes
- Ensure `docker` is installed for containerized execution.
- The system uses **FAISS** for fast document retrieval.
- The model used is **Flan-T5 Small** for text generation.

Enjoy using the **Minimal RAG System**! 🚀

