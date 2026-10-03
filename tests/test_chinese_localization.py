"""Focused checks for the partial Chinese locale and its rendering support."""
import json
import os
from pathlib import Path
import re

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import i18n
import pygame
import pygame_gui
import pytest

from scripts.ui.cjk_text import cjk_break_points, install_cjk_wrapping
from scripts.ui.generate_screen_scale_json import generate_screen_scale

ROOT = Path(__file__).resolve().parents[1]
ZH = ROOT / "resources/lang/zh"


def leaves(value, path=()):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from leaves(item, path + (key,))
    elif isinstance(value, str):
        yield path, value


@pytest.mark.parametrize("path", sorted(ZH.rglob("*.zh.json")))
def test_translation_keys_and_placeholders(path):
    english_path = ROOT / "resources/lang/en" / path.relative_to(ZH)
    english_path = english_path.with_name(english_path.name.replace(".zh.", ".en."))
    english = dict(leaves(json.loads(english_path.read_text(encoding="utf-8"))["en"]))
    chinese = dict(leaves(json.loads(path.read_text(encoding="utf-8"))["zh"]))
    for key, value in chinese.items():
        assert key in english, (path, key)
        required = set(re.findall(r"%\{([^}]+)\}", english[key]))
        actual = set(re.findall(r"%\{([^}]+)\}", value))
        assert required <= actual, (path, key, required, actual)
        # English often writes a literal '1' for the singular form.
        allowed = required | ({"count"} if key[-1] == "one" else set())
        assert actual <= allowed, (path, key, actual)


def test_chinese_font_covers_translated_characters():
    pygame.font.init()
    chars = set()
    for path in ZH.rglob("*.zh.json"):
        for _, value in leaves(json.loads(path.read_text(encoding="utf-8"))["zh"]):
            chars.update(char for char in value if "\u3400" <= char <= "\u9fff")
    assert len(chars) > 300
    for weight in ("Regular", "Bold"):
        font = pygame.font.Font(
            str(ROOT / f"resources/fonts/NotoSansCJKsc-{weight}.otf"), 16
        )
        assert all(
            metric is not None for metric in font.metrics("".join(sorted(chars)))
        )


def test_key_and_file_fallback_and_plural_counts():
    pygame.init()
    pygame.display.set_mode((800, 700))
    manager = pygame_gui.UIManager(
        (800, 700),
        starting_language="zh",
        translation_directory_paths=[str(ZH), str(ROOT / "resources/lang/en")],
    )
    assert manager.get_locale() == "zh"
    assert i18n.t("buttons.new_clan") == "创建族群"
    assert i18n.t("general.moons_age", count=1) == "1 个月亮"
    assert i18n.t("general.moons_age", count=7) == "7 个月亮"
    assert i18n.t("settings.fading") == i18n.t("settings.fading", locale="en")
    from scripts.game_structure.localization import load_lang_resource

    assert load_lang_resource("events/death/general.json") == json.loads(
        (ROOT / "resources/lang/en/events/death/general.json").read_text(
            encoding="utf-8"
        )
    )
    manager.set_locale("en")
    assert i18n.t("buttons.new_clan") == "new clan"
    manager.set_locale("zh")
    assert i18n.t("buttons.new_clan") == "创建族群"


def test_cjk_wrap_preserves_text_and_punctuation():
    install_cjk_wrapping()
    from pygame_gui.core.gui_font_pygame import GUIFontPygame
    from pygame_gui.core.text.text_line_chunk import TextLineChunkFTFont

    pygame.font.init()
    font = GUIFontPygame(str(ROOT / "resources/fonts/NotoSansCJKsc-Regular.otf"), 16)
    original = "族群生活，迎来新的月亮。" * 8
    chunk = TextLineChunkFTFont(
        original, font, False, pygame.Color("black"), True, None
    )
    parts = []
    while chunk.width > 160:
        chunk.x = 0
        rest = chunk.split(160, 160, 0)
        assert rest is not None
        parts.append(chunk.text)
        chunk = rest
    parts.append(chunk.text)
    assert "".join(parts) == original
    assert all(not part.startswith(("，", "。")) for part in parts)
    assert cjk_break_points("（族群）") == [2]
    assert cjk_break_points("ClanGen") == []


def test_scaled_theme_preserves_icon_font(tmp_path):
    generated = tmp_path / "theme.json"
    generate_screen_scale(
        ROOT / "resources/theme/master_screen_scale.json", generated, 1.5
    )
    theme = json.loads(generated.read_text(encoding="utf-8"))
    assert theme["button"]["font"][1]["name"] == "notocjk"
    assert theme["button"]["font"][1]["size"] == "24"
    assert theme["@buttonstyles_icon"]["font"][1]["name"] == "clangen"


def test_packaged_save_directory_is_separate(monkeypatch, tmp_path):
    from types import SimpleNamespace
    from scripts.housekeeping import datadir
    from platformdirs import user_data_dir

    monkeypatch.delenv("CLANGEN_ZH_DATA_DIR", raising=False)
    monkeypatch.setattr(
        datadir,
        "get_version_info",
        lambda: SimpleNamespace(is_source_build=False, is_dev=lambda: False),
    )
    assert datadir.get_data_dir() == user_data_dir("ClanGenChinese", "KestrelFeather")
    assert datadir.get_data_dir() != user_data_dir("ClanGen", "ClanGen")
    monkeypatch.setenv("CLANGEN_ZH_DATA_DIR", str(tmp_path))
    assert Path(datadir.get_data_dir()) == tmp_path
