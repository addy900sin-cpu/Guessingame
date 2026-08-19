[app]

# (str) Title of your application
title = Guess The Number

# (str) Package name
package.name = guessnumber

# (str) Package domain
package.domain = org.addy

# (str) Source code directory
source.dir = .

# (str) Main Python file
source.main = main.py

# (list) Application source files
source.include_exts = py,png,jpg,jpeg,kv,atlas,wav,mp3

# (str) Application version
version = 1.0

# (list) Application requirements
requirements = python3,kivy

# (str) Presplash
# presplash.filename = %(source.dir)s/presplash.png

# (str) Icon
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation
orientation = portrait

# (list) List of service to start
services =


[buildozer]

# (str) Log level
log_level = 2

# (int) Warning if buildozer is run as root
warn_on_root = 1


[python]

# (str) Python version
python.version = 3


[android]

# (bool) Indicate if the application is a pure Python application
android.archs = arm64-v8a, armeabi-v7a

# (str) Android API
android.api = 35

# (str) Minimum API
android.minapi = 21

# (str) Android NDK version
android.ndk = 27c

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme
android.apptheme = @android:style/Theme.Material.Light.NoActionBar

# (bool) Fullscreen
fullscreen = 0

# (str) Android permissions
android.permissions = INTERNET


[buildozer:android]

# (str) Android application name
android.app_name = Guess The Number
