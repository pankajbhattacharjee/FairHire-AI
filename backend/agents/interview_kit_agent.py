import os
from typing import Dict, List

try:
    import openai
except ImportError:
    openai = None

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def _render_questions(resume: Dict, jd: Dict, missing_skills: List[str]) -> Dict:
    candidate_name = resume.get("name", "Candidate")
    technical_questions = [
        f"Describe a project where you used {skill}. What was your architecture and outcome?"
        for skill in missing_skills[:2]
    ]
    if not technical_questions:
        technical_questions = [
            "Explain how you would deploy a FastAPI application with a machine learning model.",
            "How do you manage data schema changes when working with SQL databases?"
        ]

    hr_questions = [
        "Tell me about a time you faced a tight deadline and how you managed it.",
        "What do you do to keep learning new tools and technologies?"
    ]
    resume_questions = [
        f"Can you walk me through your experience building {resume.get('projects', ['a key project'])[0]}?"
    ]
    skill_gap_questions = [
        f"How would you approach learning and applying {missing_skills[0]} if hired?"
    ] if missing_skills else [
        "What is one technology you would like to learn next and why?"
    ]

    return {
        "technical_questions": technical_questions,
        "hr_questions": hr_questions,
        "resume_based_questions": resume_questions,
        "skill_gap_questions": skill_gap_questions,
        "evaluation_rubric": [
            "Clear technical understanding",
            "Relevant experience examples",
            "Problem-solving thought process",
            "Communication and culture fit"
        ],
        "expected_answer_points": [
            "Mention architecture, dependencies, and deployment steps.",
            "Describe collaboration, timelines, and outcomes.",
            "Cover how they close skill gaps with learning and experimentation."
        ]
    }


def generate_interview_kit(resume: Dict, jd: Dict, missing_skills: str) -> Dict:
    missing_skills_list = [skill.strip() for skill in missing_skills.split(",") if skill.strip()]
    if openai and OPENAI_API_KEY:
        try:
            openai.api_key = OPENAI_API_KEY
            prompt = (
                f"Generate an interview kit for a recruiter. Resume: {resume}. "
                f"Job description: {jd}. Missing skills: {missing_skills_list}."
            )
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a hiring assistant."},
                          {"role": "user", "content": prompt}],
                max_tokens=500,
            )
            text = response.choices[0].message.content
            return {"generated_text": text}
        except Exception:
            pass

    return _render_questions(resume, jd, missing_skills_list)
