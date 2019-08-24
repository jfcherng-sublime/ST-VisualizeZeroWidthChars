import sublime
import time
from .utils import dotted_get


def get_package_name() -> str:
    """
    @brief Getsthe package name.

    @return The package name.
    """

    # __package__ will be "XXX.plugin" under this folder structure
    # so I just have it hard-coded, sadly :/
    return "VisualizeZeroWidthChars"


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
    @brief Get the plugin settings object.

    @return The settings object.
    """

    return sublime.load_settings(get_settings_file())


def get_setting(dotted: str, default=None):
    """
    @brief Get the plugin setting with the dotted key.

    @param dotted  The dotted key
    @param default The default value if the key doesn't exist

    @return Optional[Any] The setting's value.
    """

    return dotted_get(get_settings_object(), dotted, default)


def get_timestamp() -> float:
    """
    @brief Get the current timestamp (in second).

    @return The timestamp.
    """

    return time.time()
