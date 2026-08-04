#!/usr/bin/env python3
"""
TAST Artifact Grounding Gate (pan-thesis audit 2026-08-04, prosthesis item 1).

Artifacts-layer documents cite registry claim ids ("registry claims 33, 67",
"registry claim 83", "claims 1, 2, 96-101"). This gate extracts every such
citation from artifacts/*.md and asserts each id exists in
data/sources_registry_with_ci.csv. A phantom reference is a build failure.

The gate also fails if it finds fewer than MIN_CITATIONS citations (regex rot
or a grounding appendix that stopped citing ids would otherwise pass silently).

    python TAST/scripts/check_artifact_grounding.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from typing import List, Set

HERE = Path(__file__).resolve().parent
TAST_ROOT = HERE.parent
ARTIFACTS_DIR = TAST_ROOT / "artifacts"
REGISTRY_CSV = TAST_ROOT / "data" / "sources_registry_with_ci.csv"

# "registry claim 83" / "registry claims 33, 67" / "registry claims 1, 2, 96–101"
CITE_RE = re.compile(r"registry claims?\s+([\d][\d,\s\u2013\-]*)", re.IGNORECASE)
MIN_CITATIONS = 10


def _parse_ids(raw: str) -> List[int]:
    """Parse '33, 67' or '1, 2, 96–101' (en dash or hyphen ranges) into ids."""
    ids: List[int] = []
    for part in re.split(r"[,\s]+", raw.strip()):
        if not part:
            continue
        m = re.match(r"^(\d+)\s*[\u2013\-]\s*(\d+)$", part)
        if m:
            lo, hi = int(m.group(1)), int(m.group(2))
            ids.extend(range(lo, hi + 1))
        elif part.isdigit():
            ids.append(int(part))
    return ids


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    with open(REGISTRY_CSV, newline="", encoding="utf-8") as f:
        valid_ids: Set[int] = {
            int(row["claim_id"]) for row in csv.DictReader(f)
            if str(row.get("claim_id", "")).strip().isdigit()
        }

    cited: List[int] = []
    files_scanned = 0
    for md in sorted(ARTIFACTS_DIR.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        for m in CITE_RE.finditer(text):
            cited.extend(_parse_ids(m.group(1)))
        files_scanned += 1

    failures = []
    if len(cited) < MIN_CITATIONS:
        failures.append(
            f"only {len(cited)} registry citations found (< {MIN_CITATIONS}) — "
            f"grounding appendix may have stopped citing ids; check the regex "
            f"or restore the citations."
        )
    phantoms = sorted(set(c for c in cited if c not in valid_ids))
    if phantoms:
        failures.append(
            f"phantom registry claim id(s) cited in artifacts/*.md: {phantoms}. "
            f"Every cited id must exist in data/sources_registry_with_ci.csv."
        )

    if failures:
        print("artifact-grounding: FAIL")
        for f in failures:
            print("  " + f)
        return 1
    print("artifact-grounding: OK")
    print(f"  artifacts scanned: {files_scanned}; citations checked: {len(cited)}")
    print(f"  distinct ids cited: {len(set(cited))}; all present in registry ({len(valid_ids)} claims)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
