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
        # Restore before exercising screens/reloading to avoid re-entering this hook.
        pygame.display.update = _original_update
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
        if os.environ.get("CLANGEN_ZH_SMOKE_EXTENDED") == "1":
            from scripts.cat.cats import Cat
            from scripts.clan_package.settings import get_clan_setting
            from scripts.game_structure.screen_settings import MANAGER, screen
            from scripts.screens.enums import GameScreen
            from scripts.ui.windows.herbs import HerbManagementWindow
            from scripts.ui.windows.freshkill import FreshkillManagementWindow

            assert (
                game.clan is not None
            ), "Extended probe requires an isolated fixture save"

            def snapshot():
                return json.loads(
                    json.dumps(
                        {
                            "name": game.clan.name,
                            "age": game.clan.age,
                            "cats": {
                                cat.ID: [
                                    cat.name.prefix,
                                    cat.name.suffix,
                                    cat.status.rank,
                                    cat.mentor,
                                    cat.mate,
                                    cat.adoptive_parents,
                                ]
                                for cat in Cat.all_cats.values()
                            },
                            "focus": game.clan.clans_in_focus,
                            "last_focus_change": game.clan.last_focus_change,
                            "diplomacy": get_clan_setting("lead_den_clan_event"),
                            "interaction_chosen": get_clan_setting(
                                "lead_den_interaction"
                            ),
                            "feeding_order": get_clan_setting("hungriest_first"),
                        }
                    )
                )

            expected = snapshot()

            def change(screen_name):
                old = game.all_screens[game.current_screen]
                old.change_screen(screen_name)
                game.update_game()
                old.exit_screen()
                current = frame.f_globals["all_screens"].get_screen(screen_name)
                current.screen_switches()
                game.switch_screens = False
                return current

            def capture(name):
                for _ in range(10):
                    game.all_screens[game.current_screen].on_use()
                    MANAGER.update(1 / 30)
                    MANAGER.draw_ui(screen)
                pygame.image.save(screen, str(target / f"{name}.png"))

            assert i18n.t("settings.raid_other_clans") == "掠夺其他族群"
            assert i18n.t("screens.leader_den.clans") == "族群"
            change(GameScreen.CLAN_SETTINGS)
            capture("frozen-clan-settings")
            change(GameScreen.WARRIOR_DEN)
            capture("frozen-warrior-den")
            change(GameScreen.LEADER_DEN)
            capture("frozen-leader-den")
            assert snapshot() == expected, "Opening leader den changed a pending action"
            change(GameScreen.CAMP)
            herbs = HerbManagementWindow()
            capture("frozen-herbs")
            herbs.kill()
            food = FreshkillManagementWindow()
            food.close_views()
            food.create_tactic_view()
            capture("frozen-feeding")
            food.kill()
            events = change(GameScreen.EVENTS)
            events.save_button.save_game(events)
            change(GameScreen.START)
            frame.f_globals["load_game"]()
            assert snapshot() == expected, "Frozen save/reload changed fixture state"
            change(GameScreen.WARRIOR_DEN)
            capture("frozen-reloaded")
            result["extended_save_reload"] = True
            result["checked_screens"] = [
                "clan_settings",
                "warrior_den",
                "leader_den",
                "herbs",
                "feeding",
            ]
            moons = int(os.environ.get("CLANGEN_ZH_SMOKE_MOONS", "0"))
            if moons:
                import random
                from scripts import events as month_events
                from scripts.events_module.generate_events import GenerateEvents
                from scripts.events_module.short.short_event_generation import (
                    get_event_dicts,
                )

                random.seed(42)
                assert get_event_dicts("injury/forest.json")
                assert GenerateEvents.generate_ongoing_events("disasters", "forest")
                for kind in ("other_clan", "outsider"):
                    for success in (True, False):
                        assert GenerateEvents.get_lead_den_event_dicts(kind, success)
                assert get_clan_setting(
                    "lead_den_clan_event"
                ), "Fixture must include pending diplomacy"
                month_events.handle_lead_den_event()
                assert not get_clan_setting("lead_den_clan_event")
                starting_age = game.clan.age
                for _ in range(moons):
                    month_events.one_moon()
                assert game.clan.age == starting_age + moons
                events_screen = change(GameScreen.EVENTS)
                capture("frozen-month-events")
                events_screen.save_button.save_game(events_screen)
                expected_after_moons = snapshot()
                change(GameScreen.START)
                frame.f_globals["load_game"]()
                assert snapshot() == expected_after_moons
                result["months_advanced"] = moons
                result["diplomacy_settled"] = True
                result["event_resource_fallback"] = True
                result["post_moon_save_reload"] = True
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
