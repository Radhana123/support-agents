import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)


def get_knowledge_base_collection(db_path="chroma_db"):
    client = chromadb.PersistentClient(path=db_path)
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return client.get_or_create_collection(
        name="support_docs",
        embedding_function=embedding_fn
    )


def classify_query(query: str):
    """
    Classify the query into category and urgency.
    """
    prompt = (
        "Classify this customer support query.\n"
        "Query: " + query + "\n\n"
        "Respond in this exact format:\n"
        "Category: <technical/billing/general>\n"
        "Urgency: <low/medium/high>"
    )
    response = llm.invoke(prompt)
    text = response.content

    category = "general"
    urgency = "low"

    for line in text.split("\n"):
        if line.lower().startswith("category:"):
            category = line.split(":")[1].strip().lower()
        if line.lower().startswith("urgency:"):
            urgency = line.split(":")[1].strip().lower()

    return {"category": category, "urgency": urgency}


def retrieve_context(query: str, n_results: int = 3):
    """
    Retrieve relevant chunks from knowledge base.
    """
    collection = get_knowledge_base_collection()
    results = collection.query(query_texts=[query], n_results=n_results)
    docs = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]
    return docs, sources


def draft_response(query: str, context_docs: list):
    """
    Generate a response using retrieved context, with a confidence estimate.
    """
    context_text = "\n\n".join(context_docs)

    prompt = (
        "You are a helpful customer support assistant. Answer the user's question "
        "using ONLY the context below. If the context doesn't contain the answer, "
        "say you're not sure and that this will be escalated to a human.\n\n"
        "Context:\n" + context_text + "\n\n"
        "Question: " + query + "\n\n"
        "At the end of your answer, on a new line, write:\n"
        "CONFIDENCE: <high/medium/low>"
    )

    response = llm.invoke(prompt)
    text = response.content

    confidence = "medium"
    answer = text

    if "CONFIDENCE:" in text:
        parts = text.split("CONFIDENCE:")
        answer = parts[0].strip()
        confidence = parts[1].strip().lower()

    return {"answer": answer, "confidence": confidence}


if __name__ == "__main__":
    query = "How do I handle a 404 error in FastAPI?"

    print("Query: " + query)

    classification = classify_query(query)
    print("\nClassification: " + str(classification))

    docs, sources = retrieve_context(query)
    print("\nRetrieved " + str(len(docs)) + " context chunks")

    result = draft_response(query, docs)
    print("\nAnswer: " + result["answer"])
    print("\nConfidence: " + result["confidence"])