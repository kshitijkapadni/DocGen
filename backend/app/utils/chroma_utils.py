# backend/utils/chroma_utils.py

from chromadb import Client
from chromadb.config import Settings

chroma_client = Client(Settings(
    persist_directory="./chroma_data"
))

def add_to_vectorstore(content, metadata):
    collection = chroma_client.get_or_create_collection("docgen-mvp")
    if metadata.get("file_path") == "":
        metadata["file_path"] = f"{metadata.get("id")}"
        metadata["function_name"] = "User Added Information"
    collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[f"{metadata['file_path']}-{metadata.get('function_name', 'general')}"]
    )

def fetch_all_docs():
    collection = chroma_client.get_or_create_collection("docgen-mvp")
    results = collection.get()
    documents = results.get("documents", [])
    return documents

def search_context(query: str):
    collection = chroma_client.get_or_create_collection("docgen-mvp")
    results = collection.query(query_texts=[query], n_results=3)

    # Extract documents and metadata
    docs = results['documents'][0]
    metadatas = results['metadatas'][0] if 'metadatas' in results else [{} for _ in docs]

    # Format context and references
    context_blocks = []
    references = []

    for doc, meta in zip(docs, metadatas):
        context_blocks.append(doc)
        ref = f"- Source: {meta.get('file_path', 'Unknown')}"
        if 'function_name' in meta:
            ref += f", Function: {meta['function_name']}"
        references.append(ref)
    full_context = ""
    for content, reference in zip(context_blocks, references):
        full_context+= f"\nReference: {reference}\nContext Block : {content}\n"

    return full_context
