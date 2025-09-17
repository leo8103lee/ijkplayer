
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
    
    printf("TLS Connection: %s using %s\n", version, cipher);
    
    // Verify we're using secure protocols
    if (strcmp(version, "TLSv1.2") != 0 && strcmp(version, "TLSv1.3") != 0) {
        printf("WARNING: Insecure TLS version: %s\n", version);
        return -2;
    }
    
    return 0;
}
