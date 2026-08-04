#!/usr/bin/env python3
"""
TAST Observable-Facts Parity Gate (pan-thesis audit 2026-08-04, finding 44).

surviving/observable_facts.md is hand-maintained prose that cites derived
confidence values. Before this gate existed it drifted: 21 of 26 values were
stale pre-v5.13 hand-assigned numbers, and legislative-facing artifacts cited
them as "derived." This gate keeps the prose honest:

  (a) every **[0.NNN]** value in observable_facts.md must belong to the scored
      yaml fact whose id is tagged on the same line, and must equal the
      derive_confidence.py output within 0.005;
  (b) unscored context entries must carry no numeric confidence and must be
      non_scoring in the yaml;
  (c) completeness: every scored fact with derived confidence >= 0.85 appears
      in the md (the file is the high-confidence subset; silent omission of a
      qualifying fact is a failure);
  (d) the header counts (total scored / high-confidence count) match the yaml.

    python TAST/scripts/check_observable_facts_parity.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAST_ROOT = HERE.parent
MODEL_DIR = TAST_ROOT / "model"
FACTS_YAML = TAST_ROOT / "data" / "observable_facts.yaml"
OBS_MD = TAST_ROOT / "surviving" / "observable_facts.md"

CONF_TOL = 0.005
HIGH_THRESHOLD = 0.85

# - **[0.996]** statement ... (`floor-01`)
SCORED_RE = re.compile(r"\*\*\[(\d\.\d+)\]\*\*(.*)\(`([A-Za-z0-9\-]+)`\)\s*$")
# unscored context line: - statement ... (`38`) — Source: ...
UNSCORED_RE = re.compile(r"^- .*\(`([A-Za-z0-9\-]+)`\)")
HEADER_TOTAL_RE = re.compile(r"Total scored facts:\s*(\d+)")
HEADER_HIGH_RE = re.compile(r"High confidence \(derived c ≥ 0\.85\):\s*(\d+)")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.path.insert(0, str(MODEL_DIR))
    import yaml  # noqa: E402
    import derive_confidence as dc  # noqa: E402

    spec = dc._load_spec()
    facts = yaml.safe_load(FACTS_YAML.read_text(encoding="utf-8"))["facts"]
    by_id = {str(f.get("id")): f for f in facts}

    scored_facts = [f for f in facts if not f.get("non_scoring") and not f.get("canonical_of")]
    derived = {}
    for f in scored_facts:
        fid = str(f.get("id"))
        c, _ = dc.score_fact(f, spec)
        derived[fid] = c

    failures = []
    md_text = OBS_MD.read_text(encoding="utf-8")
    lines = md_text.splitlines()

    # (a) every numeric confidence line matches its tagged fact's derived value
    md_scored_ids = set()
    n_checked = 0
    for i, line in enumerate(lines, start=1):
        m = SCORED_RE.search(line)
        if not m:
            continue
        listed, fid = float(m.group(1)), m.group(3)
        md_scored_ids.add(fid)
        n_checked += 1
        if fid not in by_id:
            failures.append(f"line {i}: tagged fact id `{fid}` not in observable_facts.yaml")
            continue
        if fid not in derived:
            failures.append(f"line {i}: `{fid}` carries a confidence value but is not scored in the yaml")
            continue
        if abs(derived[fid] - listed) > CONF_TOL:
            failures.append(
                f"line {i}: `{fid}` listed {listed:.3f} but derive_confidence gives "
                f"{derived[fid]:.3f} — update the md to the function's output"
            )

    # (b) unscored context entries: id known to yaml, non_scoring, no numeric confidence
    n_unscored = 0
    for i, line in enumerate(lines, start=1):
        if SCORED_RE.search(line) or not line.startswith("- "):
            continue
        m = UNSCORED_RE.search(line)
        if not m:
            continue
        fid = m.group(1)
        if re.search(r"\*\*\[\d\.\d+\]\*\*", line):
            failures.append(f"line {i}: unscored entry `{fid}` carries a numeric confidence")
            continue
        n_unscored += 1
        if fid not in by_id:
            failures.append(f"line {i}: unscored entry id `{fid}` not in observable_facts.yaml")
        elif not by_id[fid].get("non_scoring"):
            failures.append(
                f"line {i}: `{fid}` listed as unscored context but IS scored in the yaml "
                f"(derived {derived.get(fid, float('nan')):.3f}) — move it to a scored section"
            )

    # (c) completeness: every scored fact >= threshold appears in the md
    high_ids = {fid for fid, c in derived.items() if c >= HIGH_THRESHOLD}
    missing = sorted(high_ids - md_scored_ids)
    if missing:
        failures.append(
            f"completeness: scored fact(s) with derived confidence >= {HIGH_THRESHOLD} "
            f"missing from observable_facts.md: {missing}"
        )

    # (d) header counts
    mt = HEADER_TOTAL_RE.search(md_text)
    mh = HEADER_HIGH_RE.search(md_text)
    if not mt or int(mt.group(1)) != len(scored_facts):
        failures.append(
            f"header total-scored count wrong or missing: md says "
            f"{mt.group(1) if mt else 'none'}, yaml has {len(scored_facts)} scored facts"
        )
    if not mh or int(mh.group(1)) != len(high_ids):
        failures.append(
            f"header high-confidence count wrong or missing: md says "
            f"{mh.group(1) if mh else 'none'}, yaml has {len(high_ids)} facts >= {HIGH_THRESHOLD}"
        )

    if failures:
        print("observable-facts parity: FAIL")
        for f in failures:
            print("  " + f)
        return 1
    print("observable-facts parity: OK")
    print(f"  confidence values checked: {n_checked}; unscored context entries: {n_unscored}")
    print(f"  scored facts: {len(scored_facts)}; >= {HIGH_THRESHOLD}: {len(high_ids)} (all present in md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
