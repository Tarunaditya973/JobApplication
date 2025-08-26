## JobApplication CLI

Fetch job openings from company ATS (Greenhouse/Lever), optionally find contacts, and send a report via email.

### Quick start

1. Create and activate a Python 3.10+ virtualenv.
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Prepare a `companies.yml` based on `companies.sample.yml`:

```
cp companies.sample.yml companies.yml
# Edit companies.yml and set each company's ats and slug
```

4. Configure env vars (copy `.env.example` if available, or export manually):

```
export DEFAULT_KEYWORDS="SRE,Site Reliability,Platform,DevOps"
export LOCATION_FILTER="Remote"
export EMAIL_SENDER="you@example.com"
export EMAIL_RECIPIENTS="you@example.com"
# Either SendGrid:r
export SENDGRID_API_KEY="..."
# Or SMTP:
export SMTP_HOST="smtp.example.com"
export SMTP_PORT=587
export SMTP_USERNAME="user"
export SMTP_PASSWORD="pass"
export SMTP_USE_TLS=true
```

5. Run (dry-run prints report to stdout):

```
python main.py --companies companies.yml --dry-run
```

6. Send email for real:

```
python main.py --companies companies.yml
```

### Companies file format

```
companies:
  - name: ExampleCo (Greenhouse)
    ats: greenhouse
    slug: exampleco
  - name: AnotherCorp (Lever)
    ats: lever
    slug: anothercorp
```

### Notes

- People lookup is stubbed; can integrate People Data Labs/Apollo/Clearbit next.
- More ATS providers (Workday) and career page discovery can be added as needed.


