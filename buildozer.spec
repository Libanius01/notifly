[app]

# (str) Title of your application
title = Notification Vault

# (str) Package name
package.name = notifvault

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (enable empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (enable empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (enable empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv, .buildozer

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.0,pyjnius

# (str) Custom source folders for requirements
# Sets custom source for any requirement with recipes or source init
# requirements.source.kivy = ../kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = MyServiceName:service.py:foreground

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, white, black, yellow, magenta, cyan, gray, lightgray, darkgray,
# grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy, olive, purple, silver, teal.
#android.presplash_color = red

# (list) Permissions
android.permissions = INTERNET, POST_NOTIFICATIONS, BIND_NOTIFICATION_LISTENER_SERVICE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then automatically accept SDK license agreements.
android.accept_sdk_licenses = True

# (str) Android NDK architecture (e.g. arm64-v8a, armeabi-v7a, x86, x86_64)
android.archs = arm64-v8a

# (list) Android additionnal libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so

# (list) Android additionnal libraries to copy into libs/arm64-v8a
#android.add_libs_arm64_v8a = libs/android-v8a/*.so

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir =

# (str) The directory in which python-for-android should look for custom recipes
#p4a.local_recipes =

# (str) Python for android branch to use
p4a.branch = master

# (str) Custom Java source code to include
android.add_src = src/android/java

# (str) Extra XML snippets to merge into the AndroidManifest.xml <application> tag
android.extra_manifest_application_arguments = src/android/service.xml

# (bool) Copy library instead of making a libpack (default is False)
#android.copy_libs = 1

# (list) Gradle dependencies to add
#android.gradle_dependencies =

# (bool) Enable AndroidX support. Enabled by default for Android API 29+.
android.enable_androidx = True

# (list) Packaging options for Android Gradle
#android.packaging_options =

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable, 1 = enable)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (APK, AAB, etc) directory
# bin_dir = ./bin
