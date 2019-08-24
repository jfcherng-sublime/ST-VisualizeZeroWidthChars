import sublime
from .functions import (
    detect_chars_globally,
    get_timestamp,
    is_view_too_large,
    is_view_typing,
    view_is_dirty_val,
    view_last_update_timestamp_val,
)
from .RepeatingTimer import RepeatingTimer


class BackgroundRenderer:
    """
    @brief This class is a application-level rederer thread in the background.
    """

    def __init__(self, interval_ms: int = 500) -> None:
        self.timer = RepeatingTimer(interval_ms / 1000, self._check_current_view)

    def __del__(self) -> None:
        self.cancel()

    def start(self) -> None:
        self.timer.start()

    def cancel(self) -> None:
        self.timer.cancel()

    def change_interval(self, interval_ms: int) -> None:
        is_running = self.timer.is_running

        if is_running:
            self.cancel()

        self.timer = RepeatingTimer(interval_ms / 1000, self._check_current_view)

        if is_running:
            self.start()

    def _check_current_view(self) -> None:
        view = sublime.active_window().active_view()

        if self._need_detect_chars_globally(view):
            detect_chars_globally(view)

            # view has been updated
            view_is_dirty_val(view, False)
            view_last_update_timestamp_val(view, get_timestamp())

    def _need_detect_chars_globally(self, view: sublime.View) -> bool:
        return (
            not view.is_loading()
            and view_is_dirty_val(view)
            and not is_view_typing(view)
            and not is_view_too_large(view)
        )
