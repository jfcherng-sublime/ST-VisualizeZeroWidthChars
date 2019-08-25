import re
import sublime
import unicodedata
from collections.abc import Iterable
from .Globals import global_get
from .log import log
from .settings import get_package_name, get_setting, get_timestamp
from .utils import region_into_list_form, view_find_all_fast


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


def view_update_char_regions(view: sublime.View, char_regex_obj) -> None:
    """
    @brief Update view's "char_regions" variable

    @param view          The view
    @param char_regex_obj The char regex obj
    """

    view_char_regions_val(view, view_find_all_fast(view, char_regex_obj, False))


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


def view_char_regions_val(view: sublime.View, char_regions=...):
    """
    @brief Set/Get the char regions (in list of lists) of the current view

    @param view        The view
    @param char_regions The char regions (... = get mode, otherwise = set mode)

    @return Optional[list[list[int]]] None if the set mode, otherwise the char regions
    """

    if char_regions is ...:
        return view.settings().get("VZWC_char_regions", [])

    view.settings().set("VZWC_char_regions", [region_into_list_form(r, True) for r in char_regions])


def view_last_update_timestamp_val(view: sublime.View, timestamp_s=...):
    """
    @brief Set/Get the last timestamp (in sec) when "VZWC_char_regions" is updated

    @param view        The view
    @param timestamp_s The last timestamp (in sec)

    @return Optional[float] None if the set mode, otherwise the value
    """

    if timestamp_s is ...:
        return view.settings().get("VZWC_last_update_timestamp", False)

    view.settings().set("VZWC_last_update_timestamp", timestamp_s)


def set_is_dirty_for_all_views(is_dirty: bool) -> None:
    """
    @brief Set is_dirty for all views.

    @param is_dirty Indicate if views are dirty
    """

    for w in sublime.windows():
        for v in w.views():
            if not v.settings().get("is_widget") and not v.is_loading():
                view_is_dirty_val(v, is_dirty)


def get_phantom_set_key(window_id: int, view_id: int) -> str:
    return "w{w_id}v{v_id}".format(w_id=window_id, v_id=view_id)


def get_view_phantom_set(view: sublime.View) -> sublime.PhantomSet:
    phantom_sets = global_get("phantom_sets")
    phantom_set_id = get_phantom_set_key(view.window().id(), view.id())

    if phantom_set_id not in phantom_sets:
        phantom_sets[phantom_set_id] = sublime.PhantomSet(view, get_package_name())

    return phantom_sets[phantom_set_id]


def detect_chars_globally(view: sublime.View) -> None:
    view_update_char_regions(view, global_get("char_regex_obj"))

    char_regions = [sublime.Region(*r) for r in view_char_regions_val(view)]
    update_phantom_set(view, char_regions)
    log("debug", "Phantoms are re-rendered by detect_chars_globally()")


def generate_phantom_html(view: sublime.View, char: str) -> str:
    info = get_char_unicode_info(char)

    return global_get("PHANTOM_TEMPLATE").format(
        style=get_setting("phantom_css"), text="U+" + info["code_point"]
    )


def get_char_unicode_info(char: str) -> dict:
    code_point = "{:04X}".format(ord(char))

    try:
        name = unicodedata.name(char)
    except Exception:
        name = "UNKNOWN"

    return {"code_point": code_point, "name": name.title()}


def new_char_phantom(view: sublime.View, char_region: sublime.Region) -> sublime.Phantom:
    char = view.substr(char_region)[0]

    return sublime.Phantom(
        # the "begin" position has a better visual selection result than the "end" position
        sublime.Region(char_region.begin()),
        generate_phantom_html(view, char),
        layout=sublime.LAYOUT_INLINE,
    )


def new_char_phantoms(view: sublime.View, char_regions: Iterable) -> list:
    """
    @brief Note that "char_regions" should be Iterable[sublime.Region]

    @return list[sublime.Phantom]
    """

    return [new_char_phantom(view, r) for r in char_regions]


def delete_phantom_set(view: sublime.View) -> None:
    phantom_sets = global_get("phantom_sets")
    phantom_set_id = get_phantom_set_key(view.window().id(), view.id())
    phantom_sets.pop(phantom_set_id, None)


def erase_phantom_set(view: sublime.View) -> None:
    get_view_phantom_set(view).update([])


def update_phantom_set(view: sublime.View, char_regions: Iterable) -> None:
    """
    @brief Note that "char_regions" should be Iterable[sublime.Region]
    """

    get_view_phantom_set(view).update(new_char_phantoms(view, char_regions))


def is_view_typing(view: sublime.View) -> bool:
    """
    @brief Determine if the view typing.

    @param view The view

    @return True if the view is typing, False otherwise.
    """

    now_s = get_timestamp()
    pass_ms = (now_s - view_last_update_timestamp_val(view)) * 1000

    return pass_ms < get_setting("typing_period")


def is_view_too_large(view: sublime.View) -> bool:
    """
    @brief Determine if the view is too large. Note that size will be 0 if the view is loading.

    @param view The view

    @return True if the view is too large, False otherwise.
    """

    return view.size() > get_setting("disable_if_file_larger_than")
