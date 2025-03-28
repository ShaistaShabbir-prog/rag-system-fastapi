from fastapi import FastAPI
from app.models import Document, Query
from app.embeddings import embedding_model
from app.retrieval import vector_db
from app.generator import generate_answer
from loguru import logger
from fastapi.responses import FileResponse
import os

# Only one app instance is needed
app = FastAPI(title="Minimal RAG System")


@app.get("/")
async def root():
    return {"message": "Welcome to the RAG System!"}


@app.post("/ingest")
async def ingest_document(doc: Document):
    """Stores document embeddings in FAISS."""
    embedding = embedding_model.generate_embedding(doc.text)
    vector_db.add_document(doc.text, embedding)
    logger.info("Document ingested successfully")
    return {"message": "Document ingested"}


@app.post("/query")
async def query_system(query: Query):
    """Retrieves relevant documents and generates an answer."""
    query_embedding = embedding_model.generate_embedding(query.question)
    retrieved_docs = vector_db.search(query_embedding, top_k=3)
    context = " ".join(retrieved_docs)
    answer = generate_answer(context, query.question)
    return {"answer": answer}


@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join("path/to/favicon.ico"))
