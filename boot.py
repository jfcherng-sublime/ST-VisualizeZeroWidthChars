import sublime
from .plugin.functions import compile_invisible_chars_regex, view_is_dirty_val
from .plugin.Globals import global_get, global_set
from .plugin.log import apply_user_log_level, init_plugin_logger, log
from .plugin.RendererThread import RendererThread
from .plugin.settings import get_package_name, get_setting_renderer_interval, get_settings_object
from .plugin.utils import is_view_normal_ready

# main plugin classes
from .plugin.VisualizeZeroWidthChars import *


def plugin_loaded() -> None:
    def plugin_settings_listener() -> None:
        apply_user_log_level(global_get("logger"))
        global_get("renderer_thread").set_interval(get_setting_renderer_interval())

        char_regex_obj, activated_char_ranges = compile_invisible_chars_regex()
        global_set("activated_char_ranges", activated_char_ranges)
        global_set("char_regex_obj", char_regex_obj)
        log("info", "Activated char ranges: {}".format(activated_char_ranges))

        set_is_dirty_for_all_views(True)

    global_set("logger", init_plugin_logger())
    global_set("renderer_thread", RendererThread())
    plugin_settings_listener()

    get_settings_object().add_on_change(get_package_name(), plugin_settings_listener)
    global_get("renderer_thread").start()


def plugin_unloaded() -> None:
    get_settings_object().clear_on_change(get_package_name())
    global_get("renderer_thread").cancel()


def set_is_dirty_for_all_views(is_dirty: bool) -> None:
    """
    @brief Set is_dirty for all views.

    @param is_dirty Indicate if views are dirty
    """

    for w in sublime.windows():
        for v in w.views():
            if is_view_normal_ready(v):
                view_is_dirty_val(v, is_dirty)
