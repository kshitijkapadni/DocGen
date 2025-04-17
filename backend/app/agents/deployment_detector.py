# backend/agents/deployment_detector.py

from crewai import Agent
from pathlib import Path

class DeploymentDetectorAgent(Agent):
    def __init__(self, repo_path):
        super().__init__("DeploymentDetector")
        self.repo_path = Path(repo_path)

    def run(self):
        print("📦 Detecting deployment configuration...")
        deployment_files = []
        deployment_patterns = ["docker-compose.yml", "Dockerfile", "*ingress*.yaml", "*deploy*.yaml", "*service*.yaml", "*configmap*.yaml", "*secret*.yaml", "helm/"]
        
        for pattern in deployment_patterns:
            for path in self.repo_path.rglob(pattern):
                deployment_files.append(str(path.relative_to(self.repo_path)))
        
        if deployment_files:
            print("✅ Found deployment configs:", deployment_files)
        else:
            print("❌ No deployment configurations found.")
        
        return {"deployment_files": deployment_files}
