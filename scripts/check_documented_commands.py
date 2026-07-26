#!/usr/bin/env python3
"""
TAST Documented-Command Checker (audit findings #26, #34).

Extracts every fenced ```bash block from markdown under TAST/, executes each
command, and asserts exit code 0. A documented-but-absent flag or a referenced-
but-absent stream is a build failure on the day it is written.

    python TAST/scripts/check_documented_commands.py
    python TAST/scripts/check_documented_commands.py --check-streams
    python TAST/scripts/check_documented_commands.py --list
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

HERE = Path(__file__).resolve().parent
TAST_ROOT = HERE.parent
MODEL_DIR = TAST_ROOT / "model"
TIMEOUT = 300
NO_EXEC_RE = re.compile(r"<!--\s*no-exec:\s*(?P<reason>.*?)\s*-->", re.IGNORECASE)
UNREPRODUCIBLE_RE = re.compile(r"UNREPRODUCIBLE\s+as\s+of\s+\d{4}-\d{2}-\d{2}", re.IGNORECASE)
STREAM_REF_RE = re.compile(r"\b[Ss]tream\s*(\d+)\b")
MD_FILES = sorted(p for p in TAST_ROOT.rglob("*.md") if ".opencode" not in p.parts)
# Historical logs legitimately mention streams as past changelog entries, not as
# current measured-effects claims. Exclude them from --check-streams.
STREAM_CHECK_EXCLUDE = {"VERSION.md", "DECISIONS.md", "ACKNOWLEDGMENTS.md"}
CSV_FILES = sorted(MODEL_DIR.glob("evidence_streams*.csv"))


def _cwd_for(cmd: str) -> Path:
    """Pick the working directory that makes a TAST command resolve."""
    if " -m model." in cmd or cmd.startswith("python model/") or cmd.startswith("python scripts/"):
        return TAST_ROOT
    if " -m bayesian_core" in cmd or " -m physical_likelihoods" in cmd or " -m inference_extensions" in cmd:
        return MODEL_DIR
    return TAST_ROOT


def _normalize(cmd: str) -> str:
    """Strip leading `$`/`>` prompts and trailing inline `# comment` for execution.

    A `#` starts a shell comment only when it begins a word (preceded by
    whitespace or start of line), matching how the documented command would
    actually run in a shell.
    """
    cmd = re.sub(r"^\$\s*", "", cmd)
    cmd = re.sub(r"^\>\s*", "", cmd)
    cmd = re.sub(r"\s+#.*$", "", cmd)
    return cmd.strip()


def extract_commands() -> List[Tuple[Path, int, str, str]]:
    """Return (file, line, command, no_exec_reason_or_empty) per executable line."""
    out: List[Tuple[Path, int, str, str]] = []
    for md in MD_FILES:
        try:
            text = md.read_text(encoding="utf-8")
        except Exception:
            continue
        lines = text.splitlines()
        in_block = False
        block_no_exec = ""
        pending_no_exec = ""      # most recent no-exec marker reason
        lines_since_marker = 999
        for i, line in enumerate(lines, start=1):
            stripped_line = line.strip()
            m = NO_EXEC_RE.search(line)
            if m:
                pending_no_exec = m.group("reason")
                lines_since_marker = 0
            else:
                lines_since_marker += 1

            if stripped_line.startswith("```bash"):
                in_block = True
                # a no-exec marker on one of the ~4 lines preceding the fence applies to the block
                block_no_exec = pending_no_exec if lines_since_marker <= 4 else ""
                continue
            if in_block and stripped_line.startswith("```"):
                in_block = False
                block_no_exec = ""
                continue
            if not in_block:
                continue
            if NO_EXEC_RE.search(line):
                # marker inside the block also applies
                block_no_exec = pending_no_exec
                continue
            if not stripped_line or stripped_line.startswith("#"):
                continue
            if stripped_line.startswith("cd "):
                continue
            out.append((md, i, _normalize(stripped_line), block_no_exec))
    return out


def run_commands(commands) -> Tuple[int, int, List[str]]:
    passed = failed = 0
    failures: List[str] = []
    for md, lineno, cmd, no_exec in commands:
        if no_exec:
            print(f"  SKIP  {md.relative_to(TAST_ROOT)}:{lineno}  [{no_exec}]")
            continue
        cwd = _cwd_for(cmd)
        try:
            # Audit #38: text=True without encoding= decodes with the locale
            # codec (cp1252 on Windows), so the checker itself raised
            # UnicodeDecodeError on any command emitting non-cp1252 bytes.
            r = subprocess.run(cmd, shell=True, cwd=str(cwd),
                               capture_output=True, text=True,
                               encoding="utf-8", errors="replace",
                               timeout=TIMEOUT)
            if r.returncode == 0:
                passed += 1
            else:
                failed += 1
                err = (r.stderr or r.stdout or "").strip().splitlines()
                failures.append(
                    f"{md.relative_to(TAST_ROOT)}:{lineno}: exit {r.returncode}\n"
                    f"    cmd: {cmd}\n"
                    f"    err: {err[-1][:200] if err else '(no output)'}"
                )
        except subprocess.TimeoutExpired:
            failed += 1
            failures.append(f"{md.relative_to(TAST_ROOT)}:{lineno}: TIMEOUT (>{TIMEOUT}s)\n    cmd: {cmd}")
        except Exception as e:
            failed += 1
            failures.append(f"{md.relative_to(TAST_ROOT)}:{lineno}: {e}\n    cmd: {cmd}")
    return passed, failed, failures


def check_stream_refs() -> Tuple[int, int, List[str]]:
    """Fail when docs report measured effects for a stream id present in no CSV,
    unless the citing section carries an UNREPRODUCIBLE marker."""
    present = set()
    for csvp in CSV_FILES:
        try:
            with open(csvp, newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    sid = row.get("stream_id", "").strip()
                    if sid.isdigit():
                        present.add(int(sid))
        except Exception:
            continue
    missing_hits: List[str] = []
    total_refs = 0
    for md in MD_FILES:
        if md.name in STREAM_CHECK_EXCLUDE:
            continue
        try:
            text = md.read_text(encoding="utf-8")
        except Exception:
            continue
        # A file-level UNREPRODUCIBLE marker covers every absent-stream citation
        # in that file. Appropriate for files whose entire subject is a stream
        # that is not (or not yet) in the committed tables.
        file_unreproducible = bool(UNREPRODUCIBLE_RE.search(text))
        lines = text.splitlines()
        for i, line in enumerate(lines, start=1):
            for m in STREAM_REF_RE.finditer(line):
                sid = int(m.group(1))
                if sid not in present:
                    total_refs += 1
                    if file_unreproducible:
                        continue
                    window = "\n".join(lines[max(0, i - 8):i + 8])
                    if not UNREPRODUCIBLE_RE.search(window):
                        missing_hits.append(
                            f"{md.relative_to(TAST_ROOT)}:{i}: Stream {sid} absent from all CSVs "
                            f"(present ids: {sorted(present)})"
                        )
    return len(missing_hits), total_refs, missing_hits


def main() -> int:
    try:
        sys.path.insert(0, str(HERE))
        from check_path_parity import configure_utf8_console  # type: ignore
    except Exception:
        pass
    # standalone UTF-8 setup (this script may run before bayesian_core)
    try:
        enc = (getattr(sys.stdout, "encoding", "") or "").replace("-", "").lower()
        if enc != "utf8":
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="TAST documented-command checker")
    parser.add_argument("--check-streams", action="store_true")
    parser.add_argument("--list", action="store_true", help="list extracted commands and exit")
    args = parser.parse_args()

    commands = extract_commands()
    if args.list:
        for md, lineno, cmd, no_exec in commands:
            tag = f" [no-exec: {no_exec}]" if no_exec else ""
            print(f"{md.relative_to(TAST_ROOT)}:{lineno}{tag}\n    {cmd}")
        return 0

    print(f"Extracted {len(commands)} commands from {len(MD_FILES)} markdown files.")
    passed, failed, failures = run_commands(commands)
    print(f"commands: {passed} passed, {failed} failed")

    if args.check_streams:
        miss, total, hits = check_stream_refs()
        print(f"stream-refs: {total} to absent ids, {miss} unmarked UNREPRODUCIBLE")
        failures += hits

    if failures:
        print("\nFAILURES:")
        for f in failures:
            print("  " + f)
        return 1
    print("\nAll documented commands executed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
