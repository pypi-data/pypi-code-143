from typing import Callable

import dearpygui.dearpygui as dpg

from trainerbase import scriptengine
from trainerbase import gameobject
from trainerbase import codeinjection
from trainerbase.common import Teleport


def simple_trainerbase_menu(window_title: str, width, height):
    def menu_decorator(initializer: Callable):
        def run_menu_wrapper(on_initialized: Callable):
            dpg.create_context()
            dpg.create_viewport(
                title=window_title,
                min_width=width,
                min_height=height,
                width=width,
                height=height,
            )
            dpg.setup_dearpygui()

            with dpg.window(
                label=window_title,
                tag="menu",
                min_size=[width, height],
                no_close=True,
                no_move=True,
                no_title_bar=True,
                horizontal_scrollbar=True,
            ):
                initializer()

            dpg.show_viewport()

            on_initialized()

            dpg.start_dearpygui()
            dpg.destroy_context()

        return run_menu_wrapper

    return menu_decorator


def add_script_to_gui(
    script: scriptengine.Script,
    label: str,
):
    def on_script_state_change():
        script.enabled = dpg.get_value(script.dpg_tag)

    dpg.add_checkbox(label=label, tag=script.dpg_tag, callback=on_script_state_change, default_value=script.enabled)


def add_gameobject_to_gui(
    gameobject: gameobject.GameObject,
    label: str,
    before_set: Callable = int,
):
    def on_frozen_state_change():
        gameobject.frozen = gameobject.value if dpg.get_value(gameobject.dpg_tag_frozen) else None

    def on_value_set():
        raw_new_value = dpg.get_value(gameobject.dpg_tag_setter)
        if not raw_new_value:
            return

        new_value = before_set(raw_new_value)

        if gameobject.frozen is None:
            gameobject.value = new_value
        else:
            gameobject.frozen = new_value

    with dpg.group(horizontal=True):
        dpg.add_text(label)
        dpg.add_checkbox(tag=gameobject.dpg_tag_frozen, callback=on_frozen_state_change)
        dpg.add_input_text(width=220, tag=gameobject.dpg_tag_getter, readonly=True)
        dpg.add_input_text(width=220, tag=gameobject.dpg_tag_setter, hint="Set value here")
        dpg.add_button(label="Set", callback=on_value_set)


def add_codeinjection_to_gui(
    injection: codeinjection.CodeInjection,
    label: str,
):
    def on_codeinjection_state_change():
        if dpg.get_value(injection.dpg_tag):
            injection.inject()
        else:
            injection.eject()

    dpg.add_checkbox(label=label, tag=injection.dpg_tag, callback=on_codeinjection_state_change)


def add_teleport_to_gui(tp: Teleport):
    tag_teleport_labels = "teleport_labels"

    def on_goto_label():
        tp.goto(dpg.get_value(tag_teleport_labels))

    def on_clip_coords():
        dpg.set_clipboard_text(repr(tp.get_coords()))

    with dpg.tab(label="Teleport", tag="tab_teleport"):
        add_gameobject_to_gui(tp.player_x, "X", before_set=float)
        add_gameobject_to_gui(tp.player_y, "Y", before_set=float)
        add_gameobject_to_gui(tp.player_z, "Z", before_set=float)

        labels = sorted(tp.labels.keys())
        with dpg.group(horizontal=True):
            dpg.add_button(label="Go To", callback=on_goto_label)
            dpg.add_combo(label="Labels", tag=tag_teleport_labels, items=labels, default_value=labels[0])

        dpg.add_button(label="Clip Coords", callback=on_clip_coords)
