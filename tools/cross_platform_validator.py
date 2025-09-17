#!/usr/bin/env python3
"""
Cross-Platform Functionality Validator for IJKPlayer
Validates Android and iOS compatibility after platform upgrades
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class CrossPlatformValidator:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.android_dir = self.project_root / "android"
        self.ios_dir = self.project_root / "ios"
        
        self.validation_results = {
            'android': {'passed': 0, 'failed': 0, 'warnings': 0, 'tests': []},
            'ios': {'passed': 0, 'failed': 0, 'warnings': 0, 'tests': []},
            'cross_platform': {'passed': 0, 'failed': 0, 'warnings': 0, 'tests': []}
        }
        
    def log_result(self, platform: str, test_name: str, status: str, message: str, details: str = ""):
        """Log validation result"""
        result = {
            'test': test_name,
            'status': status,  # 'pass', 'fail', 'warning'
            'message': message,
            'details': details
        }
        
        self.validation_results[platform]['tests'].append(result)
        
        if status == 'pass':
            self.validation_results[platform]['passed'] += 1
            print(f"✅ {platform.upper()}: {test_name} - {message}")
        elif status == 'fail':
            self.validation_results[platform]['failed'] += 1
            print(f"❌ {platform.upper()}: {test_name} - {message}")
            if details:
                print(f"   Details: {details}")
        else:  # warning
            self.validation_results[platform]['warnings'] += 1
            print(f"⚠️ {platform.upper()}: {test_name} - {message}")
            
    def validate_android_build_system(self) -> None:
        """Validate Android build system after API 35 upgrade"""
        print("\n🤖 Validating Android Build System...")
        
        # Check Gradle wrapper
        gradle_wrapper = self.android_dir / "ijkplayer" / "gradle" / "wrapper" / "gradle-wrapper.properties"
        if gradle_wrapper.exists():
            content = gradle_wrapper.read_text()
            if "gradle-8.7" in content:
                self.log_result('android', 'Gradle Version', 'pass', 
                              'Gradle 8.7 wrapper configured correctly')
            else:
                self.log_result('android', 'Gradle Version', 'fail',
                              'Gradle wrapper not updated to 8.7')
        else:
            self.log_result('android', 'Gradle Wrapper', 'fail', 
                          'Gradle wrapper properties not found')
        
        # Check root build.gradle
        build_gradle = self.android_dir / "ijkplayer" / "build.gradle"
        if build_gradle.exists():
            content = build_gradle.read_text()
            
            # Check API Level 35
            if "compileSdkVersion = 35" in content:
                self.log_result('android', 'Compile SDK', 'pass',
                              'Compile SDK updated to API 35')
            else:
                self.log_result('android', 'Compile SDK', 'fail',
                              'Compile SDK not updated to API 35')
                
            # Check target SDK
            if "targetSdkVersion = 35" in content:
                self.log_result('android', 'Target SDK', 'pass',
                              'Target SDK updated to API 35')
            else:
                self.log_result('android', 'Target SDK', 'fail',
                              'Target SDK not updated to API 35')
                
            # Check AGP version
            if "com.android.tools.build:gradle:8.7.0" in content:
                self.log_result('android', 'Android Gradle Plugin', 'pass',
                              'Android Gradle Plugin updated to 8.7.0')
            else:
                self.log_result('android', 'Android Gradle Plugin', 'warning',
                              'Android Gradle Plugin version may need update')
        else:
            self.log_result('android', 'Build Configuration', 'fail',
                          'Root build.gradle not found')
            
        # Check API 35 permissions guide
        permissions_guide = self.android_dir / "API35_MANIFEST_PERMISSIONS.md"
        if permissions_guide.exists():
            self.log_result('android', 'API 35 Permissions Guide', 'pass',
                          'API 35 permissions documentation created')
        else:
            self.log_result('android', 'API 35 Permissions Guide', 'warning',
                          'API 35 permissions guide not found')
            
    def validate_ios_sdk_integration(self) -> None:
        """Validate iOS 18 SDK integration"""
        print("\n📱 Validating iOS 18 SDK Integration...")
        
        # Check for iOS 18 compatibility header
        compat_header = self.ios_dir / "IJKMediaPlayer" / "IJKMediaFramework" / "ios18_compat.h"
        if compat_header.exists():
            content = compat_header.read_text()
            if "__IPHONE_OS_VERSION_MAX_ALLOWED >= 180000" in content:
                self.log_result('ios', 'iOS 18 Compatibility Header', 'pass',
                              'iOS 18 compatibility header created with proper version checks')
            else:
                self.log_result('ios', 'iOS 18 Compatibility Header', 'warning',
                              'Compatibility header exists but version checks may be incomplete')
        else:
            self.log_result('ios', 'iOS 18 Compatibility Header', 'fail',
                          'iOS 18 compatibility header not found')
            
        # Check SceneDelegate implementation
        scene_delegate_h = self.ios_dir / "IJKMediaDemo" / "IJKMediaDemo" / "SceneDelegate.h"
        scene_delegate_m = self.ios_dir / "IJKMediaDemo" / "IJKMediaDemo" / "SceneDelegate.m"
        
        if scene_delegate_h.exists() and scene_delegate_m.exists():
            self.log_result('ios', 'Scene Delegate', 'pass',
                          'SceneDelegate files created for iOS 18 lifecycle support')
        else:
            self.log_result('ios', 'Scene Delegate', 'warning',
                          'SceneDelegate files not found - may need manual integration')
            
        # Check VideoToolbox iOS 18 integration
        vt_header = self.ios_dir / "IJKMediaPlayer" / "IJKMediaFramework" / "ijkplayer_ios18_videotoolbox.h"
        vt_impl = self.ios_dir / "IJKMediaPlayer" / "IJKMediaFramework" / "ijkplayer_ios18_videotoolbox.m"
        
        if vt_header.exists() and vt_impl.exists():
            self.log_result('ios', 'VideoToolbox iOS 18', 'pass',
                          'iOS 18 VideoToolbox integration files created')
        else:
            self.log_result('ios', 'VideoToolbox iOS 18', 'fail',
                          'iOS 18 VideoToolbox integration files not found')
            
        # Check Info.plist updates
        plist_files = [
            self.ios_dir / "IJKMediaDemo" / "IJKMediaDemo" / "IJKMediaDemo-Info.plist",
            self.ios_dir / "IJKMediaPlayer" / "IJKMediaFramework" / "Info.plist"
        ]
        
        plist_updates = 0
        for plist_file in plist_files:
            if plist_file.exists():
                content = plist_file.read_text()
                # Check for arm64 requirement (armv7 should be removed for iOS 18)
                if "armv7" not in content and "arm64" in content:
                    plist_updates += 1
                    
        if plist_updates > 0:
            self.log_result('ios', 'Info.plist Updates', 'pass',
                          f'{plist_updates} plist files updated for iOS 18 (removed armv7)')
        else:
            self.log_result('ios', 'Info.plist Updates', 'warning',
                          'Info.plist files may need iOS 18 updates')
            
    def validate_dependency_upgrades(self) -> None:
        """Validate that all dependency upgrades are properly integrated"""
        print("\n📦 Validating Dependency Upgrades...")
        
        # Check OpenSSL 3.5.1 upgrade
        openssl_android = self.project_root / "init-android-openssl.sh"
        openssl_ios = self.project_root / "init-ios-openssl.sh"
        
        openssl_version_found = False
        for script in [openssl_android, openssl_ios]:
            if script.exists():
                content = script.read_text()
                if "OPENSSL_VERSION=\"3.5.1\"" in content:
                    openssl_version_found = True
                    break
                    
        if openssl_version_found:
            self.log_result('cross_platform', 'OpenSSL Version', 'pass',
                          'OpenSSL upgraded to 3.5.1 in init scripts')
        else:
            self.log_result('cross_platform', 'OpenSSL Version', 'fail',
                          'OpenSSL version not found or not upgraded to 3.5.1')
            
        # Check FFmpeg 7.1.2 upgrade
        ffmpeg_android = self.project_root / "init-android.sh"
        ffmpeg_ios = self.project_root / "init-ios.sh"
        
        ffmpeg_version_found = False
        for script in [ffmpeg_android, ffmpeg_ios]:
            if script.exists():
                content = script.read_text()
                if "IJK_FFMPEG_COMMIT=n7.1.2" in content:
                    ffmpeg_version_found = True
                    break
                    
        if ffmpeg_version_found:
            self.log_result('cross_platform', 'FFmpeg Version', 'pass',
                          'FFmpeg upgraded to 7.1.2 in init scripts')
        else:
            self.log_result('cross_platform', 'FFmpeg Version', 'fail',
                          'FFmpeg version not found or not upgraded to 7.1.2')
            
        # Check libyuv upgrade
        libyuv_script = self.project_root / "init-android-libyuv.sh"
        if libyuv_script.exists():
            content = libyuv_script.read_text()
            if "IJK_LIBYUV_COMMIT=1904" in content:
                self.log_result('cross_platform', 'libyuv Version', 'pass',
                              'libyuv upgraded to version 1904')
            else:
                self.log_result('cross_platform', 'libyuv Version', 'warning',
                              'libyuv version may not be upgraded to 1904')
        else:
            self.log_result('cross_platform', 'libyuv Script', 'fail',
                          'libyuv init script not found')
            
        # Check SoundTouch upgrade
        soundtouch_script = self.project_root / "init-android-soundtouch.sh"
        if soundtouch_script.exists():
            content = soundtouch_script.read_text()
            if "IJK_SOUNDTOUCH_COMMIT=2.4.0" in content:
                self.log_result('cross_platform', 'SoundTouch Version', 'pass',
                              'SoundTouch upgraded to version 2.4.0')
            else:
                self.log_result('cross_platform', 'SoundTouch Version', 'warning',
                              'SoundTouch version may not be upgraded to 2.4.0')
        else:
            self.log_result('cross_platform', 'SoundTouch Script', 'fail',
                          'SoundTouch init script not found')
            
    def validate_api_compatibility_layers(self) -> None:
        """Validate API compatibility layers"""
        print("\n🔧 Validating API Compatibility Layers...")
        
        # Check FFmpeg compatibility layer
        ffmpeg_compat = self.project_root / "ijkmedia" / "ijkplayer" / "ffmpeg_compat.h"
        if ffmpeg_compat.exists():
            content = ffmpeg_compat.read_text()
            if "IJK_DECODE_VIDEO" in content and "avcodec_send_packet" in content:
                self.log_result('cross_platform', 'FFmpeg Compatibility Layer', 'pass',
                              'FFmpeg 7.1.2 compatibility macros implemented')
            else:
                self.log_result('cross_platform', 'FFmpeg Compatibility Layer', 'warning',
                              'FFmpeg compatibility layer may be incomplete')
        else:
            self.log_result('cross_platform', 'FFmpeg Compatibility Layer', 'fail',
                          'FFmpeg compatibility header not found')
            
        # Check OpenSSL security configuration
        openssl_security_h = self.project_root / "ijkmedia" / "ijkplayer" / "ijkplayer_openssl_security.h"
        openssl_security_c = self.project_root / "ijkmedia" / "ijkplayer" / "ijkplayer_openssl_security.c"
        
        if openssl_security_h.exists() and openssl_security_c.exists():
            self.log_result('cross_platform', 'OpenSSL Security Configuration', 'pass',
                          'OpenSSL 3.5.1 security configuration files created')
        else:
            self.log_result('cross_platform', 'OpenSSL Security Configuration', 'warning',
                          'OpenSSL security configuration files not found')
            
    def validate_build_system_modernization(self) -> None:
        """Validate build system modernization"""
        print("\n🏗️ Validating Build System Modernization...")
        
        # Check build system documentation
        build_modernization_doc = self.project_root / "docs" / "upgrade" / "BUILD_SYSTEM_MODERNIZATION.md"
        if build_modernization_doc.exists():
            content = build_modernization_doc.read_text()
            if "BuildDependencyAnalyzer" in content and "parallel" in content:
                self.log_result('cross_platform', 'Build System Documentation', 'pass',
                              'Build system modernization documentation complete with parallel build support')
            else:
                self.log_result('cross_platform', 'Build System Documentation', 'warning',
                              'Build system documentation may be incomplete')
        else:
            self.log_result('cross_platform', 'Build System Documentation', 'fail',
                          'Build system modernization documentation not found')
            
        # Check for upgrade tools
        upgrade_tools = [
            'tools/android_api35_upgrade.py',
            'tools/ios18_sdk_upgrade.py', 
            'tools/cross_platform_validator.py'
        ]
        
        tools_found = 0
        for tool in upgrade_tools:
            tool_path = self.project_root / tool
            if tool_path.exists():
                tools_found += 1
                
        if tools_found == len(upgrade_tools):
            self.log_result('cross_platform', 'Upgrade Tools', 'pass',
                          f'All {tools_found} upgrade tools created')
        else:
            self.log_result('cross_platform', 'Upgrade Tools', 'warning',
                          f'Only {tools_found}/{len(upgrade_tools)} upgrade tools found')
            
    def validate_cross_platform_consistency(self) -> None:
        """Validate consistency between Android and iOS implementations"""
        print("\n🤝 Validating Cross-Platform Consistency...")
        
        # Check that both platforms have init scripts updated
        android_init_updated = False
        ios_init_updated = False
        
        # Check Android init scripts
        android_scripts = ['init-android.sh', 'init-android-openssl.sh']
        for script_name in android_scripts:
            script_path = self.project_root / script_name
            if script_path.exists():
                content = script_path.read_text()
                if "7.1.2" in content or "3.5.1" in content:
                    android_init_updated = True
                    break
                    
        # Check iOS init scripts  
        ios_scripts = ['init-ios.sh', 'init-ios-openssl.sh']
        for script_name in ios_scripts:
            script_path = self.project_root / script_name
            if script_path.exists():
                content = script_path.read_text()
                if "7.1.2" in content or "3.5.1" in content:
                    ios_init_updated = True
                    break
                    
        if android_init_updated and ios_init_updated:
            self.log_result('cross_platform', 'Init Script Consistency', 'pass',
                          'Both Android and iOS init scripts updated with new versions')
        else:
            self.log_result('cross_platform', 'Init Script Consistency', 'warning',
                          f'Init script updates: Android={android_init_updated}, iOS={ios_init_updated}')
            
        # Check upgrade documentation consistency
        android_report = self.android_dir / "API35_MIGRATION_REPORT.md"
        ios_report = self.ios_dir / "iOS18_MIGRATION_REPORT.md"
        
        if android_report.exists() and ios_report.exists():
            self.log_result('cross_platform', 'Migration Reports', 'pass',
                          'Both Android and iOS migration reports generated')
        else:
            self.log_result('cross_platform', 'Migration Reports', 'warning',
                          f'Migration reports: Android={android_report.exists()}, iOS={ios_report.exists()}')
            
    def run_all_validations(self) -> None:
        """Run all validation tests"""
        print("🚀 Starting Cross-Platform Validation...")
        print("=" * 60)
        
        # Run validation tests
        self.validate_android_build_system()
        self.validate_ios_sdk_integration() 
        self.validate_dependency_upgrades()
        self.validate_api_compatibility_layers()
        self.validate_build_system_modernization()
        self.validate_cross_platform_consistency()
        
    def generate_validation_report(self) -> str:
        """Generate comprehensive validation report"""
        report_content = """# IJKPlayer Cross-Platform Validation Report

