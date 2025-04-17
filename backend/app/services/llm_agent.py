import requests
import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from config import OLLAMA_MODEL, OLLAMA_BASE_URL
from app.utils.chroma_utils import search_context

OLLAMA_BASE_URL = "http://localhost:11434"


def query_ollama(prompt: str) -> str:
    response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })
    return response.json()['response']

def answer_question(user_query: str) -> str:
    context = search_context(user_query)

    final_prompt = f"""You are an expert documentation assistant. Provide citations for your answers based on given references.

{context}

User Question:
{user_query}

Answer:"""

    response = query_ollama(final_prompt)

    return response
