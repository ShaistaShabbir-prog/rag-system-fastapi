"""Issue #7: Source citation in chat answers."""
from __future__ import annotations
from typing import Any


def answer_with_sources(
    question: str,
    session_id: str,
    collection,
    llm,
    history: list[dict] | None = None,
    n_sources: int = 4,
) -> dict[str, Any]:
    """
    Retrieve context chunks, generate answer, return both with citations.
    """
    history = history or []

    # Retrieve
    results = collection.query(query_texts=[question], n_results=n_sources)
    docs     = results["documents"][0]
    metas    = results["metadatas"][0]
    dists    = results["distances"][0]

    context = "\n\n".join(f"[{i+1}] {d}" for i, d in enumerate(docs))

    # Build prompt
    hist_txt = "".join(f"User: {h['q']}\nAssistant: {h['a']}\n" for h in history[-4:])
    prompt   = (f"{hist_txt}Context:\n{context}\n\n"
                f"Question: {question}\n"
                "Answer (cite sources as [1], [2] etc.):")

    try:
        resp   = llm.invoke(prompt)
        answer = resp.content if hasattr(resp, "content") else str(resp)
    except Exception as e:
        answer = f"LLM error: {e}"

    sources = [
        {"index": i+1, "text": d[:200], "metadata": m, "distance": round(s, 4)}
        for i, (d, m, s) in enumerate(zip(docs, metas, dists))
    ]

    return {"answer": answer, "sources": sources,
            "session_id": session_id, "sources_used": len(sources)}
