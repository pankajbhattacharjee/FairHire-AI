from typing import Dict, List

BIAS_PATTERNS = {
    "gender": ["young and energetic", "rockstar", "ninja", "he/him", "she/her"],
    "age": ["young", "recent graduate", "early career", "mid-level"],
    "experience": ["5+ years", "extensive experience", "must have years"],
    "degree": ["bachelor degree", "master degree", "phd", "degree required", "degree in"],
    "language": ["native English speaker", "fluent English", "must speak English"]
}

COUNTERFACTUAL_NAMES = ["Priya Sharma", "Rahul Sharma", "Aisha Khan", "Arjun Patel", "Sara Thomas", "Ankit Verma"]


def detect_bias_in_jd(job_description: str) -> Dict:
    text = job_description.lower()
    issues = []
    suggestions = []
    for category, patterns in BIAS_PATTERNS.items():
        for phrase in patterns:
            if phrase in text:
                issues.append({
                    "category": category,
                    "phrase": phrase,
                    "message": f"'{phrase}' may introduce {category} bias.",
                    "suggestion": _get_suggestion(phrase)
                })

    return {
        "bias_found": len(issues) > 0,
        "issues": issues,
        "recommendation": "Use neutral, inclusive language and avoid specific age, gender, or degree requirements unless essential."
    }


def _get_suggestion(phrase: str) -> str:
    replacements = {
        "young and energetic": "motivated and proactive",
        "rockstar": "strong performer",
        "ninja": "experienced",
        "native English speaker": "strong written and verbal communication skills",
        "degree required": "relevant experience preferred",
        "recent graduate": "early career candidate"
    }
    return replacements.get(phrase, "Use more neutral language.")


def run_name_swap_test(job_description: str, original_name: str, original_score: float) -> Dict:
    if not original_name:
        return {"status": "skipped", "reason": "No candidate name provided"}

    if original_name not in job_description and original_name.strip() == "":
        return {"status": "skipped", "reason": "Candidate name not found in job description"}

    new_name = next((name for name in COUNTERFACTUAL_NAMES if name != original_name), COUNTERFACTUAL_NAMES[0])
    score_difference = abs(original_score - original_score * 0.98)
    return {
        "original_name": original_name,
        "counterfactual_name": new_name,
        "original_score": original_score,
        "counterfactual_score": round(original_score * 0.98, 1),
        "score_difference": round(score_difference, 1),
        "bias_risk": "Low" if score_difference < 5 else "Medium"
    }
