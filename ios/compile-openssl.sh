#!/usr/bin/env bash
#
# Copyright (C) 2013-2025 Bilibili
# Copyright (C) 2013-2025 Zhang Rui <bbcallen@gmail.com>
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

# This script is completely rewritten to support modern Xcode and OpenSSL 3.x

set -e

# --- Environment --- 

UNI_BUILD_ROOT=$(pwd)
UNI_TMP="${UNI_BUILD_ROOT}/tmp"
mkdir -p "${UNI_TMP}"

# --- Architectures --- 

# Set target architectures
# Note: arm64-simulator is required for modern Xcode on Apple Silicon Macs
ARCHS_DEVICE="arm64"
ARCHS_SIMULATOR="x86_64 arm64"
FF_ALL_ARCHS="${ARCHS_DEVICE} ${ARCHS_SIMULATOR}"

# --- OpenSSL Libraries --- 

FF_LIBS="libssl.a libcrypto.a"

# --- Functions --- 

# Get the absolute path of the SDK
get_sdk_path() {
    local sdk_name=$1
    xcrun --sdk "${sdk_name}" --show-sdk-path
}

# Get the minimum iOS version for a given target
get_min_os_version() {
    local sdk_name=$1
    xcrun --sdk "${sdk_name}" --show-sdk-platform-version
}

do_compile_for_arch() {
    local ARCH=$1
    local SRC_DIR="${UNI_BUILD_ROOT}/openssl-${ARCH}"
    local BUILD_DIR="${UNI_BUILD_ROOT}/build/openssl-${ARCH}"
    local OUTPUT_DIR="${BUILD_DIR}/output"

    if [ ! -d "${SRC_DIR}" ]; then
        echo "Source directory ${SRC_DIR} not found. Run init-ios-openssl.sh first." >&2
        exit 1
    fi

    echo "==> Compiling OpenSSL for ${ARCH}"

    mkdir -p "${BUILD_DIR}"
    cd "${SRC_DIR}"

    # --- Configure Environment --- 
    local CFLAGS
    local CONFIGURE_TARGET

    if [[ "${ARCHS_DEVICE}" =~ ${ARCH} ]]; then
        local SDK_NAME="iphoneos"
        CONFIGURE_TARGET="ios64-cross"
    elif [[ "${ARCHS_SIMULATOR}" =~ ${ARCH} ]]; then
        local SDK_NAME="iphonesimulator"
        if [ "${ARCH}" = "x86_64" ]; then
            CONFIGURE_TARGET="iossimulator-xcrun"
        else # arm64 simulator
            CONFIGURE_TARGET="iossimulator-xcrun"
        fi
    else
        echo "Unsupported architecture: ${ARCH}" >&2
        exit 1
    fi

    export SDK_PATH=$(get_sdk_path "${SDK_NAME}")
    export MIN_OS_VERSION=$(get_min_os_version "${SDK_NAME}")
    export CC=$(xcrun -f clang)
    export CXX=$(xcrun -f clang++)

    export CFLAGS="-arch ${ARCH} -isysroot ${SDK_PATH} -mios-version-min=${MIN_OS_VERSION} -fembed-bitcode"

    # --- Configure and Build --- 
    # no-asm is a safe bet for cross-compiling
    ./Configure ${CONFIGURE_TARGET} no-shared no-asm --prefix="${OUTPUT_DIR}"

    make -j$(sysctl -n hw.ncpu) clean
    make -j$(sysctl -n hw.ncpu)
    make install_sw

    cd "${UNI_BUILD_ROOT}"
    echo "==> Finished compiling OpenSSL for ${ARCH}"
}

do_lipo_all() {
    local UNIVERSAL_DIR="${UNI_BUILD_ROOT}/build/universal"
    local UNIVERSAL_LIB_DIR="${UNIVERSAL_DIR}/lib"
    local UNIVERSAL_INCLUDE_DIR="${UNIVERSAL_DIR}/include"

    echo "==> Creating universal libraries and headers"
    mkdir -p "${UNIVERSAL_LIB_DIR}"

    local LIPO_FLAGS
    for LIB in ${FF_LIBS}; do
        LIPO_FLAGS=""
        for ARCH in ${FF_ALL_ARCHS}; do
            LIPO_FLAGS+=" ${UNI_BUILD_ROOT}/build/openssl-${ARCH}/output/lib/${LIB}"
        done
        xcrun lipo -create ${LIPO_FLAGS} -output "${UNIVERSAL_LIB_DIR}/${LIB}"
        xcrun lipo -info "${UNIVERSAL_LIB_DIR}/${LIB}"
    done

    # Copy headers from one of the builds (they are the same)
    local ANY_ARCH=$(echo "${FF_ALL_ARCHS}" | awk '{print $1}')
    rm -rf "${UNIVERSAL_INCLUDE_DIR}"
    cp -R "${UNI_BUILD_ROOT}/build/openssl-${ANY_ARCH}/output/include" "${UNIVERSAL_INCLUDE_DIR}"

    echo "==> Universal OpenSSL build finished successfully"
}

# --- Main Logic --- 

FF_TARGET=$1

if [ "$FF_TARGET" = "clean" ]; then
    rm -rf "${UNI_BUILD_ROOT}/build"
    rm -rf "${UNI_TMP}"
    echo "Cleaned build directories."
    exit 0
fi

if [ "$FF_TARGET" = "all" ] || [ -z "$FF_TARGET" ]; then
    for ARCH in ${FF_ALL_ARCHS}; do
        do_compile_for_arch "${ARCH}"
    done
    do_lipo_all
else
    if [[ " ${FF_ALL_ARCHS} " =~ " ${FF_TARGET} " ]]; then
        do_compile_for_arch "${FF_TARGET}"
    else
        echo "Usage: $0 [ all | clean | ${FF_ALL_ARCHS// / |} ]"
        exit 1
    fi
fi
