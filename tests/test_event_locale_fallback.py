"""Exercise event readers directly; random moons alone cannot cover fallback."""
import json

import i18n
import pytest

from tests.test_chinese_profile_health import locale, ROOT


@pytest.mark.parametrize(
    "path",
    [
        str(path.relative_to(ROOT / "resources/lang/en/events")).replace("\\", "/")
        for kind in ("injury", "death", "misc", "new_cat")
        for path in sorted((ROOT / "resources/lang/en/events" / kind).glob("*.json"))
        if path.name != "_debug.json"
    ],
)
def test_short_events_fall_back_to_english(locale, path):
    from scripts.events_module.short.short_event_generation import get_event_dicts

    expected = json.loads(
        (ROOT / "resources/lang/en/events" / path).read_text(encoding="utf-8")
    )
    assert get_event_dicts(path) == expected


@pytest.mark.parametrize("success", [True, False])
@pytest.mark.parametrize("kind", ["other_clan", "outsider"])
def test_diplomacy_events_fall_back_to_english(locale, kind, success):
    from scripts.events_module.generate_events import GenerateEvents

    path = f"leader_den/{'success' if success else 'fail'}/{kind}.json"
    expected = json.loads(
        (ROOT / "resources/lang/en/events" / path).read_text(encoding="utf-8")
    )
    assert GenerateEvents.get_lead_den_event_dicts(kind, success) == expected


@pytest.mark.parametrize(
    "biome",
    [
        p.stem
        for p in sorted((ROOT / "resources/lang/en/events/disasters").glob("*.json"))
    ],
)
def test_ongoing_events_fall_back_and_construct(locale, biome):
    from scripts.events_module.generate_events import GenerateEvents

    expected = json.loads(
        (ROOT / f"resources/lang/en/events/disasters/{biome}.json").read_text(
            encoding="utf-8"
        )
    )
    events = GenerateEvents.generate_ongoing_events("disasters", biome)
    assert [e.event for e in events] == [e["event"] for e in expected]


@pytest.mark.parametrize("language", ["zh", "en"])
def test_littermates_do_not_depend_on_display_language(locale, language):
    from scripts.cat.cats import Cat

    locale.set_locale(language)
    parent = Cat(disable_random=True)
    one = Cat(parent1=parent.ID, moons=1, disable_random=True)
    two = Cat(parent1=parent.ID, moons=1, disable_random=True)
    older = Cat(parent1=parent.ID, moons=3, disable_random=True)
    one.create_inheritance_new_cat()
    two.create_inheritance_new_cat()
    assert one.is_littermate(two)
    assert not one.is_littermate(older)
    assert not one.is_littermate(parent)
    locale.set_locale("en" if language == "zh" else "zh")
    assert one.is_littermate(two)


@pytest.mark.parametrize("state", ["missing", "malformed", "translated"])
def test_resource_preference_and_invalid_json_fallback(locale, tmp_path, state):
    from scripts.game_structure.localization import load_lang_resource

    for language in ("zh", "en"):
        (tmp_path / language / "events").mkdir(parents=True)
    (tmp_path / "en/events/test.json").write_text('["English"]', encoding="utf-8")
    if state != "missing":
        (tmp_path / "zh/events/test.json").write_text(
            '["中文"]' if state == "translated" else "{broken", encoding="utf-8"
        )
    assert load_lang_resource("events/test.json", root_directory=tmp_path) == (
        ["中文"] if state == "translated" else ["English"]
    )
    with pytest.raises(FileNotFoundError):
        load_lang_resource("events/absent.json", root_directory=tmp_path)
    (tmp_path / "en/events/test.json").write_text("{broken", encoding="utf-8")
    if state != "translated":
        with pytest.raises(ValueError):
            load_lang_resource("events/test.json", root_directory=tmp_path)


def test_short_event_cache_tracks_locale(locale, monkeypatch):
    from scripts.events_module.short import short_event_generation as generator

    monkeypatch.setattr(generator, "loaded_events", {})
    original = json.loads(
        (ROOT / "resources/lang/en/events/injury/forest.json").read_text(
            encoding="utf-8"
        )
    )[0]

    def resource(_):
        return [dict(original, event_text=i18n.config.get("locale"))]

    monkeypatch.setattr(generator, "get_event_dicts", resource)
    frequency = original.get("frequency", 4)
    chinese = generator.generate_event_objects("injury", "forest", frequency)
    locale.set_locale("en")
    english = generator.generate_event_objects("injury", "forest", frequency)
    assert chinese and english and chinese is not english
    locale.set_locale("zh")
    assert generator.generate_event_objects("injury", "forest", frequency) is chinese
