import sublime
from .functions import (
    is_view_normal_ready,
    is_view_too_large,
    is_view_typing,
    update_phantom_set,
    view_char_regions_val,
    view_is_dirty_val,
    view_update_char_regions,
)
from .Globals import global_get
from .log import log
from .RepeatingTimer import RepeatingTimer


class RendererThread(RepeatingTimer):
    def __init__(self, interval_ms: int = 1000) -> None:
        super().__init__(interval_ms, self._check_current_view)

    def _check_current_view(self) -> None:

        view = sublime.active_window().active_view()

        if self._need_detect_chars_globally(view):
            self._detect_chars_globally(view)
            view_is_dirty_val(view, False)

    def _need_detect_chars_globally(self, view: sublime.View) -> bool:
        return (
            is_view_normal_ready(view)
            and view_is_dirty_val(view)
            and not is_view_typing(view)
            and not is_view_too_large(view)
        )

    def _detect_chars_globally(self, view: sublime.View) -> None:
        view_update_char_regions(view, global_get("char_regex_obj"))

        char_regions = [sublime.Region(*r) for r in view_char_regions_val(view)]
        update_phantom_set(view, char_regions)
        log("debug", "Phantoms are re-rendered by detect_chars_globally()")
