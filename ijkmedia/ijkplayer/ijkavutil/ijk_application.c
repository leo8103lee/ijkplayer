/*
 * IJK Application Context for FFmpeg 7.1.2 compatibility
 * Copyright (c) 2025 Bilibili
 * Copyright (c) 2025 Zhang Rui <bbcallen@gmail.com>
 */

#include "ijk_application.h"
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include "libavutil/log.h"
#include "libavutil/mem.h"

// Default event handler that can be overridden
static int default_app_event_handler(IJKApplicationContext *ctx, int message, void *data, size_t data_size)
{
    // Default implementation - just log and return success
    av_log(NULL, AV_LOG_DEBUG, "IJK app event: message=0x%x, size=%zu\n", message, data_size);
    return 0;
}

int ijk_application_open(IJKApplicationContext **ps, void *opaque)
{
    IJKApplicationContext *ctx = NULL;

    if (!ps) {
        av_log(NULL, AV_LOG_ERROR, "ijk_application_open: invalid parameters\n");
        return -1;
    }

    ctx = av_mallocz(sizeof(IJKApplicationContext));
    if (!ctx) {
        av_log(NULL, AV_LOG_ERROR, "ijk_application_open: out of memory\n");
        return -1;
    }

    // Initialize context
    ctx->opaque = opaque;
    ctx->func_on_app_event = default_app_event_handler;
    ctx->ref_count = 1;
    ctx->last_high_water_mark_in_ms = 0;

    *ps = ctx;
    av_log(NULL, AV_LOG_DEBUG, "ijk_application_open: created context %p\n", ctx);
    return 0;
}

void ijk_application_closep(IJKApplicationContext **ps)
{
    IJKApplicationContext *ctx;

    if (!ps || !*ps)
        return;

    ctx = *ps;

    // Decrement reference count
    ctx->ref_count--;

    if (ctx->ref_count <= 0) {
        av_log(NULL, AV_LOG_DEBUG, "ijk_application_closep: freeing context %p\n", ctx);

        // Clear sensitive data
        memset(ctx, 0, sizeof(IJKApplicationContext));

        // Free memory
        av_free(ctx);
    }

    *ps = NULL;
}

int ijk_application_on_io_control(IJKApplicationContext *h, int message, void *data)
{
    IJKAppIOControl *control;

    if (!h) {
        av_log(NULL, AV_LOG_ERROR, "ijk_application_on_io_control: invalid context\n");
        return -1;
    }

    if (!data) {
        av_log(NULL, AV_LOG_WARNING, "ijk_application_on_io_control: no data provided\n");
        return 0;
    }

    control = (IJKAppIOControl *)data;

    // Validate control structure
    if (control->size < sizeof(IJKAppIOControl)) {
        av_log(NULL, AV_LOG_ERROR, "ijk_application_on_io_control: invalid control size\n");
        return -1;
    }

    // Log the I/O control operation
    av_log(NULL, AV_LOG_DEBUG,
           "ijk_application_on_io_control: message=0x%x, url=%s, segment=%d\n",
           message, control->url[0] ? control->url : "(empty)", control->segment_index);

    // Call application event handler if available
    if (h->func_on_app_event) {
        return h->func_on_app_event(h, message, data, sizeof(IJKAppIOControl));
    }

    return 0;
}

int ijk_application_on_async_statistic(IJKApplicationContext *h, IJKAppAsyncStatistic *data)
{
    if (!h || !data) {
        return -1;
    }

    // Validate data structure
    if (data->size < sizeof(IJKAppAsyncStatistic)) {
        av_log(NULL, AV_LOG_ERROR, "ijk_application_on_async_statistic: invalid data size\n");
        return -1;
    }

    av_log(NULL, AV_LOG_DEBUG,
           "ijk_application_on_async_statistic: buf_backwards=%lld, buf_forwards=%lld, capacity=%lld\n",
           (long long)data->buf_backwards, (long long)data->buf_forwards, (long long)data->buf_capacity);

    // Call application event handler if available
    if (h->func_on_app_event) {
        return h->func_on_app_event(h, 0x20001, data, sizeof(IJKAppAsyncStatistic));
    }

    return 0;
}

int ijk_application_on_async_read_speed(IJKApplicationContext *h, IJKAppAsyncReadSpeed *data)
{
    if (!h || !data) {
        return -1;
    }

    // Validate data structure
    if (data->size < sizeof(IJKAppAsyncReadSpeed)) {
        av_log(NULL, AV_LOG_ERROR, "ijk_application_on_async_read_speed: invalid data size\n");
        return -1;
    }

    av_log(NULL, AV_LOG_DEBUG,
           "ijk_application_on_async_read_speed: io_bytes=%lld, elapsed=%lld ms, speed=%lld B/s\n",
           (long long)data->io_bytes, (long long)data->elapsed_milli, (long long)data->bytes_per_sec);

    // Update high water mark for flow control
    if (data->elapsed_milli > 0) {
        h->last_high_water_mark_in_ms = data->elapsed_milli;
    }

    // Call application event handler if available
    if (h->func_on_app_event) {
        return h->func_on_app_event(h, 0x20002, data, sizeof(IJKAppAsyncReadSpeed));
    }

    return 0;
}