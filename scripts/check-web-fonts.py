#!/usr/bin/env python3
"""Check defaults against Typst's live web font inventory (requires msgpack)."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

import msgpack

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://typst.app/assets/font-derived/font-index.mpk"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, help="Use a previously downloaded MessagePack index")
    parser.add_argument("--output", type=Path, default=ROOT / "build/web-fonts-audit.json")
    args = parser.parse_args()
    if args.index:
        raw = args.index.read_bytes()
    else:
        with urllib.request.urlopen(SOURCE, timeout=45) as response:
            raw = response.read()
    index = msgpack.unpackb(raw, raw=False)
    result = subprocess.run(
        ["typst", "eval", '{ import "src/fonts.typ": default-fonts; default-fonts }', "--root", str(ROOT)],
        cwd=ROOT, check=True, text=True, capture_output=True,
    )
    defaults = json.loads(result.stdout)
    families = {}
    for role, family in defaults.items():
        rows = [dict(file=name, style=info[1][0], weight=info[1][1], stretch=info[1][2], index=info[2])
                for name, info in index if info[0] == family]
        available = {(row["style"], row["weight"]) for row in rows}
        required = {("normal", 400), ("normal", 700)}
        if role in ("english", "mono"):
            required |= {("italic", 400), ("italic", 700)}
        assert required <= available, f"Missing faces for {role}: {family}: {required - available}"
        families[family] = dict(role=role, faces=rows)
        print(f"PASS {role}: {family} ({len(rows)} faces)")
    report = dict(
        source=SOURCE,
        checked_at=datetime.now(timezone.utc).isoformat(),
        index_sha256=hashlib.sha256(raw).hexdigest(),
        font_families=families,
        scope="Live web inventory and required faces; not an interactive web-editor compilation.",
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
