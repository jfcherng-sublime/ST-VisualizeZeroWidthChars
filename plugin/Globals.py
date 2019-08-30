from typing import Any, Optional
from .utils import dotted_get, dotted_set


class Globals:
    """
    @brief This class stores application-level global variables.
    """

    # the logger to log messages
    logger = None

    # the background thread for managing phantoms for views
    renderer_thread = None

    activated_char_ranges = []
    char_regex_obj = None


def global_get(dotted: str, default: Optional[Any] = None) -> Any:
    return dotted_get(Globals, dotted, default)


def global_set(dotted: str, value: Any) -> None:
    return dotted_set(Globals, dotted, value)
