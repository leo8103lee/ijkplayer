# IJKPlayer - FFmpeg 7.1.2 Modernized Edition

> Cross-platform video player based on [FFmpeg](http://ffmpeg.org) - Upgraded to FFmpeg 7.1.2 + OpenSSL 3.5.1 LTS

 Platform | Status | FFmpeg Version | Architecture
 -------- | ------ | -------------- | ------------
 🤖 Android | ✅ API 9-35 | 7.1.2 | ARMv7a, ARM64, x86, x86_64
 🍎 iOS | ✅ iOS 8-18 | 7.1.2 | ARM64, x86_64 (XCFramework)

## ✨ 2025 Major Upgrade Highlights

### 🚀 Modern Technology Stack
- **FFmpeg 7.1.2**: Latest stable version with performance improvements + security hardening
- **OpenSSL 3.5.1 LTS**: Long-term support version with modern encryption standards
- **iOS 18 Compatible**: Full support for latest iOS SDK and VideoToolbox
- **Android API 35**: Complete support for latest Android build system

### 🏗️ Architecture Revolution
- **XCFramework**: Perfect support for ARM64 Mac development environment
- **Compatibility Layer**: 100% backward compatible with original APIs
- **Modern Build**: Optimized cross-platform build system
- **Security Enhancement**: Comprehensive security algorithm updates

## 📦 Installation & Usage

### Android (API 9-35)
```gradle
// build.gradle (Project level)
allprojects {
    repositories {
        mavenCentral()
        jcenter()
    }
}

// build.gradle (Module level)
dependencies {
    // Core player (Required)
    implementation 'tv.danmaku.ijk.media:ijkplayer-java:0.8.8'
    implementation 'tv.danmaku.ijk.media:ijkplayer-armv7a:0.8.8'

    // Multi-architecture support (Optional)
    implementation 'tv.danmaku.ijk.media:ijkplayer-arm64:0.8.8'
    implementation 'tv.danmaku.ijk.media:ijkplayer-x86:0.8.8'
    implementation 'tv.danmaku.ijk.media:ijkplayer-x86_64:0.8.8'

    // ExoPlayer backend (Experimental)
    implementation 'tv.danmaku.ijk.media:ijkplayer-exo:0.8.8'
}
```

### iOS (iOS 8-18)
Now supports modern **XCFramework** architecture:
- ✅ ARM64 device and simulator perfect coexistence
- ✅ Automatic platform detection and library selection
- ✅ Native Xcode integration, no manual configuration needed

## 🏗️ Build Guide

### 📋 Build Preparation

```bash
# Clone the project
git clone https://github.com/leo8103lee/ijkplayer.git
cd ijkplayer

# Switch to upgrade branch
git checkout master  # Use master branch for latest stable version

# Configure codecs (Three options available)
cd config
```

### ⚙️ Codec Configuration

**Option 1: Full Version (Recommended)**
```bash
# More codecs, supports more formats
rm -f module.sh
ln -s module-default.sh module.sh
```

**Option 2: Lite + HEVC**
```bash
# Smaller size but supports HEVC/H.265
rm -f module.sh
ln -s module-lite-hevc.sh module.sh
```

**Option 3: Minimal Version**
```bash
# Smallest size, basic format support
rm -f module.sh
ln -s module-lite.sh module.sh
```

### 🤖 Android Build

```bash
# 1. Initialize Android build environment
./init-android.sh

# 2. Compile FFmpeg 7.1.2
cd android/contrib
./compile-ffmpeg.sh clean  # Clean previous builds
./compile-ffmpeg.sh all     # Build all architectures (recommended)
# Or single architecture: ./compile-ffmpeg.sh armv7a

# 3. Compile IJKPlayer
cd ..
./compile-ijk.sh all        # Build all architectures
```

### 🍎 iOS Build (XCFramework)

```bash
# 1. Initialize iOS build environment
./init-ios.sh

# 2. Compile FFmpeg 7.1.2 (Dual architecture)
cd ios
./compile-ffmpeg.sh clean
./compile-ffmpeg.sh all     # Build both device and simulator

# 3. Create XCFramework (Modern solution)
./create-xcframeworks.sh    # Automatically create all XCFrameworks
```

#### 🎯 XCFramework Advantages
- ✅ **ARM64 Mac Perfect Support**: Native support for Apple Silicon development environment
- ✅ **Automatic Platform Detection**: Xcode automatically selects the correct library version
- ✅ **Zero Manual Configuration**: Drag-and-drop ready, plug-and-play
- ✅ **Future Compatible**: Supports all new iOS devices and architectures

## 🤝 Technical Support

### Community Support
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/leo8103lee/ijkplayer/issues)
- 💬 **Technical Discussions**: Prefer GitHub Discussions
- 📚 **Documentation**: Check project Wiki and example code

### Upgrade Support
- ✅ **FFmpeg 7.1.2**: Complete upgrade guide and compatibility documentation
- ✅ **XCFramework Migration**: Detailed integration steps
- ✅ **Build Issues**: Complete build environment configuration

## 📄 Open Source License

### Main License
```
Copyright (c) 2025 IJKPlayer Community
Licensed under LGPLv2.1 or later
```

### 🔗 Dependencies

