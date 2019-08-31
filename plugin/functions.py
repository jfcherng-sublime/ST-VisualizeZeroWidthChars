import re
import sublime
import unicodedata
from typing import Any, Dict, List, Tuple, Pattern, Optional
from .log import log
from .settings import get_setting, get_timestamp


def compile_invisible_chars_regex() -> Tuple[Pattern, List[str]]:
    """
    @brief Get the compiled regex object for matching Chars.

    @return (compiled regex object, wanted ranges)
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


def view_last_typing_timestamp_val(
    view: sublime.View, timestamp_s: Optional[float] = None
) -> Optional[float]:
    """
    @brief Set/Get the last timestamp (in sec) when "VZWC_char_regions" is updated

    @param view        The view
    @param timestamp_s The last timestamp (in sec)

    @return None if the set mode, otherwise the value
    """

    if timestamp_s is None:
        return view.settings().get("VZWC_last_update_timestamp", False)

    view.settings().set("VZWC_last_update_timestamp", timestamp_s)
    return None


def view_is_dirty_val(view: sublime.View, is_dirty: Optional[bool] = None) -> Optional[bool]:
    """
    @brief Set/Get the is_dirty of the current view

    @param view     The view
    @param is_dirty Indicates if dirty

    @return None if the set mode, otherwise the is_dirty
    """

    if is_dirty is None:
        return view.settings().get("VZWC_is_dirty", True)

    view.settings().set("VZWC_is_dirty", is_dirty)
    return None


def get_char_unicode_info(char: str) -> Dict[str, Any]:
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
    last_typing_s = view_last_typing_timestamp_val(view)

    if not last_typing_s:
        last_typing_s = 0

    return (now_s - last_typing_s) * 1000 < get_setting("typing_period")


def is_view_too_large(view: Optional[sublime.View]) -> bool:
    """
    @brief Determine if the view is too large. Note that size will be 0 if the view is loading.

    @param view The view

    @return True if the view is too large, False otherwise.
    """

    return bool(view and view.size() > get_setting("disable_if_file_larger_than"))
