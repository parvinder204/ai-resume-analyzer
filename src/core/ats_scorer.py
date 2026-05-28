from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from loguru import logger


class Strictness(str, Enum):
    LENIENT  = "Lenient"
    BALANCED = "Balanced"
    STRICT   = "Strict"

_WEIGHTS: dict[str, dict[str, float]] = {
    Strictness.LENIENT: {
        "keyword_match":    0.30,
        "formatting":       0.15,
        "sections":         0.20,
        "length":           0.10,
        "contact_info":     0.10,
        "action_verbs":     0.10,
        "quantification":   0.05,
    },
    Strictness.BALANCED: {
        "keyword_match":    0.35,
        "formatting":       0.15,
        "sections":         0.20,
        "length":           0.10,
        "contact_info":     0.08,
        "action_verbs":     0.07,
        "quantification":   0.05,
    },
    Strictness.STRICT: {
        "keyword_match":    0.40,
        "formatting":       0.15,
        "sections":         0.18,
        "length":           0.08,
        "contact_info":     0.07,
        "action_verbs":     0.07,
        "quantification":   0.05,
    },
}

_EXPECTED_SECTIONS = [
    "experience", "education", "skills", "summary", "objective",
    "projects", "certifications", "achievements", "publications",
]

_ACTION_VERBS = [
    "achieved", "built", "created", "delivered", "designed", "developed",
    "drove", "engineered", "established", "executed", "generated", "improved",
    "increased", "launched", "led", "managed", "optimised", "optimized",
    "reduced", "spearheaded", "streamlined", "transformed",
]

_CONTACT_PATTERNS = {
    "email":   r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone":   r"(\+?\d[\d\s\-().]{7,}\d)",
    "linkedin": r"linkedin\.com/in/",
    "github":  r"github\.com/",
}

_FORMAT_RED_FLAGS = [
    r"\[image\]", r"<img", r"\.png", r"\.jpg",
    r"header", r"footer", r"\|{3,}",
]


@dataclass
class DimensionScore:
    name:    str
    score:   float      
    weight:  float
    notes:   list[str] = field(default_factory=list)

    @property
    def weighted(self) -> float:
        return self.score * self.weight


@dataclass
class ATSResult:
    total_score:  float
    grade:        str
    dimensions:   list[DimensionScore]
    keyword_hits: list[str]
    suggestions:  list[str]

    @property
    def color(self) -> str:
        if self.total_score >= 80: return "green"
        if self.total_score >= 60: return "orange"
        return "red"


def compute_ats_score(
    resume_text: str,
    job_text: str,
    matched_skills: list[str],
    missing_skills: list[str],
    strictness: Strictness = Strictness.BALANCED,
) -> ATSResult:
    weights   = _WEIGHTS[strictness]
    text_low  = resume_text.lower()
    job_low   = job_text.lower()
    dimensions: list[DimensionScore] = []

    total_skills = len(matched_skills) + len(missing_skills)
    kw_score     = (len(matched_skills) / max(total_skills, 1)) * 100
    kw_notes     = [f"{len(matched_skills)}/{total_skills} required skills matched"]
    if missing_skills:
        kw_notes.append(f"Missing: {', '.join(missing_skills[:5])}" +
                        (f" +{len(missing_skills)-5} more" if len(missing_skills) > 5 else ""))
    dimensions.append(DimensionScore("Keyword Match", kw_score, weights["keyword_match"], kw_notes))

    fmt_issues = [p for p in _FORMAT_RED_FLAGS if re.search(p, text_low)]
    fmt_score  = max(0, 100 - len(fmt_issues) * 20)
    fmt_notes  = ["Clean text format detected"] if not fmt_issues else [f"Format issue: {p}" for p in fmt_issues]
    dimensions.append(DimensionScore("Formatting", fmt_score, weights["formatting"], fmt_notes))

    found_sections = [s for s in _EXPECTED_SECTIONS if s in text_low]
    sec_score = min(100, (len(found_sections) / 5) * 100)
    sec_notes = [f"Sections found: {', '.join(found_sections)}"]
    missing_sec = set(_EXPECTED_SECTIONS[:5]) - set(found_sections)
    if missing_sec:
        sec_notes.append(f"Consider adding: {', '.join(missing_sec)}")
    dimensions.append(DimensionScore("Section Structure", sec_score, weights["sections"], sec_notes))

    word_count = len(resume_text.split())
    if   400 <= word_count <= 800:  len_score = 100
    elif 300 <= word_count < 400:   len_score = 80
    elif 800 < word_count <= 1200:  len_score = 85
    elif word_count < 300:          len_score = 50
    else:                           len_score = 60
    dimensions.append(DimensionScore(
        "Length", len_score, weights["length"],
        [f"{word_count} words — {'ideal' if len_score == 100 else 'consider adjusting to 400–800 words'}"]
    ))

    contact_found  = {k: bool(re.search(p, resume_text)) for k, p in _CONTACT_PATTERNS.items()}
    contact_score  = (sum(contact_found.values()) / len(contact_found)) * 100
    contact_notes  = [f"{'✓' if v else '✗'} {k.title()}" for k, v in contact_found.items()]
    dimensions.append(DimensionScore("Contact Info", contact_score, weights["contact_info"], contact_notes))

    verb_hits = [v for v in _ACTION_VERBS if v in text_low]
    verb_score = min(100, len(verb_hits) * 10)
    dimensions.append(DimensionScore(
        "Action Verbs", verb_score, weights["action_verbs"],
        [f"{len(verb_hits)} power verbs found: {', '.join(verb_hits[:5])}"]
    ))

    quant_hits = re.findall(r"\b\d+\s*(%|x|times|users|customers|projects|million|k\b)", text_low)
    quant_score = min(100, len(quant_hits) * 20)
    dimensions.append(DimensionScore(
        "Quantification", quant_score, weights["quantification"],
        [f"{len(quant_hits)} measurable achievements found"]
    ))

    total = sum(d.weighted for d in dimensions)

    return ATSResult(
        total_score  = round(total, 1),
        grade        = _grade(total),
        dimensions   = dimensions,
        keyword_hits = matched_skills,
        suggestions  = _generate_suggestions(dimensions, missing_skills),
    )


def _grade(score: float) -> str:
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B+"
    if score >= 60: return "B"
    if score >= 50: return "C"
    return "D"


def _generate_suggestions(
    dimensions: list[DimensionScore],
    missing_skills: list[str],
) -> list[str]:
    suggestions: list[str] = []

    for dim in sorted(dimensions, key=lambda d: d.score):
        if dim.score < 60:
            if dim.name == "Keyword Match" and missing_skills:
                suggestions.append(
                    f"Add missing skills to your resume: {', '.join(missing_skills[:8])}"
                )
            elif dim.name == "Action Verbs":
                suggestions.append(
                    "Start bullet points with strong action verbs like 'Engineered', 'Led', 'Optimised'."
                )
            elif dim.name == "Quantification":
                suggestions.append(
                    "Quantify achievements — e.g. 'Reduced load time by 40%' or 'Managed team of 8'."
                )
            elif dim.name == "Section Structure":
                suggestions.append(
                    "Include dedicated sections for: Experience, Skills, Education, and a Summary."
                )
            elif dim.name == "Contact Info":
                suggestions.append(
                    "Ensure email, phone, and LinkedIn profile are clearly visible at the top."
                )
            elif dim.name == "Length":
                suggestions.append(
                    "Aim for 400–800 words (1–2 pages). Trim redundant content or expand thin sections."
                )

    if not suggestions:
        suggestions.append("Your resume is well-optimised! Consider tailoring keywords for each specific role.")

    return suggestions
