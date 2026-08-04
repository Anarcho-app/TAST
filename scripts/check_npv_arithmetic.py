#!/usr/bin/env python3
"""
TAST NPV Arithmetic Gate (pan-thesis audit 2026-08-04, prosthesis item 3).

The legislative-facing documents (artifacts/01_*) carry NPV and cumulative
tables. Those numbers are illustrative, but they are still arithmetic — this
gate recomputes every claimed value from the declared scenario parameters in
data/cba_scenarios.yaml and fails on drift beyond one rounding step.

    NPV(net_annual, r, T) = net_annual * (1 - (1+r)^-T) / r
    cumulative(net_annual, T) = net_annual * T

    python TAST/scripts/check_npv_arithmetic.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAST_ROOT = HERE.parent
SCENARIOS_YAML = TAST_ROOT / "data" / "cba_scenarios.yaml"


def annuity_factor(r: float, t: int) -> float:
    return (1.0 - (1.0 + r) ** (-t)) / r


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    import yaml  # noqa: E402

    data = yaml.safe_load(SCENARIOS_YAML.read_text(encoding="utf-8"))
    tol = float(data["tolerance_t"])
    t_short = int(data["horizons_years"]["short"])
    t_long = int(data["horizons_years"]["long"])
    r3 = float(data["discount_rates_real"]["r3"])
    r5 = float(data["discount_rates_real"]["r5"])

    failures = []
    checked = 0
    for sc in data["scenarios"]:
        sid = sc["id"]
        net_b = float(sc["net_annual_b"])  # billions
        claimed = sc["claimed_t"]
        computed = {
            "cum_10y": net_b * t_short / 1000.0,
            "npv_10y_r3": net_b * annuity_factor(r3, t_short) / 1000.0,
            "npv_10y_r5": net_b * annuity_factor(r5, t_short) / 1000.0,
            "npv_50y_r3": net_b * annuity_factor(r3, t_long) / 1000.0,
            "npv_50y_r5": net_b * annuity_factor(r5, t_long) / 1000.0,
        }
        for key, comp in computed.items():
            if key not in claimed:
                failures.append(f"{sid}: claimed value missing for {key}")
                continue
            checked += 1
            delta = abs(float(claimed[key]) - comp)
            if delta > tol:
                failures.append(
                    f"{sid}.{key}: claimed {claimed[key]} T vs recomputed "
                    f"{comp:.3f} T (delta {delta:.3f} > tolerance {tol})"
                )

    if failures:
        print("npv-arithmetic: FAIL")
        for f in failures:
            print("  " + f)
        return 1
    print("npv-arithmetic: OK")
    print(f"  scenarios: {len(data['scenarios'])}; values checked: {checked}")
    print(f"  horizons: {t_short}y + {t_long}y at {r3:.0%} / {r5:.0%} real; tolerance {tol} T")
    return 0


if __name__ == "__main__":
    sys.exit(main())
