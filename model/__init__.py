"""
TAST model package.

Public helper:
    configure_utf8_console() -> bool

Every TAST executable entry point SHOULD call configure_utf8_console() at the
top of its main() before emitting any non-ASCII output. This makes documented
commands succeed on a legacy single-byte console (e.g. cp1252) without
requiring the caller to export PYTHONIOENCODING / PYTHONUTF8 (audit finding
#34). Where reconfiguration fails, callers fall back to an ASCII rendering
rather than raising UnicodeEncodeError.
"""

from __future__ import annotations

import os
import sys

_CONSTANTS_YAML = os.path.join(os.path.dirname(__file__), "..", "data", "stipulated_constants.yaml")
_CONSTANTS_CACHE: dict = {}
_CONSTANTS_OVERRIDES: dict = {}


def _load_constants_raw() -> dict:
    if _CONSTANTS_CACHE:
        return _CONSTANTS_CACHE
    import yaml
    with open(_CONSTANTS_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    for c in data.get("constants", []):
        _CONSTANTS_CACHE[c["id"]] = c
    return _CONSTANTS_CACHE


def load_constant(cid: str):
    """Return the declared value for a stipulated constant id.

    Fail-closed: an undeclared id raises unless TAST_CONSTANTS_LENIENT is set
    (first-week rollback gate, design.md). Sweep code uses
    set_constant_override() to perturb values without editing the YAML.
    """
    if cid in _CONSTANTS_OVERRIDES:
        return _CONSTANTS_OVERRIDES[cid]
    try:
        consts = _load_constants_raw()
    except FileNotFoundError as e:
        if os.environ.get("TAST_CONSTANTS_LENIENT"):
            raise RuntimeError(
                f"stipulated_constants.yaml missing and TAST_CONSTANTS_LENIENT set; "
                f"cannot resolve '{cid}' — re-add the manifest or unset the flag."
            ) from e
        raise
    if cid not in consts:
        if os.environ.get("TAST_CONSTANTS_LENIENT"):
            raise RuntimeError(
                f"constant '{cid}' not declared in stipulated_constants.yaml "
                f"(fail-closed; TAST_CONSTANTS_LENIENT does not bypass undeclared ids)."
            )
        raise KeyError(
            f"constant '{cid}' not declared in stipulated_constants.yaml. "
            f"Undeclared posterior-steering scalars are rejected by design "
            f"(audit #27/#28/#31). Add an entry or mark the literal with "
            f"'# not-posterior-steering: <reason>'."
        )
    return consts[cid]["value"]


def set_constant_override(cid: str, value) -> None:
    """Override a constant for sensitivity sweeps; cleared by clear_constant_overrides."""
    _CONSTANTS_OVERRIDES[cid] = value


def clear_constant_overrides() -> None:
    _CONSTANTS_OVERRIDES.clear()


def configure_utf8_console() -> bool:
    """Reconfigure stdout/stderr to UTF-8.

    Returns True if at least one stream was (re)configured to UTF-8 or was
    already UTF-8 capable, False if the console could not be made UTF-8 safe
    and callers must render ASCII fallbacks.

    Idempotent: safe to call multiple times across modules in one process.
    """
    ok = True
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        if stream is None:
            continue
        encoding = getattr(stream, "encoding", "") or ""
        if encoding.replace("-", "").lower() == "utf8":
            continue
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
                continue
            except Exception:
                pass
        buffer = getattr(stream, "buffer", None)
        if buffer is not None:
            import io
            try:
                setattr(sys, name, io.TextIOWrapper(
                    buffer, encoding="utf-8", errors="replace", line_buffering=True,
                ))
                continue
            except Exception:
                pass
        ok = False
    return ok
