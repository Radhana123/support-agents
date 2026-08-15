import os
import requests
from bs4 import BeautifulSoup
import chromadb
from chromadb.utils import embedding_functions


DOCS_URLS = [
    "https://fastapi.tiangolo.com/tutorial/first-steps/",
    "https://fastapi.tiangolo.com/tutorial/path-params/",
    "https://fastapi.tiangolo.com/tutorial/query-params/",
    "https://fastapi.tiangolo.com/tutorial/body/",
    "https://fastapi.tiangolo.com/tutorial/response-model/",
    "https://fastapi.tiangolo.com/tutorial/handling-errors/",
    "https://fastapi.tiangolo.com/tutorial/security/",
    "https://fastapi.tiangolo.com/deployment/",
]


def scrape_docs(urls):
    """
    Scrape text content from documentation pages.
    """
    documents = []
    for url in urls:
        try:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")

            main_content = soup.find("article") or soup.find("main") or soup.body
            text = main_content.get_text(separator=" ", strip=True)

            documents.append({"url": url, "text": text})
            print("Scraped: " + url + " (" + str(len(text)) + " chars)")
        except Exception as e:
            print("Failed to scrape " + url + ": " + str(e))

    return documents


def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split text into overlapping chunks.
    """
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def build_knowledge_base(documents, db_path="chroma_db"):
    """
    Build ChromaDB collection from scraped documents.
    """
    client = chromadb.PersistentClient(path=db_path)

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name="support_docs",
        embedding_function=embedding_fn
    )

    doc_id = 0
    for doc in documents:
        chunks = chunk_text(doc["text"])
        for chunk in chunks:
            collection.add(
                documents=[chunk],
                metadatas=[{"source": doc["url"]}],
                ids=["doc_" + str(doc_id)]
            )
            doc_id += 1

    print("\nKnowledge base built with " + str(doc_id) + " chunks")
    return collection


if __name__ == "__main__":
    print("Scraping documentation...")
    docs = scrape_docs(DOCS_URLS)

    print("\nBuilding knowledge base...")
    collection = build_knowledge_base(docs)

    print("\nTesting retrieval...")
    results = collection.query(query_texts=["How do I handle errors in FastAPI?"], n_results=3)

    for i, doc in enumerate(results["documents"][0]):
        print("\nResult " + str(i + 1) + ":")
        print(doc[:200] + "...")