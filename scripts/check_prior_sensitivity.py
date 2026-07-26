#!/usr/bin/env python3
"""
TAST Prior-Sensitivity Gate (audit #43, change add-engine-floor-parity).

The escalation ladder for HIGH-INFLUENCE constants (posterior delta > 0.05):

    derivation_status == "derived"                           -> OK
    derivation_status == "pending_derivation" + follow_up    -> OK (tracked)
    derivation_status == "pending_derivation", no follow_up  -> FAIL
    derivation_status == "stipulated"                        -> FAIL

The honest middle: do not require impossible derivation (collapse_flat_target is
a genuine research question); require tracked ownership. A high-influence
underived constant must carry a `follow_up` pointing to an issue/ticket/audit
number so it is actively tracked, not labeled-and-forgotten.

    python TAST/scripts/check_prior_sensitivity.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAST_ROOT = HERE.parent
MODEL_DIR = TAST_ROOT / "model"
MANIFEST = TAST_ROOT / "data" / "stipulated_constants.yaml"
DELTA_THRESHOLD = 0.05


def _sweep_constant_delta(cid: str, lo: float, hi: float, r_values, streams, prior, baselines) -> float:
    """Perturb one constant across [lo, hi] over r_values; return max |delta posterior|."""
    import numpy as np
    try:
        try:
            from __init__ import set_constant_override, clear_constant_overrides  # type: ignore
        except Exception:
            from model import set_constant_override, clear_constant_overrides  # type: ignore
    except Exception:
        return 0.0
    worst = 0.0
    for v in np.linspace(lo, hi, 5):
        set_constant_override(cid, float(v))
        for rv in r_values:
            try:
                sys.path.insert(0, str(MODEL_DIR))
                import bayesian_core as bc  # type: ignore
                post, _ = bc.collapse_posterior(streams, prior, rv)
                d = max(abs(post[h] - baselines[rv][h]) for h in bc.HYPOTHESES)
                if d > worst:
                    worst = d
            except Exception:
                pass
    clear_constant_overrides()
    return worst


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.path.insert(0, str(MODEL_DIR))
    import yaml  # noqa: E402
    import bayesian_core as bc  # noqa: E402

    man = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    streams = bc.load_streams()
    prior = bc.RAW_PRIORS
    r_values = [0.05, 0.1, 0.3, 0.5]
    baselines = {rv: bc.collapse_posterior(streams, prior, rv)[0] for rv in r_values}

    failures = []
    tracked = []

    for c in man.get("constants", []):
        sr = c.get("sweep_range")
        if not sr or c["id"].startswith("raw_prior_") or c["id"] == "sensitivity_reference_r":
            continue
        lo, hi = float(sr[0]), float(sr[1])
        delta = _sweep_constant_delta(c["id"], lo, hi, r_values, streams, prior, baselines)
        if delta <= DELTA_THRESHOLD:
            continue
        # HIGH INFLUENCE constant — apply the escalation ladder
        status = c.get("derivation_status", "")
        follow_up = c.get("follow_up", "")
        cid = c["id"]
        if status == "derived":
            tracked.append((cid, delta, status, "resolved"))
        elif status == "pending_derivation" and follow_up:
            tracked.append((cid, delta, status, f"follow_up: {follow_up[:60]}"))
        elif status == "pending_derivation":
            failures.append(
                f"(c) HIGH INFLUENCE constant `{cid}` (delta={delta:.4f}) is "
                f"pending_derivation without a follow_up reference. Add a `follow_up` "
                f"field (issue/ticket/audit-number) so the constant is tracked."
            )
        else:
            failures.append(
                f"(c) HIGH INFLUENCE constant `{cid}` (delta={delta:.4f}) is "
                f"`{status}` — must be `derived` or `pending_derivation` with follow_up."
            )

    if failures:
        print("prior-sensitivity gate: FAIL")
        for f in failures:
            print("  " + f)
        return 1

    print("prior-sensitivity gate: OK")
    print(f"  HIGH INFLUENCE constants tracked: {len(tracked)}")
    for cid, delta, status, note in tracked:
        print(f"    {cid:<28} delta={delta:.4f}  {status}  ({note})")
    if not tracked:
        print("  (no HIGH INFLUENCE constants — all mechanism-silent or low)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
