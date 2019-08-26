import sublime
import sublime_plugin
from .functions import view_is_dirty_val, view_last_typing_timestamp_val
from .Globals import global_get
from .phantom_sets import init_phantom_set, delete_phantom_set
from .popup import show_popup
from .settings import get_timestamp


class VisualizeZeroWidthChars(sublime_plugin.ViewEventListener):
    def __init__(self, view: sublime.View) -> None:
        super().__init__(view)

        self.view = view
        init_phantom_set(self.view)
        view_is_dirty_val(self.view, True)
        view_last_typing_timestamp_val(self.view, 0)

    def on_pre_close(self) -> None:
        delete_phantom_set(self.view)

    def on_load_async(self) -> None:
        view_is_dirty_val(self.view, True)

    def on_modified_async(self) -> None:
        view_is_dirty_val(self.view, True)
        view_last_typing_timestamp_val(self.view, get_timestamp())

    def on_selection_modified_async(self) -> None:
        sel = self.view.sel()

        # only one cursor and it's empty or only select one char
        if len(sel) == 1 and (sel[0].empty() or len(sel[0]) == 1):
            char = self.view.substr(sel[0].begin())

            # if the cursor is at a zero-width char
            if global_get("char_regex_obj").match(char):
                # get a non-empty char_region
                if sel[0].empty():
                    char_region = sublime.Region(sel[0].a, sel[0].a + 1)
                else:
                    char_region = sel[0]

                show_popup(self.view, char_region, char_region.begin())
