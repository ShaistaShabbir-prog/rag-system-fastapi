from pydantic import BaseModel

class Document(BaseModel):
    """Model for document ingestion."""
    text: str

class Query(BaseModel):
    """Model for user queries."""
    question: str
