from agents import classify_query, retrieve_context, draft_response
from ticket_store import init_db, log_ticket


def handle_query(query: str):
    """
    Full pipeline: classify -> retrieve -> draft -> decide escalation.
    """
    init_db()

    classification = classify_query(query)
    docs, sources = retrieve_context(query)
    result = draft_response(query, docs)

    confidence = result["confidence"]
    status = "auto_resolved" if confidence == "high" else "escalated"

    log_ticket(
        query=query,
        category=classification["category"],
        urgency=classification["urgency"],
        answer=result["answer"],
        confidence=confidence,
        status=status
    )

    return {
        "query": query,
        "classification": classification,
        "answer": result["answer"],
        "confidence": confidence,
        "status": status,
        "sources": sources
    }


if __name__ == "__main__":
    query = "How do I add JWT authentication to my FastAPI app?"
    result = handle_query(query)

    print("Status: " + result["status"])
    print("Confidence: " + result["confidence"])
    print("Answer: " + result["answer"])