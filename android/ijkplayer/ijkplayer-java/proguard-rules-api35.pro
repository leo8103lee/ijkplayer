# IJKPlayer ProGuard Rules for Android API 35

# Keep IJKPlayer native interface
-keep class tv.danmaku.ijk.media.player.** { *; }
-keep class tv.danmaku.ijk.media.player.IjkMediaPlayer { *; }

# Keep FFmpeg JNI callbacks  
-keep class tv.danmaku.ijk.media.player.misc.IMediaDataSource { *; }

# AndroidX compatibility
-keep class androidx.** { *; }
-dontwarn androidx.**

# Modern Media APIs
-keep class android.media.** { *; }
-dontwarn android.media.**

# Hardware acceleration
-keep class android.view.Surface { *; }
-keep class android.graphics.SurfaceTexture { *; }

# Network and SSL (for OpenSSL 3.5.1)
-keep class javax.net.ssl.** { *; }
-dontwarn javax.net.ssl.**

# Audio focus and routing (Android 15)
-keep class android.media.AudioManager { *; }
-keep class android.media.AudioFocusRequest { *; }

# Scoped storage compatibility
-keep class android.provider.MediaStore { *; }
-dontwarn java.nio.file.**
