"""S-expression parser/printer for MeTTa output.

Handles nested lists, quoted strings with spaces, floats and symbols.
Used to turn proof terms into JSON trees for the UI.
"""
from __future__ import annotations

from typing import Any


def tokenize(s: str) -> list[str]:
    toks: list[str] = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
        elif c in "()":
            toks.append(c)
            i += 1
        elif c == '"':
            j = i + 1
            buf = []
            while j < n and s[j] != '"':
                if s[j] == "\\" and j + 1 < n:
                    buf.append(s[j + 1])
                    j += 2
                else:
                    buf.append(s[j])
                    j += 1
            toks.append('"' + "".join(buf) + '"')
            i = j + 1
        else:
            j = i
            while j < n and not s[j].isspace() and s[j] not in "()":
                j += 1
            toks.append(s[i:j])
            i = j
    return toks


def parse(s: str) -> Any:
    """Parse one s-expression into nested lists of strings."""
    toks = tokenize(s)
    node, idx = _read(toks, 0)
    return node


def parse_many(s: str) -> list[Any]:
    """Parse a string containing zero or more top-level s-expressions."""
    toks = tokenize(s)
    out = []
    i = 0
    while i < len(toks):
        node, i = _read(toks, i)
        out.append(node)
    return out


def _read(toks: list[str], i: int) -> tuple[Any, int]:
    if toks[i] == "(":
        out: list[Any] = []
        i += 1
        while toks[i] != ")":
            node, i = _read(toks, i)
            out.append(node)
        return out, i + 1
    return toks[i], i + 1


def unquote(tok: str) -> str:
    if isinstance(tok, str) and tok.startswith('"') and tok.endswith('"'):
        return tok[1:-1]
    return tok


def to_str(node: Any) -> str:
    """Print a parsed s-expression back to its string form."""
    if isinstance(node, list):
        return "(" + " ".join(to_str(x) for x in node) + ")"
    s = str(node)
    if s.startswith('"') and s.endswith('"'):
        return s
    if any(ch.isspace() for ch in s):
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def is_stv(node: Any) -> bool:
    return (
        isinstance(node, list)
        and len(node) == 3
        and node[0] == "stv"
        and _is_float(node[1])
        and _is_float(node[2])
    )


def stv_of(node: Any) -> tuple[float, float] | None:
    if is_stv(node):
        return float(node[1]), float(node[2])
    return None


def _is_float(x: Any) -> bool:
    try:
        float(x)
        return True
    except (TypeError, ValueError):
        return False
