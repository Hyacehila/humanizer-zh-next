#!/usr/bin/env python3
"""Read-only checks for protected Markdown content; no semantic scoring."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CATEGORIES = (
    "frontmatter", "code", "math", "links", "headings", "ids", "tables", "lists", "quotations"
)
FENCE = re.compile(r"^[ \t]*(?:>[ \t]*)*(?:(?:[-+*]|\d+[.)])[ \t]+)?(`{3,}|~{3,})(.*)$")


def _mask(chars: list[str], start: int, end: int) -> None:
    for position in range(start, end):
        if chars[position] not in "\r\n":
            chars[position] = " "


def _escaped(text: str, position: int) -> bool:
    backslashes = 0
    position -= 1
    while position >= 0 and text[position] == "\\":
        backslashes += 1
        position -= 1
    return bool(backslashes % 2)


def protected_parts(text: str) -> dict[str, list[str]]:
    parts: dict[str, list[str]] = {name: [] for name in CATEGORIES}
    chars = list(text)
    lines = text.splitlines(keepends=True)
    offsets: list[int] = []
    offset = 0
    for line in lines:
        offsets.append(offset)
        offset += len(line)

    first_body_line = 0
    if lines and lines[0].strip() == "---":
        closing = next((i for i in range(1, len(lines)) if lines[i].strip() in {"---", "..."}), None)
        if closing is not None:
            end = offsets[closing] + len(lines[closing])
            parts["frontmatter"].append(text[:end])
            _mask(chars, 0, end)
            first_body_line = closing + 1

    code_spans: list[tuple[int, str]] = []
    index = first_body_line
    while index < len(lines):
        start = offsets[index]
        opening = FENCE.match(lines[index].rstrip("\r\n"))
        if opening:
            marker = opening.group(1)
            last = index + 1
            while last < len(lines):
                candidate = FENCE.match(lines[last].rstrip("\r\n"))
                if (candidate and candidate.group(1)[0] == marker[0]
                        and len(candidate.group(1)) >= len(marker) and not candidate.group(2).strip()):
                    last += 1
                    break
                last += 1
            end = offsets[last] if last < len(lines) else len(text)
            code_spans.append((start, text[start:end]))
            _mask(chars, start, end)
            index = last
            continue
        if lines[index].startswith(("    ", "\t")) and lines[index].strip():
            last = index + 1
            while last < len(lines) and (not lines[last].strip() or lines[last].startswith(("    ", "\t"))):
                last += 1
            end = offsets[last] if last < len(lines) else len(text)
            code_spans.append((start, text[start:end]))
            _mask(chars, start, end)
            index = last
            continue
        index += 1

    visible = "".join(chars)
    position = 0
    while position < len(visible):
        if visible[position] != "`" or _escaped(visible, position):
            position += 1
            continue
        opening_end = position
        while opening_end < len(visible) and visible[opening_end] == "`":
            opening_end += 1
        marker = visible[position:opening_end]
        closing = opening_end
        found = None
        while closing < len(visible):
            if visible[closing] != "`":
                closing += 1
                continue
            run_end = closing
            while run_end < len(visible) and visible[run_end] == "`":
                run_end += 1
            if run_end - closing == len(marker):
                found = run_end
                break
            closing = run_end
        if found is None:
            position = opening_end
            continue
        code_spans.append((position, text[position:found]))
        _mask(chars, position, found)
        position = found
    parts["code"] = [value for _, value in sorted(code_spans)]
    visible = "".join(chars)

    # Inline destinations may contain escaped or balanced parentheses.
    link_spans: list[tuple[int, str]] = []
    for match in re.finditer(r"\]\(", visible):
        if _escaped(visible, match.start()):
            continue
        start = match.end()
        while start < len(visible) and visible[start].isspace():
            start += 1
        end = start
        if start < len(visible) and visible[start] == "<":
            end = start + 1
            while end < len(visible) and (visible[end] != ">" or _escaped(visible, end)):
                end += 1
            if end < len(visible):
                end += 1
        else:
            depth = 0
            while end < len(visible):
                char = visible[end]
                if char == "\\" and end + 1 < len(visible):
                    end += 2
                    continue
                if char == "(":
                    depth += 1
                elif char == ")":
                    if depth == 0:
                        break
                    depth -= 1
                elif char.isspace() and depth == 0:
                    break
                end += 1
        link_spans.append((match.start(), text[start:end]))
    definitions = list(re.finditer(r"(?m)^[ ]{0,3}\[([^\]\n]+)\]:[^\r\n]*", visible))
    reference_ids = {match.group(1).strip().casefold() for match in definitions}
    for match in definitions:
        link_spans.append((match.start(), match.group(0)))
    for match in re.finditer(r"(?<!\\)\[([^\]\n]+)\]\[([^\]\n]*)\]", visible):
        label = match.group(2) or match.group(1)
        link_spans.append((match.start(), "reference:" + label))
    for match in re.finditer(r"(?<!\\)\[([^\]\n]+)\](?![\[(:])", visible):
        if match.group(1).strip().casefold() in reference_ids:
            link_spans.append((match.start(), "shortcut:" + match.group(1)))
    for match in re.finditer(r"<(?:https?://|mailto:)[^<>\r\n]+>", visible):
        link_spans.append((match.start(), match.group(0)))
    parts["links"] = [value for _, value in sorted(link_spans)]

    math_patterns = (
        r"(?<!\\)\$\$.*?(?<!\\)\$\$",
        r"\\\[.*?\\\]",
        r"\\\(.*?\\\)",
        r"\\begin\{(?P<env>equation\*?|align\*?|gather\*?|displaymath|math)\}.*?\\end\{(?P=env)\}",
        r"(?<![\\$])\$(?!\$)[^\r\n$]*?(?<!\\)\$(?!\$)",
    )
    math_spans: list[tuple[int, str]] = []
    for pattern in math_patterns:
        for match in re.finditer(pattern, "".join(chars), re.S):
            math_spans.append((match.start(), text[match.start():match.end()]))
            _mask(chars, match.start(), match.end())
    parts["math"] = [value for _, value in sorted(math_spans)]
    visible = "".join(chars)
    visible_lines = visible.splitlines()
    raw_lines = text.splitlines()

    # ATX and Setext headings are kept, including their generated-anchor text.
    heading_spans: list[tuple[int, str]] = []
    for i, line in enumerate(visible_lines):
        if re.match(r"^[ ]{0,3}#{1,6}(?:[ \t]|$)", line):
            heading_spans.append((i, raw_lines[i]))
        elif i > 0 and re.fullmatch(r"[ ]{0,3}(?:=+|-+)[ \t]*", line) and visible_lines[i - 1].strip():
            heading_spans.append((i - 1, raw_lines[i - 1] + "\n" + raw_lines[i]))
    parts["headings"] = [value for _, value in sorted(heading_spans)]
    parts["ids"] = re.findall(r"\b(?:id|name)\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s>]+)", visible)

    table_indices: set[int] = set()
    separator = re.compile(r"^[ \t]*\|?[ \t]*:?-{3,}:?[ \t]*(?:\|[ \t]*:?-{3,}:?[ \t]*)*\|?[ \t]*$")
    for i, line in enumerate(visible_lines):
        if "|" in line and separator.fullmatch(line) and i > 0 and "|" in visible_lines[i - 1]:
            table_indices.update({i - 1, i})
            last = i + 1
            while last < len(visible_lines) and "|" in visible_lines[last] and visible_lines[last].strip():
                table_indices.add(last)
                last += 1
    parts["tables"] = [raw_lines[i] for i in sorted(table_indices)]
    parts["lists"] = [match.group(0) for match in re.finditer(r"(?m)^[ \t]*(?:>[ \t]*)*(?:[-+*]|\d+[.)])[ \t]+", visible)]
    quote_spans = list(re.finditer(r"“[^”]*”|「[^」]*」|『[^』]*』|(?<!\\)\"[^\"\r\n]*\"", visible))
    parts["quotations"] = [match.group(0) for match in quote_spans]
    parts["quotations"].extend(match.group(0) for match in re.finditer(r"(?m)^[ ]{0,3}>[^\r\n]*", visible))
    return parts


def compare_structure(original: str, edited: str, allow: set[str] | None = None) -> list[str]:
    before, after = protected_parts(original), protected_parts(edited)
    return [name for name in CATEGORIES if name not in (allow or set()) and before[name] != after[name]]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("edited", type=Path)
    parser.add_argument("--allow", choices=CATEGORIES, action="append", default=[])
    parser.add_argument("--json", action="store_true", help="Print categories and counts, never document text")
    args = parser.parse_args()
    try:
        original = args.original.read_bytes().decode("utf-8-sig")
        edited = args.edited.read_bytes().decode("utf-8-sig")
        changed = compare_structure(original, edited, set(args.allow))
    except (OSError, UnicodeError) as error:
        parser.exit(2, f"Cannot read UTF-8 inputs: {type(error).__name__}\n")
    result = {"passed": not changed, "changed_categories": changed, "allowed_categories": args.allow}
    if args.json:
        print(json.dumps(result))
    else:
        print("PASS: protected content unchanged" if not changed else "FAIL: changed " + ", ".join(changed))
    return int(bool(changed))


if __name__ == "__main__":
    raise SystemExit(main())
