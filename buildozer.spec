[app]
title = Gelir Gider Takip
package.name = butcetakip
package.domain = org.butce
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_dirs = __pycache__, .git
version = 1.0
requirements = python3==3.11.9, hostpython3==3.11.9, kivy==2.3.0, cython<3.0
orientation = portrait
fullscreen = 0
android.permissions =
android.minapi = 21
android.api = 33
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = True
android.ndk = 25b
android.ndk_api = 21

[buildozer]
log_level = 2
warn_on_root = 0
