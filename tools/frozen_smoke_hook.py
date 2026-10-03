"""Opt-in CI startup probe; inert unless CLANGEN_ZH_SMOKE_OUTPUT is set.

Capture the real frozen game's first rendered screen and then exit. Use a
separate CLANGEN_ZH_DATA_DIR to avoid reading or writing a player's save files.
"""
import os

if os.environ.get("CLANGEN_ZH_SMOKE_OUTPUT"):
    import json
    from pathlib import Path
    import sys
    import pygame

    _original_update = pygame.display.update
    _rendered_frames = 0

    def _capture_after_startup(*args, **kwargs):
        global _rendered_frames
        _original_update(*args, **kwargs)
        frame = sys._getframe(1)
        if (
            frame.f_code.co_name != "<module>"
            or Path(frame.f_code.co_filename).name != "main.py"
        ):
            return
        if not frame.f_globals.get("finished_loading"):
            return
        _rendered_frames += 1
        if _rendered_frames < 10:
            return
        import i18n
        from scripts.game_structure import game
        from scripts.game_structure.game.switches import Switch, switch_get_value
        from scripts.housekeeping.datadir import get_data_dir
        from scripts.housekeeping.version import get_version_info

        target = Path(os.environ["CLANGEN_ZH_SMOKE_OUTPUT"])
        target.mkdir(parents=True, exist_ok=True)
        pygame.image.save(
            pygame.display.get_surface(), str(target / "frozen-start.png")
        )
        error = switch_get_value(Switch.error_message)
        result = {
            "frozen": bool(getattr(sys, "frozen", False)),
            "locale": i18n.config.get("locale"),
            "new_clan_label": i18n.t("buttons.new_clan"),
            "version": get_version_info().version_number,
            "upstream": get_version_info().upstream,
            "data_dir": get_data_dir(),
            "load_error": str(error) if error else None,
            "clan_name": str(game.clan.name) if game.clan else None,
            "clan_age": game.clan.age if game.clan else None,
            "cat_count": len(game.clan.clan_cats) if game.clan else 0,
        }
        result["passed"] = (
            result["frozen"]
            and result["locale"] == "zh"
            and result["new_clan_label"] == "创建族群"
            and result["upstream"] == "KestrelFeather/clangen-zh"
            and not error
        )
        (target / "frozen-smoke.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        pygame.quit()
        raise SystemExit(0 if result["passed"] else 1)

    pygame.display.update = _capture_after_startup
