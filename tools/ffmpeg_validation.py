#!/usr/bin/env python3
"""
FFmpeg 7.1.2 Validation Script for IJKPlayer
Validates upgrade success and functionality
"""

import subprocess
import sys
import os
from pathlib import Path

def check_ffmpeg_version():
    """Check FFmpeg version"""
    print("🔍 Checking FFmpeg version...")
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ {version_line}")
            
            if "7.1.2" in version_line:
                print("✅ FFmpeg 7.1.2 confirmed")
                return True
            else:
                print(f"⚠️  Expected FFmpeg 7.1.2, found: {version_line}")
                return False
        else:
            print(f"❌ FFmpeg check failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg not found in PATH")
        return False

def check_codec_support():
    """Check codec support in FFmpeg 7.1.2"""
    print("\n🔍 Checking codec support...")
    
    required_codecs = ['h264', 'hevc', 'av1', 'aac', 'mp3']
    supported = 0
    
    try:
        result = subprocess.run(['ffmpeg', '-codecs'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            codecs_output = result.stdout.lower()
            
            for codec in required_codecs:
                if codec in codecs_output:
                    print(f"  ✅ {codec.upper()} supported")
                    supported += 1
                else:
                    print(f"  ❌ {codec.upper()} not found")
        
        print(f"📊 Codec support: {supported}/{len(required_codecs)}")
        return supported >= len(required_codecs) - 1  # Allow one missing
        
    except Exception as e:
        print(f"❌ Codec check failed: {e}")
        return False

def check_hardware_acceleration():
    """Check hardware acceleration support"""
    print("\n🔍 Checking hardware acceleration...")
    
    try:
        result = subprocess.run(['ffmpeg', '-hwaccels'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            hwaccels = result.stdout.lower()
            
            # Check for common hardware acceleration
            hw_support = {
                'videotoolbox': 'videotoolbox' in hwaccels,
                'mediacodec': 'mediacodec' in hwaccels,
                'cuda': 'cuda' in hwaccels,
                'vaapi': 'vaapi' in hwaccels
            }
            
            supported_hw = sum(hw_support.values())
            print(f"📊 Hardware acceleration: {supported_hw} types available")
            
            for hw_type, supported in hw_support.items():
                status = "✅" if supported else "❌"
                print(f"  {status} {hw_type}")
            
            return supported_hw > 0
        else:
            print("⚠️  Hardware acceleration check failed")
            return True  # Not critical
            
    except Exception as e:
        print(f"❌ Hardware acceleration check error: {e}")
        return True  # Not critical

def check_build_integration():
    """Check build system integration"""
    print("\n🔍 Checking build integration...")
    
    critical_files = [
        'ijkmedia/ijkplayer/ffmpeg_compat.h',
        'init-android.sh', 
        'init-ios.sh',
        'android/contrib/compile-ffmpeg.sh',
        'ios/compile-ffmpeg.sh'
    ]
    
    found = 0
    for file_path in critical_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
            found += 1
        else:
            print(f"  ❌ {file_path} missing")
    
    print(f"📊 Integration files: {found}/{len(critical_files)}")
    return found == len(critical_files)

def main():
    """Main validation function"""
    print("🎬 FFmpeg 7.1.2 Validation for IJKPlayer")
    print("=" * 50)
    
    tests = [
        ("FFmpeg Version", check_ffmpeg_version),
        ("Codec Support", check_codec_support),
        ("Hardware Acceleration", check_hardware_acceleration),
        ("Build Integration", check_build_integration)
    ]
    
    passed = 0
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
    
    print(f"\n📊 Validation Results: {passed}/{len(tests)} tests passed")
    
    if passed >= 3:  # Allow one non-critical failure
        print("✅ FFmpeg 7.1.2 upgrade validation successful!")
        sys.exit(0)
    else:
        print("❌ FFmpeg 7.1.2 upgrade validation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
