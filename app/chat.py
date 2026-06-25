"""
Issue #3: Multi-turn /chat endpoint with session history.
"""
from __future__ import annotations
import time, logging
from collections import defaultdict
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()
log    = logging.getLogger(__name__)

# In-memory session store (expires after 30 min)
_sessions: dict[str, dict] = defaultdict(lambda: {"history": [], "last_access": 0.0})
SESSION_TTL = 1800  # 30 minutes


class ChatRequest(BaseModel):
    question:   str
    session_id: str = "default"


class ChatResponse(BaseModel):
    answer:     str
    session_id: str
    turn:       int


def _prune_expired():
    now = time.time()
    expired = [sid for sid, s in _sessions.items() if now - s["last_access"] > SESSION_TTL]
    for sid in expired:
        del _sessions[sid]


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Multi-turn RAG chat with persistent session history (30-min TTL)."""
    _prune_expired()
    session = _sessions[req.session_id]
    session["last_access"] = time.time()
    history = session["history"]

    try:
        from .chroma_store import query as chroma_query
        docs = chroma_query(req.question, n=4)
        context = "\n\n".join(d["text"] for d in docs)
    except Exception:
        context = ""

    # Build prompt with history
    history_text = ""
    for turn in history[-6:]:  # last 3 exchanges
        history_text += f"User: {turn['q']}\nAssistant: {turn['a']}\n"

    prompt = (f"{history_text}Context:\n{context}\n\nQuestion: {req.question}\nAnswer:"
              if context else f"{history_text}Question: {req.question}\nAnswer:")

    try:
        from .llm import get_llm
        answer = get_llm().invoke(prompt)
        answer = answer.content if hasattr(answer, "content") else str(answer)
    except Exception as e:
        answer = f"LLM unavailable: {e}"

    history.append({"q": req.question, "a": answer})
    turn_num = len(history)
    return ChatResponse(answer=answer, session_id=req.session_id, turn=turn_num)


@router.delete("/chat/{session_id}")
def clear_session(session_id: str):
    _sessions.pop(session_id, None)
    return {"cleared": session_id}


@router.get("/chat/{session_id}/history")
def get_history(session_id: str):
    return {"session_id": session_id, "history": _sessions[session_id]["history"]}
