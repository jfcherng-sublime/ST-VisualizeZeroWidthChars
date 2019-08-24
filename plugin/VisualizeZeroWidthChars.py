import sublime
import sublime_plugin
from .functions import (
    delete_phantom,
    get_char_unicode_info,
    view_char_regions_val,
    view_is_dirty_val,
    view_last_update_timestamp_val,
)
from .Globals import global_get
from .settings import get_timestamp


class VisualizeZeroWidthChars(sublime_plugin.ViewEventListener):
    def __init__(self, view: sublime.View) -> None:
        super().__init__(view)

        self.view = view
        view_char_regions_val(self.view, [])
        view_is_dirty_val(self.view, True)
        view_last_update_timestamp_val(self.view, 0)

    def on_pre_close(self) -> None:
        delete_phantom_set(self.view)

    def on_load_async(self) -> None:
        view_is_dirty_val(self.view, True)

    def on_selection_modified_async(self) -> None:
        sel = self.view.sel()

        # only one cursor and it's empty or only select one char
        if len(sel) == 1 and (sel[0].empty() or len(sel[0]) == 1):
            char = self.view.substr(sel[0].begin())

            # show char info in the status bar if the cursor is at a zero-width char
            if global_get("char_regex_obj").match(char):
                info = get_char_unicode_info(char)

                self.view.set_status("VZWC_status", "[U+{code_point} = {name}]".format_map(info))

                return

        self.view.set_status("VZWC_status", "")

    def on_modified_async(self) -> None:
        view_is_dirty_val(self.view, True)
        view_last_update_timestamp_val(self.view, get_timestamp())
