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

