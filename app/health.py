"""Issue #6: Health endpoint with ChromaDB status check."""
from fastapi import APIRouter
import time

router = APIRouter()

@router.get("/health")
def health():
    checks = {}
    # ChromaDB
    try:
        from app.chroma_store import collection_stats
        stats = collection_stats()
        checks["chromadb"] = {"status": "ok", "documents": stats["count"]}
    except Exception as e:
        checks["chromadb"] = {"status": "degraded", "error": str(e)}

    # LLM connectivity (cheap check)
    checks["llm"] = {"status": "configured" if _has_llm() else "not_configured"}

    overall = "ok" if all(v.get("status") in ("ok","configured","not_configured")
                          for v in checks.values()) else "degraded"
    return {"status": overall, "checks": checks, "timestamp": time.time()}

def _has_llm() -> bool:
    import os
    return bool(os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY"))