## Executive Summary

This report validates the cross-platform compatibility of IJKPlayer after the comprehensive upgrade to:
- **FFmpeg 7.1.2** (from 4.0)
- **OpenSSL 3.5.1** (from 1.x)
- **Android API Level 35** (Android 15)
- **iOS 18 SDK** with Xcode 16

"""
        
        # Calculate totals
        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_warnings = 0
        
        for platform in ['android', 'ios', 'cross_platform']:
            results = self.validation_results[platform]
            total_tests += len(results['tests'])
            total_passed += results['passed']
            total_failed += results['failed']
            total_warnings += results['warnings']
            
        # Overall status
        if total_failed == 0:
            status = "✅ PASSED" if total_warnings == 0 else "⚠️ PASSED WITH WARNINGS"
        else:
            status = "❌ FAILED"
            
        report_content += f"""## Overall Status: {status}

- **Total Tests**: {total_tests}
- **Passed**: {total_passed}
- **Failed**: {total_failed}  
- **Warnings**: {total_warnings}
- **Success Rate**: {(total_passed / total_tests * 100):.1f}%

"""

        # Platform-specific results
        for platform_name in ['Android', 'iOS', 'Cross-Platform']:
            platform_key = platform_name.lower().replace('-', '_')
            results = self.validation_results[platform_key]
            
            report_content += f"""## {platform_name} Validation Results

