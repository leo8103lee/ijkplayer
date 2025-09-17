/*
 * IJK Application Context for FFmpeg 7.1.2 compatibility
 * Copyright (c) 2025 Bilibili
 * Copyright (c) 2025 Zhang Rui <bbcallen@gmail.com>
 *
 * This file is part of ijkPlayer.
 *
 * ijkPlayer is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 */

#ifndef IJK_APPLICATION_H
#define IJK_APPLICATION_H

#include <stdint.h>
#include <stddef.h>
#include "libavutil/dict.h"

#ifdef __cplusplus
extern "C" {
#endif

// Forward declarations
typedef struct IJKApplicationContext IJKApplicationContext;
typedef struct IJKAppIOControl IJKAppIOControl;

// IJK Application Control Messages - compatible with original AVAPP_CTRL_* constants
#define IJK_CTRL_WILL_CONCAT_SEGMENT_OPEN    0x10001
#define IJK_CTRL_WILL_TCP_OPEN              0x10002
#define IJK_CTRL_WILL_HTTP_OPEN             0x10003
#define IJK_CTRL_WILL_LIVE_OPEN             0x10004
#define IJK_CTRL_DID_TCP_OPEN               0x10005
#define IJK_CTRL_DID_HTTP_OPEN              0x10006
#define IJK_CTRL_DID_LIVE_OPEN              0x10007
#define IJK_CTRL_WILL_CONCAT_RESOLVE_HOST   0x10008
#define IJK_CTRL_DID_CONCAT_RESOLVE_HOST    0x10009

// I/O Control structure for URL operations
typedef struct IJKAppIOControl {
    size_t size;
    char url[4096];
    int segment_index;
    int retry_counter;

    // Network statistics
    int is_handled;
    int is_url_changed;

    // TCP-specific fields
    char ip[128];
    int port;
    int fd;
    int error;

    // HTTP-specific fields
    int http_code;
    int64_t filesize;

    // Additional IJK-specific fields
    void *opaque;
} IJKAppIOControl;

// Async statistics structure
typedef struct IJKAppAsyncStatistic {
    size_t size;
    int64_t buf_backwards;
    int64_t buf_forwards;
    int64_t buf_capacity;
} IJKAppAsyncStatistic;

// Speed statistics structure
typedef struct IJKAppAsyncReadSpeed {
    size_t size;
    int is_full_speed;
    int64_t io_bytes;
    int64_t elapsed_milli;
    int64_t bytes_per_sec;
} IJKAppAsyncReadSpeed;

// Application event callback function type
typedef int (*IJKApplicationEventCallback)(IJKApplicationContext *ctx, int message, void *data, size_t data_size);

// Main application context structure
struct IJKApplicationContext {
    void *opaque;                           // User data pointer (typically IJKFFPlayer)
    IJKApplicationEventCallback func_on_app_event;  // Event callback function

    // Internal state
    int64_t last_high_water_mark_in_ms;

    // Reference counting for memory management
    int ref_count;
};

// Core API functions - drop-in replacements for av_application_* functions

/**
 * Create and initialize an application context
 * @param ps Pointer to application context pointer (will be allocated)
 * @param opaque User data pointer (typically IJKFFPlayer instance)
 * @return 0 on success, negative on error
 */
int ijk_application_open(IJKApplicationContext **ps, void *opaque);

/**
 * Close and free an application context
 * @param ps Pointer to application context pointer (will be set to NULL)
 */
void ijk_application_closep(IJKApplicationContext **ps);

/**
 * Send I/O control message to application context
 * @param h Application context
 * @param message Control message type (IJK_CTRL_*)
 * @param data Message data (typically IJKAppIOControl*)
 * @return 0 on success, negative on error
 */
int ijk_application_on_io_control(IJKApplicationContext *h, int message, void *data);

/**
 * Send async statistics to application context
 * @param h Application context
 * @param data Statistics data
 * @return 0 on success, negative on error
 */
int ijk_application_on_async_statistic(IJKApplicationContext *h, IJKAppAsyncStatistic *data);

/**
 * Send async read speed info to application context
 * @param h Application context
 * @param data Speed data
 * @return 0 on success, negative on error
 */
int ijk_application_on_async_read_speed(IJKApplicationContext *h, IJKAppAsyncReadSpeed *data);

// Compatibility macros for seamless migration from FFmpeg 4.0
#define AVApplicationContext        IJKApplicationContext
#define AVAppIOControl             IJKAppIOControl
#define AVAppAsyncStatistic        IJKAppAsyncStatistic
#define AVAppAsyncReadSpeed        IJKAppAsyncReadSpeed

#define av_application_open         ijk_application_open
#define av_application_closep       ijk_application_closep
#define av_application_on_io_control ijk_application_on_io_control
#define av_application_on_async_statistic ijk_application_on_async_statistic
#define av_application_on_async_read_speed ijk_application_on_async_read_speed

#define AVAPP_CTRL_WILL_CONCAT_SEGMENT_OPEN IJK_CTRL_WILL_CONCAT_SEGMENT_OPEN
#define AVAPP_CTRL_WILL_TCP_OPEN            IJK_CTRL_WILL_TCP_OPEN
#define AVAPP_CTRL_WILL_HTTP_OPEN           IJK_CTRL_WILL_HTTP_OPEN
#define AVAPP_CTRL_WILL_LIVE_OPEN           IJK_CTRL_WILL_LIVE_OPEN
#define AVAPP_CTRL_DID_TCP_OPEN             IJK_CTRL_DID_TCP_OPEN
#define AVAPP_CTRL_DID_HTTP_OPEN            IJK_CTRL_DID_HTTP_OPEN
#define AVAPP_CTRL_DID_LIVE_OPEN            IJK_CTRL_DID_LIVE_OPEN

// Additional aliases for IJKAPP_ prefix
#define IJKAPP_CTRL_WILL_LIVE_OPEN          IJK_CTRL_WILL_LIVE_OPEN

// Application event messages for ff_ffplay.c compatibility
#define AVAPP_EVENT_IO_TRAFFIC              0x20001
#define AVAPP_EVENT_ASYNC_STATISTIC         0x20002
#define AVAPP_EVENT_ASYNC_READ_SPEED        0x20003

// HTTP event messages for IJKFFMoviePlayerController compatibility
#define AVAPP_EVENT_WILL_HTTP_OPEN          0x20004
#define AVAPP_EVENT_DID_HTTP_OPEN           0x20005
#define AVAPP_EVENT_WILL_HTTP_SEEK          0x20006
#define AVAPP_EVENT_DID_HTTP_SEEK           0x20007

// I/O Traffic structure for network statistics
typedef struct IJKAppIOTraffic {
    size_t size;
    int64_t bytes;
} IJKAppIOTraffic;

// HTTP Event structure for network monitoring
typedef struct IJKAppHttpEvent {
    size_t size;
    char url[4096];
    int64_t offset;
    int error;
    int http_code;
    int64_t filesize;
} IJKAppHttpEvent;

// Compatibility alias
#define AVAppIOTraffic IJKAppIOTraffic
#define AVAppTcpIOControl IJKAppIOControl
#define AVAppHttpEvent IJKAppHttpEvent

#ifdef __cplusplus
}
#endif

#endif /* IJK_APPLICATION_H */
