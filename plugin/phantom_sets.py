import sublime
from collections.abc import Iterable
from .functions import get_char_unicode_info
from .PhatomSetsManager import PhatomSetsManager
from .settings import get_package_name, get_setting

PHANTOM_TEMPLATE = """
<body id="visualize-zero-width-chars-phantom">
    <style>{style}</style>
    <span class="desc">{text}</span>
</body>
"""


def get_phantom_set_id(view: sublime.View) -> str:
    return "w{w_id}v{v_id}".format(w_id=view.window().id(), v_id=view.id())


def init_phantom_set(view: sublime.View) -> None:
    PhatomSetsManager.init_phantom_set(view, get_phantom_set_id(view), get_package_name())


def delete_phantom_set(view: sublime.View) -> None:
    PhatomSetsManager.delete_phantom_set(get_phantom_set_id(view))


def erase_phantom_set(view: sublime.View) -> None:
    PhatomSetsManager.erase_phantom_set(get_phantom_set_id(view))


def update_phantom_set(view: sublime.View, char_regions: Iterable) -> None:
    """
    @brief Note that "char_regions" should be Iterable[sublime.Region]
    """

    PhatomSetsManager.update_phantom_set(
        get_phantom_set_id(view), new_char_phantoms(view, char_regions)
    )


def generate_phantom_html(view: sublime.View, char: str) -> str:
    info = get_char_unicode_info(char)

    return PHANTOM_TEMPLATE.format(
        style=get_setting("phantom_css"), text="U+" + info["code_point"]
    )


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
