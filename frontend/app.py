import os
from pathlib import Path

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
ROOT_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DIR = ROOT_DIR / "sample_data"

st.set_page_config(
    page_title="FairHire AI",
    page_icon="🤖",
    layout="wide",
)

PAGE_CSS = """
<style>
:root {
    font-size: 17px;
}
body {
    background: #040812;
    color: #e4e9ff;
    font-family: Inter, sans-serif;
    line-height: 1.7;
}
section.main {
    background: transparent;
}
[data-testid="stSidebar"] {
    background: #07122e;
}
.css-1d391kg, .css-1v0mbdj {
    background-color: #07122e !important;
}
.css-18e3th9 {
    background-color: #040812 !important;
}
.css-1d391kg {
    border: 1px solid rgba(255,255,255,0.06) !important;
}
.stButton>button {
    background: linear-gradient(135deg, #4f6cf7, #2ab0ff) !important;
    color: white !important;
    border: none !important;
    font-size: 15.5px !important;
    padding: 16px 24px !important;
    min-height: 48px !important;
}
.st-bc {
    color: #94a3ff !important;
}
button[role="tab"], div[role="tab"] {
    font-size: 15.5px !important;
    min-height: 44px !important;
    padding: 12px 18px !important;
}
h1 {
    font-size: 40px !important;
    line-height: 1.05;
}
h2 {
    font-size: 30px !important;
}
h3 {
    font-size: 24px !important;
}
h4, h5, h6 {
    font-size: 20px !important;
}
p, span, label, div {
    font-size: 17px !important;
}
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stNumberInput>div>div>input {
    font-size: 16px !important;
}
.stAlert {
    background-color: #0f1a33 !important;
    color: #e4e9ff !important;
    font-size: 14.5px !important;
}
.css-1q8dd3e {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    box-shadow: 0 18px 64px rgba(0,0,0,0.30);
    padding: 24px !important;
}
.css-1d391kg, .css-1v0mbdj, .css-18e3th9 {
    padding: 18px !important;
}
.css-1q8dd3e .css-1t1iy2j {
    padding: 20px !important;
}
div[role="listitem"] {
    padding: 18px !important;
}
@media (max-width: 1200px) {
    h1 { font-size: 36px !important; }
    h2 { font-size: 28px !important; }
    h3 { font-size: 22px !important; }
    button[role="tab"], div[role="tab"] { font-size: 15px !important; }
}
@media (max-width: 800px) {
    :root { font-size: 15px; }
    h1 { font-size: 32px !important; }
    h2 { font-size: 24px !important; }
    h3 { font-size: 20px !important; }
    .stButton>button { font-size: 15px !important; padding: 14px 20px !important; }
}
</style>
"""

st.markdown(PAGE_CSS, unsafe_allow_html=True)

if "resumes" not in st.session_state:
    st.session_state["resumes"] = []
if "jd_text" not in st.session_state:
    st.session_state["jd_text"] = ""
if "jd" not in st.session_state:
    st.session_state["jd"] = {}
if "matches" not in st.session_state:
    st.session_state["matches"] = []
if "bias_report" not in st.session_state:
    st.session_state["bias_report"] = {}
if "interview_kit" not in st.session_state:
    st.session_state["interview_kit"] = {}

st.markdown("<div style='max-width:1200px; margin:auto; padding: 24px 0; display: flex; flex-wrap: wrap; gap: 24px; align-items: center;'>"
            "<img src='https://img.icons8.com/fluency/64/ffffff/robot-2.png' style='margin-right: 18px; min-width:64px;'/>"
            "<div style='flex:1; min-width:320px;'>"
            "<h1 style='margin:0 0 12px; font-size:40px; line-height:1.05;'>FairHire AI</h1>"
            "<p style='margin:0; font-size:18px; color:#a8b0ff; max-width:840px; line-height:1.8;'>An agentic recruitment assistant that screens resumes fairly, detects bias, ranks candidates, and generates interview kits.</p></div></div>", unsafe_allow_html=True)

nav_tabs = st.tabs(["Home", "Upload", "Job Description", "Rankings", "Bias Report", "Interview Kit"])

