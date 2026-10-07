#!/usr/bin/env python3
"""Fetch public profile statistics from GitHub's REST API, without credentials."""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "stats.json"


def get_json(url: str) -> object:
    request = Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "RealKazbek-profile-readme/1.0"})
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default="RealKazbek")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    user = get_json(f"https://api.github.com/users/{args.username}")
    repos = get_json(f"https://api.github.com/users/{args.username}/repos?per_page=100&type=owner")
    if not isinstance(user, dict) or not isinstance(repos, list):
        raise RuntimeError("Unexpected GitHub API response")
    payload = {
        "username": args.username,
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "public_repositories": user["public_repos"],
        "followers": user["followers"],
        "following": user["following"],
        "stars_received": sum(repo.get("stargazers_count", 0) for repo in repos),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote public statistics to {args.output}")


if __name__ == "__main__":
    main()
