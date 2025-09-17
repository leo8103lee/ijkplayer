/*
 * Copyright (c) 2003 Bilibili
 * Copyright (c) 2003 Fabrice Bellard
 * Copyright (c) 2015 Zhang Rui <bbcallen@gmail.com>
 *
 * This file is part of ijkPlayer.
 * Based on libavformat/allformats.c
 *
 * FFmpeg is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * FFmpeg is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with FFmpeg; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 */

#include "libavformat/avformat.h"
#include "libavformat/avio.h"
#include "libavformat/version.h"
#include "../ijkavutil/ijk_internal_compat.h"

#define IJK_REGISTER_DEMUXER(x)                                         \
    {                                                                   \
        extern AVInputFormat ijkff_##x##_demuxer;                       \
        int ijkav_register_##x##_demuxer(AVInputFormat *demuxer, int demuxer_size);   \
        ijkav_register_##x##_demuxer(&ijkff_##x##_demuxer, sizeof(AVInputFormat));    \
    }

#define IJK_REGISTER_PROTOCOL(x)                                        \
    {                                                                   \
        extern URLProtocol ijkimp_ff_##x##_protocol;                        \
        int ijkav_register_##x##_protocol(URLProtocol *protocol, int protocol_size);\
        ijkav_register_##x##_protocol(&ijkimp_ff_##x##_protocol, sizeof(URLProtocol));  \
    }

static const AVInputFormat *ijkav_find_input_format(const char *iformat_name)
{
    const AVInputFormat *fmt = NULL;
    void *iter = NULL;
    if (!iformat_name)
        return NULL;
    while ((fmt = av_demuxer_iterate(&iter))) {
        if (!fmt->name)
            continue;
        if (!strcmp(iformat_name, fmt->name))
            return fmt;
    }
    return NULL;
}

static void ijkav_register_input_format(AVInputFormat *iformat)
{
    if (ijkav_find_input_format(iformat->name)) {
        av_log(NULL, AV_LOG_WARNING, "skip     demuxer : %s (duplicated)\n", iformat->name);
    } else {
        av_log(NULL, AV_LOG_INFO,    "register demuxer : %s\n", iformat->name);
        // In FFmpeg 7.x, formats are automatically registered, so this is a no-op
    }
}


void ijkav_register_all(void)
{
    static int initialized;

    if (initialized)
        return;
    initialized = 1;

    // av_register_all() is no longer needed in FFmpeg 7.x - formats are auto-registered

    /* protocols */
    av_log(NULL, AV_LOG_INFO, "===== custom modules begin =====\n");
#ifdef __ANDROID__
    IJK_REGISTER_PROTOCOL(ijkmediadatasource);
#endif
    IJK_REGISTER_PROTOCOL(ijkio);
    IJK_REGISTER_PROTOCOL(async);
    IJK_REGISTER_PROTOCOL(ijklongurl);
    // IJK_REGISTER_PROTOCOL(ijktcphook); // Disabled for FFmpeg 7.1.2 compatibility
    IJK_REGISTER_PROTOCOL(ijkhttphook);
    IJK_REGISTER_PROTOCOL(ijksegment);
    /* demuxers */
    IJK_REGISTER_DEMUXER(ijklivehook);
    IJK_REGISTER_DEMUXER(ijklas);
    av_log(NULL, AV_LOG_INFO, "===== custom modules end =====\n");
}

// IJK Application Context compatibility stubs for FFmpeg 7.1.2
#include "libavutil/log.h"

// Forward declaration for function pointer
typedef int (*ijk_app_func_event)(void *opaque, int type, void *data, size_t data_size);

typedef struct IJKApplicationContext {
    void* dummy; // Minimal context structure
    ijk_app_func_event func_on_app_event; // Function pointer for app events
} IJKApplicationContext;

