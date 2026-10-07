#!/usr/bin/env python3
"""Fetch RealKazbek's public GitHub contribution calendar without credentials."""
from __future__ import annotations
import argparse, datetime as dt, json, re, sys
from pathlib import Path
from urllib.request import Request, urlopen
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "contributions.json"
def parse_days(html: str) -> list[dict[str, object]]:
    pattern = re.compile(r'<(?:td|rect)\b(?=[^>]*\bdata-date="(?P<date>\d{4}-\d{2}-\d{2})")(?=[^>]*\bdata-level="(?P<level>[0-4])")[^>]*>', re.I)
    days = [{"date": m["date"], "level": int(m["level"])} for m in pattern.finditer(html)]
    return sorted({day["date"]: day for day in days}.values(), key=lambda day: day["date"])
def main() -> int:
    p = argparse.ArgumentParser(description=__doc__); p.add_argument("--username", default="RealKazbek"); p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT); args = p.parse_args()
    try:
        request = Request(f"https://github.com/users/{args.username}/contributions", headers={"User-Agent":"RealKazbek-profile-readme/1.0","Accept":"text/html"})
        with urlopen(request, timeout=30) as response:
            source = response.read().decode("utf-8", "replace")
        days = parse_days(source)
    except Exception as error:
        print(f"Could not fetch contribution data: {error}", file=sys.stderr); return 1
    if not days: print("GitHub returned no parseable contribution days.", file=sys.stderr); return 1
    total_match = re.search(r">\s*([\d,]+)\s*contributions\s*in the last year", source, re.I)
    payload = {
        "username": args.username,
        "source": f"https://github.com/users/{args.username}/contributions",
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "total_contributions": int(total_match.group(1).replace(",", "")) if total_match else None,
        "days": days,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(days)} days to {args.output}"); return 0
if __name__ == "__main__": raise SystemExit(main())
