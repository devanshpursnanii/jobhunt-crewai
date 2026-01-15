from typing import Type, List, Dict
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os

load_dotenv()

# -------- Input schema --------
class JobSearchInput(BaseModel):
    role: str = Field(..., description="Target job role, e.g., 'ML Engineer'")
    location: str = Field(..., description="Job location, e.g., 'Remote' or 'Mumbai'")
    experience_level: str = Field(..., description="intern|junior|mid|senior")


# -------- Tool implementation --------
class JobSearchTool(BaseTool):
    name: str = "job_search_tool"
    description: str = "Fetches real job openings using Google Jobs via Serper API."
    args_schema: Type[BaseModel] = JobSearchInput

    # declare private attribute for non-pydantic fields
    _serper: SerperDevTool = PrivateAttr()

    def __init__(self):
        super().__init__()
        self._serper = SerperDevTool(search_type="jobs", country="in")

    def _run(self, role: str, location: str, experience_level: str) -> str:
        # ---- input validation ----
        if not role or not isinstance(role, str):
            raise ValueError("role must be a non-empty string")
        if not location or not isinstance(location, str):
            raise ValueError("location must be a non-empty string")
        if experience_level not in {"intern", "junior", "mid", "senior"}:
            raise ValueError("experience_level must be one of: intern, junior, mid, senior")

        query = f"{role} {experience_level} jobs in {location}"

        # ---- API call ----
        try:
            # SerperDevTool.run() only takes search_query as string
            results = self._serper.run(search_query=query)
        except Exception as e:
            raise RuntimeError(f"Job search API failed: {e}")

        # ---- output validation and parsing ----
        # SerperDevTool returns a string, parse it
        import json
        try:
            if isinstance(results, str):
                results = json.loads(results)
        except:
            pass
            
        if not isinstance(results, dict):
            return json.dumps({"jobs": []})

        raw_jobs = results.get("jobs", [])
        if not raw_jobs or not isinstance(raw_jobs, list):
            return json.dumps({"jobs": []})

        jobs: List[Dict] = []
        for r in raw_jobs:
            if not isinstance(r, dict):
                continue
            jobs.append({
                "title": r.get("title", "Unknown"),
                "company": r.get("company", "Unknown"),
                "location": r.get("location", "Unknown"),
                "apply_link": r.get("link"),
                "posted_days_ago": r.get("posted", None)
            })

        return json.dumps({"jobs": jobs})
    
job_search_tool = JobSearchTool()

# Configure PDFSearchTool with Google Generative AI embeddings and ChromaDB
from crewai_tools import PDFSearchTool

resume_reader_tool = PDFSearchTool(
    pdf="/Users/apple/Desktop/jobhunt-crewai/resume.pdf",
    config={
        "embedding_model": {
            "provider": "google-generativeai",
            "config": {
                "model": "models/text-embedding-004",  # Latest Google embedding model
                "task_type": "RETRIEVAL_DOCUMENT",
                # API key will be picked up from GOOGLE_API_KEY env var automatically
            },
        },
        "vectordb": {
            "provider": "chromadb",
            "config": {
                # ChromaDB will use local storage by default
                # Data persists in ./chroma directory
            }
        },
    }
)