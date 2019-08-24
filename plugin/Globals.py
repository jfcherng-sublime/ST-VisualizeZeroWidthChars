from .utils import dotted_get, dotted_set


class Globals:
    """
    @brief This class stores application-level global variables.
    """

    PHANTOM_TEMPLATE = """
    <body id="open-Char-phantom">
        <style>{style}</style>
        <span class="desc">{text}</span>
    </body>
    """

    logger = None
    activated_char_ranges = []
    char_regex_obj = None

    phantom_sets = {
        # phantom_set_id: sublime.PhantomSet object,
    }


def global_get(dotted: str, default=None):
    return dotted_get(Globals, dotted, default)


def global_set(dotted: str, value) -> None:
    return dotted_set(Globals, dotted, value)
