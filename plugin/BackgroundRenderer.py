import sublime
from .functions import (
    detect_chars_globally,
    get_timestamp,
    is_view_typing,
    view_last_update_timestamp_val,
)
from .RepeatingTimer import RepeatingTimer


class BackgroundRenderer:
    """
    @brief This class is a application-level rederer thread in the background.
    """

    def __init__(self, interval: float = 0.5) -> None:
        self.timer = RepeatingTimer(interval, self._check_current_view)

    def __del__(self) -> None:
        self.cancel()

    def _check_current_view(self) -> None:
        view = sublime.active_window().active_view()

        if not is_view_typing(view):
            view_last_update_timestamp_val(view, get_timestamp())
            detect_chars_globally(view)

    def start(self) -> None:
        self.timer.start()

    def cancel(self) -> None:
        self.timer.cancel()
