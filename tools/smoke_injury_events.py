"""Trigger translated injuries in smoke_chinese's disposable expanded-mode clan."""


def check_injury_events(change, render, reload_game):
    from copy import deepcopy
    import json
    import re

    from scripts.cat.cats import Cat, create_cat
    from scripts.cat.enums import CatRank
    from scripts.events_module.short.short_event_generation import generate_event_objects
    from scripts.game_structure import game
    from scripts.screens.enums import GameScreen

    scenarios = (
        ("forest", "fst_injury_broken_anyapprentice1", CatRank.APPRENTICE, CatRank.WARRIOR),
        ("forest", "fst_injury_burn_greenleafmultiage1", CatRank.WARRIOR, CatRank.KITTEN),
        ("forest", "fst_injury_shivering_multiapprentice1", CatRank.APPRENTICE, CatRank.APPRENTICE),
        ("beach", "bch_injury_waterinlungs_anyapp1", CatRank.APPRENTICE, CatRank.WARRIOR),
        ("beach", "bch_injury_war_savedenemy1", CatRank.WARRIOR, CatRank.WARRIOR),
        ("mountainous", "mtn_injury_mangledtail_anyany1", CatRank.WARRIOR, CatRank.WARRIOR),
        ("plains", "pln_injury_mangledleg_multimultitraitany1", CatRank.WARRIOR, CatRank.WARRIOR),
        ("wetlands", "wtlnd_injury_poisoned_app1", CatRank.APPRENTICE, CatRank.WARRIOR),
    )
    assert game.clan.game_mode == "expanded"
    game.cur_events_list.clear()
    expected = {}
    for biome, event_id, main_rank, other_rank in scenarios:
        events = [
            event
            for frequency in (1, 2, 3, 4)
            for event in generate_event_objects("injury", biome, frequency)
        ]
        event = deepcopy(next(e for e in events if e.event_id == event_id))
        main, other = create_cat(main_rank), create_cat(other_rank)
        for cat in (main, other):
            game.clan.add_cat(cat)
            cat.injuries.clear()
            cat.illnesses.clear()
            cat.history.possible_history.clear()
        event.main_cat, event.random_cat = main, other
        event.types = ["health"]
        event.execute_event(game.clan.all_other_clans[0])
        assert main.injuries, event_id
        assert re.search(r"[\u4e00-\u9fff]", game.cur_events_list[-1].text)
        assert not re.search(r"m_c|r_c|o_c_n|\{PRONOUN|\{VERB", game.cur_events_list[-1].text)
        for cat in (main, other):
            expected[cat.ID] = json.loads(json.dumps({
                "injuries": cat.injuries,
                "history": cat.history.possible_history,
            }))
    assert any(value["history"] for value in expected.values())
    assert any(
        "救" in entry
        for cat_id in expected
        for relation in Cat.fetch_cat(cat_id).relationships.values()
        for entry in relation.log
    ), "Expected a translated rescue relationship log"
    screen = change(GameScreen.EVENTS)
    # Forced events bypass the normal month-thread UI refresh.
    screen.update_display_events_lists()
    screen.handle_tab_switch("health")
    assert len(screen.display_events) == len(scenarios)
    render("48-translated-injury-events")
    screen.save_button.save_game(screen)
    change(GameScreen.START)
    reload_game()
    for cat_id, saved in expected.items():
        cat = Cat.fetch_cat(cat_id)
        assert json.loads(json.dumps({
            "injuries": cat.injuries,
            "history": cat.history.possible_history,
        })) == saved, cat_id
    screen = change(GameScreen.EVENTS)
    screen.update_display_events_lists()
    screen.handle_tab_switch("health")
    assert len(screen.display_events) == len(scenarios)
    render("49-translated-injury-reloaded")
    print("INJURY_EVENTS_PASS 8 forced events, injuries, relationship logs, history save/reload", flush=True)
