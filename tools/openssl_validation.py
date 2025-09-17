#!/usr/bin/env python3
"""
OpenSSL 3.5.1 Validation Script for IJKPlayer
Tests SSL/TLS functionality and security compliance
"""

import ssl
import socket
import subprocess
import sys
from urllib.request import urlopen
from urllib.error import URLError

def test_openssl_version():
    """Test OpenSSL version"""
    print("🔍 Testing OpenSSL version...")
    try:
        result = subprocess.run(['openssl', 'version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ OpenSSL version: {version}")
            if "3.5.1" in version:
                print("✅ OpenSSL 3.5.1 detected")
                return True
            else:
                print(f"⚠️  Expected OpenSSL 3.5.1, got: {version}")
                return False
        else:
            print(f"❌ Failed to get OpenSSL version: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ OpenSSL command not found")
        return False

def test_tls_connection():
    """Test TLS connection with security requirements"""
    print("\n🔍 Testing TLS connection...")
    
    test_urls = [
        "https://www.google.com",
        "https://github.com", 
        "https://www.apple.com"
    ]
    
    success_count = 0
    
    for url in test_urls:
        try:
            print(f"  Testing {url}...")
            
            # Create SSL context with security requirements
            context = ssl.create_default_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            context.maximum_version = ssl.TLSVersion.TLSv1_3
            
            # Test connection
            with urlopen(url, timeout=10, context=context) as response:
                if response.status == 200:
                    print(f"    ✅ Connection successful")
                    success_count += 1
                else:
                    print(f"    ⚠️  HTTP status: {response.status}")
                    
        except URLError as e:
            print(f"    ❌ Connection failed: {e}")
        except Exception as e:
            print(f"    ❌ Unexpected error: {e}")
    
    if success_count >= 2:
        print(f"✅ TLS connections: {success_count}/{len(test_urls)} successful")
        return True
    else:
        print(f"❌ TLS connections: {success_count}/{len(test_urls)} successful (insufficient)")
        return False

def test_cipher_suites():
    """Test available cipher suites"""
    print("\n🔍 Testing cipher suites...")
    
    try:
        result = subprocess.run(['openssl', 'ciphers', '-v', 'HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            ciphers = result.stdout.strip().split('\n')
            modern_ciphers = [c for c in ciphers if 'AES' in c or 'CHACHA20' in c]
            
            print(f"✅ Found {len(modern_ciphers)} modern cipher suites")
            if len(modern_ciphers) >= 10:
                print("✅ Sufficient modern ciphers available")
                return True
            else:
                print(f"⚠️  Only {len(modern_ciphers)} modern ciphers available")
                return False
        else:
            print(f"❌ Failed to list ciphers: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ OpenSSL command not found")
        return False

def main():
    """Main validation function"""
    print("🛡️  OpenSSL 3.5.1 Security Validation for IJKPlayer")
    print("=" * 60)
    
    tests = [
        ("OpenSSL Version", test_openssl_version),
        ("TLS Connection", test_tls_connection),  
        ("Cipher Suites", test_cipher_suites),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print(f"\n📊 Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All OpenSSL 3.5.1 security validations passed!")
        sys.exit(0)
    else:
        print("❌ Some validations failed. Please review the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
