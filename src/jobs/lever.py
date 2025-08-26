from __future__ import annotations

import requests
from typing import Dict, List

from ..models import Company


def fetch_lever_jobs(company: Company) -> List[Dict]:
    if not company.slug:
        return []
    # Lever API: https://api.lever.co/v0/postings/{slug}?mode=json
    url = f"https://api.lever.co/v0/postings/{company.slug}?mode=json"
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        jobs = resp.json() or []
        normalized: List[Dict] = []
        for j in jobs:
            categories = j.get("categories") or {}
            description = j.get("descriptionPlain") or j.get("description") or ""
            normalized.append(
                {
                    "title": j.get("text"),
                    "location": categories.get("location"),
                    "url": j.get("hostedUrl") or j.get("applyUrl"),
                    "department": categories.get("team"),
                    "remote": (categories.get("location") or "").lower().find("remote") != -1,
                    "description": description,
                }
            )
        return normalized
    except Exception:
        return []


