#ifndef IJKPLAYER_OPENSSL_COMPAT_H
#define IJKPLAYER_OPENSSL_COMPAT_H

/*
 * OpenSSL 3.5.1 Compatibility Header for IJKPlayer
 * Provides compatibility macros for OpenSSL API changes
 */

#include <openssl/opensslv.h>

#if OPENSSL_VERSION_NUMBER >= 0x30000000L
/* OpenSSL 3.0+ compatibility */

/* These functions are no longer needed in OpenSSL 3.x */
#define /* SSL_library_init() not needed in OpenSSL 3.x */ do { /* no-op */ } while(0)
#define /* SSL_load_error_strings() not needed in OpenSSL 3.x */ do { /* no-op */ } while(0)
#define /* ERR_load_crypto_strings() not needed in OpenSSL 3.x */ do { /* no-op */ } while(0)
#define /* OpenSSL_add_all_algorithms() not needed in OpenSSL 3.x */ do { /* no-op */ } while(0)
#define OpenSSL_add_all_ciphers() do { /* no-op */ } while(0)
#define OpenSSL_add_all_digests() do { /* no-op */ } while(0)

/* EVP context compatibility */
#define EVP_MD_CTX_new() EVP_MD_CTX_new()
#define EVP_MD_CTX_free(ctx) EVP_MD_CTX_free(ctx)
#define EVP_CIPHER_CTX_reset(ctx) EVP_CIPHER_CTX_reset(ctx)
#define EVP_CIPHER_CTX_reset(ctx) EVP_CIPHER_CTX_reset(ctx)

/* HMAC context compatibility */
#define HMAC_CTX_reset(ctx) HMAC_CTX_reset(ctx)

#endif /* OpenSSL 3.0+ */

#endif /* IJKPLAYER_OPENSSL_COMPAT_H */
