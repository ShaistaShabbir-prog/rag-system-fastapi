"""Issue #7: Source-grounded answers with document citations."""
from __future__ import annotations
import logging
from typing import Any

log = logging.getLogger(__name__)


def answer_with_sources(question: str, collection=None,
                        llm=None, n: int = 4) -> dict[str, Any]:
    """
    Retrieve relevant chunks and generate a grounded answer.
    Returns answer + source citations for transparency.
    """
    # Retrieve
    sources = []
    context = ""
    if collection:
        try:
            results = collection.query(query_texts=[question], n_results=n)
            docs   = results["documents"][0]
            metas  = results["metadatas"][0]
            dists  = results["distances"][0]
            sources = [
                {"text": d[:300], "metadata": m,
                 "distance": round(float(s), 4),
                 "relevance": round(1 - min(float(s), 1), 3)}
                for d, m, s in zip(docs, metas, dists)
            ]
            context = "\n\n".join(
                f"[Source {i+1}]: {d}"
                for i, d in enumerate(docs)
            )
        except Exception as e:
            log.warning("Retrieval failed: %s", e)

    # Generate
    if llm and context:
        prompt = (
            f"Answer based ONLY on these sources:\n{context}\n\n"
            f"Question: {question}\n"
            f"Answer (cite source numbers like [Source 1]):"
        )
        try:
            answer = llm.invoke(prompt)
            answer = answer.content if hasattr(answer, "content") else str(answer)
        except Exception as e:
            answer = f"LLM unavailable: {e}"
    elif context:
        answer = f"Based on retrieved documents: {context[:400]}..."
    else:
        answer = "No relevant documents found. Please upload documents first."

    return {
        "answer": answer,
        "sources": sources,
        "context_used": bool(context),
        "source_count": len(sources),
    }
