"""Build the review inventory from the actual generator pools and reviewed evidence.

Run from the repository root. No source names or random weights are modified.
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://warriors.huijiwiki.com/wiki/"


def inventory():
    data = json.loads((ROOT / "resources/dicts/names/names.json").read_text(encoding="utf-8"))
    result = defaultdict(set)
    pools = {
        "prefix": ("normal_prefixes", "colour_prefixes", "eye_prefixes", "biome_prefixes"),
        "suffix": ("normal_suffixes", "pelt_suffixes", "tortie_pelt_suffixes", "biome_suffixes", "special_suffixes"),
    }

    def walk(value, path, kind):
        if isinstance(value, dict):
            for key, child in value.items():
                walk(child, path + "/" + key, kind)
        elif isinstance(value, list):
            for child in value:
                walk(child, path, kind)
        else:
            result[(kind, value)].add(path)

    for kind, groups in pools.items():
        for group in groups:
            walk(data[group], group, kind)
    return result


def build():
    pools = inventory()
    evidence = json.loads((ROOT / "localization/name-affix-evidence.json").read_text(encoding="utf-8"))
    reviewed = {}
    for group in evidence["groups"]:
        for pair in group["pairs"].split():
            en, zh = pair.split("=")
            for kind in group["kinds"]:
                key = (kind, en.capitalize() if kind == "prefix" else en)
                if key in pools:
                    assert key not in reviewed, key
                    reviewed[key] = {"translation": zh, "source": BASE + group["page"], "basis": group["basis"]}
    pending = evidence["pending"]
    rows = []
    mapping = {"prefix": {}, "suffix": {}}
    for (kind, en), paths in sorted(pools.items()):
        key = kind + ":" + en
        verified = reviewed.get((kind, en))
        decision = pending.get(key, pending.get(en.lower()))
        assert not (verified and decision), key
        row = {"id": key, "kind": kind, "english": en, "pools": sorted(paths)}
        if verified:
            row.update(status="已核实", **verified)
            mapping[kind][en] = verified["translation"]
        elif decision:
            row.update(status="译法待选择", translation="", candidates=decision[0], basis=decision[1], source=BASE + decision[2])
        else:
            row.update(status="本次未核实", translation="", candidates="", basis="未取得足以确定统一译法的灰机站内证据；正文访问受限，不代表该站没有此词。", source="")
        rows.append(row)
    dest = ROOT / "resources/lang/zh/name_affixes.json"
    dest.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out = ROOT / ".localization-work/affixes"
    out.mkdir(parents=True, exist_ok=True)
    (out / "review.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"prefixes": sum(k[0] == "prefix" for k in pools), "suffixes": sum(k[0] == "suffix" for k in pools), "confirmed": len(reviewed), "pending": len(rows)-len(reviewed)}, ensure_ascii=False))


if __name__ == "__main__":
    build()
