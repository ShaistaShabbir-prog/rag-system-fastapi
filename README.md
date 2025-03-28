# Simplified RAG-Based Document Retrieval and Question Answering System

This repository contains a **Retrieval-Augmented Generation (RAG)**-based system that integrates **document retrieval** and **question answering** using **FastAPI**, **FAISS**, and **SentenceTransformers** for document embeddings. The system allows users to ingest documents, store them as embeddings, and retrieve relevant documents to generate context-aware answers.

---

## Features
- **Document Embedding**: Uses a pre-trained embedding model (e.g., `SentenceTransformers`) to convert text documents into dense vector representations.
- **Document Retrieval**: Implements a similarity search mechanism with **FAISS** for fast retrieval of relevant documents.
- **Question Answering**: Uses a Large Language Model (LLM) to generate answers based on the retrieved documents.
- **API Endpoints**:
  - `/ingest`: Ingest documents and store their embeddings.
  - `/query`: Accept a query, retrieve relevant documents, and generate a response.
- **Containerized Deployment**: The application is containerized using Docker and Docker Compose for easy deployment.

---

## Setup and Installation

Follow these instructions to set up the project locally.

### Prerequisites
- Docker and Docker Compose installed on your machine.
- Basic knowledge of how Docker works.
  
### Steps to Run the Application

1. **Clone the repository:**
    ```bash
    git clone https://github.com/ShaistaShabbir-prog/rag-system-fastapi.git
    cd rag-document-retrieval
    ```

2. **Build the Docker image:**
    In the project directory (where the `Dockerfile` is located), run:
    ```bash
    docker-compose build
    ```

3. **Start the services using Docker Compose:**
    This will start the FastAPI app container.
    ```bash
    docker-compose up
    ```

4. **Test the API:**
    After the containers are running, open a web browser or use **Postman**/**cURL** to interact with the following endpoints:
    - **POST /ingest**: To ingest documents. Example:
      ```json
      POST http://localhost:8000/ingest
      Body:
      {
        "document": "This is a sample document."
      }
      ```
    - **POST /query**: To submit a query. Example:
      ```json
      POST http://localhost:8000/query
      Body:
      {
        "query": "What is this document about?"
      }
      ```

---

## How It Works

### 1. Document Ingestion (`/ingest` Endpoint)
- Users submit text documents via the `/ingest` endpoint.
- The document text is converted into an embedding using a pre-trained model (e.g., `SentenceTransformers`).
- The embeddings are stored in **FAISS**, a fast vector search library.

### 2. Query Processing (`/query` Endpoint)
- When a user submits a query, the query is also embedded into a vector using the same embedding model.
- **FAISS** is used to search for the top N most similar documents to the query.
- The retrieved documents are provided as context to a **Large Language Model** (LLM), which generates a relevant answer based on the context.

---

## Development

### Dependencies

- **FastAPI**: The web framework to create the API.
- **Uvicorn**: ASGI server to run FastAPI.
- **SentenceTransformers**: To generate embeddings from documents and queries.
- **FAISS**: For similarity search and storing embeddings.
- **OpenAI**: (Optional) To generate answers using a language model (if used).
  
You can install the dependencies manually using:

```bash
pip install -r requirements.txt
