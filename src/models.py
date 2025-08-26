from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Company:
    name: str
    careers_url: Optional[str] = None
    ats: Optional[str] = None  # greenhouse|lever|workday|unknown
    slug: Optional[str] = None  # greenhouse/lever org slug if known
