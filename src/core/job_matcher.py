from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Optional

import numpy as np
from loguru import logger
from sentence_transformers import SentenceTransformer, util


_MODEL_NAME = "all-MiniLM-L6-v2"   

@dataclass
class JobMatch:
    job_id:            str
    title:             str
    company:           str
    location:          str
    description:       str
    required_skills:   list[str]
    salary_range:      str
    similarity_score:  float
    matched_skills:    list[str] = field(default_factory=list)
    missing_skills:    list[str] = field(default_factory=list)

    @property
    def match_tier(self) -> str:
        if self.similarity_score >= 80: return "Excellent"
        if self.similarity_score >= 65: return "Strong"
        if self.similarity_score >= 50: return "Good"
        return "Fair"

    @property
    def tier_color(self) -> str:
        return {"Excellent": "green", "Strong": "green",
                "Good": "orange", "Fair": "red"}[self.match_tier]


@lru_cache(maxsize=1)
def _load_model() -> SentenceTransformer:
    logger.info(f"Loading SentenceTransformer '{_MODEL_NAME}' …")
    model = SentenceTransformer(_MODEL_NAME)
    logger.info("Model ready.")
    return model


def embed(texts: list[str]) -> np.ndarray:
    model = _load_model()
    return model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)


def match_jobs(
    resume_text: str,
    resume_skills: set[str],
    jobs: list[dict],
    top_k: int = 5,
) -> list[JobMatch]:
    
    if not jobs:
        return []

    model = _load_model()

    job_texts = [
        f"{j['title']} at {j['company']}. {j['description']} Skills: {', '.join(j.get('required_skills', []))}"
        for j in jobs
    ]

    all_texts    = [resume_text[:2048]] + job_texts    
    embeddings   = embed(all_texts)
    resume_emb   = embeddings[0:1]
    job_embs     = embeddings[1:]

    scores: np.ndarray = (resume_emb @ job_embs.T).flatten() * 100

    top_indices = np.argsort(scores)[::-1][:top_k]

    results: list[JobMatch] = []
    for idx in top_indices:
        job    = jobs[idx]
        jskills = set(job.get("required_skills", []))
        results.append(
            JobMatch(
                job_id           = job.get("id", str(idx)),
                title            = job["title"],
                company          = job["company"],
                location         = job.get("location", "Remote"),
                description      = job["description"],
                required_skills  = sorted(jskills),
                salary_range     = job.get("salary_range", "Competitive"),
                similarity_score = round(float(scores[idx]), 1),
                matched_skills   = sorted(resume_skills & jskills),
                missing_skills   = sorted(jskills - resume_skills),
            )
        )

    return results


def compare_resumes(
    resumes: list[tuple[str, str]],   
    job_text: str,
) -> list[tuple[str, float]]:
    texts    = [job_text] + [r[1] for r in resumes]
    embs     = embed(texts)
    job_emb  = embs[0:1]
    res_embs = embs[1:]
    scores   = (job_emb @ res_embs.T).flatten() * 100

    ranked = sorted(
        [(resumes[i][0], round(float(scores[i]), 1)) for i in range(len(resumes))],
        key=lambda x: x[1],
        reverse=True,
    )
    return ranked
