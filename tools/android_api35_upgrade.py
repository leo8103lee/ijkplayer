#!/usr/bin/env python3
"""
Android API Level 35 (Android 15) Upgrade Tool for IJKPlayer
Updates build configurations, dependencies, and API usage for Android 15 compatibility
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

class AndroidAPI35Upgrader:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.android_dir = self.project_root / "android"
        
        # Android 15 / API Level 35 configurations
        self.new_config = {
            'compileSdkVersion': '35',
            'targetSdkVersion': '35',
            'buildToolsVersion': '"35.0.0"',
            'gradle_version': '8.7',
            'gradle_plugin': '8.7.0',
            'kotlin_version': '2.0.21',
            'min_gradle_version': '8.0'
        }
        
        # Dependency updates for Android 15 compatibility
        self.dependency_updates = {
            'androidx.appcompat:appcompat': '1.7.0',
            'androidx.preference:preference': '1.2.1',
            'androidx.annotation:annotation': '1.8.2',
            'com.google.android.material:material': '1.12.0'
        }
        
    def analyze_current_config(self) -> Dict[str, any]:
        """Analyze current Android configuration"""
        print("🔍 Analyzing current Android configuration...")
        
        config = {}
        build_gradle = self.android_dir / "ijkplayer" / "build.gradle"
        
        if build_gradle.exists():
            content = build_gradle.read_text()
            
            # Extract current values
            patterns = {
                'compileSdkVersion': r'compileSdkVersion = (\d+)',
                'targetSdkVersion': r'targetSdkVersion = (\d+)',
                'buildToolsVersion': r'buildToolsVersion = "([^"]+)"',
                'gradle_plugin': r'com\.android\.tools\.build:gradle:([^\']+)',
                'gradle_version': r'gradleVersion = \'([^\']+)\''
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, content)
                config[key] = match.group(1) if match else 'not_found'
                
        return config
        
    def update_root_build_gradle(self) -> bool:
        """Update root build.gradle with API 35 configurations"""
        print("📝 Updating root build.gradle for API Level 35...")
        
        build_gradle = self.android_dir / "ijkplayer" / "build.gradle"
        if not build_gradle.exists():
            print(f"❌ File not found: {build_gradle}")
            return False
            
        content = build_gradle.read_text()
        original_content = content
        
        # Update Android Gradle Plugin
        content = re.sub(
            r"classpath 'com\.android\.tools\.build:gradle:[^']+'",
            f"classpath 'com.android.tools.build:gradle:{self.new_config['gradle_plugin']}'",
            content
        )
        
        # Update SDK versions
        content = re.sub(
            r'compileSdkVersion = \d+',
            f'compileSdkVersion = {self.new_config["compileSdkVersion"]}',
            content
        )
        
        content = re.sub(
            r'targetSdkVersion = \d+',
            f'targetSdkVersion = {self.new_config["targetSdkVersion"]}',
            content
        )
        
        content = re.sub(
            r'buildToolsVersion = "[^"]+"',
            f'buildToolsVersion = {self.new_config["buildToolsVersion"]}',
            content
        )
        
        # Update Gradle wrapper version
        content = re.sub(
            r"gradleVersion = '[^']+'",
            f"gradleVersion = '{self.new_config['gradle_version']}'",
            content
        )
        
        # Add repository updates for newer dependencies
        if 'google()' not in content:
            content = content.replace('jcenter()', 'google()\n        mavenCentral()\n        jcenter()')
        
        if content != original_content:
            build_gradle.write_text(content)
            print("✅ Updated root build.gradle")
            return True
        else:
            print("ℹ️ No changes needed in root build.gradle")
            return False
            
    def update_module_build_files(self) -> List[str]:
        """Update individual module build.gradle files"""
        print("📝 Updating module build.gradle files...")
        
        updated_files = []
        gradle_files = list(self.android_dir.glob("**/build.gradle"))
        
        for gradle_file in gradle_files:
            if 'ijkplayer' in str(gradle_file):
                content = gradle_file.read_text()
                original_content = content
                
                # Update compile to implementation for Android Gradle Plugin 3.0+
                content = re.sub(r'\bcompile\b(?=\s)', 'implementation', content)
                
                # Update support library dependencies to AndroidX
                for old_dep, new_dep in self.dependency_updates.items():
                    if 'com.android.support:appcompat-v7' in content:
                        content = content.replace(
                            'com.android.support:appcompat-v7:23.0.1',
                            f'{new_dep}'
                        )
                    if 'com.android.support:preference-v7' in content:
                        content = content.replace(
                            'com.android.support:preference-v7:23.0.1',
                            'androidx.preference:preference:1.2.1'
                        )
                    if 'com.android.support:support-annotations' in content:
                        content = content.replace(
                            'com.android.support:support-annotations:23.0.1',
                            'androidx.annotation:annotation:1.8.2'
                        )
                
                # Add namespace for Android Gradle Plugin 8.0+
                if 'namespace' not in content and 'android {' in content:
                    app_id_match = re.search(r'applicationId "([^"]+)"', content)
                    if app_id_match:
                        app_id = app_id_match.group(1)
                        content = re.sub(
                            r'(android\s*{[^}]*defaultConfig\s*{)',
                            f'android {{\n    namespace "{app_id}"\n\n    defaultConfig {{',
                            content,
                            flags=re.DOTALL
                        )
                
                if content != original_content:
                    gradle_file.write_text(content)
                    updated_files.append(str(gradle_file.relative_to(self.project_root)))
                    
        return updated_files
        
    def create_gradle_wrapper_update(self) -> bool:
        """Update Gradle wrapper for compatibility"""
        print("📝 Updating Gradle wrapper...")
        
        gradle_wrapper = self.android_dir / "ijkplayer" / "gradle" / "wrapper" / "gradle-wrapper.properties"
        if gradle_wrapper.exists():
            content = gradle_wrapper.read_text()
            
            # Update Gradle distribution URL
            new_content = re.sub(
                r'distributionUrl=.*',
                f'distributionUrl=https\\://services.gradle.org/distributions/gradle-{self.new_config["gradle_version"]}-all.zip',
                content
            )
            
            if new_content != content:
                gradle_wrapper.write_text(new_content)
                print("✅ Updated Gradle wrapper")
                return True
                
        return False
        
    def create_api35_manifest_permissions(self) -> None:
        """Create manifest permissions guide for API 35"""
        print("📝 Creating API 35 manifest permissions guide...")
        
        permissions_guide = self.android_dir / "API35_MANIFEST_PERMISSIONS.md"
        
        guide_content = """# Android API Level 35 Manifest Permissions Guide

