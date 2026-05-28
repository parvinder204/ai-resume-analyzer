from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import ClassVar

import spacy
from spacy.matcher import PhraseMatcher
from loguru import logger


SKILL_TAXONOMY: dict[str, list[str]] = {
    "Programming Languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust",
        "Swift", "Kotlin", "Ruby", "PHP", "Scala", "R", "MATLAB", "Dart", "Perl",
        "Haskell", "Elixir", "Julia",
    ],
    "Web Frameworks": [
        "React", "Angular", "Vue", "Next.js", "Nuxt", "Svelte", "Django", "Flask",
        "FastAPI", "Express", "NestJS", "Spring Boot", "Laravel", "Rails",
        "ASP.NET", "Remix",
    ],
    "Data & ML": [
        "TensorFlow", "PyTorch", "Keras", "scikit-learn", "XGBoost", "LightGBM",
        "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly", "Spark", "Hadoop",
        "Airflow", "dbt", "MLflow", "Hugging Face", "LangChain", "OpenAI",
        "Sentence Transformers", "BERT", "GPT", "LLM",
    ],
    "Databases": [
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "Cassandra",
        "DynamoDB", "SQLite", "Oracle", "SQL Server", "Snowflake", "BigQuery",
        "Neo4j", "InfluxDB", "Pinecone", "Weaviate",
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Ansible",
        "Jenkins", "GitHub Actions", "CI/CD", "Helm", "ArgoCD", "Prometheus",
        "Grafana", "Datadog", "Nginx", "Linux", "Bash",
    ],
    "Mobile": [
        "iOS", "Android", "React Native", "Flutter", "Xamarin", "Ionic",
    ],
    "Soft Skills": [
        "Leadership", "Communication", "Teamwork", "Problem Solving",
        "Critical Thinking", "Agile", "Scrum", "Project Management",
        "Mentoring", "Collaboration", "Adaptability",
    ],
    "Tools": [
        "Git", "GitHub", "GitLab", "Jira", "Confluence", "Figma", "Postman",
        "VS Code", "IntelliJ", "Vim", "Jupyter", "Tableau", "Power BI",
    ],
}

_SKILL_CANONICAL: dict[str, str] = {
    s.lower(): s
    for skills in SKILL_TAXONOMY.values()
    for s in skills
}

_ALIASES: dict[str, str] = {
    "js":       "JavaScript",
    "ts":       "TypeScript",
    "py":       "Python",
    "k8s":      "Kubernetes",
    "tf":       "TensorFlow",
    "sk-learn": "scikit-learn",
    "sklearn":  "scikit-learn",
    "nlp":      "NLP",
    "ml":       "Machine Learning",
    "dl":       "Deep Learning",
    "cv":       "Computer Vision",
    "gcp":      "GCP",
    "aws":      "AWS",
    "pg":       "PostgreSQL",
    "psql":     "PostgreSQL",
    "mongo":    "MongoDB",
    "es":       "Elasticsearch",
}


@dataclass
class ExtractedSkills:
    by_category: dict[str, list[str]] = field(default_factory=dict)
    all_skills:  list[str]            = field(default_factory=list)
    raw_matches: set[str]             = field(default_factory=set)

    @property
    def total(self) -> int:
        return len(self.all_skills)


@lru_cache(maxsize=1)
def _load_nlp() -> spacy.language.Language:
    try:
        nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        logger.info("spaCy model loaded.")
        return nlp
    except OSError:
        logger.warning("spaCy model not found — using blank en model.")
        return spacy.blank("en")


@lru_cache(maxsize=1)
def _build_matcher(nlp: spacy.language.Language) -> PhraseMatcher:
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    all_skills = [s for skills in SKILL_TAXONOMY.values() for s in skills]
    patterns   = list(nlp.pipe(all_skills))
    matcher.add("SKILLS", patterns)
    return matcher


def extract_skills(text: str) -> ExtractedSkills:
    nlp     = _load_nlp()
    matcher = _build_matcher(nlp)
    doc     = nlp(text[:100_000])  

    found: set[str] = set()

    for _, start, end in matcher(doc):
        span = doc[start:end].text
        canonical = _SKILL_CANONICAL.get(span.lower(), span)
        found.add(canonical)

    text_lower = text.lower()
    for alias, canonical in _ALIASES.items():
        pattern = rf"\b{re.escape(alias)}\b"
        if re.search(pattern, text_lower):
            found.add(canonical)

    for skill_lower, canonical in _SKILL_CANONICAL.items():
        if canonical not in found and skill_lower in text_lower:
            found.add(canonical)

    by_cat: dict[str, list[str]] = {}
    categorised: set[str]        = set()

    for category, skills in SKILL_TAXONOMY.items():
        matched = [s for s in skills if s in found]
        if matched:
            by_cat[category] = sorted(matched)
            categorised.update(matched)

    uncategorised = found - categorised
    if uncategorised:
        by_cat["Other"] = sorted(uncategorised)

    return ExtractedSkills(
        by_category=by_cat,
        all_skills=sorted(found),
        raw_matches=found,
    )


def compare_skills(
    resume_skills: set[str],
    job_skills: set[str],
) -> dict[str, list[str]]:
    return {
        "matched": sorted(resume_skills & job_skills),
        "missing": sorted(job_skills - resume_skills),
        "bonus":   sorted(resume_skills - job_skills),
    }
