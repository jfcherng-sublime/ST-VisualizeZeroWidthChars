import os
import sublime
from .plugin.BackgroundRenderer import BackgroundRenderer
from .plugin.Globals import global_get, global_set
from .plugin.log import apply_user_log_level, init_plugin_logger, log
from .plugin.functions import compile_invisible_chars_regex
from .plugin.settings import get_package_name, get_settings_file, get_settings_object

# main plugin classes
from .plugin.VisualizeZeroWidthChars import *

# the background thread for managing phantoms for views
background_renderer = BackgroundRenderer()


def plugin_loaded() -> None:
    def plugin_settings_listener() -> None:
        apply_user_log_level(global_get("logger"))

        char_regex_obj, activated_char_ranges = compile_invisible_chars_regex()
        global_set("activated_char_ranges", activated_char_ranges)
        global_set("char_regex_obj", char_regex_obj)
        log("info", "Activated char ranges: {}".format(activated_char_ranges))

        refresh_if_settings_file()

    def refresh_if_settings_file() -> None:
        """ refresh the saved settings file to directly reflect visual changes """
        v = sublime.active_window().active_view()
        if os.path.basename(v.file_name() or "").endswith(get_settings_file()):
            v.run_command("revert")

    global_set("logger", init_plugin_logger())
    get_settings_object().add_on_change(get_package_name(), plugin_settings_listener)
    plugin_settings_listener()
    background_renderer.start()


def plugin_unloaded() -> None:
    get_settings_object().clear_on_change(get_package_name())
    background_renderer.cancel()