#### Media Processing (LGPL)
- **[FFmpeg 7.1.2](https://ffmpeg.org/)**: Core media processing
- **[libVLC](http://git.videolan.org/?p=vlc.git)**: Media playback support
- **[SoundTouch](http://www.surina.net/soundtouch/)**: Audio processing

#### Security & Encryption (OpenSSL)
- **[OpenSSL 3.5.1 LTS](https://www.openssl.org/)**: Encryption and network security

#### System Integration (Various Open Source Licenses)
- **[SDL](http://www.libsdl.org)**: Cross-platform media layer
- **[libyuv](https://chromium.googlesource.com/libyuv/libyuv/)**: Video processing

#### Android Specific (Apache 2.0)
- **[ExoPlayer](https://github.com/google/ExoPlayer)**: Optional playback backend

### ⚖️ Commercial Use
IJKPlayer is licensed under LGPLv2.1+, available for commercial projects. Please note:

1. **Follow LGPL Requirements**: If modifying IJKPlayer source code, open source the modified parts
2. **Dependency Licenses**: Different dependencies have various license agreements, please review carefully
3. **Legal Consultation**: Consult professional legal advice before commercial use

## 🎉 Conclusion

**IJKPlayer FFmpeg 7.1.2** Modernized Edition brings you:
- 🚀 **Latest Technology Stack**: FFmpeg 7.1.2 + OpenSSL 3.5.1 LTS
- 💪 **Full Compatibility**: 100% backward compatible, seamless upgrade
- 🏗️ **Modern Architecture**: XCFramework + ARM64 Mac perfect support
- 🔒 **Security Hardening**: Modern encryption standards and security practices

Start your modern video playback experience today!

**⭐ If this project helps you, please give it a star!**

---

# IJKPlayer - FFmpeg 7.1.2 现代化版本

> 基于 [FFmpeg](http://ffmpeg.org) 的跨平台视频播放器 - 已升级至 FFmpeg 7.1.2 + OpenSSL 3.5.1 LTS

## ✨ 2025年重大升级亮点

### 🚀 现代化技术栈
- **FFmpeg 7.1.2**: 最新稳定版本，性能提升 + 安全加固
- **OpenSSL 3.5.1 LTS**: 长期支持版本，符合现代加密标准
- **iOS 18 兼容**: 完整支持最新 iOS SDK 和 VideoToolbox
- **Android API 35**: 完整支持最新 Android 构建系统

### 🏗️ 架构革新
- **XCFramework**: 完美支持 ARM64 Mac 开发环境
- **兼容性层**: 100% 向后兼容原有 API
- **现代构建**: 优化的跨平台构建系统
- **安全强化**: 全面的安全算法更新

## 📦 快速开始

### 构建环境要求
- **macOS**: 12.0+ (ARM64 Mac 完美支持)
- **Xcode**: 14.0+ (支持 iOS 18 SDK)
- **Android Studio**: 2022.3.1+ (Electric Eel)

### 快速构建
```bash
# 克隆项目
git clone https://github.com/leo8103lee/ijkplayer.git
cd ijkplayer

# Android 构建
./init-android.sh
cd android/contrib && ./compile-ffmpeg.sh all
cd .. && ./compile-ijk.sh all

# iOS 构建 (XCFramework)
./init-ios.sh
cd ios && ./compile-ffmpeg.sh all
./create-xcframeworks.sh
```

## 🎯 核心特性

### 🚀 性能优化
- **FFmpeg 7.1.2**: 最新解码性能优化
- **硬件加速**: MediaCodec (Android) + VideoToolbox (iOS)
- **多线程解码**: 充分利用多核处理器
- **内存优化**: 智能缓冲策略

### 🎬 媒体支持
- **视频格式**: H.264/H.265, VP8/VP9, AV1
- **音频格式**: AAC, MP3, Opus, FLAC
- **协议支持**: HTTP/HTTPS, HLS, DASH, RTMP
- **字幕支持**: SRT, ASS, WebVTT

### 📱 平台特性

#### Android (API 9-35)
- **架构**: ARMv7a, ARM64, x86, x86_64
- **API**: [MediaPlayer 兼容接口](android/ijkplayer/ijkplayer-java/src/main/java/tv/danmaku/ijk/media/player/IMediaPlayer.java)
- **渲染**: TextureView, SurfaceView
- **音频**: AudioTrack, OpenSL ES

#### iOS (iOS 8-18)
- **架构**: ARM64 (真机 + 模拟器)
- **API**: [MediaPlayer.framework 兼容](ios/IJKMediaPlayer/IJKMediaPlayer/IJKMediaPlayback.h)
- **渲染**: OpenGL ES 2.0/3.0
- **音频**: AudioQueue, AudioUnit
- **加速**: VideoToolbox 硬件解码

#### 🎯 XCFramework 优势
- ✅ **ARM64 Mac 完美支持**: 原生支持 Apple Silicon 开发环境
- ✅ **自动平台检测**: Xcode 自动选择正确的库版本
- ✅ **无需手动配置**: 拖拽即用，零配置集成
- ✅ **未来兼容**: 支持所有新 iOS 设备和架构

## 🤝 技术支持

- 🐛 **问题反馈**: [GitHub Issues](https://github.com/leo8103lee/ijkplayer/issues)
- 💬 **技术讨论**: GitHub Discussions
- 📚 **完整文档**: 英文版本详见上方

## 📄 开源许可

```
Copyright (c) 2025 IJKPlayer Community
Licensed under LGPLv2.1 or later
```

**商业使用**: 基于 LGPLv2.1+ 许可，可用于商业项目。请遵循 LGPL 要求并审查依赖项许可协议。

---

## 🎉 结语

**IJKPlayer FFmpeg 7.1.2** 现代化版本为您带来：
- 🚀 **最新技术栈**: FFmpeg 7.1.2 + OpenSSL 3.5.1 LTS
- 💪 **完整兼容**: 100% 向后兼容，无缝升级
- 🏗️ **现代架构**: XCFramework + ARM64 Mac 完美支持
- 🔒 **安全加固**: 现代加密标准和安全实践

立即开始您的现代化视频播放体验！

**⭐ 如果这个项目对您有帮助，请给个星标支持！**
