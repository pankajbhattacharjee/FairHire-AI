from pathlib import Path
from typing import Dict, Any

from backend.agents.resume_parser_agent import parse_resume_pdf
from backend.agents.jd_analyzer_agent import analyze_job_description
from backend.agents.matching_agent import compute_candidate_match
from backend.agents.bias_detection_agent import detect_bias_in_jd, run_name_swap_test
from backend.agents.interview_kit_agent import generate_interview_kit


def run_agentic_workflow(resume_path: str, job_description: str, candidate_name: str = "") -> Dict[str, Any]:
    """Run the FairHire AI agent pipeline in a single workflow."""
    parsed_resume = parse_resume_pdf(resume_path)
    jd_analysis = analyze_job_description(job_description)
    match_output = compute_candidate_match(parsed_resume, jd_analysis)
    bias_report = detect_bias_in_jd(job_description)
    counterfactual = run_name_swap_test(job_description, candidate_name or parsed_resume.get("name", ""), match_output.get("overall_match_score", 0))
    interview_kit = generate_interview_kit(parsed_resume, jd_analysis, ", ".join(match_output.get("missing_skills", [])))

    return {
        "resume": parsed_resume,
        "job_description_analysis": jd_analysis,
        "match_output": match_output,
        "bias_report": bias_report,
        "counterfactual_test": counterfactual,
        "interview_kit": interview_kit,
    }