with nav_tabs[0]:
    st.markdown("<div style='padding: 40px; background: linear-gradient(135deg, rgba(12, 28, 66, 0.95), rgba(9, 19, 52, 0.95)); border-radius: 30px; box-shadow: 0 35px 95px rgba(0,0,0,0.34); max-width:1200px; margin:auto;'>"
                "<div style='display: flex; flex-wrap: wrap; gap: 30px; align-items:flex-start;'>"
                "<div style='flex:1; min-width:320px;'>"
                "<h2 style='margin:0 0 20px; font-size:40px; color:#b3baff; line-height:1.1;'>AI-powered resume screening with fairness baked in.</h2>"
                "<p style='color:#cfd7ff; font-size:18px; line-height:1.85; max-width:780px; margin-bottom:28px;'>Upload candidate resumes, match them to job requirements, detect biased language, and create tailored interview kits — all in one streamlined dashboard.</p>"
                "<div style='display:flex; flex-wrap:wrap; gap:16px; margin-top:12px;'>"
                "<a href='#upload' style='text-decoration:none;'><button style='padding:16px 28px; border-radius:999px; border:none; background:#4f6cf7; color:white; font-size:15.5px; cursor:pointer;'>Upload Resumes</button></a>"
                "<button id='demo-button' style='padding:16px 28px; border-radius:999px; border:1px solid rgba(255,255,255,0.18); background:transparent; color:#cfd7ff; font-size:15.5px; cursor:pointer;'>Load Demo Data</button>"
                "</div></div>"
                "<div style='flex:0.9; min-width:320px;'>"
                "<div style='padding:28px; border-radius:26px; background:rgba(31, 51, 94, 0.96); border:1px solid rgba(255,255,255,0.08);'>"
                "<h3 style='margin-bottom:16px; font-size:24px; color:#84d9ff;'>5-Agent LangGraph Pipeline</h3>"
                "<div style='display:grid; grid-template-columns:repeat(auto-fit, minmax(120px, 1fr)); gap:14px;'>"
                "<div style='padding:18px 14px; border-radius:20px; background:rgba(255,255,255,0.06); text-align:center; font-size:16px;'>Parser</div>"
                "<div style='padding:18px 14px; border-radius:20px; background:rgba(255,255,255,0.06); text-align:center; font-size:16px;'>JD Analyzer</div>"
                "<div style='padding:18px 14px; border-radius:20px; background:rgba(255,255,255,0.06); text-align:center; font-size:16px;'>Matcher</div>"
                "<div style='padding:18px 14px; border-radius:20px; background:rgba(255,255,255,0.06); text-align:center; font-size:16px;'>Bias Detect</div>"
                "<div style='padding:18px 14px; border-radius:20px; background:rgba(255,255,255,0.06); text-align:center; font-size:16px;'>Interview</div>"
                "</div></div></div></div>", unsafe_allow_html=True)

    st.markdown("<div style='display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:22px; margin-top:30px;'>"
                "<div style='padding:28px; border-radius:26px; background:rgba(16, 35, 70, 0.9); border:1px solid rgba(255,255,255,0.08);'>"
                "<h3 style='margin-top:0; margin-bottom:12px; font-size:24px; color:#99caff;'>Smart Screening</h3><p style='color:#cfd7ff; font-size:17px; line-height:1.8;'>RAG-based semantic candidate matching with explainable scores and detail-level resume parsing.</p></div>"
                "<div style='padding:28px; border-radius:26px; background:rgba(16, 35, 70, 0.9); border:1px solid rgba(255,255,255,0.08);'>"
                "<h3 style='margin-top:0; margin-bottom:12px; font-size:24px; color:#99caff;'>Bias Detection</h3><p style='color:#cfd7ff; font-size:17px; line-height:1.8;'>Find gendered, exclusionary, or unfair language with counterfactual name-swap testing.</p></div>"
                "<div style='padding:28px; border-radius:26px; background:rgba(16, 35, 70, 0.9); border:1px solid rgba(255,255,255,0.08);'>"
                "<h3 style='margin-top:0; margin-bottom:12px; font-size:24px; color:#99caff;'>Interview Kits</h3><p style='color:#cfd7ff; font-size:17px; line-height:1.8;'>Auto-generate candidate-specific questions, evaluation rubrics, and model answers.</p></div>"
                "</div>", unsafe_allow_html=True)

    st.info("This demo uses real AI to analyze resumes and job descriptions. Upload PDFs or load demo data to explore all features.")

