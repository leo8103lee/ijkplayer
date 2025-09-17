#ifndef IJKPLAYER_FFMPEG_COMPAT_H
#define IJKPLAYER_FFMPEG_COMPAT_H

/*
 * FFmpeg 7.1.2 Compatibility Layer for IJKPlayer
 * Handles API changes and provides backward compatibility macros
 */

#include <libavutil/version.h>
#include <libavcodec/version.h>
#include <libavformat/version.h>

/* FFmpeg version checks */
#if LIBAVUTIL_VERSION_INT < AV_VERSION_INT(59, 8, 100)
#error "FFmpeg 7.1.2 or later required"
#endif

/* API compatibility macros for FFmpeg 7.x */

/* Decoder API changes */
#if LIBAVCODEC_VERSION_INT >= AV_VERSION_INT(61, 3, 100)
#define IJK_USE_NEW_DECODE_API 1

/* Helper macro for new decode API */
#define IJK_DECODE_VIDEO(avctx, frame, pkt) \
    do { \
        int ret; \
        if ((ret = avcodec_send_packet(avctx, pkt)) < 0) { \
            av_log(NULL, AV_LOG_ERROR, "Error sending packet to decoder\n"); \
            break; \
        } \
        ret = avcodec_receive_frame(avctx, frame); \
        if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF) { \
            ret = 0; /* Not an error, just need more data */ \
        } \
    } while(0)

#else
/* Fallback to old API if somehow using older FFmpeg */
#define IJK_DECODE_VIDEO(avctx, frame, pkt) \
    avcodec_decode_video2(avctx, frame, got_frame, pkt)
#endif

/* Hardware acceleration compatibility */
#if LIBAVUTIL_VERSION_INT >= AV_VERSION_INT(59, 8, 100)
#define IJK_HWACCEL_AUTO AV_HWDEVICE_TYPE_NONE  /* Let FFmpeg choose */
#define IJK_HWACCEL_MEDIACODEC AV_HWDEVICE_TYPE_MEDIACODEC
#define IJK_HWACCEL_VIDEOTOOLBOX AV_HWDEVICE_TYPE_VIDEOTOOLBOX
#endif

/* Filter graph compatibility */
#if LIBAVFILTER_VERSION_INT >= AV_VERSION_INT(10, 1, 100)
#define IJK_FILTER_GRAPH_THREADSAFE 1
#endif

/* Format context improvements */
#if LIBAVFORMAT_VERSION_INT >= AV_VERSION_INT(61, 1, 100)
#define IJK_AVFORMAT_INIT_STRICT 1
#endif

/* Logging improvements in FFmpeg 7.x */
#define IJK_LOG_TRACE    AV_LOG_TRACE
#define IJK_LOG_DEBUG    AV_LOG_DEBUG  
#define IJK_LOG_VERBOSE  AV_LOG_VERBOSE
#define IJK_LOG_INFO     AV_LOG_INFO
#define IJK_LOG_WARNING  AV_LOG_WARNING
#define IJK_LOG_ERROR    AV_LOG_ERROR
#define IJK_LOG_FATAL    AV_LOG_FATAL

/* Memory management helpers */
#define IJK_FREEP(p) av_freep(p)
#define IJK_FREE(p) av_free(p)

/* Packet management for FFmpeg 7.x */
#define IJK_PACKET_ALLOC() av_packet_alloc()
#define IJK_PACKET_FREE(pkt) av_packet_free(pkt)
#define IJK_PACKET_UNREF(pkt) av_packet_unref(pkt)

#endif /* IJKPLAYER_FFMPEG_COMPAT_H */
