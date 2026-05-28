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

