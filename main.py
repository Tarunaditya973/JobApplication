import argparse
import os
import sys
from typing import List

from pathlib import Path


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="JobApplication CLI: fetch job openings and notify"
    )
    parser.add_argument(
        "--companies",
        type=str,
        default="companies.yml",
        help="Path to companies YAML file (default: companies.yml)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not send emails; print output to stdout",
    )
    args = parser.parse_args(argv)

    companies_path = Path(args.companies)
    if not companies_path.exists():
        print(
            f"Companies file not found at {companies_path}. Create it based on companies.sample.yml.",
            file=sys.stderr,
        )
        return 2

    # Lazy imports so the script can start even if optional deps are missing
    try:
        from src.config import load_config
        from src.runner import run_once
    except Exception as e:  # noqa: BLE001
        print(f"Failed to import modules: {e}", file=sys.stderr)
        return 1

    config = load_config()
    result = run_once(companies_file=str(companies_path), config=config, dry_run=args.dry_run)
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())





