#!/usr/bin/env python3
"""
OpenSSL API Migration Tool for IJKPlayer
Handles migration from OpenSSL 1.x to 3.5.1

This tool automatically updates deprecated OpenSSL API calls in the IJKPlayer codebase.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class OpenSSLAPIMigrator:
    """OpenSSL API migration helper"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.migration_patterns = self._define_migration_patterns()
        self.files_modified = 0
        self.changes_made = 0
        
    def _define_migration_patterns(self) -> List[Dict]:
        """Define API migration patterns"""
        return [
            # SSL library initialization (no longer needed in OpenSSL 3.x)
            {
                'pattern': r'SSL_library_init\(\);?',
                'replacement': '/* SSL_library_init() not needed in OpenSSL 3.x */',
                'description': 'Remove SSL_library_init() calls'
            },
            {
                'pattern': r'SSL_load_error_strings\(\);?',
                'replacement': '/* SSL_load_error_strings() not needed in OpenSSL 3.x */',
                'description': 'Remove SSL_load_error_strings() calls'
            },
            {
                'pattern': r'ERR_load_crypto_strings\(\);?',
                'replacement': '/* ERR_load_crypto_strings() not needed in OpenSSL 3.x */',
                'description': 'Remove ERR_load_crypto_strings() calls'
            },
            {
                'pattern': r'OpenSSL_add_all_algorithms\(\);?',
                'replacement': '/* OpenSSL_add_all_algorithms() not needed in OpenSSL 3.x */',
                'description': 'Remove OpenSSL_add_all_algorithms() calls'
            },
            
            # SSL method updates
            {
                'pattern': r'TLSv1_method\(\)',
                'replacement': 'TLS_method()',
                'description': 'Update TLSv1_method() to TLS_method()'
            },
            {
                'pattern': r'TLSv1_client_method\(\)',
                'replacement': 'TLS_client_method()',
                'description': 'Update TLSv1_client_method() to TLS_client_method()'
            },
            {
                'pattern': r'TLSv1_server_method\(\)',
                'replacement': 'TLS_server_method()',
                'description': 'Update TLSv1_server_method() to TLS_server_method()'
            },
            {
                'pattern': r'SSLv23_method\(\)',
                'replacement': 'TLS_method()',
                'description': 'Update SSLv23_method() to TLS_method()'
            },
            {
                'pattern': r'SSLv23_client_method\(\)',
                'replacement': 'TLS_client_method()',
                'description': 'Update SSLv23_client_method() to TLS_client_method()'
            },
            {
                'pattern': r'SSLv23_server_method\(\)',
                'replacement': 'TLS_server_method()',
                'description': 'Update SSLv23_server_method() to TLS_server_method()'
            },
            
            # EVP key and cipher updates
            {
                'pattern': r'EVP_CIPHER_CTX_init\(([^)]+)\)',
                'replacement': r'EVP_CIPHER_CTX_reset(\1)',
                'description': 'Update EVP_CIPHER_CTX_init() to EVP_CIPHER_CTX_reset()'
            },
            {
                'pattern': r'EVP_CIPHER_CTX_cleanup\(([^)]+)\)',
                'replacement': r'EVP_CIPHER_CTX_reset(\1)',
                'description': 'Update EVP_CIPHER_CTX_cleanup() to EVP_CIPHER_CTX_reset()'
            },
            
            # Hash context updates
            {
                'pattern': r'EVP_MD_CTX_destroy\(([^)]+)\)',
                'replacement': r'EVP_MD_CTX_free(\1)',
                'description': 'Update EVP_MD_CTX_destroy() to EVP_MD_CTX_free()'
            },
            {
                'pattern': r'EVP_MD_CTX_create\(\)',
                'replacement': 'EVP_MD_CTX_new()',
                'description': 'Update EVP_MD_CTX_create() to EVP_MD_CTX_new()'
            },
            
            # RSA key updates
            {
                'pattern': r'RSA_generate_key\(([^,]+),([^,]+),([^,]+),([^)]+)\)',
                'replacement': r'RSA_generate_key_ex(\1, \2, NULL, NULL)',
                'description': 'Update RSA_generate_key() to RSA_generate_key_ex()'
            },
            
            # HMAC updates
            {
                'pattern': r'HMAC_CTX_init\(([^)]+)\)',
                'replacement': r'HMAC_CTX_reset(\1)',
                'description': 'Update HMAC_CTX_init() to HMAC_CTX_reset()'
            },
            {
                'pattern': r'HMAC_CTX_cleanup\(([^)]+)\)',
                'replacement': r'HMAC_CTX_free(\1)',
                'description': 'Update HMAC_CTX_cleanup() to HMAC_CTX_free()'
            },
        ]
    
    def find_source_files(self) -> List[Path]:
        """Find all C/C++ source files in the project"""
        extensions = {'.c', '.cpp', '.cc', '.cxx', '.h', '.hpp'}
        source_files = []
        
        # Search in ijkmedia directory (main source)
        ijkmedia_dir = self.project_root / 'ijkmedia'
        if ijkmedia_dir.exists():
            for file_path in ijkmedia_dir.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in extensions:
                    source_files.append(file_path)
        
        # Search in android directory for JNI code
        android_dir = self.project_root / 'android'
        if android_dir.exists():
            for file_path in android_dir.rglob('*.c'):
                source_files.append(file_path)
            for file_path in android_dir.rglob('*.cpp'):
                source_files.append(file_path)
            for file_path in android_dir.rglob('*.h'):
                source_files.append(file_path)
        
        # Search in ios directory
        ios_dir = self.project_root / 'ios'
        if ios_dir.exists():
            for file_path in ios_dir.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in {'.c', '.cpp', '.m', '.mm', '.h'}:
                    source_files.append(file_path)
        
        return sorted(source_files)
    
    def migrate_file(self, file_path: Path) -> int:
        """Migrate a single file, returns number of changes made"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            changes = 0
            
            # Apply each migration pattern
            for migration in self.migration_patterns:
                pattern = migration['pattern']
                replacement = migration['replacement']
                
                # Count matches before replacement
                matches = len(re.findall(pattern, content))
                if matches > 0:
                    content = re.sub(pattern, replacement, content)
                    changes += matches
                    print(f"  📝 {migration['description']}: {matches} changes")
            
            # Write back if changes were made
            if changes > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return changes
                
        except Exception as e:
            print(f"⚠️  Error processing {file_path}: {e}")
            
        return 0
    
    def run_migration(self) -> None:
        """Run the complete migration process"""
        print("🔄 OpenSSL API Migration Tool")
        print("=" * 50)
        print(f"Project root: {self.project_root}")
        
        # Find source files
        print("\n🔍 Finding source files...")
        source_files = self.find_source_files()
        print(f"Found {len(source_files)} source files")
        
        if not source_files:
            print("No source files found. Nothing to migrate.")
            return
        
        # Process each file
        print("\n🔧 Processing files...")
        for file_path in source_files:
            relative_path = file_path.relative_to(self.project_root)
            
            # Check if file contains OpenSSL references
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                if 'openssl' in content.lower() or 'ssl_' in content or 'evp_' in content:
                    print(f"\n📁 {relative_path}")
                    changes = self.migrate_file(file_path)
                    if changes > 0:
                        self.files_modified += 1
                        self.changes_made += changes
                        
            except Exception as e:
                print(f"⚠️  Error reading {relative_path}: {e}")
        
        # Summary
        print(f"\n✅ Migration complete!")
        print(f"Files modified: {self.files_modified}")
        print(f"Total changes: {self.changes_made}")
        
        if self.files_modified > 0:
            print(f"\n📋 Next steps:")
            print(f"1. Review the changes made to ensure correctness")
            print(f"2. Test compilation with OpenSSL 3.5.1")
            print(f"3. Run SSL/TLS functionality tests")
        
    def create_compatibility_header(self) -> None:
        """Create compatibility header for OpenSSL 3.x"""
        header_content = '''#ifndef IJKPLAYER_OPENSSL_COMPAT_H
#define IJKPLAYER_OPENSSL_COMPAT_H

/*
 * OpenSSL 3.5.1 Compatibility Header for IJKPlayer
 * Provides compatibility macros for OpenSSL API changes
 */

#include <openssl/opensslv.h>

#if OPENSSL_VERSION_NUMBER >= 0x30000000L
/* OpenSSL 3.0+ compatibility */

/* These functions are no longer needed in OpenSSL 3.x */
#define SSL_library_init() do { /* no-op */ } while(0)
#define SSL_load_error_strings() do { /* no-op */ } while(0)
#define ERR_load_crypto_strings() do { /* no-op */ } while(0)
#define OpenSSL_add_all_algorithms() do { /* no-op */ } while(0)
#define OpenSSL_add_all_ciphers() do { /* no-op */ } while(0)
#define OpenSSL_add_all_digests() do { /* no-op */ } while(0)

/* EVP context compatibility */
#define EVP_MD_CTX_create() EVP_MD_CTX_new()
#define EVP_MD_CTX_destroy(ctx) EVP_MD_CTX_free(ctx)
#define EVP_CIPHER_CTX_init(ctx) EVP_CIPHER_CTX_reset(ctx)
#define EVP_CIPHER_CTX_cleanup(ctx) EVP_CIPHER_CTX_reset(ctx)

/* HMAC context compatibility */
#define HMAC_CTX_init(ctx) HMAC_CTX_reset(ctx)

#endif /* OpenSSL 3.0+ */

#endif /* IJKPLAYER_OPENSSL_COMPAT_H */
'''
        
        header_path = self.project_root / 'ijkmedia' / 'ijkplayer' / 'openssl_compat.h'
        header_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(header_path, 'w', encoding='utf-8') as f:
            f.write(header_content)
        
        print(f"📄 Created compatibility header: {header_path}")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = "."
    
    migrator = OpenSSLAPIMigrator(project_root)
    
    print("🔧 OpenSSL 3.5.1 API Migration for IJKPlayer")
    print("=" * 60)
    
    # Create compatibility header
    migrator.create_compatibility_header()
    
    # Run migration
    migrator.run_migration()

if __name__ == "__main__":
    main()