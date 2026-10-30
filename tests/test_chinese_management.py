"""Management text composition must preserve IDs and custom player text."""
from types import SimpleNamespace

import i18n
import pytest

from tests.test_chinese_profile_health import locale, ROOT


@pytest.mark.parametrize(
    "gender", ["male", "female", "nonbinary", "trans male", "trans female", "自定义认同"]
)
@pytest.mark.parametrize("relationship", [False, True])
def test_management_info_translates_default_gender_but_preserves_custom(
    locale, gender, relationship
):
    from scripts.game_structure import game
    from scripts.cat.cats import Cat

    cat = SimpleNamespace(
        genderalign=gender,
        moons=24,
        status=SimpleNamespace(rank="warrior"),
        personality=SimpleNamespace(trait="loyal"),
        skills=SimpleNamespace(skill_string=lambda **kwargs: "医术"),
    )
    cat.get_genderalign_string = lambda: Cat.get_genderalign_string(cat)
    displayed = Cat.get_info_block(cat, relationship=relationship)
    expected = gender if gender == "自定义认同" else i18n.t(f"general.{gender}")
    assert expected in displayed and "忠诚" in displayed
    assert cat.genderalign == gender and cat.personality.trait == "loyal"
    locale.set_locale("en")
    assert gender in Cat.get_info_block(cat, relationship=relationship)


def test_names_next_to_chinese_and_plural_labels(locale):
    from scripts.events_module.text_adjust import process_text

    cats = {"m_c": ("黑莓掌", {}), "r_c": ("酸模尾", {})}
    assert (
        process_text(i18n.t("screens.choose_mate.no_kits_pair"), cats)
        == "黑莓掌与酸模尾没有共同的子女。"
    )
    assert (
        process_text(i18n.t("screens.choose_mentor.current_mentor", count=1), cats)
        == "黑莓掌目前的导师是酸模尾"
    )
    assert i18n.t("screens.choose_mentor.former_apps", count=0) == ""
    assert i18n.t("screens.choose_mentor.former_apps", count=3) == "\n曾带过 3 名学徒"
    assert i18n.t("relationships.trust", count=-10) == "信任（-10）"


@pytest.mark.parametrize(
    "name",
    [
        "screens/relationship",
        "screens/choose_mate",
        "screens/choose_mentor",
        "screens/choose_adoptive_parent",
        "screens/family_tree",
        "screens/role",
        "screens/mediation",
        "relationships",
        "inheritance",
    ],
)
def test_management_resource_coverage(name):
    from tests.test_chinese_localization import leaves
    import json

    en = json.loads(
        (ROOT / f"resources/lang/en/{name}.en.json").read_text(encoding="utf-8")
    )["en"]
    zh = json.loads(
        (ROOT / f"resources/lang/zh/{name}.zh.json").read_text(encoding="utf-8")
    )["zh"]
    assert set(dict(leaves(en))) == set(dict(leaves(zh)))
