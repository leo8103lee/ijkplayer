#!/bin/bash
set -e

echo "=== Creating XCFrameworks for IJKPlayer FFmpeg 7.1.2 ==="

DEVICE_LIB_PATH="/Users/leo/Code/ijkplayer/ios/build/ffmpeg-arm64/output/lib"
SIMULATOR_LIB_PATH="/Users/leo/Code/ijkplayer/ios/build/ffmpeg-arm64-sim/output/lib" 
XCFRAMEWORK_OUTPUT="/Users/leo/Code/ijkplayer/ios/build/xcframeworks"

# FFmpeg libraries to process
FFMPEG_LIBS="libavcodec libavformat libavutil libswscale libswresample libavfilter"

for lib in $FFMPEG_LIBS; do
    echo ""
    echo "Creating XCFramework for $lib..."
    
    # Remove existing XCFramework if it exists
    rm -rf "$XCFRAMEWORK_OUTPUT/$lib.xcframework"
    
    # Create XCFramework
    xcodebuild -create-xcframework \
        -library "$DEVICE_LIB_PATH/$lib.a" \
        -library "$SIMULATOR_LIB_PATH/$lib.a" \
        -output "$XCFRAMEWORK_OUTPUT/$lib.xcframework"
    
    echo "✅ Created $lib.xcframework"
done

echo ""
echo "🎉 All XCFrameworks created successfully!"
echo "📁 Location: $XCFRAMEWORK_OUTPUT"

# List created XCFrameworks
echo ""
echo "📦 Created XCFrameworks:"
ls -la "$XCFRAMEWORK_OUTPUT"

echo ""
echo "🔍 Verify architectures in libavcodec.xcframework:"
xcodebuild -showBuildSettings -xcframework "$XCFRAMEWORK_OUTPUT/libavcodec.xcframework"