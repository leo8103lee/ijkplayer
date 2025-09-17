#!/bin/bash

# Script to update IJKMediaPlayer project to use XCFrameworks instead of static libraries

set -e

PROJECT_PATH="/Users/leo/Code/ijkplayer/ios/IJKMediaPlayer/IJKMediaPlayer.xcodeproj/project.pbxproj"
XCFRAMEWORKS_PATH="/Users/leo/Code/ijkplayer/ios/build/xcframeworks"

echo "Updating IJKMediaPlayer project to use XCFrameworks..."

# Make a backup of the original project file
cp "$PROJECT_PATH" "$PROJECT_PATH.backup"

# Define the libraries to replace
LIBS=(
    "libavcodec"
    "libavfilter"
    "libavformat"
    "libavutil"
    "libswresample"
    "libswscale"
)

# Copy XCFrameworks to the IJKMediaPlayer directory
echo "Copying XCFrameworks to IJKMediaPlayer directory..."
cp -r "$XCFRAMEWORKS_PATH" "/Users/leo/Code/ijkplayer/ios/IJKMediaPlayer/"

# For each library, we need to:
# 1. Update PBXFileReference entries to point to .xcframework instead of .a
# 2. Update the file type from archive.ar to wrapper.xcframework
# 3. Update the path references

for lib in "${LIBS[@]}"; do
    echo "Updating references for $lib..."

    # Update the PBXFileReference entries
    sed -i "" "s|${lib}\.a.*lastKnownFileType = archive\.ar; path = ${lib}\.a|${lib}.xcframework \/\* ${lib}.xcframework \*\/ = {isa = PBXFileReference; lastKnownFileType = wrapper.xcframework; path = xcframeworks\/${lib}.xcframework|g" "$PROJECT_PATH"

    # Also handle any remaining .a references for this lib
    sed -i "" "s|${lib}\.a|${lib}.xcframework|g" "$PROJECT_PATH"
done

echo "Project file updated successfully!"
echo "Backup saved as: $PROJECT_PATH.backup"