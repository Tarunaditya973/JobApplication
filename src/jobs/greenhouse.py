from __future__ import annotations

import requests
from typing import Dict, List

from ..models import Company


def fetch_greenhouse_jobs(company: Company) -> List[Dict]:
    if not company.slug:
        return []
    # Greenhouse API: https://boards-api.greenhouse.io/v1/boards/{slug}/jobs
    url = f"https://boards-api.greenhouse.io/v1/boards/{company.slug}/jobs?content=true"
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json() or {}
        jobs = data.get("jobs", [])
        normalized: List[Dict] = []
        for j in jobs:
            content = (j.get("content") or "")
            normalized.append(
                {
                    "title": j.get("title"),
                    "location": (j.get("location") or {}).get("name"),
                    "url": j.get("absolute_url"),
                    "department": (j.get("departments") or [{}])[0].get("name"),
                    "remote": j.get("location", {}).get("name", "").lower().find("remote") != -1,
                    "description": content,
                }
            )
        return normalized
    except Exception:
        return []