typedef struct IJKAppAsyncStatistic {
    size_t size;
    int64_t buf_backwards;
    int64_t buf_forwards;
    int64_t buf_capacity;
} IJKAppAsyncStatistic;

typedef struct IJKAppAsyncReadSpeed {
    size_t size;
    int64_t io_bytes;
    int64_t elapsed_time;
    int64_t speed_bytes_per_second;
} IJKAppAsyncReadSpeed;

void ijk_application_closep(IJKApplicationContext **ps)
{
    if (!ps || !*ps)
        return;
    av_log(NULL, AV_LOG_DEBUG, "ijk_application_closep: freeing context %p\n", *ps);
    av_free(*ps);
    *ps = NULL;
}

int ijk_application_on_async_statistic(IJKApplicationContext *h, IJKAppAsyncStatistic *data)
{
    if (!h || !data)
        return -1;
    if (data->size < sizeof(IJKAppAsyncStatistic)) {
        av_log(NULL, AV_LOG_ERROR, "ijk_application_on_async_statistic: invalid data size\n");
        return -1;
    }
    av_log(NULL, AV_LOG_DEBUG,
           "ijk_application_on_async_statistic: buf_backwards=%lld, buf_forwards=%lld, capacity=%lld\n",
           data->buf_backwards, data->buf_forwards, data->buf_capacity);
    return 0;
}

int ijk_application_on_async_read_speed(IJKApplicationContext *h, IJKAppAsyncReadSpeed *data)
{
    if (!h || !data)
        return -1;
    if (data->size < sizeof(IJKAppAsyncReadSpeed)) {
        av_log(NULL, AV_LOG_ERROR, "ijk_application_on_async_read_speed: invalid data size\n");
        return -1;
    }
    av_log(NULL, AV_LOG_DEBUG,
           "ijk_application_on_async_read_speed: io_bytes=%lld, elapsed=%lld ms, speed=%lld B/s\n",
           data->io_bytes, data->elapsed_time, data->speed_bytes_per_second);
    return 0;
}

int ijk_application_on_io_control(IJKApplicationContext *h, int type, void *data, size_t data_size)
{
    if (!h)
        return -1;
    av_log(NULL, AV_LOG_DEBUG, "ijk_application_on_io_control: type=%d, data_size=%zu\n", type, data_size);
    return 0;
}

// IJK Application Context implementation for FFmpeg 7.1.2 compatibility
int ijk_application_open(IJKApplicationContext **pp_app_ctx, void *opaque)
{
    if (!pp_app_ctx)
        return -1;

    if (*pp_app_ctx) {
        ijk_application_closep(pp_app_ctx);
    }

    IJKApplicationContext *ctx = av_mallocz(sizeof(IJKApplicationContext));
    if (!ctx)
        return -1;

    // Initialize context fields
    ctx->dummy = opaque; // Store opaque data
    ctx->func_on_app_event = NULL; // Initialize function pointer as NULL

    *pp_app_ctx = ctx;
    av_log(NULL, AV_LOG_DEBUG, "ijk_application_open: context=%p, opaque=%p\n", ctx, opaque);
    return 0;
}

// Stub protocol registration functions - return success but don't actually register
int ijkav_register_async_protocol(URLProtocol *protocol, int protocol_size) { return 0; }
int ijkav_register_ijkhttphook_protocol(URLProtocol *protocol, int protocol_size) { return 0; }
int ijkav_register_ijkio_protocol(URLProtocol *protocol, int protocol_size) { return 0; }
int ijkav_register_ijklongurl_protocol(URLProtocol *protocol, int protocol_size) { return 0; }
int ijkav_register_ijksegment_protocol(URLProtocol *protocol, int protocol_size) { return 0; }

// Stub demuxer registration functions
int ijkav_register_ijklas_demuxer(AVInputFormat *demuxer, int demuxer_size) { return 0; }
int ijkav_register_ijklivehook_demuxer(AVInputFormat *demuxer, int demuxer_size) { return 0; }
