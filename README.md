# Sublime-VisualizeZeroWidthChars

<a href="https://packagecontrol.io/packages/VisualizeZeroWidthChars"><img alt="Package Control" src="https://img.shields.io/packagecontrol/dt/VisualizeZeroWidthChars?style=flat-square"></a>
<a href="https://github.com/jfcherng/Sublime-VisualizeZeroWidthChars/tags"><img alt="GitHub tag (latest SemVer)" src="https://img.shields.io/github/tag/jfcherng/Sublime-VisualizeZeroWidthChars?style=flat-square&logo=github"></a>
<a href="https://github.com/jfcherng/Sublime-VisualizeZeroWidthChars/blob/master/LICENSE"><img alt="Project license" src="https://img.shields.io/github/license/jfcherng/Sublime-VisualizeZeroWidthChars?style=flat-square&logo=github"></a>
<a href="https://github.com/jfcherng/Sublime-VisualizeZeroWidthChars/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/jfcherng/Sublime-VisualizeZeroWidthChars?style=flat-square&logo=github"></a>
<a href="https://www.paypal.me/jfcherng/5usd" title="Donate to this project using Paypal"><img src="https://img.shields.io/badge/paypal-donate-blue.svg?style=flat-square&logo=paypal"></a>

![screenshot](https://raw.githubusercontent.com/jfcherng/Sublime-VisualizeZeroWidthChars/master/docs/screenshot.png)

`VisualizeZeroWidthChars` is a Sublime Text 3 plugin which indicates locations of zero-width chars.

```
Can you tel​l me wh​ere are ​zero-width spaces?
```


## Installation

Currently, [this plugin has not been published on Package Control yet](https://github.com/wbond/package_control_channel/pull/7671).
To install this plugin, you have 2 ways:

- Download the tarball from GitHub and decompress it to `Packages/` 
  with this plugin's directory renamed to `VisualizeZeroWidthChars`.
- Or add a custom Package Control repository (recommended, plugin will be auto updated).

  1. Go to `Preferences` » `Package Settings` » `Package Control` » `Settings - User`.
  1. Add custom repository and package name mapping as the following.
     ```javascript
     "package_name_map":
     {
       "Sublime-VisualizeZeroWidthChars": "VisualizeZeroWidthChars",
     },
     "repositories":
     [
       "https://github.com/jfcherng/Sublime-VisualizeZeroWidthChars",
     ]
     ```
  1. Restart Sublime Text.
  1. You should be able to install this package with Package Control with the name of `VisualizeZeroWidthChars`.
  1. After this plugin is published on Package Control, you can remove above settings.

Note that this plugin only supports ST >= 3118 because of Phantom API.

💡 You may also interest in my other plugins: https://packagecontrol.io/search/jfcherng


## Settings

To edit settings, go to `Preferences` » `Package Settings` » `VisualizeZeroWidthChars` » `Settings`.

I think the [settings file](https://github.com/jfcherng/Sublime-VisualizeZeroWidthChars/blob/master/VisualizeZeroWidthChars.sublime-settings) 
is self-explanatory. But if you still have questions, feel free to open an issue.
