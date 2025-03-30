
import requests
from fastapi import FastAPI
from app.models import Document, Query
from app.embeddings import embedding_model
from app.retrieval import vector_db
from loguru import logger
from fastapi.responses import FileResponse
import os
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# FastAPI instance with Swagger metadata
app = FastAPI(
    title="Minimal RAG System",
    description="A lightweight Retrieval-Augmented Generation (RAG) system using FAISS and Transformers.",
    version="1.0.0",
)

@app.get("/", tags=["General"], summary="Root Endpoint")
async def root():
    """Root endpoint to check if the system is running."""
    return {"message": "Welcome to the RAG System!"}

@app.post("/ingest", tags=["Document Ingestion"], summary="Ingest a document")
async def ingest_document(doc: Document):
    """
    Stores document embeddings in FAISS for retrieval.
    
    - **text**: The document content to be stored
    """
    embedding = embedding_model.generate_embedding(doc.text)
    vector_db.add_document(doc.text, embedding)
    logger.info("Document ingested successfully")
    return {"message": "Document ingested"}

@app.post("/query", tags=["Retrieval"], summary="Query the system")
async def query_system(query: Query):
    """
    Retrieves relevant documents and generates an AI-powered answer.
    
    - **question**: The query input from the user
    
    Returns an AI-generated answer based on retrieved context.
    """
    query_embedding = embedding_model.generate_embedding(query.question)
    retrieved_docs = vector_db.search(query_embedding, top_k=3)
    context = " ".join(retrieved_docs)
    answer = generate_answer(context, query.question)
    return {"answer": answer}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return {"status": "no favicon"}

# Load a small, lightweight model
MODEL_NAME = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def generate_answer(context: str, query: str) -> str:
    """
    Generates an answer using a locally loaded transformer model.
    
    - **context**: The retrieved documents forming the background knowledge
    - **query**: The user question
    
    Returns a generated answer.
    """
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=120, temperature=0.8)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)