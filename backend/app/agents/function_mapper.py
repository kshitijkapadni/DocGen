# backend/agents/function_mapper.py

from crewai import Agent
import ast
from pathlib import Path
import ollama
from config import OLLAMA_MODEL

class FunctionMapperAgent(Agent):
    def __init__(self, repo_path):
        super().__init__("FunctionMapper")
        self.repo_path = Path(repo_path)

    def run(self):
        print("🧠 Mapping functions and generating explanations...")
        functions_info = []

        for path in self.repo_path.rglob("*.py"):
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_name = node.name
                        func_docstring = ast.get_docstring(node) or "No description"
                        if func_docstring:
                            functions_info.append({
                                "file_path": str(path.relative_to(self.repo_path)),
                                "function_name": func_name,
                                "description": func_docstring
                            })
                        else:
                            # Generate a description using the LLM if no docstring is present
                            prompt = f"Generate a description for the function \n'{func_name}'\n and args \n'{node.args}'\n with definition \n'{node.body}'\n and returns '{node.returns}'."
                            response = ollama.chat(prompt, model=OLLAMA_MODEL, temperature=0.5)
                            functions_info.append({
                                "file_path": str(path.relative_to(self.repo_path)),
                                "function_name": func_name,
                                "description": response["message"]["content"]
                            })
        if functions_info:
            print(f"✅ Found {len(functions_info)} functions.")
        else:
            print("❌ No functions found.")
        
        return {"functions_info": functions_info}
