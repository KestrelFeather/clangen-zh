"""Translated narrative must preserve every simulation field and actor reference."""
from copy import deepcopy
import json
import re
from types import SimpleNamespace

import pygame
import pytest

from tests.test_chinese_profile_health import locale, ROOT

BIOMES = ("forest", "beach", "mountainous", "plains", "wetlands")
ACTORS = re.compile(r"o_c_n|m_c|r_c|cat_from|cat_to")


def read_events(language, biome):
    return json.loads(
        (ROOT / f"resources/lang/{language}/events/injury/{biome}.json").read_text(
            encoding="utf-8"
        )
    )


def text_fields(event):
    yield event, "event_text"
    for history in event.get("history", []):
        for field in ("scar", "death", "lead_death"):
            if field in history:
                yield history, field
    for relationship in event.get("relationships", []):
        for field in relationship.get("log", {}):
            yield relationship["log"], field


@pytest.mark.parametrize("biome", BIOMES)
def test_injury_translation_preserves_mechanics_and_renders(locale, biome):
    from scripts.events_module.text_adjust import event_text_adjust, process_text
    from scripts.game_structure.localization import load_lang_resource

    english = read_events("en", biome)
    chinese = load_lang_resource(f"events/injury/{biome}.json")
    assert chinese == read_events("zh", biome)
    assert [e["event_id"] for e in english] == [e["event_id"] for e in chinese]
    font = pygame.font.Font(
        str(ROOT / "resources/fonts/fusion-pixel-12px-proportional-zh_hans.otf"), 16
    )
    main = SimpleNamespace(name="测试主猫", pronouns=[{}])
    other = SimpleNamespace(name="测试同伴", pronouns=[{}])
    for source, translated in zip(english, chinese):
        restored = deepcopy(translated)
        for (src, key), (dst, dst_key) in zip(text_fields(source), text_fields(restored)):
            assert key == dst_key
            text = dst[key]
            assert re.search(r"[\u4e00-\u9fff]", text), source["event_id"]
            assert set(ACTORS.findall(src[key])) == set(ACTORS.findall(text))
            assert re.findall(r"</?\w+[^>]*>", src[key]) == re.findall(
                r"</?\w+[^>]*>", text
            )
            rendered = event_text_adjust(
                None, text, main_cat=main, random_cat=other,
                other_clan=SimpleNamespace(name="测试邻"),
            )
            rendered = process_text(
                rendered,
                {"cat_from": ("测试主猫", {}), "cat_to": ("测试同伴", {})},
                raise_exception=True,
            )
            assert not ACTORS.search(rendered) and "{" not in rendered
            assert not re.search(r"[A-Za-z]", rendered), rendered
            assert all(metric is not None for metric in font.metrics(rendered))
            dst[key] = src[key]
        # Exact deep equality includes IDs, ordering, conditions, injury keys,
        # history recipients, relationship direction, amounts, and frequencies.
        assert restored == source, source["event_id"]
    locale.set_locale("en")
    assert load_lang_resource(f"events/injury/{biome}.json") == english


@pytest.mark.parametrize("biome", BIOMES)
def test_translated_injury_objects_switch_languages(locale, monkeypatch, biome):
    from scripts.events_module.short import short_event_generation as generator

    monkeypatch.setattr(generator, "loaded_events", {})
    snapshots = {}
    for language in ("zh", "en", "zh"):
        locale.set_locale(language)
        events = [
            event
            for frequency in (1, 2, 3, 4)
            for event in generator.generate_event_objects("injury", biome, frequency)
        ]
        actual = {event.event_id: event.text_template for event in events}
        assert actual == {
            event["event_id"]: event["event_text"]
            for event in read_events(language, biome)
        }
        if language in snapshots:
            assert actual == snapshots[language]
        snapshots[language] = actual
