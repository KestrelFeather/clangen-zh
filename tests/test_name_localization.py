"""Display translation must not alter name generation or saved affixes."""
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import i18n
import pygame
import pytest

from scripts.cat.name_localization import display_name
from scripts.cat.enums import CatAge, CatRank
from scripts.cat.names import Name
from scripts.game_structure import constants
from tools.prepare_name_affixes import inventory


@pytest.fixture(autouse=True)
def locale():
    previous = i18n.config.get('locale')
    i18n.set('locale', 'zh')
    yield
    i18n.set('locale', previous)


def name_for(rank=CatRank.WARRIOR):
    status = SimpleNamespace(rank=rank, is_former_clancat=False, is_lost=Mock(return_value=False))
    cat = SimpleNamespace(status=status, age=CatAge.ADULT)
    name = Name.__new__(Name)
    name.prefix, name.suffix, name.cat, name.specsuffix_hidden = 'Bramble', 'claw', cat, False
    return name


def test_rank_changes_and_locale_toggle_preserve_raw_parts():
    name = name_for()
    for rank, expected in [(CatRank.KITTEN,'小黑莓'), (CatRank.APPRENTICE,'黑莓爪'), (CatRank.WARRIOR,'黑莓掌'), (CatRank.LEADER,'黑莓星')]:
        name.cat.status.rank = rank
        assert str(name) == expected
        assert (name.prefix, name.suffix) == ('Bramble','claw')
    i18n.set('locale','en')
    assert str(name) == 'Bramblestar'
    i18n.set('locale','zh')
    assert str(name) == '黑莓星'


def test_hidden_special_suffix_and_ceremony_preview():
    name = name_for(CatRank.APPRENTICE)
    assert name.get_specsuffix_name(CatRank.LEADER) == '黑莓星'
    name.specsuffix_hidden = True
    assert str(name) == name.get_specsuffix_name(CatRank.LEADER) == '黑莓掌'


def test_former_and_lost_clan_cats_keep_existing_rank_rules():
    name = name_for(CatRank.LONER)
    name.cat.status.is_former_clancat = True
    name.cat.status.find_prior_clan_rank = lambda: CatRank.LEADER
    assert str(name) == '黑莓星'
    name.cat.status.is_former_clancat = False
    name.cat.status.is_lost.return_value = True
    name.cat.age = CatAge.KITTEN
    assert str(name) == '小黑莓'
    name.cat.age = CatAge.ADULT
    assert str(name) == '黑莓掌'


@pytest.mark.parametrize('prefix,suffix', [('Sorrel','tail'),('Fire','pelt'),('Unknown','fur'),('Bramble','unknown'),('Jay',''),('我的猫',''),('fire','heart')])
def test_unconfirmed_custom_and_standalone_names_are_unchanged(prefix,suffix):
    assert display_name(prefix,suffix) == prefix+suffix


def test_april_fools_still_uses_original_egg_name(monkeypatch):
    monkeypatch.setitem(constants.CONFIG['fun'],'april_fools',True)
    assert str(name_for()) == 'Brambleegg'


def test_mapping_matches_inventory_and_pixel_font():
    mapping = json.loads(Path('resources/lang/zh/name_affixes.json').read_text(encoding='utf-8'))
    pools=inventory()
    chars=set()
    for kind, entries in mapping.items():
        for en, zh in entries.items():
            assert (kind,en) in pools
            assert zh and not any(c.isascii() for c in zh)
            chars.update(zh)
    pygame.font.init()
    font=pygame.font.Font('resources/fonts/fusion-pixel-12px-proportional-zh_hans.otf',16)
    missing=[c for c,m in zip(sorted(chars),font.metrics(''.join(sorted(chars)))) if m is None]
    assert not missing
