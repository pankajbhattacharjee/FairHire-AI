import re
from typing import Dict, List

SKILL_NORMALIZATION = {
    "python": "Python",
    "fastapi": "FastAPI",
    "langchain": "LangChain",
    "faiss": "FAISS",
    "chromadb": "ChromaDB",
    "chroma": "ChromaDB",
    "nlp": "NLP",
    "sql": "SQL",
    "rag": "RAG",
    "numpy": "NumPy",
    "pandas": "Pandas",
    "langgraph": "LangGraph",
    "huggingface transformers": "HuggingFace Transformers",
    "huggingface": "HuggingFace",
    "transformers": "Transformers",
    "docker": "Docker",
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "react": "React",
    "node": "Node.js",
    "git": "Git",
    "spark": "Spark",
    "postgresql": "PostgreSQL",
    "mysql": "MySQL",
    "r programming": "R",
    "r language": "R",
    "r": "R",
    "cloud deployment": "Cloud Deployment",
}

REQUIRED_SKILL_TERMS = [
    "python", "fastapi", "langchain", "sql", "docker", "aws", "azure", "gcp", "pandas", "numpy",
    "tensorflow", "pytorch", "react", "node", "git", "nlp", "spark", "postgresql", "mysql",
    "r programming", "r language", "cloud deployment", "langgraph", "huggingface transformers", "transformers"
]
PREFERRED_SKILL_TERMS = [
    "docker", "aws", "helm", "kubernetes", "chroma", "chromadb", "faiss", "terraform", "pytorch", "tensorflow",
    "langgraph", "rag", "sql", "cloud deployment", "huggingface transformers"
]
EDUCATION_LEVELS = ["bachelor", "master", "phd", "diploma", "mba", "b.sc", "m.sc", "bs", "ms"]
EXPERIENCE_PATTERNS = [
    ("Intern", r"\b(intern|internship)\b"),
    ("Fresher", r"\b(fresher|fresh graduate|fresh graduates|recent graduate)\b"),
    ("Entry-level", r"\bentry[- ]level\b"),
    ("Junior", r"\bjunior\b"),
    ("Mid-level", r"\bmid[- ]level\b"),
    ("Senior", r"\bsenior\b"),
    ("Lead", r"\blead\b"),
]
YEAR_PATTERNS = [r"\b(\d+)\+?\s*years?\b", r"\b(\d+)-year\b", r"\b(\d+)\s*year\b"]
STOPWORDS = {
    "the", "and", "for", "with", "to", "of", "in", "a", "an", "is", "are", "on", "at", "by", "or",
    "this", "that", "be", "can", "able", "about", "as", "such", "from", "will", "using", "use",
    "required", "preferred", "responsibilities", "responsibility", "experience", "skills", "team", "work",
    "role", "job", "you", "your", "candidate", "strong", "apply", "ability", "include", "including",
    "based", "knowledge", "requirements", "must", "must-have", "needed", "need",
}
SECTION_PATTERNS = {
    "required": [r"required", r"required skills?", r"requirements?", r"must haves?", r"must-have skills?", r"skills required"],
    "preferred": [r"preferred", r"preferred skills?", r"good to have", r"nice to have", r"nice-to-have", r"preferred qualifications?", r"nice to have skills?"],
    "qualifications": [r"qualifications?", r"education", r"education requirements?", r"educational qualifications?", r"qualification requirements?"],
    "responsibilities": [r"responsibilities?", r"responsibility", r"what you will do", r"what you'll do", r"role responsibilities?", r"your responsibilities?"],
    "experience": [r"experience", r"experience level", r"years of experience"],
}


def normalize_skill(token: str) -> str:
    token = token.strip().lower()
    if token in SKILL_NORMALIZATION:
        return SKILL_NORMALIZATION[token]
    if token == "node":
        return "Node.js"
    return token.title()


def is_section_header(line: str) -> str:
    header = line.strip().lower().rstrip(":")
    for section, patterns in SECTION_PATTERNS.items():
        for pattern in patterns:
            if re.fullmatch(pattern, header) or header.startswith(pattern):
                return section
    return ""


