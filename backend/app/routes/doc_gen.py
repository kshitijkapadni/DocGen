from fastapi import APIRouter, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from app.services.generator import create_structured_doc
import uuid, os

from app.services.llm_agent import answer_question
from app.services.llm_agent import add_to_vectorstore

from app.agents.crew_runner import run_crew_analysis  # triggers repo analysis
from app.utils.chroma_utils import fetch_all_docs
from app.utils.version import get_git_version

router = APIRouter()

OUTPUT_DIR = "generated_docs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/generate-docx")
def generate_docx(regenerate: bool = False):
    if regenerate:
        run_crew_analysis()  # Crawls repo and updates vector DB

    # Fetch content
    content_items = fetch_all_docs()
    version = get_git_version()

    # Generate file name
    file_id = str(uuid.uuid4())[:8]
    file_path = os.path.join(OUTPUT_DIR, f"Documentation_v{version}_{file_id}.docx")

    # Generate docx
    create_structured_doc(content_items, version=version, output_path=file_path)

    # Serve file
    return FileResponse(file_path, filename=os.path.basename(file_path))

@router.post("/ask")
def ask_docgen_agent(query: dict):
    user_question = query.get("question")
    answer = answer_question(user_question)
    return {"answer": answer}

@router.post("/describe")
async def submit_description(payload: dict):
    description = payload.get("description")
    if not description:
        return {"error": "Missing 'description'"}
    
    metadata = {"id": "app_description"}
    add_to_vectorstore(description, metadata)
    
    return {"status": "Description stored and indexed for RAG."}

