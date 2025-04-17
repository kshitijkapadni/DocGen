# backend/agents/entrypoint_detector.py

from crewai import Agent
from pathlib import Path

class EntrypointDetectorAgent(Agent):
    def __init__(self, repo_path):
        super().__init__("EntrypointDetector")
        self.repo_path = Path(repo_path)

    def run(self):
        print("🔍 Detecting entry points...")
        entry_points = []
        for path in self.repo_path.rglob("*.py"):
            content = path.read_text(encoding="utf-8")
            if "__main__" in content:
                entry_points.append(str(path.relative_to(self.repo_path)))
        
        if entry_points:
            print("✅ Found entry points:", entry_points)
        else:
            print("❌ No entry points detected.")
        
        return {"entry_points": entry_points}