def parse_sections(text: str) -> Dict[str, List[str]]:
    sections = {key: [] for key in SECTION_PATTERNS}
    current = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        header = is_section_header(line)
        if header:
            current = header
            # capture same-line section content after a colon
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) > 1 and parts[1].strip():
                    sections[current].append(parts[1].strip())
            continue
        if current:
            sections[current].append(line)
    return sections


def extract_section_text(lines: List[str]) -> str:
    return "\n".join(lines).strip()


def find_skills_in_text(text: str, terms: List[str]) -> List[str]:
    normalized = text.lower()
    found = set()
    for term in terms:
        term = term.lower()
        if term == "r":
            if re.search(r"\br\s+(programming|language)\b", normalized):
                found.add("R")
            continue
        if re.search(rf"\b{re.escape(term)}\b", normalized):
            found.add(normalize_skill(term))
    return sorted(found)


def extract_experience(text: str) -> str:
    normalized = text.lower()
    for label, pattern in EXPERIENCE_PATTERNS:
        if re.search(pattern, normalized):
            return label
    for pattern in YEAR_PATTERNS:
        match = re.search(pattern, normalized)
        if match:
            return f"{match.group(1)}+ years"
    return "Not specified"


def extract_education(text: str) -> str:
    normalized = text.lower()
    for level in EDUCATION_LEVELS:
        if re.search(rf"\b{re.escape(level)}\b", normalized):
            if level == "bachelor":
                return "Bachelor's"
            if level == "master":
                return "Master's"
            if level == "phd":
                return "PhD"
            return level.title()
    if re.search(r"\bbachelor.*degree\b", normalized):
        return "Bachelor's"
    if re.search(r"\bmaster.*degree\b", normalized):
        return "Master's"
    return "Not specified"


def extract_responsibilities(text: str) -> List[str]:
    sections = parse_sections(text)
    lines = sections.get("responsibilities", [])
    if not lines:
        sentence_matches = re.findall(r"([^.?!]*\b(responsib|responsible|responsibilities)\b[^.?!]*[.?!])", text, re.I)
        if sentence_matches:
            return [match[0].strip() for match in sentence_matches][:8]
        lines = [line.strip() for line in text.splitlines() if re.match(r"^\s*[-*•]", line)]
    responsibilities = []
    for line in lines:
        clean_line = re.sub(r"^\s*[-*•]+\s*", "", line).strip()
        if not clean_line:
            continue
        if re.match(r"^(responsibilities|responsibility|requirements|preferred|qualifications|experience|skills?)[:\-]?", clean_line.lower()):
            continue
        responsibilities.append(clean_line)
        if len(responsibilities) >= 8:
            break
    return responsibilities


def extract_keywords(text: str) -> List[str]:
    tokens = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+\-]*\b", text.lower())
    keywords = []
    for token in tokens:
        if token in STOPWORDS or len(token) == 1:
            continue
        if token.isdigit():
            continue
        if token.startswith("r") and token == "r":
            continue
        keywords.append(token)
    return sorted({token for token in keywords})[:20]


def analyze_job_description(job_description: str) -> Dict:
    sections = parse_sections(job_description)
    required_section = extract_section_text(sections.get("required", []))
    preferred_section = extract_section_text(sections.get("preferred", []))
    qualification_section = extract_section_text(sections.get("qualifications", []))
    experience_section = extract_section_text(sections.get("experience", []))

    required_skills = find_skills_in_text(required_section, REQUIRED_SKILL_TERMS) if required_section else []
    preferred_skills = find_skills_in_text(preferred_section, PREFERRED_SKILL_TERMS) if preferred_section else []
    experience = extract_experience(experience_section or job_description)
    education = extract_education(qualification_section or job_description)
    responsibilities = extract_responsibilities(job_description)
    keywords = extract_keywords(job_description)
    tools_frameworks = sorted(set(required_skills + preferred_skills))[:12]

    return {
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "experience_level": experience,
        "education_requirement": education,
        "responsibilities": responsibilities,
        "tools_frameworks": tools_frameworks,
        "keywords": keywords,
    }
