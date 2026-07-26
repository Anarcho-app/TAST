"""Regression tests for derive_confidence (audit #40, #41, #42).

Run: python tests/test_derive_confidence.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "model"))
import derive_confidence as dc


def _assert(cond, msg):
    if not cond:
        print(f"  FAIL: {msg}")
        return 1
    print(f"  ok: {msg}")
    return 0


def main():
    fails = 0
    s = dc._load_spec()

    print("Audit #42 — substring matching has word boundaries (no silent mis-derive):")
    # Each bug case Opus 4.8 High identified, with the class it SHOULD derive.
    cases = [
        ("birth registration records", "federal_enumerator",
         "'registration' must not match 'ration' (self_presentation)"),
        ("plantation website archive", "owner_mediated",
         "'website' must not match 'site' (physical); 'plantation' is owner_mediated"),
        ("important administrative correspondence", "federal_enumerator",
         "'important' must not match 'import' (trader_manifest); 'administrative' is federal"),
    ]
    for archive, expected, note in cases:
        got = dc.derive_source_class(archive, s)
        fails += _assert(got == expected, f"{archive!r} -> {got} (expect {expected}). {note}")

    print("\nAudit #42 — legitimate stems still match their inflections (leading \\b only):")
    stems = [
        ("ration rolls", "self_presentation"),
        ("rations issued", "self_presentation"),
        ("genomic data", "physical"),
        ("self-presentation at muster", "self_presentation"),
        ("burial site", "physical"),
    ]
    for archive, expected in stems:
        got = dc.derive_source_class(archive, s)
        fails += _assert(got == expected, f"{archive!r} -> {got} (expect {expected})")

    print("\nAudit #41 — artifact_status maps to re_verifiability tiers:")
    for status, tier in [("survives_direct", "high"), ("survives_derivative", "medium"), ("lost", "low")]:
        got = dc.derive_re_verifiability(status, s)
        fails += _assert(got == tier, f"{status} -> {got} (expect {tier})")

    print("\nAudit #40 — sampled_fraction computes from n_observed/reference:")
    for n, ref, expect in [(50, 100, 0.5), (200, 100, 1.0), (None, 100, None)]:
        got = dc.derive_sampled_fraction(n, ref)
        fails += _assert(got == expect, f"n={n} ref={ref} -> {got} (expect {expect})")

    print(f"\n{'ALL PASS' if fails == 0 else f'{fails} FAILURES'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
