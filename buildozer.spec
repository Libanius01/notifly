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
source.include_exts = py,png,jpg,kv,atlas,json,xml,txt,java

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy==2.3.0,pyjnius

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, POST_NOTIFICATIONS, BIND_NOTIFICATION_LISTENER_SERVICE

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

android.build_tools_version = 33.0.2

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then automatically accept SDK license agreements.
android.accept_sdk_licenses = True

# (str) Android NDK architecture
android.archs = arm64-v8a

# CRITICAL FIX: Comment out master branch to prevent unstable p4a breaking changes
# p4a.branch = master

# (str) Custom Java source code to include
android.add_src = src/android/java

# (str) Extra XML snippets to merge into the AndroidManifest.xml <application> tag
android.extra_manifest_application_arguments = src/android/service.xml

# (bool) Enable AndroidX support.
android.enable_androidx = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
