# backend/agents/vector_writer.py

from crewai import Agent
from utils.chroma_utils import add_to_vectorstore

class VectorWriterAgent(Agent):
    def __init__(self, repo_path):
        super().__init__("VectorWriter")
        self.repo_path = repo_path
        self.pending_data = []

    def run(self, data):
        print("💾 Writing structured data to ChromaDB...")
        for item in data:
            add_to_vectorstore(item["content"], item["metadata"])
        print("✅ Data indexed.")
