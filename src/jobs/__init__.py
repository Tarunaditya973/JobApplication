from __future__ import annotations

from typing import Dict, List

from ..runner import Company
from .greenhouse import fetch_greenhouse_jobs
from .lever import fetch_lever_jobs


class JobFetcher:
    def fetch_company_jobs(self, company: Company) -> List[Dict]:
        ats = (company.ats or "").lower()
        if ats == "greenhouse":
            return fetch_greenhouse_jobs(company)
        if ats == "lever":
            return fetch_lever_jobs(company)
        # Unknown ATS: return empty for now (we can add Workday or discovery later)
        return []


