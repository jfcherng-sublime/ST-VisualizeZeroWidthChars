import logging
import threading
from typing import Any, List, Optional, Pattern
from .utils import dotted_get, dotted_set


class Globals:
    """
    @brief This class stores application-level global variables.
    """

    # the logger to log messages
    logger = None  # type: logging.Logger

    # the background thread for managing phantoms for views
    renderer_thread = None  # type: threading.Thread

    activated_char_ranges = []  # type: List[str]
    char_regex_obj = None  # type: Pattern


def global_get(dotted: str, default: Optional[Any] = None) -> Any:
    return dotted_get(Globals, dotted, default)


def global_set(dotted: str, value: Any) -> None:
    return dotted_set(Globals, dotted, value)
