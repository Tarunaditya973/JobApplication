from __future__ import annotations

import json
from typing import Dict, Iterable, List, Optional

import sys

try:
    import yaml  # type: ignore
except Exception as _e:  # noqa: N816
    yaml = None  # type: ignore

from .config import AppConfig
from .models import Company
from . import jobs as jobs_pkg  # will import providers via __init__
from .emailer import EmailSender
from .people import PeopleLookup


def _load_companies(path: str) -> List[Company]:
    if yaml is None:
        raise RuntimeError("PyYAML not installed. Add it to requirements and install.")
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    items = raw.get("companies", [])
    companies: List[Company] = []
    for item in items:
        companies.append(
            Company(
                name=str(item.get("name")),
                careers_url=item.get("careers_url"),
                ats=item.get("ats"),
                slug=item.get("slug"),
            )
        )
    return companies


SENIOR_TITLE_KEYWORDS = (
    "senior",
    "sr.",
    "staff",
    "principal",
    "lead ",
    "leader",
    "manager",
    "director",
    "head ",
)


def _parse_years_experience(text: str) -> Optional[int]:
    import re

    # Look for patterns like '3+ years', '3-5 years', 'at least 4 years'
    m = re.search(r"(\d+)\s*\+?\s*years", text, re.IGNORECASE)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            return None
    m = re.search(r"(\d+)\s*[-to]{1,3}\s*(\d+)\s*years", text, re.IGNORECASE)
    if m:
        try:
            low = int(m.group(1))
            high = int(m.group(2))
            return low
        except Exception:
            return None
    return None


def _filter_postings(postings: List[Dict], keywords: Optional[str], location_filter: Optional[str], *, exclude_senior_titles: bool = True, max_years_experience: Optional[int] = None) -> List[Dict]:
    if not postings:
        return []
    keyword_terms = [k.strip().lower() for k in (keywords or "").split(",") if k.strip()]
    location_terms = [l.strip().lower() for l in (location_filter or "").split(",") if l.strip()]

    def tokenize(text: str) -> set[str]:
        import re

        return set(re.findall(r"[a-z0-9]+", text.lower()))

    def matches(job: Dict) -> bool:
        title_lower = str(job.get("title", "")).lower()
        location_lower = str(job.get("location", "")).lower()
        description_lower = str(job.get("description", "")).lower()

        # OR across title keywords
        if keyword_terms and not any(term in title_lower for term in keyword_terms):
            return False

        # OR across location terms
        if location_terms:
            location_tokens = tokenize(location_lower)

            def location_term_matches(term: str) -> bool:
                # For very short terms (<=3), require exact token match to avoid false positives like 'in' in 'dublin'
                if len(term) <= 3:
                    return term in location_tokens
                # Otherwise allow substring match for fuzzy cases like 'banglore'
                return term in location_lower

            if not any(location_term_matches(term) for term in location_terms):
                return False

        # Exclude senior titles if requested
        if exclude_senior_titles and any(sen in title_lower for sen in SENIOR_TITLE_KEYWORDS):
            return False

        # Cap by years of experience if provided (based on description text)
        if max_years_experience is not None:
            yrs = _parse_years_experience(description_lower)
            if yrs is not None and yrs > max_years_experience:
                return False

        return True

    return [j for j in postings if matches(j)]


def run_once(companies_file: str, config: AppConfig, dry_run: bool = False) -> bool:
    companies = _load_companies(companies_file)
    if not companies:
        print("No companies found in companies file.", file=sys.stderr)
        return False

    # Initialize helpers
    emailer = EmailSender(config.email)
    people = PeopleLookup()
    jobs_client = jobs_pkg.JobFetcher()

    all_results: List[Dict] = []
    for company in companies:
        postings = jobs_client.fetch_company_jobs(company)
        filtered = _filter_postings(
            postings,
            config.default_keywords,
            config.location_filter,
            exclude_senior_titles=config.exclude_senior_titles,
            max_years_experience=config.max_years_experience,
        )
        contacts = people.find_contacts(company.name) if filtered else []
        if filtered:
            all_results.append(
                {
                    "company": company.name,
                    "job_count": len(filtered),
                    "jobs": filtered,
                    "contacts": contacts,
                }
            )

    if not all_results:
        print("No matching jobs found.")
        return True

    subject = "Job openings report"
    body = json.dumps(all_results, indent=2)
    emailer.send(subject=subject, body=body, dry_run=dry_run)
    return True


