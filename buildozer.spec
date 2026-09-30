[app]
title = Notification Vault
package.name = notifvault
package.domain = org.example
source.dir = .
source.include_exts = py
version = 0.1
requirements = python3,kivy==2.3.0,pyjnius
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, POST_NOTIFICATIONS, BIND_NOTIFICATION_LISTENER_SERVICE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.add_src = src/android/java
android.extra_manifest_application_arguments = src/android/service.xml

[buildozer]
log_level = 2
warn_on_root = 1