## New Permissions in Android 15

### Media and Audio Permissions
```xml
<!-- For audio recording with background processing -->
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK" 
                 android:minSdkVersion="35" />

<!-- For media projection (screen recording) -->
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_MEDIA_PROJECTION" 
                 android:minSdkVersion="35" />
```

### Network and Internet
```xml
<!-- Still required for network access -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

<!-- For partial wake locks during media playback -->
<uses-permission android:name="android.permission.WAKE_LOCK" />
```

### Storage (Scoped Storage)
```xml
<!-- Legacy external storage (deprecated) -->
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" 
                 android:maxSdkVersion="32" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"
                 android:maxSdkVersion="32" />

<!-- Modern storage access -->
<uses-permission android:name="android.permission.READ_MEDIA_VIDEO" />
<uses-permission android:name="android.permission.READ_MEDIA_AUDIO" />
```

## Application Configuration

### Target SDK and Compatibility
```xml
<uses-sdk
    android:minSdkVersion="21"
    android:targetSdkVersion="35" />
```

### Application Theme and Hardware Features
```xml
<application
    android:theme="@style/AppTheme"
    android:hardwareAccelerated="true"
    android:largeHeap="true">
    
    <!-- Declare media capabilities -->
    <meta-data android:name="android.media.decode-support" 
               android:value="true" />
</application>
```

## Behavioral Changes in Android 15

1. **Stricter Background Activity Restrictions**
2. **Enhanced Privacy Controls for Media Access**  
3. **Updated MediaCodec and Hardware Acceleration APIs**
4. **New Audio Focus and Routing Requirements**
5. **Scoped Storage Enforcement**

## Testing Recommendations

