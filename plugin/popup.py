import sublime
from .functions import get_char_unicode_info

POPUP_TEMPLATE = """
<body id="visualize-zero-width-chars-popup">
    <span>U+{code_point}: {name}</span>
</body>
"""


def generate_popup_html(view: sublime.View, char_region: sublime.Region) -> str:
    char = view.substr(char_region)
    char_info = get_char_unicode_info(char)

    return POPUP_TEMPLATE.format_map(char_info)


def show_popup(view: sublime.View, char_region: sublime.Region, point: int) -> None:
    view.show_popup(
        generate_popup_html(view, char_region),
        flags=sublime.COOPERATE_WITH_AUTO_COMPLETE,
        location=point,
        max_width=500,
    )
