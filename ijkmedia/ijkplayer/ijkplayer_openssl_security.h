#ifndef IJKPLAYER_OPENSSL_SECURITY_H
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