1. Test on API 35 emulator with latest system images
2. Verify media playback with different content types
3. Test background playback scenarios
4. Validate hardware acceleration functionality
5. Test with scoped storage restrictions
"""

        permissions_guide.write_text(guide_content)
        print("✅ Created API 35 permissions guide")
        
    def create_proguard_updates(self) -> None:
        """Create updated ProGuard rules for API 35"""
        print("📝 Creating updated ProGuard rules...")
        
        proguard_file = self.android_dir / "ijkplayer" / "ijkplayer-java" / "proguard-rules-api35.pro"
        
        proguard_rules = """# IJKPlayer ProGuard Rules for Android API 35

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
"""

        proguard_file.write_text(proguard_rules)
        print("✅ Created updated ProGuard rules")
        
    def generate_migration_report(self, updated_files: List[str]) -> str:
        """Generate migration report"""
        report_content = f"""# Android API Level 35 Migration Report

## Summary
- **Target SDK**: Android 15 (API Level 35)
- **Gradle Plugin**: {self.new_config['gradle_plugin']}  
- **Gradle Version**: {self.new_config['gradle_version']}
- **Build Tools**: {self.new_config['buildToolsVersion']}

## Files Updated
"""
        for file_path in updated_files:
            report_content += f"- {file_path}\n"
            
        report_content += """
## Key Changes Made

### 1. Build System Updates
- Updated Android Gradle Plugin to 8.7.0 (compatible with API 35)
- Updated Gradle wrapper to 8.7
- Added Google and Maven Central repositories
- Updated build tools to 35.0.0

### 2. Dependency Modernization  
- Migrated from compile to implementation
- Updated support libraries to AndroidX equivalents
- Added namespace declarations for modules

### 3. Permissions and Manifest
- Created API 35 permissions guide
- Documented background service restrictions
- Added scoped storage compatibility notes

### 4. ProGuard Updates
- Created API 35 specific ProGuard rules
- Added AndroidX and modern media API keep rules
- Enhanced hardware acceleration compatibility

## Testing Required

1. **Build Verification**
   ```bash
   cd android/ijkplayer
   ./gradlew clean build
   ```

2. **API Compatibility Testing**
   - Test on Android 15 emulator
   - Verify media playback functionality
   - Test hardware acceleration
   - Validate background playback

3. **Permission Testing**
   - Test runtime permission requests
   - Verify scoped storage access
   - Test foreground service functionality

## Potential Issues to Monitor

1. **Background Activity Restrictions**: Android 15 has stricter rules
2. **Scoped Storage**: May affect file access patterns
3. **Hardware Acceleration**: MediaCodec API changes
4. **Audio Focus**: New audio routing requirements

## Next Steps

1. Run gradle build to verify configuration
2. Test on Android 15 device/emulator  
3. Update CI/CD pipelines for API 35
4. Consider gradual rollout strategy
"""

        report_file = self.android_dir / "API35_MIGRATION_REPORT.md"
        report_file.write_text(report_content)
        
        return report_content
        
def main():
    project_root = "/Users/leo/Code/ijkplayer"
    upgrader = AndroidAPI35Upgrader(project_root)
    
    print("🚀 Starting Android API Level 35 upgrade...")
    
    # Analyze current configuration
    current_config = upgrader.analyze_current_config()
    print(f"📊 Current configuration: {current_config}")
    
    # Perform upgrades
    updated_files = []
    
    # Update root build.gradle
    if upgrader.update_root_build_gradle():
        updated_files.append("android/ijkplayer/build.gradle")
    
    # Update module build files
    module_updates = upgrader.update_module_build_files()
    updated_files.extend(module_updates)
    
    # Update Gradle wrapper
    if upgrader.create_gradle_wrapper_update():
        updated_files.append("android/ijkplayer/gradle/wrapper/gradle-wrapper.properties")
    
    # Create supporting files
    upgrader.create_api35_manifest_permissions()
    upgrader.create_proguard_updates()
    
    # Generate report
    report = upgrader.generate_migration_report(updated_files)
    
    print("\n✅ Android API Level 35 upgrade completed!")
    print(f"📄 Files updated: {len(updated_files)}")
    print("📋 Migration report created: android/API35_MIGRATION_REPORT.md")
    
    if updated_files:
        print("\n📝 Updated files:")
        for file in updated_files:
            print(f"  - {file}")
    
    return len(updated_files)

if __name__ == "__main__":
    main()