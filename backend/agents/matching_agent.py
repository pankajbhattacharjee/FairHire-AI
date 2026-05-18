from typing import Dict, List


def compute_skill_score(candidate_skills: List[str], required_skills: List[str]) -> float:
    if not required_skills:
        return 1.0
    matched = [skill for skill in required_skills if skill in candidate_skills]
    return round(len(matched) / len(required_skills), 2)


def compute_experience_score(experience_text: str) -> float:
    if experience_text and experience_text != "Not specified":
        return 0.8
    return 0.4


def compute_education_score(candidate_education: List[str], required_education: str) -> float:
    if not required_education or required_education == "Not specified":
        return 0.5
    if any(required_education.lower() in edu.lower() for edu in candidate_education):
        return 1.0
    return 0.5


def compute_candidate_match(resume: Dict, jd: Dict) -> Dict:
    required_skills = jd.get("required_skills", [])
    candidate_skills = resume.get("skills", [])
    skill_score = compute_skill_score(candidate_skills, required_skills)
    experience_score = compute_experience_score(jd.get("experience_level", ""))
    education_score = compute_education_score(resume.get("education", []), jd.get("education_requirement", ""))

    overall = round((skill_score * 0.55 + experience_score * 0.25 + education_score * 0.2) * 100)
    strengths = [skill for skill in candidate_skills if skill in required_skills]
    missing_skills = [skill for skill in required_skills if skill not in candidate_skills]
    recommendation = "Shortlist"
    if overall < 70:
        recommendation = "Maybe"
    if overall < 55:
        recommendation = "Consider"

    return {
        "overall_match_score": overall,
        "skill_match_score": int(skill_score * 100),
        "experience_match_score": int(experience_score * 100),
        "education_match_score": int(education_score * 100),
        "strengths": strengths,
        "missing_skills": missing_skills,
        "recommendation": recommendation,
        "candidate_name": resume.get("name", "Unknown"),
    }


def rank_candidates(matches: List[Dict]) -> List[Dict]:
    return sorted(matches, key=lambda item: item.get("overall_match_score", 0), reverse=True)
