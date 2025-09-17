#! /usr/bin/env bash
#
# Copyright (C) 2014 Miguel Botón <waninkoko@gmail.com>
# Copyright (C) 2014 Zhang Rui <bbcallen@gmail.com>
# Updated for OpenSSL 3.5.1 and NDK r27 (2025)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#--------------------
set -e

if [ -z "$ANDROID_NDK" ]; then
    echo "You must define ANDROID_NDK before starting."
    echo "They must point to your NDK directories."
    exit 1
fi

#--------------------
# Common defines for OpenSSL 3.5.1
FF_ARCH=$1
if [ -z "$FF_ARCH" ]; then
    echo "You must specify an architecture 'armv7a, arm64, x86, x86_64'."
    exit 1
fi

FF_BUILD_ROOT=$(pwd)

# Updated platform versions for modern Android support
FF_ANDROID_PLATFORM=android-21  # Minimum for 64-bit architectures
FF_ANDROID_PLATFORM_32=android-16  # Minimum for 32-bit architectures

FF_BUILD_NAME=
FF_SOURCE=
FF_CROSS_PREFIX=
FF_CONFIGURE_TARGET=

FF_OPENSSL_CONFIG_FLAGS=
FF_EXTRA_CFLAGS=
FF_EXTRA_LDFLAGS=

#--------------------
echo ""
echo "--------------------"
echo "[*] Configuring OpenSSL 3.5.1 for $FF_ARCH"
echo "--------------------"

# Modern NDK r27 toolchain configuration
if [ "$FF_ARCH" = "armv7a" ]; then
    FF_BUILD_NAME=openssl-armv7a
    FF_SOURCE=$FF_BUILD_ROOT/$FF_BUILD_NAME
    FF_ANDROID_PLATFORM=$FF_ANDROID_PLATFORM_32
    
    FF_CROSS_PREFIX=armv7a-linux-androideabi
    FF_CONFIGURE_TARGET="android-arm"
    FF_EXTRA_CFLAGS="-march=armv7-a -mfloat-abi=softfp -mfpu=neon"

elif [ "$FF_ARCH" = "armv5" ]; then
    echo "Warning: armv5 is deprecated. Use armv7a instead."
    FF_BUILD_NAME=openssl-armv5
    FF_SOURCE=$FF_BUILD_ROOT/$FF_BUILD_NAME
    FF_ANDROID_PLATFORM=$FF_ANDROID_PLATFORM_32
    
    FF_CROSS_PREFIX=arm-linux-androideabi
    FF_CONFIGURE_TARGET="android-arm"

elif [ "$FF_ARCH" = "x86" ]; then
    FF_BUILD_NAME=openssl-x86
    FF_SOURCE=$FF_BUILD_ROOT/$FF_BUILD_NAME
    FF_ANDROID_PLATFORM=$FF_ANDROID_PLATFORM_32
    
    FF_CROSS_PREFIX=i686-linux-android
    FF_CONFIGURE_TARGET="android-x86"

elif [ "$FF_ARCH" = "x86_64" ]; then
    FF_BUILD_NAME=openssl-x86_64
    FF_SOURCE=$FF_BUILD_ROOT/$FF_BUILD_NAME
    
    FF_CROSS_PREFIX=x86_64-linux-android
    FF_CONFIGURE_TARGET="android-x86_64"

elif [ "$FF_ARCH" = "arm64" ]; then
    FF_BUILD_NAME=openssl-arm64
    FF_SOURCE=$FF_BUILD_ROOT/$FF_BUILD_NAME
    
    FF_CROSS_PREFIX=aarch64-linux-android
    FF_CONFIGURE_TARGET="android-arm64"

else
    echo "Unknown architecture: $FF_ARCH"
    echo "Supported: armv7a, arm64, x86, x86_64"
    exit 1
fi

FF_PREFIX=$FF_BUILD_ROOT/build/$FF_BUILD_NAME/output
mkdir -p "$FF_PREFIX"

#--------------------
echo ""
echo "--------------------"
echo "[*] Setup modern NDK r27 toolchain"
echo "--------------------"

# NDK r27 uses direct toolchain binaries, no more make-standalone-toolchain
export NDK_TOOLCHAIN_PATH="$ANDROID_NDK/toolchains/llvm/prebuilt/darwin-x86_64"
export PATH="$NDK_TOOLCHAIN_PATH/bin:$PATH"

# Set API level in cross-compiler name
API_LEVEL=$(echo $FF_ANDROID_PLATFORM | sed 's/android-//')
export CC="${FF_CROSS_PREFIX}${API_LEVEL}-clang"
export CXX="${FF_CROSS_PREFIX}${API_LEVEL}-clang++"
export AR="llvm-ar"
export RANLIB="llvm-ranlib"
export STRIP="llvm-strip"

# Verify toolchain
echo "Checking toolchain:"
echo "CC: $(which $CC)"
echo "API Level: $API_LEVEL"

#--------------------
echo ""
echo "--------------------"
echo "[*] Configure OpenSSL 3.5.1"
echo "--------------------"

cd "$FF_SOURCE"

# OpenSSL 3.5.1 configuration flags for security and performance
FF_OPENSSL_CONFIG_FLAGS="
    --prefix=$FF_PREFIX
    --openssldir=$FF_PREFIX/ssl
    no-shared
    no-tests
    no-apps
    no-docs
    -D__ANDROID_API__=$API_LEVEL
"

# Add architecture-specific flags
if [ -n "$FF_EXTRA_CFLAGS" ]; then
    FF_OPENSSL_CONFIG_FLAGS="$FF_OPENSSL_CONFIG_FLAGS $FF_EXTRA_CFLAGS"
fi

# Security-focused configuration for OpenSSL 3.5.1
FF_OPENSSL_CONFIG_FLAGS="$FF_OPENSSL_CONFIG_FLAGS enable-tls1_3"
FF_OPENSSL_CONFIG_FLAGS="$FF_OPENSSL_CONFIG_FLAGS no-ssl3"
FF_OPENSSL_CONFIG_FLAGS="$FF_OPENSSL_CONFIG_FLAGS no-weak-ssl-ciphers"
FF_OPENSSL_CONFIG_FLAGS="$FF_OPENSSL_CONFIG_FLAGS no-comp"

echo "Configure command:"
echo "./Configure $FF_CONFIGURE_TARGET $FF_OPENSSL_CONFIG_FLAGS"

./Configure $FF_CONFIGURE_TARGET $FF_OPENSSL_CONFIG_FLAGS

#--------------------
echo ""
echo "--------------------"
echo "[*] Build OpenSSL 3.5.1"
echo "--------------------"

# Use parallel build for faster compilation
NPROC=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
echo "Building with $NPROC parallel jobs"

make clean
make -j$NPROC
make install_sw

#--------------------
echo ""
echo "--------------------"
echo "[*] Verify OpenSSL build"
echo "--------------------"

if [ -f "$FF_PREFIX/lib/libssl.a" ] && [ -f "$FF_PREFIX/lib/libcrypto.a" ]; then
    echo "✅ OpenSSL 3.5.1 build successful for $FF_ARCH"
    echo "Libraries:"
    ls -la "$FF_PREFIX/lib/"*.a
    echo "Headers:"
    ls -la "$FF_PREFIX/include/openssl/" | head -5
    echo "..."
else
    echo "❌ OpenSSL build failed for $FF_ARCH"
    exit 1
fi

echo ""
echo "--------------------"
echo "[*] OpenSSL 3.5.1 build complete for $FF_ARCH"
echo "--------------------"
echo "Output: $FF_PREFIX"