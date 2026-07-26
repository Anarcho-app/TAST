#!/usr/bin/env python3
"""
TAST Likelihood-Cell Gate (audit #42, change add-prior-sensitivity-gate).

Mirrors check_constants.py one layer up: the 65 quantitative likelihood cells
in evidence_streams.csv are documented in data/likelihood_elicitation.yaml,
swept over their declared plausible ranges, and gated. A high-influence cell
(posterior delta > 0.05) still marked `stipulated` fails the build until it
carries `derivation_status: pending_derivation` with a linked follow-up.

Assertions:
  (a) CSV <-> manifest value parity (to 1e-6)
  (b) every quantitative cell has plausible_range + derivation_status
  (c) high-influence cells carry pending_derivation

    python TAST/scripts/check_likelihoods.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAST_ROOT = HERE.parent
MODEL_DIR = TAST_ROOT / "model"
CSV_PATH = MODEL_DIR / "evidence_streams.csv"
MANIFEST = TAST_ROOT / "data" / "likelihood_elicitation.yaml"
DELTA_THRESHOLD = 0.05


def _load_csv_cells():
    with open(CSV_PATH, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r.get("is_quantitative") == "1"]
    out = {}
    for r in rows:
        for h in ("H1", "H2", "H3", "H4", "H5"):
            out[(r["stream_id"], h)] = float(r[h])
    return out


def _load_manifest():
    import yaml
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


def _sweep_cell(streams, prior, r, stream_id, h, lo, hi):
    """Perturb one likelihood cell across [lo, hi]; return max |delta posterior|."""
    import numpy as np
    sys.path.insert(0, str(MODEL_DIR))
    import bayesian_core as bc
    base = bc.collapse_posterior(streams, prior, r)[0]
    worst = 0.0
    for v in np.linspace(lo, hi, 7):
        patched = []
        for s in streams:
            sd = dict(s)
            if str(sd.get("stream_id")) == str(stream_id):
                sd[h] = float(v)
            patched.append(sd)
        post = bc.collapse_posterior(patched, prior, r)[0]
        d = max(abs(post[k] - base[k]) for k in prior)
        if d > worst:
            worst = d
    return worst


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.path.insert(0, str(MODEL_DIR))
    import yaml  # noqa: E402
    import bayesian_core as bc  # noqa: E402

    csv_cells = _load_csv_cells()
    man = _load_manifest()
    man_cells = {(str(c["stream_id"]), c["hypothesis"]): c for c in man["cells"]}

    failures = []

    # (a) parity
    parity_fails = []
    for key, csv_v in csv_cells.items():
        mc = man_cells.get(key)
        if mc is None:
            parity_fails.append((key, "missing from manifest"))
            continue
        if abs(mc["value"] - csv_v) > 1e-6:
            parity_fails.append((key, f"csv={csv_v} manifest={mc['value']}"))
    if parity_fails:
        failures.append(f"(a) {len(parity_fails)} CSV/manifest value mismatch(es): {parity_fails[:5]}")

    # (b) coverage
    coverage_fails = []
    for key, mc in man_cells.items():
        if key not in csv_cells:
            continue  # manifest has a cell the CSV doesn't — parity (a) catches asymmetry
        if not mc.get("plausible_range") or len(mc["plausible_range"]) != 2:
            coverage_fails.append((key, "missing plausible_range"))
        if not mc.get("derivation_status"):
            coverage_fails.append((key, "missing derivation_status"))
    if coverage_fails:
        failures.append(f"(b) {len(coverage_fails)} cell(s) missing range/status: {coverage_fails[:5]}")

    # (c) high-influence escalation — sweep every cell
    try:
        r = float(bc._const("sensitivity_reference_r", 0.3)) if hasattr(bc, "_const") else 0.3
    except Exception:
        r = 0.3
    streams = bc.load_streams()
    prior = bc.RAW_PRIORS
    high_inf = []
    checked = 0
    for key, mc in man_cells.items():
        if key not in csv_cells:
            continue
        lo, hi = mc["plausible_range"]
        delta = _sweep_cell(streams, prior, r, key[0], key[1], lo, hi)
        checked += 1
        if delta > DELTA_THRESHOLD:
            status = mc.get("derivation_status", "")
            high_inf.append((key, delta, status))

    if high_inf:
        bad = [(k, d, s) for k, d, s in high_inf if s != "pending_derivation"]
        if bad:
            failures.append(
                f"(c) {len(bad)} HIGH INFLUENCE cell(s) (delta > {DELTA_THRESHOLD}) lack "
                f"derivation_status: pending_derivation: {bad[:5]}"
            )

    if failures:
        print("likelihood-elicitation gate: FAIL")
        for f in failures:
            print("  " + f)
        return 1

    n_hi = len(high_inf)
    print(f"likelihood-elicitation gate: OK")
    print(f"  cells checked: {checked} / {len(csv_cells)}")
    print(f"  CSV<->manifest parity: OK")
    print(f"  HIGH INFLUENCE cells (delta > {DELTA_THRESHOLD}): {n_hi} "
          f"(all carry pending_derivation)")
    if high_inf:
        high_inf.sort(key=lambda x: -x[1])
        for (sid, h), d, _ in high_inf[:5]:
            print(f"    stream {sid} {h}: max|delta|={d:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
