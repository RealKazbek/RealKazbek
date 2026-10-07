#!/usr/bin/env python3
"""Render a small terminal statistics panel from locally fetched public data."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stats", type=Path, default=ROOT / "data" / "stats.json")
    parser.add_argument("--contributions", type=Path, default=ROOT / "data" / "contributions.json")
    parser.add_argument("--output", type=Path, default=ROOT / "assets" / "stats.svg")
    args = parser.parse_args()
    stats = json.loads(args.stats.read_text(encoding="utf-8"))
    contributions = json.loads(args.contributions.read_text(encoding="utf-8"))
    values = [
        ("public repositories", stats["public_repositories"]),
        ("followers", stats["followers"]),
        ("stars received", stats["stars_received"]),
        ("contributions / year", contributions["total_contributions"] if contributions["total_contributions"] is not None else "unavailable"),
    ]
    rows = "".join(
        f'<text class="label row" x="25" y="{57 + index * 24}">{html.escape(label)}</text>'
        f'<text class="value row" x="305" y="{57 + index * 24}">{html.escape(str(value))}</text>'
        for index, (label, value) in enumerate(values)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 450 160" role="img" aria-labelledby="title desc">
<title id="title">RealKazbek public GitHub statistics</title><desc id="desc">Public repositories, followers, stars received, and annual contributions.</desc>
<style><![CDATA[text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:14px}}.shell{{fill:#0b0f10;stroke:#293235}}.label{{fill:#8b9994}}.value{{fill:#e8f2ec}}.row{{opacity:0;animation:print .35s ease-out forwards}}.row:nth-of-type(2){{animation-delay:.12s}}.row:nth-of-type(3){{animation-delay:.24s}}.row:nth-of-type(4){{animation-delay:.36s}}.row:nth-of-type(5){{animation-delay:.48s}}@keyframes print{{from{{opacity:0;transform:translateX(5px)}}to{{opacity:1;transform:none}}}}@media(prefers-reduced-motion:reduce){{.row{{animation:none;opacity:1}}}}]]></style>
<rect class="shell" x=".5" y=".5" width="449" height="159" rx="9"/><text x="24" y="30" fill="#83f0b2">kazbek@github:~$ ./stats</text><line x1="24" y1="39" x2="426" y2="39" stroke="#293235"/>{rows}</svg>'''
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
