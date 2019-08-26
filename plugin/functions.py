import re
import sublime
import unicodedata
from .log import log
from .settings import get_setting, get_timestamp


def compile_invisible_chars_regex() -> tuple:
    """
    @brief Get the compiled regex object for matching Chars.

    @return Compiled regex object
    """

    # fmt: off
    wanted_ranges = [
        range_
        for range_, enabled in get_setting("invisible_char_regex_ranges").items()
        if enabled
    ]
    # fmt: on

    regex = "[{char_range}]".format(char_range="".join(wanted_ranges))

    log("debug", "Invisible chars matching regex: {}".format(regex))

    try:
        regex_obj = re.compile(regex, re.IGNORECASE)
    except Exception as e:
        log(
            "critical",
            "Cannot compile regex `{regex}` because `{reason}`. "
            'Please check "invisible_char_regex_ranges" in plugin settings.'.format(
                regex=regex, reason=e
            ),
        )

    return regex_obj, wanted_ranges


def view_last_typing_timestamp_val(view: sublime.View, timestamp_s=...):
    """
    @brief Set/Get the last timestamp (in sec) when "VZWC_char_regions" is updated

    @param view        The view
    @param timestamp_s The last timestamp (in sec)

    @return Optional[float] None if the set mode, otherwise the value
    """

    if timestamp_s is ...:
        return view.settings().get("VZWC_last_update_timestamp", False)

    view.settings().set("VZWC_last_update_timestamp", timestamp_s)


def view_is_dirty_val(view: sublime.View, is_dirty=...):
    """
    @brief Set/Get the is_dirty of the current view

    @param view     The view
    @param is_dirty Indicates if dirty

    @return Optional[bool] None if the set mode, otherwise the is_dirty
    """

    if is_dirty is ...:
        return view.settings().get("VZWC_is_dirty", True)

    view.settings().set("VZWC_is_dirty", is_dirty)


def get_char_unicode_info(char: str) -> dict:
    code_point = "{:04X}".format(ord(char))

    try:
        name = unicodedata.name(char)
    except Exception:
        name = "UNKNOWN"

    return {"code_point": code_point, "name": name.title()}


def is_view_typing(view: sublime.View) -> bool:
    """
    @brief Determine if the view typing.

    @param view The view

    @return True if the view is typing, False otherwise.
    """

    now_s = get_timestamp()
    pass_ms = (now_s - view_last_typing_timestamp_val(view)) * 1000

    return pass_ms < get_setting("typing_period")


def is_view_too_large(view: sublime.View) -> bool:
    """
    @brief Determine if the view is too large. Note that size will be 0 if the view is loading.

    @param view The view

    @return True if the view is too large, False otherwise.
    """

    return view.size() > get_setting("disable_if_file_larger_than")
