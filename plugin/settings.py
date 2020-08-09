import sublime
import sys
import time
from typing import Any, Optional


def get_package_name() -> str:
    """
    @brief Getsthe package name.

    @return The package name.
    """

    # __package__ will be "THE_PLUGIN_NAME.plugin" under this folder structure
    # anyway, the top module should always be the plugin name
    return __package__.partition(".")[0]


def get_package_path() -> str:
    """
    @brief Gets the package path.

    @return The package path.
    """

    return "Packages/" + get_package_name()


def get_settings_file() -> str:
    """
    @brief Get the settings file name.

    @return The settings file name.
    """

    return get_package_name() + ".sublime-settings"


def get_settings_object() -> sublime.Settings:
    """
    @brief Get the plugin settings object. This function will call `sublime.load_settings()`.

    @return The settings object.
    """

    return sublime.load_settings(get_settings_file())


def get_setting(dotted: str, default: Optional[Any] = None) -> Any:
    """
    @brief Get the plugin setting with the dotted key.

    @param dotted  The dotted key
    @param default The default value if the key doesn't exist

    @return Optional[Any] The setting's value.
    """

    from .Globals import global_get

    return global_get("settings.{}".format(dotted), default)


def get_timestamp() -> float:
    """
    @brief Get the current timestamp (in second).

    @return The timestamp.
    """

    return time.time()


def get_setting_renderer_interval() -> int:
    """
    @brief Get the renderer interval.

    @return The renderer interval.
    """

    interval = get_setting("renderer_interval", 250)

    if interval < 0:
        interval = sys.maxsize

    # a minimum for not crashing the system accidentally
    return int(max(30, interval))
