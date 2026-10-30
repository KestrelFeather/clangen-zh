"""Optional management checks, called inside smoke_chinese's isolated game session."""


def check_management(change, render, reload_game):
    import i18n
    import pygame
    import pygame_gui
    from scripts.cat.cats import Cat
    from scripts.cat.enums import CatRank
    from scripts.game_structure import game
    from scripts.game_structure.game.switches import Switch, switch_set_value
    from scripts.screens.enums import GameScreen

    def fixture(prefix, suffix, moons, gender, rank):
        cat = Cat(
            prefix=prefix,
            suffix=suffix,
            moons=moons,
            gender=gender,
            status_dict={"rank": rank},
        )
        game.clan.add_cat(cat)
        return cat

    first = fixture("Bramble", "claw", 40, "male", CatRank.WARRIOR)
    second = fixture("Sorrel", "tail", 40, "female", CatRank.WARRIOR)
    apprentice = fixture("Jay", "feather", 8, "male", CatRank.APPRENTICE)
    mediator = fixture("Sage", "nose", 50, "female", CatRank.MEDIATOR)
    for cat in (first, second, apprentice, mediator):
        cat.create_relationships_new_cat()
        cat.create_inheritance_new_cat()
    first.relationships[second.ID].romance = 60

    def focus(cat, target):
        switch_set_value(Switch.cat, cat.ID)
        return change(target)

    relation = focus(first, GameScreen.RELATIONSHIP)
    relation.inspect_cat = second
    relation.update_inspected_relation()
    render("22-relationships")

    mates = focus(first, GameScreen.CHOOSE_MATE)
    assert second in mates.get_valid_mates()
    mates.selected_cat = second
    mates.update_selected_cat()
    render("23-mate-selection")
    mates.change_mate()
    mates.update_both()
    assert second.ID in first.mate and first.ID in second.mate
    render("24-mates-confirmed")

    mentors = focus(apprentice, GameScreen.CHOOSE_MENTOR)
    mentors.selected_mentor = first
    mentors.update_selected_cat()
    mentors.change_mentor(first)
    mentors.selected_mentor = first
    mentors.update_buttons()
    mentors.update_selected_cat()
    assert apprentice.mentor == first.ID and apprentice.ID in first.apprentice
    render("25-mentor-selection")

    parents = focus(apprentice, GameScreen.CHOOSE_ADOPTIVE_PARENT)
    parents.mates_current_parents = False
    assert second in parents.get_valid_adoptive_parents()
    parents.selected_cat = second
    parents.update_selected_cat()
    parents.change_adoptive_parent()
    parents.update_after_change()
    assert second.ID in apprentice.adoptive_parents
    render("26-adoptive-parents")

    family = focus(apprentice, GameScreen.FAMILY_TREE)
    family.handle_event(
        pygame.event.Event(
            pygame_gui.UI_BUTTON_START_PRESS, ui_element=family.parents_button
        )
    )
    assert family.current_group_name == "parents"
    render("27-family-tree")
    roles = focus(first, GameScreen.CHANGE_ROLE)
    assert "武士" in roles.get_role_blurb()
    render("28-roles")
    # The button changes a real role in the test clan, exercising the translated control.
    roles.handle_event(
        pygame.event.Event(
            pygame_gui.UI_BUTTON_START_PRESS, ui_element=roles.switch_mediator
        )
    )
    assert first.status.rank == CatRank.MEDIATOR
    assert "调解者" in roles.get_role_blurb()
    render("29-role-changed")

    mediation = focus(mediator, GameScreen.MEDIATION)
    mediation.selected_cat_1 = first
    mediation.selected_cat_2 = second
    mediation.update_selected_cats()
    render("30-mediation")
    mediation.handle_event(
        pygame.event.Event(
            pygame_gui.UI_BUTTON_START_PRESS, ui_element=mediation.mediate_button
        )
    )
    assert [first.ID, second.ID] in game.mediated
    assert mediator.ID in game.patrolled
    render("31-mediation-result")
    assert i18n.t("relationships.trust", count=25) == "信任（25）"

    def saved_fields(cat):
        return (
            cat.name.prefix,
            cat.name.suffix,
            cat.genderalign,
            cat.status.rank,
            cat.mentor,
            tuple(cat.mate),
            tuple(cat.adoptive_parents),
        )

    expected = {
        cat.ID: saved_fields(cat) for cat in (first, second, apprentice, mediator)
    }
    events = change(GameScreen.EVENTS)
    events.save_button.save_game(events)
    change(GameScreen.START)
    reload_game()
    assert {
        cat_id: saved_fields(Cat.fetch_cat(cat_id)) for cat_id in expected
    } == expected
    focus(Cat.fetch_cat(apprentice.ID), GameScreen.FAMILY_TREE)
    render("32-management-reloaded")
    print(
        "MANAGEMENT_PASS mate, mentor, adoption, family, role, mediation, save_reload",
        flush=True,
    )
