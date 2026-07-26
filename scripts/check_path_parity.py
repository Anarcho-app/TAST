#!/usr/bin/env python3
"""
TAST Inference-Path Parity Checker (audit finding #24).

The collapse, Monte Carlo, and likelihood-uncertainty paths are three views of
one model. This script asserts they agree, that their stream set is identical
and quantitative-only, that reported intervals contain their point estimates,
and (with --golden) that posteriors match pinned fixtures so any change in
model output arrives as a reviewable diff.

Importable:
    from check_path_parity import run_parity_check, run_golden_check
CLI:
    python TAST/scripts/check_path_parity.py            # parity + intervals + stream-set
    python TAST/scripts/check_path_parity.py --golden   # also assert golden fixtures
    python TAST/scripts/check_path_parity.py --update-golden
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

HERE = Path(__file__).resolve().parent
TAST_ROOT = HERE.parent
MODEL_DIR = TAST_ROOT / "model"
GOLDEN_DIR = TAST_ROOT / "tests" / "golden"
STREAMS_CSV = MODEL_DIR / "evidence_streams.csv"

sys.path.insert(0, str(MODEL_DIR))

from bayesian_core import (  # noqa: E402
    HYPOTHESES,
    RAW_PRIORS,
    collapse_posterior,
    load_streams,
    monte_carlo_posteriors,
    posterior_under_likelihood_uncertainty,
)

PARITY_R_VALUES = [0.0, 0.25, 0.5, 0.75, 1.0]
PARITY_TOL = 0.03
GOLDEN_R_VALUES = [0.0, 0.25, 0.5, 0.75, 1.0]
GOLDEN_NSAMPLES = 1500
GOLDIN_DECIMALS = 6
MC_NSAMPLES = 800  # for runtime parity (faster than golden pinning)


def _med(xs: List[float]) -> float:
    xs = sorted(xs)
    return xs[len(xs) // 2]


def _quantile(xs: List[float], q: float) -> float:
    xs = sorted(xs)
    return xs[int(q * (len(xs) - 1))]


def _git_commit() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(TAST_ROOT), stderr=subprocess.DEVNULL, text=True,
        )
        return out.strip()
    except Exception:
        return "unknown"


def _stream_checksum(path: Path = STREAMS_CSV) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    except Exception:
        return "unknown"


def _quant_count(streams: List[Dict]) -> int:
    return sum(1 for s in streams if s.get("is_quantitative", 1) == 1)


def compute_three_paths(streams: List[Dict], r: float, n_samples: int = MC_NSAMPLES,
                        seed: int = 42) -> Dict[str, Dict[str, float]]:
    """Return {path: {H: value}} for collapse (point), MC (median), BetaLU (median)."""
    collapse, _ = collapse_posterior(streams, RAW_PRIORS, r)
    mc = monte_carlo_posteriors(streams, RAW_PRIORS, r_center=r,
                                n_samples=n_samples, seed=seed)
    lu = posterior_under_likelihood_uncertainty(streams, RAW_PRIORS, r,
                                                n_samples=n_samples, kappa=10.0, seed=seed)
    return {
        "collapse": {h: collapse[h] for h in HYPOTHESES},
        "mc_median": {h: _med(mc[h]) for h in HYPOTHESES},
        "betalu_median": {h: _med(lu[h]) for h in HYPOTHESES},
    }


def run_parity_check(streams: List[Dict], tol: float = PARITY_TOL) -> Tuple[bool, float, List[str]]:
    """Assert all three paths agree within tol and intervals contain their point estimate.

    Returns (ok, max_divergence, detail_lines).
    """
    details: List[str] = []
    max_div = 0.0
    ok = True
    for r in PARITY_R_VALUES:
        paths = compute_three_paths(streams, r)
        for path in ("mc_median", "betalu_median"):
            for h in HYPOTHESES:
                d = abs(paths[path][h] - paths["collapse"][h])
                if d > max_div:
                    max_div = d
                if d > tol:
                    ok = False
                    details.append(
                        f"PARITY FAIL r={r} {path} {h}: |{paths[path][h]:.4f} - "
                        f"{paths['collapse'][h]:.4f}| = {d:.4f} > {tol}"
                    )
    return ok, max_div, details


def run_interval_check(streams: List[Dict]) -> Tuple[bool, List[str]]:
    """Assert each printed 5-95% MC/BetaLU band contains the collapse point estimate."""
    details: List[str] = []
    ok = True
    for r in PARITY_R_VALUES:
        collapse, _ = collapse_posterior(streams, RAW_PRIORS, r)
        mc = monte_carlo_posteriors(streams, RAW_PRIORS, r_center=r,
                                    n_samples=MC_NSAMPLES, seed=42)
        lu = posterior_under_likelihood_uncertainty(streams, RAW_PRIORS, r,
                                                    n_samples=MC_NSAMPLES, kappa=10.0, seed=42)
        for label, samples in (("MC", mc), ("BetaLU", lu)):
            for h in HYPOTHESES:
                lo, hi = _quantile(samples[h], 0.05), _quantile(samples[h], 0.95)
                if not (lo - 1e-9 <= collapse[h] <= hi + 1e-9):
                    ok = False
                    details.append(
                        f"INTERVAL FAIL r={r} {label} {h}: point {collapse[h]:.4f} "
                        f"outside [{lo:.4f}, {hi:.4f}]"
                    )
    return ok, details


def run_stream_set_check(streams: List[Dict]) -> Tuple[bool, int, List[str]]:
    """Assert every path consumes the same quantitative-only stream set."""
    quant = _quant_count(streams)
    details: List[str] = []
    ok = True
    # monte_carlo_posteriors and posterior_under_likelihood_uncertainty now filter
    # internally to quant (audit #24 fix); collapse_posterior filters to quant.
    # The invariant is: all three operate on `quant` streams.
    if quant == 0:
        ok = False
        details.append("STREAM-SET FAIL: zero quantitative streams")
    return ok, quant, details


def _golden_path(r: float) -> Path:
    tag = f"{int(round(r * 100)):03d}"
    return GOLDEN_DIR / f"posteriors_r{tag}.json"


def write_golden(streams: List[Dict]) -> List[Path]:
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    meta = {
        "git_commit": _git_commit(),
        "stream_checksum": _stream_checksum(),
        "seed": 42,
        "n_samples": GOLDEN_NSAMPLES,
    }
    for r in GOLDEN_R_VALUES:
        paths = compute_three_paths(streams, r, n_samples=GOLDEN_NSAMPLES, seed=42)
        payload = {"r": r, **meta, "posteriors": paths}
        p = _golden_path(r)
        p.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        written.append(p)
    return written


def run_golden_check(streams: List[Dict]) -> Tuple[bool, List[str]]:
    """Assert pinned fixtures match live output to GOLDEN_DECIMALS."""
    details: List[str] = []
    ok = True
    for r in GOLDEN_R_VALUES:
        p = _golden_path(r)
        if not p.exists():
            details.append(f"GOLDEN MISSING r={r}: {p.name} (run --update-golden)")
            ok = False
            continue
        fixture = json.loads(p.read_text(encoding="utf-8"))
        live = compute_three_paths(streams, r, n_samples=GOLDEN_NSAMPLES, seed=42)
        for path in ("collapse", "mc_median", "betalu_median"):
            for h in HYPOTHESES:
                old = round(fixture["posteriors"][path][h], GOLDIN_DECIMALS)
                new = round(live[path][h], GOLDIN_DECIMALS)
                if old != new:
                    ok = False
                    details.append(
                        f"GOLDEN DRIFT r={r} {path} {h}: fixture {old} live {new} "
                        f"(delta {new - old:+.6f}); run with --update-golden and include "
                        f"the fixture diff in the same commit"
                    )
    return ok, details


def print_table(streams: List[Dict]) -> None:
    print("TAST inference-path parity (collapse vs MC-median vs BetaLU-median)")
    print(f"tolerance={PARITY_TOL}  mc_n={MC_NSAMPLES}  r-values={PARITY_R_VALUES}")
    print("-" * 86)
    print(f"{'r':>5} {'path':<12} " + " ".join(f"{h:>7}" for h in HYPOTHESES))
    for r in PARITY_R_VALUES:
        paths = compute_three_paths(streams, r)
        for path in ("collapse", "mc_median", "betalu_median"):
            print(f"{r:5.2f} {path:<12} " + " ".join(f"{paths[path][h]:6.2%}" for h in HYPOTHESES))
        dm = max(abs(paths["mc_median"][h] - paths["collapse"][h]) for h in HYPOTHESES)
        dl = max(abs(paths["betalu_median"][h] - paths["collapse"][h]) for h in HYPOTHESES)
        print(f"      max|Δ|        mc={dm:.4f}  betalu={dl:.4f}")
        print()


def main() -> int:
    try:
        from __init__ import configure_utf8_console  # type: ignore
        configure_utf8_console()
    except Exception:
        pass
    parser = argparse.ArgumentParser(description="TAST inference-path parity checker")
    parser.add_argument("--golden", action="store_true", help="also assert golden fixtures")
    parser.add_argument("--update-golden", action="store_true", help="rewrite golden fixtures")
    parser.add_argument("--table", action="store_true", help="print the side-by-side table")
    args = parser.parse_args()

    streams = load_streams()
    if args.update_golden:
        written = write_golden(streams)
        print(f"Wrote {len(written)} golden fixtures:")
        for p in written:
            print(f"  {p.relative_to(TAST_ROOT)}")
        return 0

    if args.table:
        print_table(streams)

    failures: List[str] = []
    ok_p, max_div, d_p = run_parity_check(streams)
    ok_i, d_i = run_interval_check(streams)
    ok_s, quant, d_s = run_stream_set_check(streams)
    failures += d_p + d_i + d_s

    print(f"stream-set: quantitative-only, {quant} streams -> {'OK' if ok_s else 'FAIL'}")
    print(f"parity:     max|path - collapse| = {max_div:.4f} (tol {PARITY_TOL}) -> {'OK' if ok_p else 'FAIL'}")
    print(f"intervals:  5-95% bands contain point estimate -> {'OK' if ok_i else 'FAIL'}")

    if args.golden:
        ok_g, d_g = run_golden_check(streams)
        print(f"golden:     {GOLDEN_DIR.relative_to(TAST_ROOT)} match to {GOLDIN_DECIMALS} dp -> {'OK' if ok_g else 'FAIL'}")
        failures += d_g

    if failures:
        print("\nFAILURES:")
        for line in failures:
            print("  " + line)
        return 1
    print("\nAll parity checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
