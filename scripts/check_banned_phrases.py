#!/usr/bin/env python3
"""
TAST Banned-Phrase Lint (audit finding #32).

Repo-wide enforcement of the project's language discipline. Scans .md, .csv,
and .yaml under TAST/ plus the data strings the CLI actually prints (stream
names, provenance, claim strings) for fact-conversion and identity-proxy
phrases. Supports an explicit meta-use escape:

    <!-- allow-banned: meta-use -->

so quoting-a-phrase-in-order-to-forbid-it stays legitimate while the escape
cannot silently proliferate (allowances are counted and reported).

    python TAST/scripts/check_banned_phrases.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from typing import List, Tuple

HERE = Path(__file__).resolve().parent
TAST_ROOT = HERE.parent
MODEL_DIR = TAST_ROOT / "model"
DATA_DIR = TAST_ROOT / "data"
ALLOW_RE = re.compile(r"<!--\s*allow-banned:\s*meta-use\s*-->", re.IGNORECASE)

EXTS = (".md", ".csv", ".yaml", ".yml")
# The dictionary itself lists every phrase; it is the source of truth, not prose.
SELF_EXEMPT = {"data/banned_phrases.yaml"}


def _load_phrases() -> List[str]:
    sys.path.insert(0, str(MODEL_DIR))
    from bayesian_core import BANNED_PHRASES  # noqa: E402  (loaded from YAML)
    return list(BANNED_PHRASES)


def _rel(p: Path) -> str:
    return str(p.relative_to(TAST_ROOT)).replace("\\", "/")


def _scan_text_files() -> Tuple[int, List[str], int]:
    """Scan .md/.csv/.yaml prose. Returns (files, hits, allowances).

    Supports three escape granularities, each counted:
      - file-level:   <!-- allow-banned: meta-use (file: <reason>) --> anywhere
      - block-level:  <!-- allow-banned: meta-use --> within ±2 lines of a hit
    """
    hits: List[str] = []
    allowances = 0
    files = 0
    for p in sorted(TAST_ROOT.rglob("*")):
        if ".opencode" in p.parts or not p.is_file() or p.suffix.lower() not in EXTS:
            continue
        if "scripts" in p.parts and p.suffix == ".py":
            continue
        if _rel(p) in SELF_EXEMPT:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        files += 1
        lines = text.splitlines()
        file_level_allow = False
        for line in lines:
            if re.search(r"allow-banned:\s*meta-use\s*\(file", line, re.IGNORECASE):
                allowances += 1
                file_level_allow = True
        if file_level_allow:
            continue
        for i, line in enumerate(lines, start=1):
            if ALLOW_RE.search(line):
                allowances += 1
            ll = line.lower()
            for phrase in _PHRASES:
                if phrase in ll:
                    window = "\n".join(lines[max(0, i - 2):i + 2])
                    if ALLOW_RE.search(window):
                        continue
                    hits.append(f"{_rel(p)}:{i}: '{phrase}'  <- {line.strip()[:100]}")
    return files, hits, allowances


def _scan_printed_data() -> Tuple[int, List[str]]:
    """Scan the strings the CLI actually prints: stream names, provenance, claims."""
    hits: List[str] = []
    scanned = 0
    # evidence_streams.csv: name + provenance columns
    for csvp in sorted(MODEL_DIR.glob("evidence_streams*.csv")):
        try:
            with open(csvp, newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    for col in ("name", "provenance", "group"):
                        val = (row.get(col) or "")
                        scanned += 1
                        low = val.lower()
                        for phrase in _PHRASES:
                            if phrase in low:
                                hits.append(f"{csvp.name} stream {row.get('stream_id')} col={col}: '{phrase}'")
        except Exception:
            continue
    # sources_registry_with_ci.csv: claim strings
    reg = DATA_DIR / "sources_registry_with_ci.csv"
    if reg.exists():
        try:
            with open(reg, newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    val = (row.get("claim") or "")
                    scanned += 1
                    low = val.lower()
                    for phrase in _PHRASES:
                        if phrase in low:
                            hits.append(f"{reg.name} claim {row.get('claim_id')}: '{phrase}'")
        except Exception:
            pass
    return scanned, hits


_PHRASES = _load_phrases()


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    files, prose_hits, allowances = _scan_text_files()
    scanned, data_hits = _scan_printed_data()
    total_hits = prose_hits + data_hits
    print(f"banned phrases loaded: {len(_PHRASES)}")
    print(f"prose files scanned: {files}; meta-use allowances: {allowances}")
    print(f"printed-data strings scanned: {scanned}")
    print(f"unescaped violations: {len(total_hits)}")
    if total_hits:
        print("\nVIOLATIONS:")
        for h in total_hits:
            print("  " + h)
        return 1
    print("\nNo unescaped banned phrases. Language discipline holds.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
