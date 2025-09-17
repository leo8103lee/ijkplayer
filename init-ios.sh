#! /usr/bin/env bash
#
# Copyright (C) 2013-2015 Bilibili
# Copyright (C) 2013-2015 Zhang Rui <bbcallen@gmail.com>
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

set -e

# IJK_FFMPEG_UPSTREAM=https://git.ffmpeg.org/ffmpeg.git
IJK_FFMPEG_FORK=https://git.ffmpeg.org/ffmpeg.git
IJK_FFMPEG_COMMIT=n7.1.2
IJK_FFMPEG_LOCAL_REPO=extra/ffmpeg

# iOS architectures for FFmpeg compilation
FF_ALL_ARCHS_IOS="armv7 arm64 i386 x86_64"

echo "========================================"
echo "   Initializing iOS FFmpeg Environment"
echo "========================================"
echo "FFmpeg Fork: $IJK_FFMPEG_FORK"
echo "FFmpeg Commit: $IJK_FFMPEG_COMMIT"
echo "Target Architectures: $FF_ALL_ARCHS_IOS"
echo ""

# Function to setup FFmpeg source for each architecture
setup_ffmpeg_source() {
    ARCH=$1
    FF_SOURCE="ios/ffmpeg-$ARCH"

    echo "--------------------"
    echo "[*] setup FFmpeg source for $ARCH"
    echo "--------------------"

    if [ -d "$FF_SOURCE" ]; then
        echo "FFmpeg source already exists for $ARCH, cleaning..."
        rm -rf "$FF_SOURCE"
    fi

    # Clone FFmpeg source
    echo "Cloning FFmpeg source to $FF_SOURCE..."
    git clone "$IJK_FFMPEG_FORK" "$FF_SOURCE"

    # Checkout specific version
    cd "$FF_SOURCE"
    echo "Checking out FFmpeg $IJK_FFMPEG_COMMIT..."
    git checkout "$IJK_FFMPEG_COMMIT" -B ijkplayer

    # Apply any necessary patches
    echo "FFmpeg source ready for $ARCH"
    cd ../..
}

# Main execution
echo "Starting FFmpeg source setup for iOS..."

# Create iOS directory if not exists
mkdir -p ios

# Setup FFmpeg source for each architecture
for ARCH in $FF_ALL_ARCHS_IOS; do
    setup_ffmpeg_source $ARCH
done

# Initialize OpenSSL (use our upgraded version)
if [ -f "init-ios-openssl.sh" ]; then
    echo ""
    echo "========================================"
    echo "   Initializing OpenSSL 3.5.1"
    echo "========================================"
    ./init-ios-openssl.sh
fi

echo ""
echo "========================================"
echo "   iOS Environment Setup Complete"
echo "========================================"
echo "Next steps:"
echo "1. Configure FFmpeg modules in config/"
echo "2. Run: cd ios && ./compile-ffmpeg.sh all"
echo "3. Build IJKMediaPlayer framework"
echo ""