- **Tests Run**: {len(results['tests'])}
- **Passed**: {results['passed']}
- **Failed**: {results['failed']}
- **Warnings**: {results['warnings']}

### Detailed Results

"""
            
            for test in results['tests']:
                status_icon = {'pass': '✅', 'fail': '❌', 'warning': '⚠️'}[test['status']]
                report_content += f"- {status_icon} **{test['test']}**: {test['message']}\n"
                if test['details']:
                    report_content += f"  - Details: {test['details']}\n"
                    
            report_content += "\n"
            
        # Recommendations
        report_content += """## Recommendations

### Critical Issues
"""
        
        critical_issues = []
        for platform in ['android', 'ios', 'cross_platform']:
            for test in self.validation_results[platform]['tests']:
                if test['status'] == 'fail':
                    critical_issues.append(f"- **{platform.title()}**: {test['test']} - {test['message']}")
                    
        if critical_issues:
            report_content += "\n".join(critical_issues)
        else:
            report_content += "No critical issues found.\n"
            
        report_content += """

### Warnings to Address
"""
        
        warnings = []
        for platform in ['android', 'ios', 'cross_platform']:
            for test in self.validation_results[platform]['tests']:
                if test['status'] == 'warning':
                    warnings.append(f"- **{platform.title()}**: {test['test']} - {test['message']}")
                    
        if warnings:
            report_content += "\n".join(warnings)
        else:
            report_content += "No warnings found.\n"
            
        report_content += """

