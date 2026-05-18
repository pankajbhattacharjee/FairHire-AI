# FairHire AI

FairHire AI is an **agentic resume screening and bias detection platform** for recruiters. It combines resume parsing, job description analysis, candidate matching, bias detection, counterfactual fairness testing, and interview kit generation into one demo-ready AI product.

---

## Demo

### Live Demo

Add your deployed app link here:

```text
https://your-live-demo-link.com
```

### Demo Video

Add your demo video link here:

```text
https://www.youtube.com/shorts/ZrrGORu6AxE
```

---

## Screenshots

Add screenshots inside a folder named `screenshots/`.

### Home Page

![Home Page](https://drive.google.com/file/d/1wRLBTb2-BsDoro3z75PvdQrjhi7OaEv2/view?usp=sharing)

### Resume Upload

![Resume Upload](https://drive.google.com/file/d/1Bw82mMJqcFK84TDPGMQR6lnhwiId18oo/view?usp=sharing)

### Job Description Analysis

![Job Description Analysis](https://drive.google.com/file/d/1PDPCzGmEiKiveQyYQx0rR5q4N5Md0Vhr/view?usp=sharing)

### Candidate Ranking

![Candidate Ranking](https://drive.google.com/file/d/1j2UvA_vzKpikyt7Wd8jEk9yoAZZdc2Ui/view?usp=sharing)

### Bias Report

![Bias Report](https://drive.google.com/file/d/1YeMDbgqftD9jknI5LDPqlU92vsai2Yd-/view?usp=sharing)

### Interview Kit

![Interview Kit](https://drive.google.com/file/d/1PE_Kq2w-jOhOu0ffpFd6vcRK7mij1i-m/view?usp=sharing)

---

## Project Overview

FairHire AI helps recruiters screen resumes faster, fairly, and explainably by using multiple AI agents to:

- Parse resumes into structured candidate data
- Analyze job descriptions for required and preferred skills
- Compute match scores and rank candidates
- Detect biased or exclusionary hiring language
- Perform counterfactual name-swap fairness testing
- Generate recruiter-ready interview preparation kits

---

## Problem Statement

Recruiters often need fast, fair, and explainable tools to evaluate candidates. Manual resume review is time-consuming and can be inconsistent. Basic ATS systems mostly depend on keyword matching and may miss nuanced candidate fit, project relevance, and responsible hiring checks.

FairHire AI solves this by combining **resume intelligence, agentic AI, explainable ranking, and responsible AI checks** in a single platform.

---

## Why FairHire AI Is Different

Most resume screening projects only calculate a basic ATS score.

FairHire AI goes further by adding:

- Multi-agent AI workflow
- Resume-to-job semantic matching
- Explainable candidate ranking
- Bias detection in job descriptions
- Counterfactual name-swap fairness testing
- Candidate-specific interview kit generation
- Recruiter-friendly dashboard

This makes FairHire AI closer to a real recruitment assistant than a simple resume parser.

---

## Features

- Resume upload and PDF parsing
- Job description analysis with required and preferred skills
- Candidate-job match scoring
- Candidate ranking dashboard
- Strength and missing-skill detection
- Bias detection for gender, age, and exclusionary language
- Counterfactual name-swap fairness testing
- Interview kit generation with:
  - Technical questions
  - HR questions
  - Resume-based questions
  - Skill-gap questions
  - Evaluation rubric

---

## Tech Stack

| Area | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| PDF Extraction | PyPDF2 / pdfplumber |
| NLP | spaCy |
| AI / LLM | OpenAI API / Gemini API |
| Agent Workflow | LangGraph-ready architecture |
| RAG / Vectorstore | FAISS / ChromaDB support |
| Database | SQLite-ready patterns |
| Deployment | Streamlit Cloud / Hugging Face Spaces / Render |

---

## Agent Architecture

The backend is organized as a 5-agent architecture:

### 1. Resume Parser Agent

Extracts candidate information such as:

- Name
- Email
- Education
- Skills
- Projects
- Experience
- Certifications

### 2. JD Analyzer Agent

Analyzes the job description and extracts:

- Required skills
- Preferred skills
- Experience level
- Education requirement
- Responsibilities
- Tools and frameworks

### 3. Matching & Ranking Agent

Compares resume data with the job description and generates:

- Match score
- Strengths
- Missing skills
- Candidate ranking
- Hiring recommendation

### 4. Bias Detection Agent

Detects unfair or exclusionary hiring language and performs counterfactual fairness checks.

### 5. Interview Kit Generator Agent

Generates recruiter-ready interview preparation kits with technical, HR, and skill-gap questions.

---

## System Workflow

```text
Resume PDF + Job Description
        ↓
Resume Parser Agent
        ↓
JD Analyzer Agent
        ↓
Matching & Ranking Agent
        ↓
Bias Detection Agent
        ↓
Interview Kit Generator Agent
        ↓
Final Recruiter Dashboard
```

---

## Folder Structure

```text
FairHire_AI/
│
├── backend/
│   ├── main.py
│   ├── agents/
│   │   ├── resume_parser_agent.py
│   │   ├── jd_analyzer_agent.py
│   │   ├── matching_agent.py
│   │   ├── bias_detection_agent.py
│   │   └── interview_kit_agent.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── app.py
│   └── requirements.txt
│
├── sample_data/
│   └── sample_jd.txt
│
├── screenshots/
│   ├── home.png
│   ├── upload.png
│   ├── jd-analysis.png
│   ├── ranking.png
│   ├── bias-report.png
│   └── interview-kit.png
│
├── demo_video_link.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/FairHire_AI.git
cd FairHire_AI
```

Install backend dependencies:

```bash
cd backend
python -m pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Install frontend dependencies:

```bash
cd ../frontend
python -m pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file inside the `backend/` folder:

```bash
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
BACKEND_URL=http://localhost:8000
```

Use either OpenAI or Gemini depending on your setup.

---

## Running Locally

Start the backend:

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Start the frontend in a new terminal:

```bash
cd frontend
streamlit run app.py
```

Open the Streamlit app in your browser and test the full workflow.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/upload-resume` | Upload one or more resume PDFs |
| POST | `/analyze-jd` | Analyze a job description |
| POST | `/match-candidate` | Score a candidate against a job description |
| POST | `/detect-bias` | Analyze hiring bias and counterfactual fairness |
| POST | `/generate-interview-kit` | Generate interview questions and evaluation rubric |
| POST | `/agent-workflow` | Run the complete FairHire AI pipeline |

---

## Sample Job Description

Sample job description is available at:

```text
sample_data/sample_jd.txt
```

Example role:

```text
AI/ML Engineer Intern
Required Skills: Python, Machine Learning, NLP, FastAPI, Streamlit, Git
Preferred Skills: LangChain, LangGraph, FAISS, ChromaDB, Docker, SQL
```

---

## Sample Output

```json
{
  "candidate_name": "Pankaj Bhattacharjee",
  "match_score": 86,
  "strengths": [
    "Python",
    "Machine Learning",
    "NLP",
    "LangChain",
    "FastAPI"
  ],
  "missing_skills": [
    "Docker",
    "Cloud Deployment"
  ],
  "recommendation": "Shortlist",
  "bias_risk": "Low",
  "interview_focus": [
    "FastAPI deployment",
    "RAG pipeline design",
    "Docker basics"
  ]
}
```

---

## Ethical AI Note

FairHire AI is designed to **assist recruiters**, not replace human hiring decisions. The platform provides explainable recommendations, bias warnings, and interview preparation support. Final hiring decisions should always be made by human recruiters with proper review.

The Interview Kit Generator is intended for recruiter preparation only. It does not generate answers for candidates or manipulate hiring decisions.

---

## Resume Highlight

You can add this project to your resume as:

```text
FairHire AI: Agentic Resume Screening & Bias Detection Platform

Built an agentic AI recruitment assistant using FastAPI, Streamlit, LangChain-ready workflows, and RAG-style matching to parse resumes, analyze job descriptions, rank candidates, detect hiring bias, and generate recruiter-ready interview kits.
```

---

## Future Improvements

- Replace heuristic matching with advanced vector-based RAG using FAISS / ChromaDB
- Add PostgreSQL for persisted candidate and job data
- Add recruiter authentication and role-based access
- Add downloadable PDF reports for recruiters
- Move frontend to React for production-ready UI
- Add email integration for sending interview kits
- Add analytics dashboard for recruiter activity
- Add evaluation using real resume and hiring datasets

---

## Author

**Pankaj Bhattacharjee**

- GitHub: `https://github.com/pankajbhattacharjee`
- LinkedIn: `https://www.linkedin.com/in/pankaj-bhattacharjee-475b86325/`
- Portfolio: `https://pankajbhattacharjee.github.io/Portfolio./`

---

## License

This project is for educational and portfolio purposes.
