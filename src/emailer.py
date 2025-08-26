from __future__ import annotations

import json
import os
import smtplib
from email.mime.text import MIMEText
from typing import Optional

from .config import EmailConfig


class EmailSender:
    def __init__(self, cfg: EmailConfig) -> None:
        self.cfg = cfg

    def _send_via_sendgrid(self, subject: str, body: str) -> bool:
        import requests

        if not (self.cfg.sendgrid_api_key and self.cfg.sender and self.cfg.recipients):
            return False
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {self.cfg.sendgrid_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "personalizations": [
                {
                    "to": [{"email": r.strip()} for r in self.cfg.recipients.split(",")],
                }
            ],
            "from": {"email": self.cfg.sender},
            "subject": subject,
            "content": [{"type": "text/plain", "value": body}],
        }
        try:
            resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
            return 200 <= resp.status_code < 300
        except Exception:
            return False

    def _send_via_smtp(self, subject: str, body: str) -> bool:
        if not (self.cfg.smtp_host and self.cfg.sender and self.cfg.recipients):
            return False
        message = MIMEText(body, _subtype="plain", _charset="utf-8")
        message["Subject"] = subject
        message["From"] = self.cfg.sender
        message["To"] = self.cfg.recipients
        try:
            server = smtplib.SMTP(self.cfg.smtp_host, self.cfg.smtp_port or 25, timeout=15)
            if self.cfg.smtp_use_tls:
                server.starttls()
            if self.cfg.smtp_username and self.cfg.smtp_password:
                server.login(self.cfg.smtp_username, self.cfg.smtp_password)
            server.sendmail(self.cfg.sender, [r.strip() for r in self.cfg.recipients.split(",")], message.as_string())
            server.quit()
            return True
        except Exception:
            return False

    def send(self, subject: str, body: str, dry_run: bool = False) -> bool:
        if dry_run:
            print(body)
            return True
        # Prefer SendGrid if configured
        if self._send_via_sendgrid(subject, body):
            return True
        # Fallback to SMTP
        if self._send_via_smtp(subject, body):
            return True
        # Last resort: write to file for visibility
        try:
            with open("job_report.txt", "w", encoding="utf-8") as f:
                f.write(body)
            return True
        except Exception:
            return False


