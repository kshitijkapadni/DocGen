# backend/crew_runner.py

from crewai import Crew
from agents.repo_crawler import RepoCrawlerAgent
from agents.entrypoint_detector import EntrypointDetectorAgent
from agents.deployment_detector import DeploymentDetectorAgent
from agents.function_mapper import FunctionMapperAgent
from agents.vector_writer import VectorWriterAgent

def run_code_analysis(repo_path: str):
    print(f"🚀 Starting CrewAI repo analysis for: {repo_path}")
    
    crew = Crew(
        agents=[
            RepoCrawlerAgent(repo_path),
            EntrypointDetectorAgent(repo_path),
            DeploymentDetectorAgent(repo_path),
            FunctionMapperAgent(repo_path),
            VectorWriterAgent(repo_path),
        ]
    )
    crew.run()
