from typing import List


def normalized_score(value: float) -> int:
    return max(0, min(100, int(round(value * 100))))


def compare_skills(candidate: List[str], required: List[str]) -> dict:
    matched = [skill for skill in required if skill in candidate]
    missing = [skill for skill in required if skill not in candidate]
    return {
        "matched": matched,
        "missing": missing,
        "skill_match_score": normalized_score(len(matched) / max(1, len(required)))
    }
