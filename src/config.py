from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


def _load_dotenv_if_present() -> None:
    try:
        from dotenv import load_dotenv  # type: ignore

        load_dotenv()
    except Exception:
        # Optional dependency
        pass


@dataclass(frozen=True)
class EmailConfig:
    sender: Optional[str]
    recipients: Optional[str]
    sendgrid_api_key: Optional[str]
    smtp_host: Optional[str]
    smtp_port: Optional[int]
    smtp_username: Optional[str]
    smtp_password: Optional[str]
    smtp_use_tls: bool


@dataclass(frozen=True)
class AppConfig:
    email: EmailConfig
    default_keywords: Optional[str]
    location_filter: Optional[str]
    exclude_senior_titles: bool
    max_years_experience: Optional[int]


def load_config() -> AppConfig:
    _load_dotenv_if_present()

    email = EmailConfig(
        sender=os.getenv("EMAIL_SENDER"),
        recipients=os.getenv("EMAIL_RECIPIENTS"),
        sendgrid_api_key=os.getenv("SENDGRID_API_KEY"),
        smtp_host=os.getenv("SMTP_HOST"),
        smtp_port=int(os.getenv("SMTP_PORT", "0")) or None,
        smtp_username=os.getenv("SMTP_USERNAME"),
        smtp_password=os.getenv("SMTP_PASSWORD"),
        smtp_use_tls=os.getenv("SMTP_USE_TLS", "true").lower() in {"1", "true", "yes", "on"},
    )

    return AppConfig(
        email=email,
        default_keywords=os.getenv("DEFAULT_KEYWORDS"),
        location_filter=os.getenv("LOCATION_FILTER"),
        exclude_senior_titles=os.getenv("EXCLUDE_SENIOR_TITLES", "true").lower()
        in {"1", "true", "yes", "on"},
        max_years_experience=(int(os.getenv("MAX_YEARS_EXPERIENCE", "0")) or None),
    )


