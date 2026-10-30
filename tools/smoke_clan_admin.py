"""Optional clan administration checks in smoke_chinese's isolated save."""


def check_clan_admin(change, render, reload_game):
    import json

    import pygame
    import pygame_gui

    from scripts.game_structure import game
    from scripts.clan_package.settings import get_clan_setting
    from scripts.screens.enums import GameScreen
    from scripts.ui.windows.select_focus_clans import SelectFocusClansWindow
    from scripts.ui.windows.herbs import HerbManagementWindow
    from scripts.ui.windows.freshkill import FreshkillManagementWindow

    def press(element, event_type=pygame_gui.UI_BUTTON_START_PRESS):
        return pygame.event.Event(event_type, ui_element=element)

    settings = change(GameScreen.CLAN_SETTINGS)
    render("33-clan-general")
    setting = next(iter(settings.checkboxes))
    before = get_clan_setting(setting)
    settings.handle_event(press(settings.checkboxes[setting]))
    expected_setting = get_clan_setting(setting)
    assert expected_setting != before
    settings.open_relation_settings()
    render("34-clan-relations")
    settings.open_roles_settings()
    render("35-clan-roles")
    settings.open_clan_stats()
    render("36-clan-stats")

    # Heal the fixture leader so diplomacy is available in this test.
    game.clan.leader.illnesses.clear()
    game.clan.leader.injuries.clear()
    leader = change(GameScreen.LEADER_DEN)
    render("37-leader-den")
    leader.focus_clan = game.clan.all_other_clans[0]
    leader.update_other_clan_focus()
    leader.handle_event(press(leader.focus_frame_elements["positive_interaction"]))
    # JSON turns temperament tuples into lists; compare the saved representation.
    expected_event = json.loads(json.dumps(get_clan_setting("lead_den_clan_event")))
    assert expected_event["other_clan"] == leader.focus_clan.name
    assert expected_event["interaction_type"] in ("praise", "befriend", "appease")
    render("38-diplomacy-selected")
    leader.open_outsiders_tab()
    render("39-outsiders")

    warrior = change(GameScreen.WARRIOR_DEN)
    render("40-warrior-den")
    warrior.handle_event(press(warrior.focus_buttons["raid_other_clans"]))
    assert warrior.active_code == "raid_other_clans"
    window = SelectFocusClansWindow()
    target = game.clan.all_other_clans[0].name
    window.process_event(press(window.checkboxes[target]))
    render("41-select-focus-clans")
    window.process_event(press(window.save_button))
    assert get_clan_setting("raid_other_clans")
    assert game.clan.clans_in_focus == [target]
    changed_at = game.clan.last_focus_change
    render("42-focus-confirmed")

    change(GameScreen.CAMP)
    herbs = HerbManagementWindow()
    render("43-herb-window")
    herbs.kill()
    freshkill = FreshkillManagementWindow()
    render("44-freshkill-window")
    assert "warrior" not in freshkill.get_help_tooltip()
    freshkill.process_event(
        press(freshkill.change_tactics, pygame_gui.UI_BUTTON_PRESSED)
    )
    assert freshkill.open_view == "tactic"
    freshkill.process_event(
        press(
            freshkill.tactic_view_elements["hungriest_first"],
            pygame_gui.UI_BUTTON_PRESSED,
        )
    )
    assert get_clan_setting("hungriest_first")
    render("45-feeding-tactics")
    freshkill.process_event(press(freshkill.open_log, pygame_gui.UI_BUTTON_PRESSED))
    assert freshkill.open_view == "log"
    render("46-freshkill-log")
    freshkill.kill()

    events = change(GameScreen.EVENTS)
    events.save_button.save_game(events)
    change(GameScreen.START)
    reload_game()
    assert get_clan_setting(setting) == expected_setting
    assert get_clan_setting("raid_other_clans")
    assert game.clan.clans_in_focus == [target]
    assert game.clan.last_focus_change == changed_at
    assert get_clan_setting("hungriest_first")
    assert get_clan_setting("lead_den_clan_event") == expected_event, (
        get_clan_setting("lead_den_clan_event"),
        expected_event,
    )
    change(GameScreen.WARRIOR_DEN)
    render("47-clan-admin-reloaded")
    print(
        "CLAN_ADMIN_PASS settings, diplomacy, targeted_focus, resources, save_reload",
        flush=True,
    )
