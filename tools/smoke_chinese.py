"""Exercise the real game bootstrap and screens in an isolated SDL test session."""
import json
import os
from pathlib import Path
import random
import runpy
import sys

repo = Path(__file__).resolve().parents[1]
output = Path(
    os.environ.get(
        "CLANGEN_ZH_TEST_OUTPUT", repo / ".localization-work" / "screenshots"
    )
).resolve()
output.mkdir(parents=True, exist_ok=True)
data_dir = repo / ".localization-work" / ("smoke-data-" + str(os.getpid()))
os.environ["CLANGEN_ZH_DATA_DIR"] = str(data_dir)
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.chdir(repo)
sys.path.insert(0, str(repo))
random.seed(42)


def check_game(namespace):
    import pygame
    import pygame_gui
    import i18n
    from scripts.game_structure import game
    from scripts.game_structure.screen_settings import MANAGER, screen
    from scripts.screens.enums import GameScreen
    from scripts.game_structure.game.settings import (
        game_setting_set,
        game_settings_save,
    )
    from scripts.game_structure.game.switches import Switch, switch_set_value
    from scripts.cat.cats import Cat

    screens = namespace["all_screens"]

    def render(name):
        for _ in range(10):
            game.all_screens[game.current_screen].on_use()
            MANAGER.update(1 / 30)
            MANAGER.draw_ui(screen)
        pygame.image.save(screen, str(output / (name + ".png")))
        print("SCREENSHOT", name, flush=True)

    def change(target):
        old = game.all_screens[game.current_screen]
        old.change_screen(target)
        game.update_game()
        old.exit_screen()
        current = screens.get_screen(target)
        current.screen_switches()
        game.switch_screens = False
        return current

    assert MANAGER.get_locale() == "zh"
    assert i18n.t("buttons.new_clan") == "创建族群"
    render("01-start")
    settings = change(GameScreen.SETTINGS)
    render("02-settings")
    settings.open_lang_settings()
    settings.handle_checkbox_events(
        pygame.event.Event(
            pygame_gui.UI_BUTTON_START_PRESS, ui_element=settings.checkboxes["en"]
        )
    )
    assert i18n.t("buttons.new_clan") == "new clan"
    settings.handle_checkbox_events(
        pygame.event.Event(
            pygame_gui.UI_BUTTON_START_PRESS, ui_element=settings.checkboxes["zh"]
        )
    )
    assert i18n.t("buttons.new_clan") == "创建族群"
    render("03-language")
    game_settings_save()
    maker = change(GameScreen.MAKE_CLAN)
    render("04-game-mode")
    maker.open_name_clan()
    maker.elements["name_entry"].set_text("晨光")
    render("05-name")
    maker.handle_name_clan_key(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
    assert maker.clan_name == "晨光"
    render("06-leader")
    maker.random_quick_start()
    maker.clan_name = "晨光"
    maker.game_mode = "classic"
    maker.save_clan()
    maker.open_clan_saved_screen()
    render("07-created")
    print("CLAN", game.clan.name, game.clan.age, flush=True)
    change(GameScreen.CAMP)
    render("08-camp")
    switch_set_value(Switch.cat, game.clan.leader.ID)
    change(GameScreen.PROFILE)
    render("09-profile")
    patrol = change(GameScreen.PATROL)
    render("10-patrol-select")
    patrol.current_patrol = [game.clan.leader, game.clan.deputy]
    patrol.run_patrol_start()
    patrol.open_patrol_event_screen()
    render("11-patrol-event")
    patrol.run_patrol_proceed("proceed")
    patrol.open_patrol_complete_screen()
    render("12-patrol-result")
    events = change(GameScreen.EVENTS)
    render("13-events-before")
    old_age = game.clan.age
    events.handle_event(
        pygame.event.Event(
            pygame_gui.UI_BUTTON_PRESSED, ui_element=events.timeskip_button
        )
    )
    events.events_thread.join(timeout=45)
    assert not events.events_thread.is_alive(), "Moon skip timed out"
    for _ in range(5):
        events.on_use()
        MANAGER.update(1 / 30)
    assert game.clan.age == old_age + 1
    events.save_button.save_game(events)
    render("14-events-after")
    expected_ids = sorted(game.clan.clan_cats)
    expected_name = str(game.clan.name)
    expected_displayname = game.clan.displayname
    change(GameScreen.START)
    namespace["load_game"]()
    assert game.clan.age == old_age + 1
    assert sorted(game.clan.clan_cats) == expected_ids
    assert str(game.clan.name) == expected_name
    assert game.clan.displayname == expected_displayname
    change(GameScreen.CAMP)
    render("15-reloaded")
    result = {
        "clan": str(game.clan.name),
        "age": game.clan.age,
        "cat_count": len(game.clan.clan_cats),
        "language": MANAGER.get_locale(),
        "patrol_complete": True,
        "moon_skip": True,
        "save_reload": True,
        "data_dir": str(data_dir),
    }
    (output / "smoke-result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("SMOKE_PASS", result, flush=True)


main_path = repo / "main.py"
stop_line = next(
    i
    for i, line in enumerate(main_path.read_text(encoding="utf-8").splitlines(), 1)
    if line == "while 1:"
)


def trace(frame, event, arg):
    if frame.f_code.co_filename != str(main_path):
        return None
    if event == "line" and frame.f_lineno == stop_line:
        sys.settrace(None)
        check_game(frame.f_globals)
        raise SystemExit(0)
    return trace


sys.settrace(trace)
runpy.run_path(str(main_path), run_name="__main__")
