# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [0.2.8] - 2020-05-24

### Fixed
- Phantom padding for some color schemes.

  Some color schemes such as Material Theme's have large
  unneeded padding for phantoms somehow.


## [0.2.7] - 2020-04-09

### Changed
- Run with Python 3.8 in ST 4.


## [0.2.6] - 2019-09-02

### Added
- Bound renderer interval with a minimum value.
  So if you accidentally use a tiny value like `0` will not causing ST unresponsive.


## [0.2.5] - 2019-09-01

### Added
- Add and utilize the `typing` module.
- Introduce `mypy` for static analysis.

### Changed
- Make `get_package_name()` not hard-coded.


## [0.2.4] - 2019-08-29

### Fixed
- Do not let exceptions terminate the rendering thread.


## [0.2.3] - 2019-08-29

### Fixed
- Fix renderer thread crashes when viewing an image file with ST.


## [0.2.2] - 2019-08-26

### Changed
- Use a popup to show char information rather than use the status bar.

### Fixed
- Prevent from weird `phantom_set_id` KeyError.


## [0.2.1] - 2019-08-26

### Changed
- Just some code structure tweaks.


## [0.2.0] - 2019-08-26

### Added
- Add the main menu.
- Add new log level: `"DEBUG_LOW`


## [0.1.3] - 2019-08-25

### Changed
- Change default `typing_period` to 250ms and `renderer_interval` to 500ms.
- Minor optimizations.

### Fixed
- Clean up phantoms when file is too large.
- Prevent thread jobs from being overlapped when using a low interval.


## [0.1.2] - 2019-08-25

### Changed
- Minor optimizations.


## [0.1.1] - 2019-08-25

### Fixed
- Fix `phantom_set` is not deleted after closing a view.
- Fix and remove workaround for `is_view_too_large()`.

### Changed
- Disable "dodgy single-ish spaces" by default.


## [0.1.0] - 2019-08-25

### Added
- Make background renderer interval configurable. (`typing_period`)

### Changed
- Optimize background renderer checking procedures.
- Phantoms are now inserted to the begin position of zero-width chars.


## [0.0.2] - 2019-08-25

### Changed
- Show status bar as well if the selection is only one char.


## [0.0.1] - 2019-08-25

### Added
- Initial release.
