import sublime
import sublime_plugin
from .functions import (
    detect_chars_globally,
    erase_phantom,
    get_char_unicode_info,
    view_char_regions_val,
    view_last_update_timestamp_val,
)
from .Globals import global_get
from .settings import get_setting, get_timestamp


class VisualizeZeroWidthChars(sublime_plugin.ViewEventListener):
    def __init__(self, view: sublime.View) -> None:
        super().__init__(view)

        self.view = view
        view_last_update_timestamp_val(self.view, 0)
        view_char_regions_val(self.view, [])

    def __del__(self) -> None:
        self._clean_up()

    def on_load_async(self) -> None:
        self._refresh()

    def on_activated_async(self) -> None:
        self._refresh()

    def on_selection_modified_async(self) -> None:
        sel = self.view.sel()

        # only one cursor and it's empty or only select one char
        if len(sel) == 1 and (sel[0].empty() or len(sel[0]) == 1):
            char = self.view.substr(sel[0].begin())

            # show char info in the status bar if the cursor is at a zero-width char
            if global_get("char_regex_obj").match(char):
                code_point, name = get_char_unicode_info(char)

                self.view.set_status(
                    "VZWC_status",
                    "[U+{code_point} = {name}]".format(code_point=code_point, name=name),
                )

                return

        self.view.set_status("VZWC_status", "")

    def on_modified_async(self) -> None:
        if not self._need_detect_chars_globally():
            return

        view_last_update_timestamp_val(self.view, get_timestamp())

    def on_close(self) -> None:
        self._clean_up()

    def _clean_up(self) -> None:
        view_char_regions_val(self.view, [])
        erase_phantom(self.view)

    def _refresh(self) -> None:
        if not self._need_detect_chars_globally():
            return

        detect_chars_globally(self.view)

    def _need_detect_chars_globally(self) -> bool:
        return not self._clean_up_if_file_too_large()

    def _clean_up_if_file_too_large(self) -> bool:
        is_file_too_large = self._is_file_too_large()

        if is_file_too_large:
            self._clean_up()

        return is_file_too_large

    def _is_file_too_large(self) -> bool:
        view_size = self.view.size()

        # somehow ST sometimes return size == 0 when reloading a file...
        # it looks like ST thinks the file content is empty dCharng reloading
        # and triggered "on_modified_async()"
        if view_size == 0:
            return True

        return view_size > get_setting("disable_if_file_larger_than")
