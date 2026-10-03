"""Inventory English JSON string values without treating metadata as translation.

Uses only Python's standard library. Does not import or launch the game.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


def strings(value, pointer=""):
    if isinstance(value, dict):
        for key in sorted(value):
            escaped = key.replace("~", "~0").replace("/", "~1")
            yield from strings(value[key], f"{pointer}/{escaped}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from strings(item, f"{pointer}/{index}")
    elif isinstance(value, str):
        yield pointer, value


def inventory(root):
    source = root / "resources/lang/en"
    if not source.is_dir():
        raise ValueError(f"English resource directory not found: {source}")
    files = sorted(source.rglob("*.json"))
    if not files:
        raise ValueError("No English JSON resources found")
    entries = []
    file_counts = Counter()
    string_counts = Counter()
    for path in files:
        relative = path.relative_to(source).as_posix()
        category = relative.split("/")[0] if "/" in relative else "root"
        file_counts[category] += 1
        data = json.loads(path.read_text(encoding="utf-8"))
        kind = "i18n" if path.name.endswith(".en.json") else "mixed_resource"
        for pointer, text in strings(data):
            entries.append({
                "id": f"{relative}#{pointer}",
                "file": relative,
                "pointer": pointer,
                "kind": kind,
                "source": text,
                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            })
            string_counts[category] += 1
    return {
        "schema_version": 1,
        "source_directory": "resources/lang/en",
        "scope_note": "All JSON string values, including internal IDs, tags and configuration. Not a translation word count or coverage measure. Excludes Python literals, images and resources outside this directory.",
        "summary": {
            "json_files": len(files),
            "string_values": len(entries),
            "by_category": {
                category: {"files": file_counts[category], "string_values": string_counts[category]}
                for category in sorted(file_counts)
            },
        },
        "entries": entries,
    }


def compare(previous, current):
    if previous.get("schema_version") != current["schema_version"]:
        raise ValueError("Inventory schema versions must match")
    old = {entry["id"]: entry["sha256"] for entry in previous["entries"]}
    new = {entry["id"]: entry["sha256"] for entry in current["entries"]}
    return {
        "added": sorted(new.keys() - old.keys()),
        "removed": sorted(old.keys() - new.keys()),
        "changed": sorted(key for key in old.keys() & new.keys() if old[key] != new[key]),
        "note": "Array positions are locators, not stable event IDs. Reordered arrays require manual matching; never automatically overwrite translations from this diff.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--baseline", type=Path)
    args = parser.parse_args()
    try:
        report = inventory(args.root)
        if args.baseline:
            report["changes"] = compare(
                json.loads(args.baseline.read_text(encoding="utf-8")), report
            )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"Inventory failed: {error}\n")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
