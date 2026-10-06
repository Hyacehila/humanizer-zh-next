#!/usr/bin/env python3
"""Validate this package's metadata, local links and upstream provenance offline."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
RUNTIME_REFERENCES = {
    "academic-writing.md",
    "commercial-editing.md",
    "grant-proposals.md",
}


def validate_package(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    required = [
        "SKILL.md", "README.md", "LICENSE", "THIRD_PARTY_NOTICES.md",
        "docs/upstream-sources.md", "docs/upstreams.json",
        *[f"references/{name}" for name in sorted(RUNTIME_REFERENCES)],
    ]
    for name in required:
        if not (root / name).is_file():
            errors.append(f"Missing required package file: {name}")
    if errors:
        return errors
    skill = (root / "SKILL.md").read_text(encoding="utf-8-sig")
    metadata = re.match(r"\A---\n(.*?)\n---(?:\n|$)", skill, re.S)
    if metadata is None:
        return ["SKILL.md must start with closed YAML frontmatter"]
    header = metadata.group(1)
    keys = set(re.findall(r"(?m)^([a-z][a-z-]*):", header))
    if not {"name", "description"} <= keys or keys - {"name", "description", "license", "metadata"}:
        errors.append("Use portable name, description, license and metadata fields")
    if not re.search(r"(?m)^name: humanizer-zh-next$", header):
        errors.append("Keep the existing skill identity: humanizer-zh-next")
    description = re.search(r"(?m)^description: \|\n((?:  .*(?:\n|$))+)", header + "\n")
    if description is None or not 1 <= len(description.group(1).strip()) <= 1024:
        errors.append("Provide a non-empty description of at most 1024 characters")
    version = re.search(r'(?m)^  version: "(\d+\.\d+\.\d+)"$', header)
    if version is None:
        errors.append("Store the version as a string in metadata.version")
    actual_references = {path.name for path in (root / "references").iterdir()}
    if actual_references != RUNTIME_REFERENCES:
        errors.append("Keep only commercial, academic and grant files in references/")
    expected_targets = {f"references/{name}" for name in RUNTIME_REFERENCES}
    routed_targets = set(re.findall(r"\]\((references/[^\s)]+)\)", skill))
    if routed_targets != expected_targets:
        errors.append("SKILL.md must route to exactly the three supported references")
    lock = json.loads((root / "docs/upstreams.json").read_text(encoding="utf-8-sig"))
    if lock.get("schema_version") != 1:
        errors.append("Unsupported upstream record schema")
    if set(lock.get("runtime_references", [])) != expected_targets:
        errors.append("The upstream record must list the same three runtime references")
    if version and lock.get("project_version") != version.group(1):
        errors.append("SKILL.md and the upstream record disagree on the version")
    readme = (root / "README.md").read_text(encoding="utf-8-sig")
    if version and version.group(1) not in readme:
        errors.append("README.md must describe the current version")
    notices = (root / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8-sig")
    seen: set[str] = set()
    for source in lock.get("sources", []):
        repository = source.get("repository", "")
        commit = source.get("commit", "")
        if repository in seen or not re.fullmatch(r"[\w.-]+/[\w.-]+", repository):
            errors.append(f"Invalid or duplicate source repository: {repository}")
        seen.add(repository)
        if not re.fullmatch(r"[0-9a-f]{40}", commit):
            errors.append(f"Pin a full commit for {repository}")
        if repository not in notices or commit not in notices:
            errors.append(f"Missing pinned attribution for {repository}")
        if source.get("license") != "MIT":
            errors.append(f"Review the license boundary before adapting {repository}")
        if not source.get("source_paths") or not source.get("adapted_into") or not source.get("not_adopted"):
            errors.append(f"Record source paths, integration targets and exclusions for {repository}")
        for target in source.get("adapted_into", []):
            path = (root / target).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file():
                errors.append(f"Missing or outside integration target: {target}")
    if not seen:
        errors.append("Record the adapted upstream sources")

    # These are package links, not network availability checks or a Markdown renderer.
    docs = [
        root / "SKILL.md", root / "README.md", root / "THIRD_PARTY_NOTICES.md",
        *sorted((root / "references").glob("*.md")),
        *sorted((root / "docs").glob("*.md")),
        *sorted((root / "tests").glob("*.md")),
    ]
    for document in docs:
        content = document.read_text(encoding="utf-8-sig")
        content = re.sub(r"(?ms)^```[^\n]*\n.*?^```[ \t]*$", "", content)
        for match in re.finditer(r"\]\(([^\s)]+)\)", content):
            destination = urlsplit(match.group(1))
            if destination.scheme or not destination.path:
                continue
            path = (document.parent / unquote(destination.path)).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file():
                errors.append(f"Broken local link in {document.relative_to(root)}: {destination.path}")
    return errors


def main() -> int:
    try:
        errors = validate_package()
    except (OSError, ValueError, TypeError) as error:
        print(f"FAIL: cannot validate package ({type(error).__name__})")
        return 1
    if errors:
        for error in errors:
            print("FAIL: " + error)
        return 1
    print("PASS: metadata, references, version and pinned attribution are consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
