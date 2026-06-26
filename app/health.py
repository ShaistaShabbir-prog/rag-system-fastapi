"""Issue #6: Health endpoint with ChromaDB connection check."""
from fastapi import APIRouter
import time

router = APIRouter()

@router.get("/health")
def health():
    checks = {}
    start = time.time()
    try:
        from app.chroma_store import collection_stats
        stats = collection_stats()
        checks["chromadb"] = {"status": "ok", "documents": stats["count"]}
    except Exception as e:
        checks["chromadb"] = {"status": "error", "message": str(e)[:100]}
    elapsed = round((time.time() - start) * 1000, 1)
    all_ok = all(v.get("status") == "ok" for v in checks.values())
    return {
        "status": "healthy" if all_ok else "degraded",
        "elapsed_ms": elapsed,
        "checks": checks,
        "version": "1.0.0",
    }
