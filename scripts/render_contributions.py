#!/usr/bin/env python3
"""Render public contribution levels as a compact terminal-themed animated SVG."""
from __future__ import annotations
import argparse, datetime as dt, html, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DEFAULT_INPUT=ROOT/"data"/"contributions.json"; DEFAULT_OUTPUT=ROOT/"assets"/"contributions.svg"; PALETTE=["#1b2225","#12352b","#1f6b4f","#31a66f","#83f0b2"]
def main() -> int:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--input",type=Path,default=DEFAULT_INPUT);p.add_argument("--output",type=Path,default=DEFAULT_OUTPUT);args=p.parse_args()
    data=json.loads(args.input.read_text(encoding="utf-8")); days={dt.date.fromisoformat(day["date"]):int(day["level"]) for day in data["days"]}
    first,last=min(days),max(days); start=first-dt.timedelta(days=(first.weekday()+1)%7); end=last+dt.timedelta(days=6-((last.weekday()+1)%7)); weeks=((end-start).days//7)+1
    cell,gap,left,top=10,3,56,48; width,height=max(620,left+weeks*(cell+gap)+22),178; cells=[]
    for date,level in days.items():
        offset=(date-start).days; week,weekday=divmod(offset,7); x,y=left+week*(cell+gap),top+weekday*(cell+gap); delay=.15+(week+weekday)*.018
        cells.append(f'<rect class="cell" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{PALETTE[min(4,level)]}" style="animation-delay:{delay:.2f}s"><title>{date.isoformat()}: level {level}</title></rect>')
    labels=[]; previous=None
    for week in range(weeks):
        date=start+dt.timedelta(days=week*7)
        if date.month != previous: labels.append(f'<text x="{left+week*(cell+gap)}" y="33">{html.escape(date.strftime("%b"))}</text>'); previous=date.month
    username=html.escape(data.get("username","RealKazbek")); generated=html.escape(data.get("generated_at","")); total=data.get("total_contributions")
    footer = f"{total:,} contributions in the last year" if isinstance(total, int) else f"public activity · refreshed {generated[:10]}"
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{username} GitHub activity terminal</title><desc id="desc">A custom 53-week GitHub contribution calendar generated from public contribution data.</desc><style><![CDATA[text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#aeb8b3;font-size:11px}}.shell{{fill:#0b0f10;stroke:#293235}}.cell{{opacity:0;transform:translateY(4px);animation:reveal .35s ease-out forwards}}.cursor{{animation:blink 1.1s steps(2,start) infinite}}@keyframes reveal{{to{{opacity:1;transform:translateY(0)}}}}@keyframes blink{{50%{{opacity:0}}}}@media(prefers-reduced-motion:reduce){{.cell{{animation:none;opacity:1;transform:none}}.cursor{{animation:none}}}}]]></style><rect class="shell" x=".5" y=".5" width="{width-1}" height="{height-1}" rx="10"/><circle cx="19" cy="18" r="4" fill="#83f0b2"/><text x="31" y="22" fill="#e7f3eb">kazbek@github:~$ ./contributions.sh</text><text class="cursor" x="259" y="22" fill="#83f0b2">▋</text>{''.join(labels)}<text x="17" y="56">Sun</text><text x="17" y="82">Tue</text><text x="17" y="108">Thu</text><text x="17" y="134">Sat</text>{''.join(cells)}<text x="18" y="163" fill="#697671">{footer}</text><text x="{width-154}" y="163" fill="#697671">less</text><rect x="{width-119}" y="154" width="10" height="10" rx="2" fill="#1b2225"/><rect x="{width-106}" y="154" width="10" height="10" rx="2" fill="#12352b"/><rect x="{width-93}" y="154" width="10" height="10" rx="2" fill="#1f6b4f"/><rect x="{width-80}" y="154" width="10" height="10" rx="2" fill="#31a66f"/><rect x="{width-67}" y="154" width="10" height="10" rx="2" fill="#83f0b2"/><text x="{width-48}" y="163" fill="#697671">more</text></svg>'''
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(svg+"\n",encoding="utf-8");print(f"Wrote {args.output}");return 0
if __name__=="__main__":raise SystemExit(main())
