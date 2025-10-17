[app]
title = MedScan AI
package.name = medscan
package.domain = org.mounir
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy,easyocr,torch,opencv-python,requests,pillow
orientation = portrait
fullscreen = 1

android.api = 33
android.ndk = 25b
android.arch = armeabi-v7a
android.permissions = INTERNET,CAMERA,WRITE_EXTERNAL_STORAGE

# signing (placeholders, replaced by CI)
android.release_keystore = release.keystore
android.release_keystore_password = YOUR_KEYSTORE_PASSWORD
android.release_keyalias = YOUR_KEY_ALIAS
android.release_keyalias_password = YOUR_KEY_PASSWORD
