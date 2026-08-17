[app]

title = Guessing Game
package.name = guessinggame
package.domain = org.addy

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
