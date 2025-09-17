# IJKPlayer - FFmpeg 7.1.2 现代化版本

> 基于 [FFmpeg](http://ffmpeg.org) 的跨平台视频播放器 - 已升级至 FFmpeg 7.1.2 + OpenSSL 3.5.1 LTS

 Platform | Status | FFmpeg Version | Architecture
 -------- | ------ | -------------- | ------------
 🤖 Android | ✅ API 9-35 | 7.1.2 | ARMv7a, ARM64, x86, x86_64
 🍎 iOS | ✅ iOS 8-18 | 7.1.2 | ARM64, x86_64 (XCFramework)

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

## 📦 安装使用

### Android (API 9-35)
```gradle
// build.gradle (项目级别)
allprojects {
    repositories {
        mavenCentral()
        jcenter()
    }
}

// build.gradle (模块级别)
dependencies {
    // 核心播放器 (必需)
    implementation 'tv.danmaku.ijk.media:ijkplayer-java:0.8.8'
    implementation 'tv.danmaku.ijk.media:ijkplayer-armv7a:0.8.8'

    // 多架构支持 (可选)
    implementation 'tv.danmaku.ijk.media:ijkplayer-arm64:0.8.8'
    implementation 'tv.danmaku.ijk.media:ijkplayer-x86:0.8.8'
    implementation 'tv.danmaku.ijk.media:ijkplayer-x86_64:0.8.8'

    // ExoPlayer 后端 (实验性)
    implementation 'tv.danmaku.ijk.media:ijkplayer-exo:0.8.8'
}
```

### iOS (iOS 8-18)
现在支持现代 **XCFramework** 架构：
- ✅ ARM64 真机和模拟器完美共存
- ✅ 自动平台检测和库选择
- ✅ Xcode 原生集成，无需手动配置

## 💻 现代化构建环境

### 系统要求
- **macOS**: 12.0+ (ARM64 Mac 完美支持)
- **Xcode**: 14.0+ (支持 iOS 18 SDK)
- **Android Studio**: 2022.3.1+ (Electric Eel)

### Android 构建环境
- **NDK**: r25c+ (支持 API 35)
- **Gradle**: 8.0+
- **Target SDK**: 35 (Android 15)
- **Min SDK**: 9 (Android 2.3+)

### iOS 构建环境
- **iOS Deployment Target**: 8.0+
- **支持架构**: ARM64 真机 + ARM64 模拟器
- **XCFramework**: 原生支持 Apple Silicon

### 依赖安装
```bash
# Homebrew 安装 (Apple Silicon 优化)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 必需工具
brew install git yasm cmake pkg-config

# 环境变量设置 (添加到 ~/.zshrc)
export ANDROID_SDK_ROOT="$HOME/Library/Android/sdk"
export ANDROID_NDK="$ANDROID_SDK_ROOT/ndk/25.2.9519653"
```

## 🔄 版本更新
- **FFmpeg 7.1.2 升级完成** - 查看详细信息: [更新日志](NEWS.md)
- **XCFramework 架构迁移** - ARM64 Mac 完美支持
- **安全加固** - OpenSSL 3.5.1 LTS + 现代加密算法

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
- **后端**: 原生播放器 + ExoPlayer 可选

#### iOS (iOS 8-18)
- **架构**: ARM64 (真机 + 模拟器)
- **API**: [MediaPlayer.framework 兼容](ios/IJKMediaPlayer/IJKMediaPlayer/IJKMediaPlayback.h)
- **渲染**: OpenGL ES 2.0/3.0
- **音频**: AudioQueue, AudioUnit
- **加速**: VideoToolbox 硬件解码

## 🏗️ 构建指南

### 📋 构建准备

```bash
# 克隆项目
git clone https://github.com/leo8103lee/ijkplayer.git
cd ijkplayer

# 切换到升级分支
git checkout upgrade-2025

# 配置编解码器 (三种配置可选)
cd config
```

### ⚙️ 编解码器配置

**选择一：完整版本 (推荐)**
```bash
# 包含更多编解码器，支持更多格式
rm -f module.sh
ln -s module-default.sh module.sh
```

**选择二：轻量 + HEVC**
```bash
# 体积较小但支持 HEVC/H.265
rm -f module.sh
ln -s module-lite-hevc.sh module.sh
```

**选择三：最小版本**
```bash
# 最小体积，基础格式支持
rm -f module.sh
ln -s module-lite.sh module.sh
```

### 🤖 Android 构建

```bash
# 1. 初始化 Android 构建环境
./init-android.sh

# 2. 编译 FFmpeg 7.1.2
cd android/contrib
./compile-ffmpeg.sh clean  # 清理之前的构建
./compile-ffmpeg.sh all     # 构建所有架构 (推荐)
# 或单架构构建: ./compile-ffmpeg.sh armv7a

# 3. 编译 IJKPlayer
cd ..
./compile-ijk.sh all        # 构建所有架构
```

#### Android Studio 集成
```bash
# 打开 Android Studio
# File -> Open -> 选择 android/ijkplayer/

# 在项目根目录的 build.gradle 添加:
ext {
    compileSdkVersion = 35         # Android 15
    targetSdkVersion = 35          # 目标API
    minSdkVersion = 9              # 最低API
    buildToolsVersion = "35.0.0"   # 构建工具版本
}
```


### 🍎 iOS 构建 (XCFramework)

```bash
# 1. 初始化 iOS 构建环境
./init-ios.sh

# 2. 编译 FFmpeg 7.1.2 (双架构)
cd ios
./compile-ffmpeg.sh clean
./compile-ffmpeg.sh all     # 同时构建真机和模拟器

# 3. 创建 XCFramework (现代化方案)
./create-xcframeworks.sh    # 自动创建所有 XCFrameworks
```

#### 🎯 XCFramework 优势
- ✅ **ARM64 Mac 完美支持**: 原生支持 Apple Silicon 开发环境
- ✅ **自动平台检测**: Xcode 自动选择正确的库版本
- ✅ **无需手动配置**: 拖拽即用，零配置集成
- ✅ **未来兼容**: 支持所有新 iOS 设备和架构

#### Xcode 项目集成

**方法一：直接使用 Demo**
```bash
# 打开示例项目
open ios/IJKMediaDemo/IJKMediaDemo.xcodeproj
```

**方法二：集成到现有项目**
1. **添加 XCFrameworks**：
   - 将 `ios/IJKMediaPlayer/xcframeworks/` 下所有 `.xcframework` 拖拽到项目中
   - 选择 "Copy items if needed"

2. **添加系统框架**：
   ```
   AudioToolbox.framework
   AVFoundation.framework
   CoreMedia.framework
   CoreVideo.framework
   VideoToolbox.framework
   OpenGLES.framework
   QuartzCore.framework
   ```

3. **完成！** - 无需其他配置，Xcode 会自动处理架构选择


## 🤝 技术支持

### 社区支持
- 🐛 **问题反馈**: [GitHub Issues](https://github.com/leo8103lee/ijkplayer/issues)
- 💬 **技术讨论**: 优先使用 GitHub Discussions
- 📚 **文档**: 查看项目 Wiki 和示例代码

### 升级支持
- ✅ **FFmpeg 7.1.2**: 完整升级指南和兼容性文档
- ✅ **XCFramework 迁移**: 详细的集成步骤说明
- ✅ **构建问题**: 提供完整的构建环境配置

## 📄 开源许可

### 主要许可
```
Copyright (c) 2025 IJKPlayer Community
Licensed under LGPLv2.1 or later
```

### 🔗 依赖项目

#### 媒体处理 (LGPL)
- **[FFmpeg 7.1.2](https://ffmpeg.org/)**: 核心媒体处理
- **[libVLC](http://git.videolan.org/?p=vlc.git)**: 媒体播放支持
- **[SoundTouch](http://www.surina.net/soundtouch/)**: 音频处理

#### 安全加密 (OpenSSL)
- **[OpenSSL 3.5.1 LTS](https://www.openssl.org/)**: 加密和网络安全

#### 系统集成 (各种开源许可)
- **[SDL](http://www.libsdl.org)**: 跨平台媒体层
- **[libyuv](https://chromium.googlesource.com/libyuv/libyuv/)**: 视频处理

#### Android 特定 (Apache 2.0)
- **[ExoPlayer](https://github.com/google/ExoPlayer)**: 可选播放后端

### ⚖️ 商业使用
IJKPlayer 基于 LGPLv2.1+ 许可，可用于商业项目。但请注意：

1. **遵循 LGPL 要求**: 如修改 IJKPlayer 源码，需开源修改部分
2. **依赖项许可**: 各依赖项有不同许可协议，请仔细审查
3. **法律咨询**: 商业使用前建议咨询专业法律意见

---

## 🎉 结语

**IJKPlayer FFmpeg 7.1.2** 现代化版本为您带来：
- 🚀 **最新技术栈**: FFmpeg 7.1.2 + OpenSSL 3.5.1 LTS
- 💪 **完整兼容**: 100% 向后兼容，无缝升级
- 🏗️ **现代架构**: XCFramework + ARM64 Mac 完美支持
- 🔒 **安全加固**: 现代加密标准和安全实践

立即开始您的现代化视频播放体验！

**⭐ 如果这个项目对您有帮助，请给个星标支持！**