with nav_tabs[1]:
    st.markdown("<h2 id='upload'>Upload Resumes</h2>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload one or more resumes (PDF)", type=["pdf"], accept_multiple_files=True)
    if st.button("Parse Resumes"):
        if not uploaded_files:
            st.warning("Please upload at least one resume.")
        else:
            with st.spinner("Parsing resumes..."):
                files = [
                    ("files", (uploaded_file.name, uploaded_file.getvalue(), "application/pdf"))
                    for uploaded_file in uploaded_files
                ]
                response = requests.post(f"{BACKEND_URL}/upload-resume", files=files)
            if response.ok:
                result = response.json()
                if isinstance(result, dict):
                    if "resumes" in result:
                        parsed_resumes = result["resumes"]
                    elif "parsed_resumes" in result:
                        parsed_resumes = result["parsed_resumes"]
                    elif "data" in result:
                        parsed_resumes = result["data"]
                    else:
                        parsed_resumes = [result]
                elif isinstance(result, list):
                    parsed_resumes = result
                else:
                    parsed_resumes = []

                st.session_state["resumes"] = parsed_resumes
                st.session_state["matches"] = []
                st.session_state["interview_kit"] = {}
                st.success(f"{len(parsed_resumes)} resume(s) parsed and saved successfully.")
                st.json(st.session_state["resumes"])
            else:
                st.error(response.text)

    if st.session_state["resumes"]:
        st.success(f"Saved resumes in session: {len(st.session_state['resumes'])}")
        st.json(st.session_state["resumes"])

    if st.button("Load Demo Data"):
        demo_jd = (SAMPLE_DIR / "sample_jd.txt").read_text(encoding="utf-8")
        sample_files = [SAMPLE_DIR / "sample_resume_1.pdf", SAMPLE_DIR / "sample_resume_2.pdf"]
        try:
            files = [("files", (file.name, file.open("rb"), "application/pdf")) for file in sample_files]
            response = requests.post(f"{BACKEND_URL}/upload-resume", files=files)
            if response.ok:
                resumes = response.json().get("resumes", [])
                st.session_state["resumes"] = resumes
                st.session_state["matches"] = []
                st.session_state["interview_kit"] = {}
                st.session_state["jd"] = {"job_description": demo_jd}
                st.success("Demo resumes and job description loaded.")
                st.write("Demo job description loaded into Job Description tab.")
            else:
                st.error(response.text)
        except Exception as exc:
            st.error(f"Unable to load demo data: {exc}")

with nav_tabs[2]:
    st.markdown("<h2>Add Job Description</h2>", unsafe_allow_html=True)
    jd_text = st.text_area(
        "Paste the job description here",
        value=st.session_state["jd"].get("job_description", ""),
        height=260,
    )
    if st.button("Analyze Job Description"):
        if not jd_text.strip():
            st.warning("Please add a job description first.")
        else:
            response = requests.post(f"{BACKEND_URL}/analyze-jd", json={"job_description": jd_text})
            if response.ok:
                jd = response.json()
                st.session_state["jd"] = jd
                st.success("Job description analyzed")
                st.json(jd)
            else:
                st.error(response.text)

