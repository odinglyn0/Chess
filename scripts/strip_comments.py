"""Detect and remove Python source comments across the repository.

Run with ``--check`` to fail when any ``#`` comment is present, or with
``--write`` to strip comments in place. Shebang lines on the first row are
preserved so executable scripts keep working.
"""

from __future__ import annotations

import io
import sys
import tokenize
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Tuple

EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "venv",
    "build",
    "dist",
    "data",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
}


def iter_python_files(paths: Iterable[str]) -> Iterator[Path]:
    seen = set()
    for raw in paths:
        base = Path(raw)
        candidates: Iterable[Path]
        if base.is_dir():
            candidates = base.rglob("*.py")
        elif base.suffix == ".py":
            candidates = [base]
        else:
            candidates = []
        for candidate in candidates:
            resolved = candidate.resolve()
            if resolved in seen:
                continue
            if any(part in EXCLUDED_PARTS for part in candidate.parts):
                continue
            seen.add(resolved)
            yield candidate


def comment_rows(source: str) -> Dict[int, int]:
    rows: Dict[int, int] = {}
    reader = io.StringIO(source).readline
    for token in tokenize.generate_tokens(reader):
        if token.type == tokenize.COMMENT:
            row, col = token.start
            if row not in rows or col < rows[row]:
                rows[row] = col
    return rows


def _is_shebang_row(source: str, row: int) -> bool:
    if row != 1:
        return False
    first_line = source.splitlines()[0] if source else ""
    return first_line.startswith("#!")


def collect_comments(source: str) -> Dict[int, int]:
    try:
        rows = comment_rows(source)
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return {}
    return {row: col for row, col in rows.items() if not _is_shebang_row(source, row)}


def strip_source(source: str) -> str:
    rows = collect_comments(source)
    if not rows:
        return source
    lines = source.splitlines(keepends=True)
    output: List[str] = []
    for index, line in enumerate(lines, start=1):
        if index not in rows:
            output.append(line)
            continue
        newline = ""
        body = line
        for ending in ("\r\n", "\n", "\r"):
            if line.endswith(ending):
                newline = ending
                body = line[: -len(ending)]
                break
        code = body[: rows[index]].rstrip()
        if code == "":
            continue
        output.append(code + newline)
    return "".join(output)


def _parse_args(argv: List[str]) -> Tuple[bool, bool, List[str]]:
    write = "--write" in argv
    check = "--check" in argv
    targets = [arg for arg in argv if not arg.startswith("-")]
    if not targets:
        targets = ["."]
    if not write and not check:
        write = True
    return write, check, targets


def main(argv: List[str]) -> int:
    write, check, targets = _parse_args(argv)
    offenders: List[Tuple[Path, List[int]]] = []
    changed: List[Path] = []
    for file in iter_python_files(targets):
        try:
            source = file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        rows = collect_comments(source)
        if rows and check:
            offenders.append((file, sorted(rows)))
        if write:
            updated = strip_source(source)
            if updated != source:
                file.write_text(updated, encoding="utf-8")
                changed.append(file)
    if write and changed:
        for file in changed:
            print(f"stripped comments: {file.as_posix()}")
    if check and offenders:
        print("Python comments are not allowed (no-stubs steering rule):")
        for file, lines in offenders:
            listed = ", ".join(str(line) for line in lines)
            print(f"  {file.as_posix()}: line(s) {listed}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