## Next Steps

### Immediate Actions Required
1. **Resolve Critical Issues**: Address all failed validation tests
2. **Build Testing**: Attempt compilation on both platforms
3. **Runtime Testing**: Test core media playback functionality

### Recommended Testing
1. **Android Testing**
   - Test on Android 15 devices/emulators
   - Verify API Level 35 specific features
   - Test hardware acceleration with MediaCodec

2. **iOS Testing**  
   - Test on iOS 18 devices/simulators
   - Verify Xcode 16 build process
   - Test VideoToolbox hardware acceleration

3. **Cross-Platform Testing**
   - Compare functionality between platforms
   - Test same media files on both platforms
   - Verify consistent API behavior

### Long-term Monitoring
1. **Performance Benchmarks**: Establish baseline metrics
2. **Compatibility Matrix**: Track supported OS versions
3. **Regression Testing**: Automated test suite for future changes

## Validation Methodology

This validation was performed using automated tools that:
1. **Static Analysis**: Checked file presence and content
2. **Configuration Validation**: Verified build settings and dependencies
3. **Cross-Platform Consistency**: Ensured both platforms are updated consistently
4. **Documentation Verification**: Confirmed upgrade documentation completeness

The validation focuses on integration completeness rather than runtime functionality, which requires actual compilation and testing.
"""

        # Save report
        report_file = self.project_root / "CROSS_PLATFORM_VALIDATION_REPORT.md"
        report_file.write_text(report_content)
        
        return report_content
        
    def print_summary(self) -> None:
        """Print validation summary"""
        print("\n" + "=" * 60)
        print("🎯 CROSS-PLATFORM VALIDATION SUMMARY")
        print("=" * 60)
        
        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_warnings = 0
        
        for platform_name in ['Android', 'iOS', 'Cross-Platform']:
            platform_key = platform_name.lower().replace('-', '_')
            results = self.validation_results[platform_key]
            
            total_tests += len(results['tests'])
            total_passed += results['passed']
            total_failed += results['failed']
            total_warnings += results['warnings']
            
            print(f"{platform_name:15}: {results['passed']:2d} passed, {results['failed']:2d} failed, {results['warnings']:2d} warnings")
            
        print("-" * 60)
        print(f"{'TOTAL':15}: {total_passed:2d} passed, {total_failed:2d} failed, {total_warnings:2d} warnings")
        
        if total_failed == 0:
            if total_warnings == 0:
                print("\n✅ ALL VALIDATIONS PASSED!")
            else:
                print(f"\n⚠️ PASSED WITH {total_warnings} WARNINGS")
        else:
            print(f"\n❌ {total_failed} CRITICAL ISSUES FOUND")
            
        print(f"\n📊 Success Rate: {(total_passed / total_tests * 100):.1f}%")
        print("📄 Detailed report: CROSS_PLATFORM_VALIDATION_REPORT.md")

def main():
    project_root = "/Users/leo/Code/ijkplayer"
    validator = CrossPlatformValidator(project_root)
    
    # Run all validations
    validator.run_all_validations()
    
    # Generate report
    validator.generate_validation_report()
    
    # Print summary
    validator.print_summary()
    
    return validator.validation_results

if __name__ == "__main__":
    main()