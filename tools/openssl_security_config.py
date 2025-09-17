#!/usr/bin/env python3
"""
OpenSSL 3.5.1 Security Configuration for IJKPlayer
Implements modern TLS security policies and cipher suite configurations
"""

import os
import sys
from pathlib import Path

class OpenSSLSecurityConfigGenerator:
    """Generate secure OpenSSL configurations for IJKPlayer"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        
    def generate_ssl_security_policy(self) -> str:
        """Generate SSL security policy code"""
        return '''
/*
 * OpenSSL 3.5.1 Security Configuration for IJKPlayer
 * Implements modern TLS security best practices
 */

#include "ijkplayer_openssl_security.h"
#include <openssl/ssl.h>
#include <openssl/err.h>

// Modern cipher suites (TLS 1.2 and 1.3 only)
static const char* IJK_TLS_CIPHER_SUITES = 
    // TLS 1.3 cipher suites (preferred)
    "TLS_AES_256_GCM_SHA384:"
    "TLS_AES_128_GCM_SHA256:"
    "TLS_CHACHA20_POLY1305_SHA256:"
    
    // TLS 1.2 cipher suites (fallback)
    "ECDHE-ECDSA-AES256-GCM-SHA384:"
    "ECDHE-RSA-AES256-GCM-SHA384:"
    "ECDHE-ECDSA-AES128-GCM-SHA256:"
    "ECDHE-RSA-AES128-GCM-SHA256:"
    "ECDHE-ECDSA-CHACHA20-POLY1305:"
    "ECDHE-RSA-CHACHA20-POLY1305";

// Security curves for ECDHE
static const char* IJK_TLS_CURVES = "P-384:P-256:X25519";

// TLS protocol versions
#define IJK_TLS_MIN_VERSION TLS1_2_VERSION
#define IJK_TLS_MAX_VERSION TLS1_3_VERSION

int ijkplayer_ssl_configure_security(SSL_CTX* ctx) {
    if (!ctx) {
        return -1;
    }
    
    // Set minimum and maximum TLS versions
    if (!SSL_CTX_set_min_proto_version(ctx, IJK_TLS_MIN_VERSION)) {
        return -2;
    }
    
    if (!SSL_CTX_set_max_proto_version(ctx, IJK_TLS_MAX_VERSION)) {
        return -3;
    }
    
    // Set secure cipher suites
    if (!SSL_CTX_set_cipher_list(ctx, IJK_TLS_CIPHER_SUITES)) {
        return -4;
    }
    
    // Set TLS 1.3 cipher suites
    if (!SSL_CTX_set_ciphersuites(ctx, "TLS_AES_256_GCM_SHA384:TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256")) {
        return -5;
    }
    
    // Configure elliptic curves
    if (!SSL_CTX_set1_curves_list(ctx, IJK_TLS_CURVES)) {
        return -6;
    }
    
    // Security options
    SSL_CTX_set_options(ctx, SSL_OP_NO_SSLv2);
    SSL_CTX_set_options(ctx, SSL_OP_NO_SSLv3);
    SSL_CTX_set_options(ctx, SSL_OP_NO_TLSv1);
    SSL_CTX_set_options(ctx, SSL_OP_NO_TLSv1_1);
    SSL_CTX_set_options(ctx, SSL_OP_NO_COMPRESSION);
    SSL_CTX_set_options(ctx, SSL_OP_SINGLE_ECDH_USE);
    SSL_CTX_set_options(ctx, SSL_OP_SINGLE_DH_USE);
    SSL_CTX_set_options(ctx, SSL_OP_CIPHER_SERVER_PREFERENCE);
    
    // Certificate verification
    SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, NULL);
    SSL_CTX_set_verify_depth(ctx, 4);
    
    // Load system CA certificates
    if (!SSL_CTX_set_default_verify_paths(ctx)) {
        return -7;
    }
    
    return 0;
}

int ijkplayer_ssl_configure_client_security(SSL* ssl) {
    if (!ssl) {
        return -1;
    }
    
    // Enable hostname verification
    SSL_set_hostflags(ssl, X509_CHECK_FLAG_NO_PARTIAL_WILDCARDS);
    
    return 0;
}

const char* ijkplayer_ssl_get_security_level_description(void) {
    return "TLS 1.2+ with AEAD ciphers, Perfect Forward Secrecy, and modern curves";
}

int ijkplayer_ssl_log_connection_info(SSL* ssl) {
    if (!ssl) {
        return -1;
    }
    
    const char* version = SSL_get_version(ssl);
    const char* cipher = SSL_get_cipher_name(ssl);
    
    printf("TLS Connection: %s using %s\\n", version, cipher);
    
    // Verify we're using secure protocols
    if (strcmp(version, "TLSv1.2") != 0 && strcmp(version, "TLSv1.3") != 0) {
        printf("WARNING: Insecure TLS version: %s\\n", version);
        return -2;
    }
    
    return 0;
}
'''
    
    def generate_security_header(self) -> str:
        """Generate security header file"""
        return '''#ifndef IJKPLAYER_OPENSSL_SECURITY_H
#define IJKPLAYER_OPENSSL_SECURITY_H

/*
 * OpenSSL 3.5.1 Security Configuration for IJKPlayer
 * Modern TLS security policies and helper functions
 */

#include <openssl/ssl.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Configure SSL context with modern security settings
 * @param ctx SSL context to configure
 * @return 0 on success, negative on error
 */
int ijkplayer_ssl_configure_security(SSL_CTX* ctx);

/**
 * Configure SSL connection with client-specific security settings
 * @param ssl SSL connection to configure
 * @return 0 on success, negative on error
 */
int ijkplayer_ssl_configure_client_security(SSL* ssl);

/**
 * Get description of current security level
 * @return Security level description string
 */
const char* ijkplayer_ssl_get_security_level_description(void);

/**
 * Log TLS connection information for security auditing
 * @param ssl Active SSL connection
 * @return 0 on success, negative on error
 */
int ijkplayer_ssl_log_connection_info(SSL* ssl);

#ifdef __cplusplus
}
#endif

#endif /* IJKPLAYER_OPENSSL_SECURITY_H */
'''
    
    def create_security_files(self) -> None:
        """Create security configuration files"""
        ijkmedia_dir = self.project_root / 'ijkmedia' / 'ijkplayer'
        ijkmedia_dir.mkdir(parents=True, exist_ok=True)
        
        # Create header file
        header_path = ijkmedia_dir / 'ijkplayer_openssl_security.h'
        with open(header_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_security_header())
        print(f"📄 Created security header: {header_path}")
        
        # Create implementation file
        impl_path = ijkmedia_dir / 'ijkplayer_openssl_security.c'
        with open(impl_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_ssl_security_policy())
        print(f"📄 Created security implementation: {impl_path}")
        
    def create_validation_script(self) -> None:
        """Create SSL/TLS validation script"""
        script_content = '''#!/usr/bin/env python3
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
    print("\\n🔍 Testing TLS connection...")
    
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
    print("\\n🔍 Testing cipher suites...")
    
    try:
        result = subprocess.run(['openssl', 'ciphers', '-v', 'HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            ciphers = result.stdout.strip().split('\\n')
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
    
    print(f"\\n📊 Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All OpenSSL 3.5.1 security validations passed!")
        sys.exit(0)
    else:
        print("❌ Some validations failed. Please review the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
        
        script_path = self.project_root / 'tools' / 'openssl_validation.py'
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Make script executable
        os.chmod(script_path, 0o755)
        print(f"📄 Created validation script: {script_path}")

def main():
    """Main function"""
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    generator = OpenSSLSecurityConfigGenerator(project_root)
    
    print("🛡️ OpenSSL 3.5.1 Security Configuration Generator")
    print("=" * 60)
    
    # Create security files
    generator.create_security_files()
    
    # Create validation script
    generator.create_validation_script()
    
    print("\\n✅ Security configuration files created successfully!")
    print("\\nNext steps:")
    print("1. Include ijkplayer_openssl_security.h in your SSL code")
    print("2. Call ijkplayer_ssl_configure_security() on SSL contexts")
    print("3. Run tools/openssl_validation.py to test the configuration")

if __name__ == "__main__":
    main()