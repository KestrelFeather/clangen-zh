"""Clan administration translations and name substitution regressions."""

import json
from types import SimpleNamespace

import i18n
import pytest

from tests.test_chinese_profile_health import locale, ROOT
from tests.test_chinese_localization import leaves


@pytest.mark.parametrize(
    "name",
    ["settings", "screens/clan_settings", "screens/leader_den", "screens/warrior_den"],
)
def test_clan_admin_resource_coverage(name):
    en = json.loads(
        (ROOT / f"resources/lang/en/{name}.en.json").read_text(encoding="utf-8")
    )["en"]
    zh = json.loads(
        (ROOT / f"resources/lang/zh/{name}.zh.json").read_text(encoding="utf-8")
    )["zh"]
    assert set(dict(leaves(en))) == set(dict(leaves(zh)))


def test_other_clan_display_preserves_raw_name_and_english(locale):
    from scripts.events_module.text_adjust import event_text_adjust

    other = SimpleNamespace(name="River")
    assert event_text_adjust(None, "向o_c_n宣战。", other_clan=other) == "向River族宣战。"
    assert other.name == "River"
    locale.set_locale("en")
    assert (
        event_text_adjust(None, "Declare war on o_c_n.", other_clan=other)
        == "Declare war on RiverClan."
    )
    assert event_text_adjust(None, "o_c_n", other_clan="CustomClan") == "CustomClan"


@pytest.mark.parametrize("count", [0, 1, 3])
def test_focus_cooldown_and_prey_counts(locale, count):
    remaining = i18n.t(
        "screens.warrior_den.next_change",
        count=count,
        moons=i18n.t("general.moons_age", count=count),
    )
    assert remaining == ("（现在可以更改）" if count == 0 else f"（{count} 个月后可更改）")
    assert i18n.t("windows.prey_count", count=count, amount=count) == f"{count} 份"


@pytest.mark.parametrize("existing_save", [False, True])
def test_pending_leader_actions_survive_settings_reload(
    monkeypatch, tmp_path, existing_save
):
    from importlib import import_module

    settings = import_module("scripts.clan_package.settings.clan_settings")
    monkeypatch.setattr(settings, "clan_settings", {})
    monkeypatch.setattr(settings, "get_save_dir", lambda: str(tmp_path))
    monkeypatch.setattr(settings, "switch_get_value", lambda _: ["test-clan"])
    expected = {
        "lead_den_interaction": True,
        "lead_den_clan_event": {
            "cat_ID": "13",
            "other_clan": "River",
            "interaction_type": "befriend",
            "success": False,
        },
        "lead_den_outsider_event": {
            "cat_ID": "14",
            "interaction_type": "invite",
            "success": True,
        },
    }
    if existing_save:
        folder = tmp_path / "test-clan"
        folder.mkdir()
        (folder / "clan_settings.json").write_text(
            json.dumps(expected | {"unknown_future_key": 7}), encoding="utf-8"
        )
    settings.load_clan_settings()
    for key, value in expected.items():
        assert settings.get_clan_setting(key) == (
            value if existing_save else (False if isinstance(value, bool) else {})
        )
    assert "unknown_future_key" not in settings.clan_settings


def test_med_den_narrative_structure_tokens_and_font(locale):
    import re
    import pygame
    from scripts.game_structure.localization import load_lang_resource
    from scripts.events_module.text_adjust import process_text

    en = json.loads(
        (ROOT / "resources/lang/en/screens/med_den_messages.json").read_text(
            encoding="utf-8"
        )
    )
    zh = load_lang_resource("screens/med_den_messages.json")
    font = pygame.font.Font(
        str(ROOT / "resources/fonts/fusion-pixel-12px-proportional-zh_hans.otf"), 16
    )

    def check(source, translated):
        if isinstance(source, dict):
            assert source.keys() == translated.keys()
            for key in source:
                check(source[key], translated[key])
        elif isinstance(source, list):
            assert len(source) == len(translated)
            for left, right in zip(source, translated):
                check(left, right)
        else:
            # Chinese omits English pronoun/verb conjugation, but keeps actor references.
            assert set(re.findall(r"m_c|c_n|lead_name|dep_name", source)) == set(
                re.findall(r"m_c|c_n|lead_name|dep_name", translated)
            )
            assert re.findall(r"</?i>", source) == re.findall(r"</?i>", translated)
            rendered = process_text(translated, {"m_c": ("酸模尾", {})})
            assert "m_c" not in rendered and "{" not in rendered
            assert all(
                x is not None
                for x in font.metrics("".join(c for c in translated if ord(c) > 127))
            )

    check(en, zh)
    locale.set_locale("en")
    assert load_lang_resource("screens/med_den_messages.json") == en


@pytest.mark.parametrize("outsider", [False, True])
def test_restoring_leader_notice_does_not_reroll_action(monkeypatch, outsider):
    from unittest.mock import Mock
    from scripts.game_structure import game
    from scripts.screens.LeaderDenScreen import LeaderDenScreen

    monkeypatch.setattr(game, "clan", SimpleNamespace(leader=object()))
    notice = Mock()
    handler = Mock()
    screen = SimpleNamespace(
        screen_elements={"clan_notice_text": notice, "outsider_notice_text": notice},
        focus_clan=object(),
        focus_cat=object(),
        handle_other_clan_interaction=handler,
        handle_outsider_interaction=handler,
    )
    method = (
        LeaderDenScreen.update_outsider_interaction_choice
        if outsider
        else LeaderDenScreen.update_clan_interaction_choice
    )
    action = "invite" if outsider else "befriend"
    method(screen, action, update_event=False)
    notice.set_text.assert_called_once()
    handler.assert_not_called()
    method(screen, action)
    handler.assert_called_once_with(action)
