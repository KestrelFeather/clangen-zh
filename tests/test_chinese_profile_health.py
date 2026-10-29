"""Verify composed descriptions and treatment logs, keeping simulation keys intact."""
import json
import os
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import i18n
import pygame
import pygame_gui
import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def locale():
    previous = i18n.config.get("locale")
    pygame.init()
    pygame.display.set_mode((800, 700))
    manager = pygame_gui.UIManager(
        (800, 700),
        starting_language="zh",
        translation_directory_paths=[
            str(ROOT / "resources/lang/zh"),
            str(ROOT / "resources/lang/en"),
        ],
    )
    yield manager
    i18n.set("locale", previous)


def test_chinese_description_and_english_switch(locale):
    from scripts.game_structure import game
    from scripts.cat.pelts import Pelt
    from scripts.events_module.text_adjust import adjust_list_text

    cat = SimpleNamespace(
        genderalign="male",
        pelt=SimpleNamespace(
            name="Tabby",
            colour="GINGER",
            scars=["NOTAIL", "ONE", "TWO"],
            length="long",
            white_patches=None,
            points=None,
            vitiligo="VITILIGO",
        ),
    )
    assert Pelt.describe_appearance(cat) == "伤痕累累的长毛姜黄色虎斑公猫，带有白斑，没有尾巴"
    assert adjust_list_text(["猫薄荷", "蜘蛛网", "马尾草"]) == "猫薄荷、蜘蛛网和马尾草"
    locale.set_locale("en")
    english = Pelt.describe_appearance(cat)
    assert "long-furred" in english and ", with " in english and "tom" in english
    assert (
        adjust_list_text(["catmint", "cobwebs", "horsetail"])
        == "catmint, cobwebs, and horsetail"
    )
    assert cat.pelt.colour == "GINGER" and cat.pelt.name == "Tabby"


def test_backstory_substitutes_names_and_clan_and_keeps_english_pronouns(locale):
    from scripts.events_module.text_adjust import event_text_adjust

    pronouns = {
        "subject": "he",
        "object": "him",
        "poss": "his",
        "self": "himself",
        "conju": 2,
    }
    cat = SimpleNamespace(name="火星", pronouns=[pronouns])
    clan = SimpleNamespace(displayname="晨光", biome="Forest", override_biome=None)
    text = event_text_adjust(
        None, i18n.t("cat.backstories.clan_guide6"), main_cat=cat, clan=clan
    )
    assert "火星" in text and "晨光族" in text
    assert not any(token in text for token in ("m_c", "c_n", "Clan", "PRONOUN"))
    # Missing narrative resources still use the original English grammar.
    fallback = "m_c knows c_n. {PRONOUN/m_c/subject/CAP} {VERB/m_c/are/is} here."
    assert event_text_adjust(None, fallback, main_cat=cat, clan=clan).endswith(
        "He is here."
    )
    locale.set_locale("en")
    assert "晨光Clan" in event_text_adjust(None, fallback, main_cat=cat, clan=clan)


@pytest.mark.parametrize(
    "category,condition,expected",
    [
        ("illnesses", "whitecough", "白咳症"),
        ("injuries", "sprain", "扭伤"),
        ("permanent_condition", "weak leg", "腿部无力"),
    ],
)
def test_treatment_log_localizes_display_only(
    monkeypatch, locale, category, condition, expected
):
    from scripts.clan_resources.herb.herb_supply import HerbSupply
    from scripts.clan_resources.herb.herb_effects import HerbEffect
    from scripts.game_structure import game

    monkeypatch.setattr(game, "clan", SimpleNamespace(game_mode="expanded"))
    data = {"mortality": 10, "born_with": False}
    cat = SimpleNamespace(
        name="火星", pronouns=[{}], illnesses={}, injuries={}, permanent_condition={}
    )
    getattr(cat, category)[condition] = data
    herbs = HerbSupply()
    herbs._HerbSupply__apply_herb_effect(
        cat, condition, "catmint", HerbEffect.MORTALITY, 1, 1
    )
    assert herbs.log[-1] == f"火星用了猫薄荷来治疗{expected}。死亡的可能性降低了。"
    assert list(getattr(cat, category)) == [condition]
    assert data["mortality"] > 10
    locale.set_locale("en")
    herbs._HerbSupply__apply_herb_effect(
        cat, condition, "catmint", HerbEffect.MORTALITY, 1, 1
    )
    assert "a catmint" in herbs.log[-1] and condition in herbs.log[-1]


@pytest.mark.parametrize(
    "name",
    [
        "cat/personality",
        "cat/skills",
        "cat/eyes",
        "cat/pelts",
        "cat/backstories",
        "cat/accessories",
        "conditions/illnesses",
        "conditions/injuries",
        "conditions/permanent_conditions",
        "conditions/nutrition",
        "conditions/herbs",
        "conditions/pregnancy",
        "screens/med_den",
        "utility",
    ],
)
def test_batch_covers_all_visible_resource_keys(name):
    def keys(value, prefix=()):
        if isinstance(value, dict):
            return {p for k, v in value.items() for p in keys(v, prefix + (k,))}
        return {prefix} if isinstance(value, str) else set()

    english = json.loads(
        (ROOT / f"resources/lang/en/{name}.en.json").read_text(encoding="utf-8")
    )["en"]
    chinese = json.loads(
        (ROOT / f"resources/lang/zh/{name}.zh.json").read_text(encoding="utf-8")
    )["zh"]
    assert keys(english) == keys(chinese)