with nav_tabs[3]:
    st.markdown("<h2>Candidate Ranking</h2>", unsafe_allow_html=True)
    resumes = st.session_state["resumes"]
    jd = st.session_state["jd"]
    if not resumes:
        st.info("Upload resumes first.")
    elif not jd:
        st.info("Analyze a job description first.")
    else:
        if not st.session_state["matches"]:
            if st.button("Generate Rankings"):
                with st.spinner("Scoring candidates..."):
                    matches = []
                    for resume in resumes:
                        response = requests.post(
                            f"{BACKEND_URL}/match-candidate",
                            json={"resume": resume, "jd": jd},
                        )
                        if response.ok:
                            matches.append(response.json())
                    sorted_matches = sorted(matches, key=lambda item: item.get("overall_match_score", 0), reverse=True)
                    st.session_state["matches"] = sorted_matches
                    if sorted_matches:
                        st.table([
                            {
                                "Rank": idx + 1,
                                "Candidate": match.get("candidate_name"),
                                "Match Score": f"{match.get('overall_match_score')}%",
                                "Missing Skills": ", ".join(match.get("missing_skills", [])),
                                "Recommendation": match.get("recommendation"),
                            }
                            for idx, match in enumerate(sorted_matches)
                        ])
                    else:
                        st.warning("No match results returned.")
            else:
                st.info("Click Generate Rankings to score the uploaded resumes against the job description.")
        else:
            sorted_matches = st.session_state["matches"]
            st.table([
                {
                    "Rank": idx + 1,
                    "Candidate": match.get("candidate_name"),
                    "Match Score": f"{match.get('overall_match_score')}%",
                    "Missing Skills": ", ".join(match.get("missing_skills", [])),
                    "Recommendation": match.get("recommendation"),
                }
                for idx, match in enumerate(sorted_matches)
            ])

with nav_tabs[4]:
    st.markdown("<h2>Bias Report</h2>", unsafe_allow_html=True)
    jd_text = st.text_area(
        "Job description for bias analysis",
        value=st.session_state["jd"].get("job_description", ""),
        height=240,
    )
    default_candidate_name = ""
    if st.session_state["matches"]:
        first_match = st.session_state["matches"][0]
        default_candidate_name = (
            first_match.get("candidate_name")
            or first_match.get("name")
            or (first_match.get("candidate") or {}).get("name", "")
        )
    elif st.session_state["resumes"]:
        first_resume = st.session_state["resumes"][0]
        default_candidate_name = (
            first_resume.get("name")
            or first_resume.get("candidate_name")
            or (first_resume.get("personal_info") or {}).get("name", "")
            or first_resume.get("filename", "")
        )

    default_score = 80.0
    if st.session_state["matches"]:
        first_match = st.session_state["matches"][0]
        default_score = float(
            first_match.get("match_score")
            or first_match.get("score")
            or first_match.get("overall_score")
            or first_match.get("overall_match_score")
            or 80.0
        )

    score = st.number_input(
        "Candidate score for counterfactual test",
        min_value=0.0,
        max_value=100.0,
        value=default_score,
    )
    candidate_name = st.text_input(
        "Candidate name for counterfactual test",
        value=default_candidate_name,
    )
    if st.button("Detect Bias"):
        response = requests.post(
            f"{BACKEND_URL}/detect-bias",
            json={"job_description": jd_text, "candidate_score": score, "candidate_name": candidate_name},
        )
        if response.ok:
            report = response.json()
            st.session_state["bias_report"] = report
            st.json(report)
        else:
            st.error(response.text)
    elif st.session_state.get("bias_report"):
        st.json(st.session_state["bias_report"])

with nav_tabs[5]:
    st.markdown("<h2>Interview Kit</h2>", unsafe_allow_html=True)
    resumes = st.session_state.get("resumes", [])
    jd = st.session_state.get("jd")
    if not resumes or not jd:
        st.info("Upload resumes and analyze a JD first.")
    else:
        candidate_options = [resume.get("name", resume.get("filename", "Unnamed")) for resume in resumes]
        selected = st.selectbox("Select candidate", candidate_options)
        missing_skills = st.text_input("Missing skills (comma-separated)")
        if st.button("Generate Interview Kit"):
            selected_resume = next(
                (resume for resume in resumes if resume.get("name") == selected or resume.get("filename") == selected),
                resumes[0],
            )
            response = requests.post(
                f"{BACKEND_URL}/generate-interview-kit",
                json={"resume": selected_resume, "jd": jd, "missing_skills": missing_skills},
            )
            if response.ok:
                kit = response.json()
                st.session_state["interview_kit"] = kit
                st.json(kit)
            else:
                st.error(response.text)
        elif st.session_state.get("interview_kit"):
            st.json(st.session_state["interview_kit"])

with st.expander("Debug Session State"):
    st.write("Resumes:", st.session_state["resumes"])
    st.write("JD:", st.session_state["jd"])
    st.write("Matches:", st.session_state["matches"])
    st.write("Bias Report:", st.session_state["bias_report"])
    st.write("Interview Kit:", st.session_state["interview_kit"])
