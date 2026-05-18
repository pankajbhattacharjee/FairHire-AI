from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import List, Optional
import shutil
import uuid
from pydantic import BaseModel

from backend.agents.resume_parser_agent import parse_resume_pdf
from backend.agents.jd_analyzer_agent import analyze_job_description
from backend.agents.matching_agent import compute_candidate_match
from backend.agents.bias_detection_agent import detect_bias_in_jd, run_name_swap_test
from backend.agents.interview_kit_agent import generate_interview_kit
from backend.agents.langgraph_workflow import run_agentic_workflow

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="FairHire AI Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JDRequest(BaseModel):
    job_description: str


class MatchRequest(BaseModel):
    resume: dict
    jd: dict


class BiasRequest(BaseModel):
    job_description: str
    candidate_score: float = 0.0
    candidate_name: str = ""


class InterviewKitRequest(BaseModel):
    resume: dict
    jd: dict
    missing_skills: Optional[str] = ""


@app.get("/")
def root():
    return {"message": "FairHire AI backend is running"}


@app.post("/upload-resume")
async def upload_resume(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No resume files provided")

    parsed_resumes = []
    for upload_file in files:
        filename = f"{uuid.uuid4().hex}_{upload_file.filename}"
        destination = UPLOAD_DIR / filename
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

        parsed = parse_resume_pdf(str(destination))
        parsed["filename"] = upload_file.filename
        parsed_resumes.append(parsed)

    return {"resumes": parsed_resumes}


@app.post("/analyze-jd")
async def analyze_jd(request: JDRequest):
    if not request.job_description:
        raise HTTPException(status_code=400, detail="Job description text is required")
    analysis = analyze_job_description(request.job_description)
    return analysis


@app.post("/match-candidate")
async def match_candidate(request: MatchRequest):
    if not request.resume or not request.jd:
        raise HTTPException(status_code=400, detail="Resume and JD data are required")
    match_output = compute_candidate_match(request.resume, request.jd)
    return match_output


@app.post("/detect-bias")
async def detect_bias(request: BiasRequest):
    bias_report = detect_bias_in_jd(request.job_description)
    counterfactual = run_name_swap_test(request.job_description, request.candidate_name, request.candidate_score)
    return {"bias_report": bias_report, "counterfactual_test": counterfactual}


@app.post("/generate-interview-kit")
async def interview_kit(request: InterviewKitRequest):
    kit = generate_interview_kit(request.resume, request.jd, request.missing_skills)
    return kit


@app.post("/agent-workflow")
async def agent_workflow(file: UploadFile = File(...), job_description: str = Form(...), candidate_name: str = Form("")):
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    destination = UPLOAD_DIR / filename
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    workflow_output = run_agentic_workflow(str(destination), job_description, candidate_name)
    return workflow_output
