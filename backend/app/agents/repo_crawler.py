# backend/agents/repo_crawler.py

from crewai import Agent
from pathlib import Path

class RepoCrawlerAgent(Agent):
    def __init__(self, repo_path):
        super().__init__("RepoCrawler")
        self.repo_path = Path(repo_path)

    def run(self):
        print("📁 Crawling repository...")
        self.file_structure = []
        for path in self.repo_path.rglob("*"):
            if path.is_file():
                self.file_structure.append(str(path.relative_to(self.repo_path)))
        print("✅ Found files:", len(self.file_structure))
        return {"files": self.file_structure}
