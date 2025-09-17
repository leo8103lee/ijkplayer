#!/usr/bin/env python3
"""
Compilation Validator for IJKPlayer Upgrade
Validates and attempts compilation after all upgrades are complete
"""

import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class CompilationValidator:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.android_dir = self.project_root / "android"
        self.ios_dir = self.project_root / "ios"
        
        self.compilation_results = {
            'environment': {'status': 'unknown', 'details': []},
            'dependencies': {'status': 'unknown', 'details': []},
            'android': {'status': 'unknown', 'details': [], 'build_log': ''},
            'ios': {'status': 'unknown', 'details': [], 'build_log': ''}
        }
        
    def log_step(self, category: str, step: str, status: str, message: str, details: str = ""):
        """Log compilation step result"""
        result = {
            'step': step,
            'status': status,  # 'pass', 'fail', 'warning', 'info'
            'message': message,
            'details': details
        }
        
        self.compilation_results[category]['details'].append(result)
        
        status_icons = {'pass': '✅', 'fail': '❌', 'warning': '⚠️', 'info': 'ℹ️'}
        icon = status_icons.get(status, '📋')
        print(f"{icon} {category.upper()}: {step} - {message}")
        
        if details:
            print(f"   Details: {details}")
            
    def check_environment_prerequisites(self) -> bool:
        """Check development environment prerequisites"""
        print("\n🔧 Checking Environment Prerequisites...")
        
        all_good = True
        
        # Check macOS version
        try:
            result = subprocess.run(['sw_vers', '-productVersion'], 
                                  capture_output=True, text=True, check=True)
            macos_version = result.stdout.strip()
            self.log_step('environment', 'macOS Version', 'info', 
                         f'macOS {macos_version} detected')
        except Exception as e:
            self.log_step('environment', 'macOS Version', 'warning',
                         f'Could not detect macOS version: {e}')
            
        # Check Homebrew and required tools
        required_tools = {
            'brew': 'Homebrew package manager',
            'git': 'Git version control',
            'yasm': 'Assembly compiler for FFmpeg',
            'cmake': 'Build system generator',
            'automake': 'Build tool for autotools'
        }
        
        for tool, description in required_tools.items():
            try:
                result = subprocess.run([tool, '--version'], 
                                      capture_output=True, text=True, check=True)
                version = result.stdout.split('\n')[0]
                self.log_step('environment', f'{tool.title()}', 'pass',
                             f'{description} available: {version}')
            except FileNotFoundError:
                self.log_step('environment', f'{tool.title()}', 'fail',
                             f'{description} not found')
                all_good = False
            except Exception as e:
                self.log_step('environment', f'{tool.title()}', 'warning',
                             f'Error checking {description}: {e}')
                
        # Check Android SDK/NDK
        android_sdk = os.environ.get('ANDROID_SDK')
        android_ndk = os.environ.get('ANDROID_NDK')
        
        if android_sdk and Path(android_sdk).exists():
            self.log_step('environment', 'Android SDK', 'pass',
                         f'Android SDK found at {android_sdk}')
        else:
            self.log_step('environment', 'Android SDK', 'fail',
                         'Android SDK not found or ANDROID_SDK not set')
            all_good = False
            
        if android_ndk and Path(android_ndk).exists():
            self.log_step('environment', 'Android NDK', 'pass',
                         f'Android NDK found at {android_ndk}')
        else:
            self.log_step('environment', 'Android NDK', 'warning',
                         'Android NDK not found or ANDROID_NDK not set')
            
        # Check Xcode
        try:
            result = subprocess.run(['xcode-select', '--print-path'], 
                                  capture_output=True, text=True, check=True)
            xcode_path = result.stdout.strip()
            
            # Get Xcode version
            result = subprocess.run(['xcodebuild', '-version'], 
                                  capture_output=True, text=True, check=True)
            xcode_version = result.stdout.split('\n')[0]
            self.log_step('environment', 'Xcode', 'pass',
                         f'{xcode_version} at {xcode_path}')
        except Exception as e:
            self.log_step('environment', 'Xcode', 'fail',
                         f'Xcode not found or not configured: {e}')
            all_good = False
            
        self.compilation_results['environment']['status'] = 'pass' if all_good else 'fail'
        return all_good
        
    def initialize_dependencies(self) -> bool:
        """Initialize and download all dependencies"""
        print("\n📦 Initializing Dependencies...")
        
        all_good = True
        init_scripts = [
            ('init-android.sh', 'Android FFmpeg'),
            ('init-android-openssl.sh', 'Android OpenSSL'), 
            ('init-android-libyuv.sh', 'Android libyuv'),
            ('init-android-soundtouch.sh', 'Android SoundTouch'),
            ('init-ios.sh', 'iOS FFmpeg'),
            ('init-ios-openssl.sh', 'iOS OpenSSL')
        ]
        
        for script_name, description in init_scripts:
            script_path = self.project_root / script_name
            
            if not script_path.exists():
                self.log_step('dependencies', description, 'fail',
                             f'Init script {script_name} not found')
                all_good = False
                continue
                
            self.log_step('dependencies', description, 'info',
                         f'Starting initialization of {description}...')
            
            try:
                # Run initialization script
                result = subprocess.run([str(script_path)], 
                                      cwd=self.project_root,
                                      capture_output=True, text=True, 
                                      timeout=600)  # 10 minute timeout
                
                if result.returncode == 0:
                    self.log_step('dependencies', description, 'pass',
                                 f'{description} initialized successfully')
                else:
                    self.log_step('dependencies', description, 'fail',
                                 f'{description} initialization failed',
                                 f'Error: {result.stderr[:500]}')
                    all_good = False
                    
            except subprocess.TimeoutExpired:
                self.log_step('dependencies', description, 'fail',
                             f'{description} initialization timed out (10 minutes)')
                all_good = False
            except Exception as e:
                self.log_step('dependencies', description, 'fail',
                             f'{description} initialization error: {e}')
                all_good = False
                
        self.compilation_results['dependencies']['status'] = 'pass' if all_good else 'fail'
        return all_good
        
    def compile_android(self) -> bool:
        """Attempt Android compilation"""
        print("\n🤖 Compiling Android...")
        
        if not self.android_dir.exists():
            self.log_step('android', 'Directory Check', 'fail',
                         'Android directory not found')
            self.compilation_results['android']['status'] = 'fail'
            return False
            
        # Check if FFmpeg contrib directory exists
        contrib_dir = self.android_dir / "contrib"
        if not contrib_dir.exists():
            self.log_step('android', 'FFmpeg Sources', 'fail',
                         'FFmpeg contrib directory not found')
            self.compilation_results['android']['status'] = 'fail'
            return False
            
        all_good = True
        
        # Compile FFmpeg first
        self.log_step('android', 'FFmpeg Compilation', 'info',
                     'Starting Android FFmpeg compilation...')
        
        try:
            # Clean previous builds
            result = subprocess.run(['./compile-ffmpeg.sh', 'clean'], 
                                  cwd=contrib_dir,
                                  capture_output=True, text=True,
                                  timeout=300)
            
            if result.returncode == 0:
                self.log_step('android', 'FFmpeg Clean', 'pass',
                             'FFmpeg clean completed')
            else:
                self.log_step('android', 'FFmpeg Clean', 'warning',
                             'FFmpeg clean had issues, continuing...')
                
            # Compile for arm64 (fastest single architecture)
            self.log_step('android', 'FFmpeg arm64', 'info',
                         'Compiling FFmpeg for arm64...')
            
            result = subprocess.run(['./compile-ffmpeg.sh', 'arm64'], 
                                  cwd=contrib_dir,
                                  capture_output=True, text=True,
                                  timeout=1800)  # 30 minute timeout
            
            build_log = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            self.compilation_results['android']['build_log'] += build_log
            
            if result.returncode == 0:
                self.log_step('android', 'FFmpeg arm64', 'pass',
                             'FFmpeg arm64 compilation successful')
            else:
                self.log_step('android', 'FFmpeg arm64', 'fail',
                             'FFmpeg arm64 compilation failed',
                             f'Exit code: {result.returncode}')
                all_good = False
                
        except subprocess.TimeoutExpired:
            self.log_step('android', 'FFmpeg arm64', 'fail',
                         'FFmpeg compilation timed out (30 minutes)')
            all_good = False
        except Exception as e:
            self.log_step('android', 'FFmpeg arm64', 'fail',
                         f'FFmpeg compilation error: {e}')
            all_good = False
            
        # If FFmpeg succeeded, try IJKPlayer compilation
        if all_good:
            ijkplayer_dir = self.android_dir
            self.log_step('android', 'IJKPlayer Compilation', 'info',
                         'Starting IJKPlayer compilation...')
            
            try:
                result = subprocess.run(['./compile-ijk.sh', 'arm64'], 
                                      cwd=ijkplayer_dir,
                                      capture_output=True, text=True,
                                      timeout=1200)  # 20 minute timeout
                
                build_log = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
                self.compilation_results['android']['build_log'] += "\n\n" + build_log
                
                if result.returncode == 0:
                    self.log_step('android', 'IJKPlayer arm64', 'pass',
                                 'IJKPlayer arm64 compilation successful')
                else:
                    self.log_step('android', 'IJKPlayer arm64', 'fail',
                                 'IJKPlayer arm64 compilation failed',
                                 f'Exit code: {result.returncode}')
                    all_good = False
                    
            except subprocess.TimeoutExpired:
                self.log_step('android', 'IJKPlayer arm64', 'fail',
                             'IJKPlayer compilation timed out (20 minutes)')
                all_good = False
            except Exception as e:
                self.log_step('android', 'IJKPlayer arm64', 'fail',
                             f'IJKPlayer compilation error: {e}')
                all_good = False
                
        self.compilation_results['android']['status'] = 'pass' if all_good else 'fail'
        return all_good
        
    def compile_ios(self) -> bool:
        """Attempt iOS compilation"""
        print("\n📱 Compiling iOS...")
        
        if not self.ios_dir.exists():
            self.log_step('ios', 'Directory Check', 'fail',
                         'iOS directory not found')
            self.compilation_results['ios']['status'] = 'fail'
            return False
            
        all_good = True
        
        # Compile FFmpeg for iOS
        self.log_step('ios', 'FFmpeg Compilation', 'info',
                     'Starting iOS FFmpeg compilation...')
        
        try:
            # Clean previous builds
            result = subprocess.run(['./compile-ffmpeg.sh', 'clean'], 
                                  cwd=self.ios_dir,
                                  capture_output=True, text=True,
                                  timeout=300)
            
            if result.returncode == 0:
                self.log_step('ios', 'FFmpeg Clean', 'pass',
                             'iOS FFmpeg clean completed')
            else:
                self.log_step('ios', 'FFmpeg Clean', 'warning',
                             'iOS FFmpeg clean had issues, continuing...')
                
            # Compile for arm64 (iPhone/iPad)
            self.log_step('ios', 'FFmpeg arm64', 'info',
                         'Compiling iOS FFmpeg for arm64...')
            
            result = subprocess.run(['./compile-ffmpeg.sh', 'arm64'], 
                                  cwd=self.ios_dir,
                                  capture_output=True, text=True,
                                  timeout=1800)  # 30 minute timeout
            
            build_log = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            self.compilation_results['ios']['build_log'] += build_log
            
            if result.returncode == 0:
                self.log_step('ios', 'FFmpeg arm64', 'pass',
                             'iOS FFmpeg arm64 compilation successful')
            else:
                self.log_step('ios', 'FFmpeg arm64', 'fail',
                             'iOS FFmpeg arm64 compilation failed',
                             f'Exit code: {result.returncode}')
                all_good = False
                
        except subprocess.TimeoutExpired:
            self.log_step('ios', 'FFmpeg arm64', 'fail',
                         'iOS FFmpeg compilation timed out (30 minutes)')
            all_good = False
        except Exception as e:
            self.log_step('ios', 'FFmpeg arm64', 'fail',
                         f'iOS FFmpeg compilation error: {e}')
            all_good = False
            
        # Try Xcode project build
        if all_good:
            xcode_project = self.ios_dir / "IJKMediaPlayer" / "IJKMediaPlayer.xcodeproj"
            if xcode_project.exists():
                self.log_step('ios', 'Xcode Build', 'info',
                             'Starting Xcode project build...')
                
                try:
                    result = subprocess.run([
                        'xcodebuild', '-project', str(xcode_project),
                        '-scheme', 'IJKMediaFramework',
                        '-configuration', 'Release',
                        'clean', 'build'
                    ], capture_output=True, text=True, timeout=1200)
                    
                    build_log = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
                    self.compilation_results['ios']['build_log'] += "\n\n" + build_log
                    
                    if result.returncode == 0:
                        self.log_step('ios', 'Xcode Build', 'pass',
                                     'Xcode project build successful')
                    else:
                        self.log_step('ios', 'Xcode Build', 'fail',
                                     'Xcode project build failed',
                                     f'Exit code: {result.returncode}')
                        all_good = False
                        
                except subprocess.TimeoutExpired:
                    self.log_step('ios', 'Xcode Build', 'fail',
                                 'Xcode build timed out (20 minutes)')
                    all_good = False
                except Exception as e:
                    self.log_step('ios', 'Xcode Build', 'fail',
                                 f'Xcode build error: {e}')
                    all_good = False
            else:
                self.log_step('ios', 'Xcode Project', 'warning',
                             'Xcode project not found, skipping Xcode build')
                
        self.compilation_results['ios']['status'] = 'pass' if all_good else 'fail'
        return all_good
        
    def analyze_build_errors(self) -> List[str]:
        """Analyze build errors and provide recommendations"""
        recommendations = []
        
        for platform in ['android', 'ios']:
            if self.compilation_results[platform]['status'] == 'fail':
                build_log = self.compilation_results[platform]['build_log']
                
                # Common error patterns
                if 'No such file or directory' in build_log:
                    recommendations.append(f"{platform.title()}: Missing files - check dependency initialization")
                    
                if 'NDK' in build_log and platform == 'android':
                    recommendations.append("Android: NDK path issues - verify ANDROID_NDK environment variable")
                    
                if 'permission denied' in build_log.lower():
                    recommendations.append(f"{platform.title()}: Permission issues - check script execute permissions")
                    
                if 'clang' in build_log and 'not found' in build_log:
                    recommendations.append(f"{platform.title()}: Compiler not found - check toolchain installation")
                    
                if 'undefined symbol' in build_log.lower():
                    recommendations.append(f"{platform.title()}: Linking issues - check library compatibility")
                    
        return recommendations
        
    def generate_compilation_report(self) -> str:
        """Generate comprehensive compilation report"""
        report_content = """# IJKPlayer Compilation Validation Report

## Executive Summary

This report documents the compilation validation of IJKPlayer after the comprehensive upgrade:
- **FFmpeg 4.0 → 7.1.2**
- **OpenSSL 1.x → 3.5.1** 
- **Android API 25 → 35**
- **iOS SDK → 18.0**

"""
        
        # Overall status
        env_ok = self.compilation_results['environment']['status'] == 'pass'
        deps_ok = self.compilation_results['dependencies']['status'] == 'pass' 
        android_ok = self.compilation_results['android']['status'] == 'pass'
        ios_ok = self.compilation_results['ios']['status'] == 'pass'
        
        overall_status = "✅ SUCCESS" if all([env_ok, deps_ok, android_ok, ios_ok]) else "❌ FAILED"
        
        report_content += f"## Overall Status: {overall_status}\n\n"
        
        # Environment section
        report_content += """## Environment Prerequisites

| Component | Status | Details |
|-----------|--------|---------|
"""
        
        for detail in self.compilation_results['environment']['details']:
            status_icon = {'pass': '✅', 'fail': '❌', 'warning': '⚠️', 'info': 'ℹ️'}[detail['status']]
            report_content += f"| {detail['step']} | {status_icon} | {detail['message']} |\n"
            
        # Dependencies section
        report_content += """
## Dependency Initialization

| Dependency | Status | Details |
|------------|--------|---------|
"""
        
        for detail in self.compilation_results['dependencies']['details']:
            status_icon = {'pass': '✅', 'fail': '❌', 'warning': '⚠️', 'info': 'ℹ️'}[detail['status']]
            report_content += f"| {detail['step']} | {status_icon} | {detail['message']} |\n"
            
        # Android compilation
        report_content += """
## Android Compilation

| Step | Status | Details |
|------|--------|---------|
"""
        
        for detail in self.compilation_results['android']['details']:
            status_icon = {'pass': '✅', 'fail': '❌', 'warning': '⚠️', 'info': 'ℹ️'}[detail['status']]
            report_content += f"| {detail['step']} | {status_icon} | {detail['message']} |\n"
            
        # iOS compilation  
        report_content += """
## iOS Compilation

| Step | Status | Details |
|------|--------|---------|
"""
        
        for detail in self.compilation_results['ios']['details']:
            status_icon = {'pass': '✅', 'fail': '❌', 'warning': '⚠️', 'info': 'ℹ️'}[detail['status']]
            report_content += f"| {detail['step']} | {status_icon} | {detail['message']} |\n"
            
        # Error analysis and recommendations
        recommendations = self.analyze_build_errors()
        
        report_content += """
## Error Analysis and Recommendations

"""
        
        if recommendations:
            for rec in recommendations:
                report_content += f"- {rec}\n"
        else:
            report_content += "No specific error patterns identified.\n"
            
        report_content += """
## Next Steps

### If Compilation Succeeded
1. **Functional Testing**: Test basic media playback
2. **Performance Testing**: Benchmark against previous version
3. **Compatibility Testing**: Test on multiple device types
4. **Integration Testing**: Test in sample applications

### If Compilation Failed
1. **Review Error Logs**: Check detailed build logs saved separately
2. **Fix Dependencies**: Ensure all prerequisites are met
3. **Check Environment**: Verify SDK/NDK paths and versions
4. **Incremental Building**: Try building individual components

## Build Logs Location

Detailed build logs are available in:
- Android build log: `android_build.log`
- iOS build log: `ios_build.log`

These logs contain complete stdout/stderr output for debugging compilation issues.
"""

        # Save report
        report_file = self.project_root / "COMPILATION_VALIDATION_REPORT.md"
        report_file.write_text(report_content)
        
        # Save build logs
        if self.compilation_results['android']['build_log']:
            android_log = self.project_root / "android_build.log"
            android_log.write_text(self.compilation_results['android']['build_log'])
            
        if self.compilation_results['ios']['build_log']:
            ios_log = self.project_root / "ios_build.log"
            ios_log.write_text(self.compilation_results['ios']['build_log'])
        
        return report_content
        
    def print_summary(self) -> None:
        """Print compilation summary"""
        print("\n" + "=" * 60)
        print("🎯 COMPILATION VALIDATION SUMMARY")
        print("=" * 60)
        
        categories = [
            ('Environment', 'environment'),
            ('Dependencies', 'dependencies'), 
            ('Android', 'android'),
            ('iOS', 'ios')
        ]
        
        for name, key in categories:
            status = self.compilation_results[key]['status']
            status_icon = {'pass': '✅', 'fail': '❌', 'unknown': '❓'}[status]
            
            passed = sum(1 for d in self.compilation_results[key]['details'] if d['status'] == 'pass')
            failed = sum(1 for d in self.compilation_results[key]['details'] if d['status'] == 'fail')
            warnings = sum(1 for d in self.compilation_results[key]['details'] if d['status'] == 'warning')
            
            print(f"{name:12}: {status_icon} {status.upper():8} ({passed} passed, {failed} failed, {warnings} warnings)")
            
        # Overall result
        all_passed = all(self.compilation_results[key]['status'] == 'pass' 
                        for key in ['environment', 'dependencies', 'android', 'ios'])
        
        print("-" * 60)
        if all_passed:
            print("🎉 ALL COMPILATIONS SUCCESSFUL!")
            print("✅ Ready for functional and performance testing")
        else:
            print("❌ COMPILATION ISSUES FOUND")
            print("📋 Check COMPILATION_VALIDATION_REPORT.md for details")
            
        print("📄 Detailed report: COMPILATION_VALIDATION_REPORT.md")
        
def main():
    project_root = "/Users/leo/Code/ijkplayer"
    validator = CompilationValidator(project_root)
    
    print("🚀 Starting IJKPlayer Compilation Validation...")
    
    # Check environment first
    env_ok = validator.check_environment_prerequisites()
    
    if not env_ok:
        print("\n❌ Environment prerequisites not met. Fix issues before proceeding.")
        validator.generate_compilation_report()
        return False
        
    # Initialize dependencies
    deps_ok = validator.initialize_dependencies()
    
    if not deps_ok:
        print("\n⚠️ Some dependencies failed to initialize. Proceeding with compilation attempt...")
        
    # Attempt compilation
    print("\n🔨 Starting compilation attempts...")
    android_ok = validator.compile_android()
    ios_ok = validator.compile_ios()
    
    # Generate report and summary
    validator.generate_compilation_report()
    validator.print_summary()
    
    return env_ok and android_ok and ios_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)