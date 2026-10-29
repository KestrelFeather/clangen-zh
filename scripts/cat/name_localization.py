"""Display-only translations. Raw name parts remain stable in saves and logic."""
import json
from functools import lru_cache
from pathlib import Path

import i18n


@lru_cache(maxsize=1)
def _chinese_affixes():
    with Path("resources/lang/zh/name_affixes.json").open(encoding="utf-8") as source:
        return json.load(source)


def display_name(prefix: str, suffix: str) -> str:
    """Translate only fully reviewed pairs; preserve unknown and standalone names."""
    original = prefix + suffix
    if i18n.config.get("locale") != "zh" or not prefix or not suffix:
        return original
    translations = _chinese_affixes()
    translated_prefix = translations["prefix"].get(prefix)
    translated_suffix = translations["suffix"].get(suffix)
    if translated_prefix is None or translated_suffix is None:
        return original
    # The Mainland Chinese kit name reverses the order of its two parts.
    if suffix == "kit":
        return translated_suffix + translated_prefix
    return translated_prefix + translated_suffix
