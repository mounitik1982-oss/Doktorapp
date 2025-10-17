[app]
title = MedScan AI
package.name = medscan
package.domain = org.lensmed
source.dir = .
source.include_exts = py,kv,png,jpg
version = 1.0.0
requirements = python3,kivy,pillow,opencv-python
orientation = portrait
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 33
android.ndk = 23b
android.arch = armeabi-v7a
android.release = 1
android.keystore = release.keystore
android.keyalias = SUN
android.keyalias_passwd = MedScan2025
android.keystore_passwd = MedScan2025
android.allow_backup = False
android.minapi = 21
android.permissions = INTERNET,CAMERA
