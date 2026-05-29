from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from loguru import logger

_JOBS_PATH = Path(__file__).parent.parent.parent / "data" / "sample_jobs" / "jobs.json"


def load_jobs(path: Optional[Path] = None) -> list[dict]:
    target = path or _JOBS_PATH
    try:
        with open(target, encoding="utf-8") as f:
            jobs = json.load(f)
        logger.info(f"Loaded {len(jobs)} jobs from {target}.")
        return jobs
    except FileNotFoundError:
        logger.warning(f"Jobs file not found at {target}. Returning empty list.")
        return []
    except json.JSONDecodeError as exc:
        logger.error(f"Malformed JSON: {exc}")
        return []


def parse_custom_job(text: str) -> dict:
    return {
        "id":              "custom_001",
        "title":           "Custom Job",
        "company":         "Provided by User",
        "location":        "See description",
        "salary_range":    "See description",
        "description":     text,
        "required_skills": [],   
    }
