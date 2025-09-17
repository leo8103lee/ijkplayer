#! /usr/bin/env bash
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

# This script is modified to download and extract official OpenSSL source tarball
# instead of cloning from a git repository.

set -e

OPENSSL_VERSION="3.5.1"
OPENSSL_TARBALL="openssl-${OPENSSL_VERSION}.tar.gz"
OPENSSL_URL="https://www.openssl.org/source/${OPENSSL_TARBALL}"
OPENSSL_DIR="openssl-${OPENSSL_VERSION}"
CONTRIB_DIR="ios"
TARGET_DIR_PREFIX="openssl"

# ---

echo "==> Downloading OpenSSL ${OPENSSL_VERSION}"

if [ ! -f "${OPENSSL_TARBALL}" ]; then
    curl -L -O "${OPENSSL_URL}"
fi

# ---
# Unarchive and create separate source folders for each architecture.
# This is to avoid build conflicts when compiling for different targets.

function unarchive_for_arch()
{
    local ARCH=$1
    local TARGET_DIR="${CONTRIB_DIR}/${TARGET_DIR_PREFIX}-${ARCH}"

    echo "==> Unarchiving for ${ARCH} into ${TARGET_DIR}"

    rm -rf "${TARGET_DIR}"
    mkdir -p "${TARGET_DIR}"
    tar -xzf "${OPENSSL_TARBALL}" -C "${TARGET_DIR}" --strip-components=1
}

unarchive_for_arch "arm64"
unarchive_for_arch "x86_64"

echo "==> OpenSSL source prepared successfully"

