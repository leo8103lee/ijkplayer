/*
 * IJK Internal Compatibility Layer for FFmpeg 7.1.2
 * Copyright (c) 2025 Bilibili
 *
 * This file provides compatibility for internal FFmpeg APIs that were
 * removed or changed in FFmpeg 7.x but are still used by IJKPlayer.
 */

#ifndef IJK_INTERNAL_COMPAT_H
#define IJK_INTERNAL_COMPAT_H

#include "libavformat/avformat.h"
#include "libavformat/avio.h"
#include "libavutil/opt.h"
#include "libavcodec/avcodec.h"
#include "libswresample/swresample.h"
#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif

// Threading compatibility - FFmpeg 7.x moved thread utilities
#include <pthread.h>

// Interrupt callback compatibility
static inline int ff_check_interrupt(AVIOInterruptCB *cb)
{
    if (cb && cb->callback)
        return cb->callback(cb->opaque);
    return 0;
}

#define IJK_THREAD_TYPE pthread_t
#define IJK_MUTEX_TYPE pthread_mutex_t
#define IJK_COND_TYPE pthread_cond_t

// Thread function compatibility
static inline int ijk_thread_create(IJK_THREAD_TYPE *thread, void *(*start_routine)(void *), void *arg)
{
    return pthread_create(thread, NULL, start_routine, arg);
}

static inline int ijk_thread_join(IJK_THREAD_TYPE thread)
{
    return pthread_join(thread, NULL);
}

static inline int ijk_mutex_init(IJK_MUTEX_TYPE *mutex)
{
    return pthread_mutex_init(mutex, NULL);
}

static inline int ijk_mutex_destroy(IJK_MUTEX_TYPE *mutex)
{
    return pthread_mutex_destroy(mutex);
}

static inline int ijk_mutex_lock(IJK_MUTEX_TYPE *mutex)
{
    return pthread_mutex_lock(mutex);
}

static inline int ijk_mutex_unlock(IJK_MUTEX_TYPE *mutex)
{
    return pthread_mutex_unlock(mutex);
}

// AVIO internal compatibility
// These functions replace the missing avio_internal.h functionality

/**
 * Initialize AVIO buffer for custom I/O
 * Replacement for internal AVIO buffer management
 */
static inline int ijk_avio_alloc_buffer(AVIOContext **ctx, unsigned char *buffer,
                                       int buffer_size, int write_flag,
                                       void *opaque,
                                       int (*read_packet)(void *opaque, uint8_t *buf, int buf_size),
                                       int (*write_packet)(void *opaque, const uint8_t *buf, int buf_size),
                                       int64_t (*seek)(void *opaque, int64_t offset, int whence))
{
    *ctx = avio_alloc_context(buffer, buffer_size, write_flag, opaque,
                             (int (*)(void *, uint8_t *, int))read_packet,
                             (int (*)(void *, const uint8_t *, int))write_packet, seek);
    return *ctx ? 0 : -1;
}

// FLV format compatibility
// Basic FLV constants that were in the internal header
#define IJK_FLV_TAG_TYPE_AUDIO    8
#define IJK_FLV_TAG_TYPE_VIDEO    9
#define IJK_FLV_TAG_TYPE_META     18

// FLV tag type enumeration for compatibility
enum FlvTagType {
    FLV_TAG_TYPE_AUDIO = 8,
    FLV_TAG_TYPE_VIDEO = 9,
    FLV_TAG_TYPE_META  = 18,
};

// FIFO compatibility - AVFifoBuffer renamed to AVFifo in FFmpeg 7.x
#include "libavutil/fifo.h"
typedef AVFifo AVFifoBuffer;

// FIFO function compatibility
static inline AVFifoBuffer *av_fifo_alloc(unsigned int size)
{
    return av_fifo_alloc2(1, size, AV_FIFO_FLAG_AUTO_GROW);
}

static inline void av_fifo_freep(AVFifoBuffer **f)
{
    av_fifo_freep2(f);
}

static inline void av_fifo_reset(AVFifoBuffer *f)
{
    av_fifo_reset2(f);
}

static inline int av_fifo_size(AVFifoBuffer *f)
{
    return (int)av_fifo_can_read(f);
}

static inline int av_fifo_space(AVFifoBuffer *f)
{
    return (int)av_fifo_can_write(f);
}

static inline int av_fifo_generic_read(AVFifoBuffer *f, void *dest, int buf_size, void (*func)(void*, void*, int))
{
    return av_fifo_read(f, dest, buf_size);
}

static inline int av_fifo_generic_write(AVFifoBuffer *f, void *src, int size, int (*func)(void*, void*, int))
{
    return av_fifo_write(f, src, size);
}

static inline int av_fifo_generic_peek_at(AVFifoBuffer *f, void *dest, int offset, int buf_size, void (*func)(void*, void*, int))
{
    return av_fifo_peek(f, dest, buf_size, offset);
}

static inline void av_fifo_drain(AVFifoBuffer *f, int size)
{
    av_fifo_drain2(f, size);
}

// Format registration compatibility - these functions were removed in FFmpeg 7.x
// We provide stub implementations for backward compatibility
static inline AVInputFormat *av_iformat_next(AVInputFormat *f)
{
    // In FFmpeg 7.x, format iteration is no longer supported this way
    // Return NULL to terminate loops
    return NULL;
}

static inline void av_register_input_format(AVInputFormat *format)
{
    // In FFmpeg 7.x, formats are auto-registered
    // This function is no longer needed but we keep it for compatibility
}

static inline void av_register_all(void)
{
    // In FFmpeg 7.x, this function is deprecated and does nothing
    // All formats and codecs are automatically registered
}

// ID3v2 compatibility stubs
// These provide minimal functionality for ID3v2 operations
static inline int ijk_id3v2_tag_size(const uint8_t *buf, int len)
{
    // Minimal ID3v2 size calculation
    if (len < 10 || memcmp(buf, "ID3", 3))
        return 0;

    // Calculate size from syncsafe integer
    int size = ((buf[6] & 0x7f) << 21) |
               ((buf[7] & 0x7f) << 14) |
               ((buf[8] & 0x7f) << 7) |
               (buf[9] & 0x7f);

    return size + 10; // Include header size
}

// Error code compatibility
#ifndef AVERROR_EXIT
#define AVERROR_EXIT AVERROR(EIO)
#endif

#ifndef AVERROR_EXTERNAL
#define AVERROR_EXTERNAL AVERROR(EIO)
#endif

// AVC (H.264) format compatibility
// Basic AVC utilities that replace libavformat/avc.h

#define IJK_AVC_PROFILE_BASELINE    66
#define IJK_AVC_PROFILE_MAIN        77
#define IJK_AVC_PROFILE_HIGH        100

// Simplified AVC parsing functions
static inline int ijk_avc_parse_nal_units_buf(const uint8_t *buf_in, uint8_t **buf, int *size)
{
    // Minimal implementation for AVC parsing
    if (!buf_in || !buf || !size)
        return -1;

    // For now, just pass through - this would need proper NALU parsing
    // in a production implementation
    *buf = (uint8_t *)buf_in;
    return 0;
}

static inline int ijk_avc_parse_nal_units(AVIOContext *pb, const uint8_t *buf_in, int size)
{
    // Simplified NALU parsing for VideoToolbox compatibility
    if (!buf_in || size <= 0)
        return -1;

    // Basic NALU detection and parsing
    const uint8_t *p = buf_in;
    const uint8_t *end = buf_in + size;

    while (p < end - 4) {
        if (p[0] == 0 && p[1] == 0 && (p[2] == 1 || (p[2] == 0 && p[3] == 1))) {
            // Found start code, write it to AVIO if needed
            if (pb) {
                int start_code_size = (p[2] == 1) ? 3 : 4;
                avio_write(pb, p, start_code_size);
                p += start_code_size;
            }
        } else {
            p++;
        }
    }

    return 0;
}

// URLContext and ffurl compatibility for FFmpeg 7.1.2
// These functions replace the internal URL handling that was moved/changed

// Forward declarations
typedef struct URLContext URLContext;
typedef struct URLProtocol URLProtocol;

// Complete URLContext and URLProtocol definitions for compatibility
struct URLProtocol {
    const char *name;
    int (*url_open2)(URLContext *h, const char *url, int flags, AVDictionary **options);
    int (*url_open)(URLContext *h, const char *url, int flags);
    int (*url_read)(URLContext *h, unsigned char *buf, int size);
    int (*url_write)(URLContext *h, const unsigned char *buf, int size);
    int64_t (*url_seek)(URLContext *h, int64_t pos, int whence);
    int (*url_close)(URLContext *h);
    int (*url_read_pause)(URLContext *h, int pause);
    int64_t (*url_read_seek)(URLContext *h, int stream_index, int64_t timestamp, int flags);
    int (*url_get_file_handle)(URLContext *h);
    int (*url_get_multi_file_handle)(URLContext *h, int **handles, int *numhandles);
    int (*url_shutdown)(URLContext *h, int flags);
    const AVClass *priv_data_class;
    int priv_data_size;
    int flags;
    int (*url_check)(URLContext *h, int mask);
    int (*url_open_dir)(URLContext *h);
    int (*url_read_dir)(URLContext *h, AVIODirEntry **next);
    int (*url_close_dir)(URLContext *h);
    int (*url_delete)(URLContext *h);
    int (*url_move)(URLContext *h_src, URLContext *h_dst);
    const char *default_whitelist;
};

struct URLContext {
    const AVClass *av_class;
    const struct URLProtocol *prot;
    void *priv_data;
    char *filename;
    int flags;
    int max_packet_size;
    int is_streamed;
    int is_connected;
    AVIOInterruptCB interrupt_callback;
    int64_t rw_timeout;
    const char *protocol_whitelist;
    const char *protocol_blacklist;
    int min_packet_size;
};

// ffurl function stubs - these need to be implemented or mapped to new FFmpeg 7.1.2 APIs
static inline int ffurl_open_whitelist(URLContext **puc, const char *filename, int flags,
                                      const AVIOInterruptCB *int_cb, AVDictionary **options,
                                      const char *whitelist, const char *blacklist, URLContext *parent)
{
    // TODO: Map to appropriate FFmpeg 7.1.2 avio functions
    return AVERROR(ENOSYS);
}

static inline int ffurl_read(URLContext *h, unsigned char *buf, int size)
{
    // TODO: Map to appropriate FFmpeg 7.1.2 avio functions  
    return AVERROR(ENOSYS);
}

static inline int64_t ffurl_seek(URLContext *h, int64_t pos, int whence)
{
    // TODO: Map to appropriate FFmpeg 7.1.2 avio functions
    return AVERROR(ENOSYS);
}

static inline int ffurl_close(URLContext *h)
{
    // TODO: Map to appropriate FFmpeg 7.1.2 avio functions
    return AVERROR(ENOSYS);
}

static inline int64_t ffurl_size(URLContext *h)
{
    // TODO: Map to appropriate FFmpeg 7.1.2 avio functions
    return AVERROR(ENOSYS);
}

static inline int ffurl_write(URLContext *h, const unsigned char *buf, int size)
{
    // TODO: Map to appropriate FFmpeg 7.1.2 avio functions
    return AVERROR(ENOSYS);
}

static inline int ffurl_closep(URLContext **h)
{
    if (h && *h) {
        int ret = ffurl_close(*h);
        *h = NULL;
        return ret;
    }
    return 0;
}

// Additional ffurl functions needed for ijklas.c
static inline int ffurl_read_complete(URLContext *h, unsigned char *buf, int size)
{
    return ffurl_read(h, buf, size);
}

// AVIO internal functions compatibility
static inline int ffio_init_context(AVIOContext *s, unsigned char *buffer, int buffer_size,
                                    int write_flag, void *opaque,
                                    int (*read_packet)(void *opaque, uint8_t *buf, int buf_size),
                                    int (*write_packet)(void *opaque, uint8_t *buf, int buf_size),
                                    int64_t (*seek)(void *opaque, int64_t offset, int whence))
{
    AVIOContext *ctx = avio_alloc_context(buffer, buffer_size, write_flag, opaque,
                                         read_packet, (int (*)(void *, const uint8_t *, int))write_packet, seek);
    if (!ctx)
        return AVERROR(ENOMEM);

    memcpy(s, ctx, sizeof(AVIOContext));
    av_free(ctx);
    return 0;
}

// avpriv functions compatibility
static inline void avpriv_set_pts_info(AVStream *s, int pts_wrap_bits, unsigned int pts_num, unsigned int pts_den)
{
    // In FFmpeg 7.x, this is simplified
    s->time_base.num = pts_num;
    s->time_base.den = pts_den;
}

// Error to string conversion compatibility
static inline char* ijk_av_err2str(int errnum) {
    static char error_buffer[AV_ERROR_MAX_STRING_SIZE];
    return av_make_error_string(error_buffer, AV_ERROR_MAX_STRING_SIZE, errnum);
}

// Codec compatibility functions
static inline AVRational av_codec_get_pkt_timebase(const AVCodecContext *avctx)
{
    return avctx->pkt_timebase;
}

// Channel layout compatibility functions  
static inline int av_get_channel_layout_nb_channels(uint64_t channel_layout)
{
    return av_popcount64(channel_layout);
}

static inline uint64_t av_get_default_channel_layout(int nb_channels)
{
    switch (nb_channels) {
    case 1: return AV_CH_LAYOUT_MONO;
    case 2: return AV_CH_LAYOUT_STEREO;
    case 3: return AV_CH_LAYOUT_2POINT1;
    case 4: return AV_CH_LAYOUT_QUAD;
    case 5: return AV_CH_LAYOUT_5POINT0;
    case 6: return AV_CH_LAYOUT_5POINT1;
    case 7: return AV_CH_LAYOUT_6POINT1;
    case 8: return AV_CH_LAYOUT_7POINT1;
    default: return 0;
    }
}

// SwrContext compatibility - swr_alloc_set_opts was removed in favor of swr_alloc_set_opts2
static inline struct SwrContext *swr_alloc_set_opts(struct SwrContext *s,
                                                   int64_t out_ch_layout, enum AVSampleFormat out_sample_fmt, int out_sample_rate,
                                                   int64_t in_ch_layout,  enum AVSampleFormat  in_sample_fmt, int  in_sample_rate,
                                                   int log_offset, void *log_ctx)
{
    if (!s)
        s = swr_alloc();
    if (!s)
        return NULL;
        
    // Convert channel layouts to new format
    AVChannelLayout out_layout, in_layout;
    av_channel_layout_from_mask(&out_layout, out_ch_layout);
    av_channel_layout_from_mask(&in_layout, in_ch_layout);
    
    // Set options using new API
    av_opt_set_chlayout(s, "out_channel_layout", &out_layout, 0);
    av_opt_set_chlayout(s, "in_channel_layout", &in_layout, 0);
    av_opt_set_int(s, "out_sample_rate", out_sample_rate, 0);
    av_opt_set_int(s, "in_sample_rate", in_sample_rate, 0);
    av_opt_set_sample_fmt(s, "out_sample_fmt", out_sample_fmt, 0);
    av_opt_set_sample_fmt(s, "in_sample_fmt", in_sample_fmt, 0);
    
    av_channel_layout_uninit(&out_layout);
    av_channel_layout_uninit(&in_layout);
    
    return s;
}

// Encoding compatibility - avcodec_encode_video2 was removed in FFmpeg 6.0
static inline int avcodec_encode_video2(AVCodecContext *avctx, AVPacket *avpkt,
                                       const AVFrame *frame, int *got_packet_ptr)
{
    int ret;
    
    if (got_packet_ptr)
        *got_packet_ptr = 0;
        
    ret = avcodec_send_frame(avctx, frame);
    if (ret < 0)
        return ret;
        
    ret = avcodec_receive_packet(avctx, avpkt);
    if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF) {
        return 0;
    } else if (ret < 0) {
        return ret;
    }
    
    if (got_packet_ptr)
        *got_packet_ptr = 1;
        
    return 0;
}

// Additional codec compatibility functions
static inline void av_codec_set_pkt_timebase(AVCodecContext *avctx, AVRational val)
{
    avctx->pkt_timebase = val;
}

static inline int av_codec_get_max_lowres(const AVCodec *codec)
{
    // In FFmpeg 7.x, max_lowres is not a direct field
    // Return 0 for compatibility
    return 0;
}

static inline void av_codec_set_lowres(AVCodecContext *avctx, int val)
{
    // In FFmpeg 7.x, lowres is not supported the same way
    // This is a no-op for compatibility
}

// Channel layout conversion compatibility for FFmpeg 7.x
static inline uint64_t channel_layout_from_ch_layout(const AVChannelLayout *ch_layout)
{
    if (ch_layout->order == AV_CHANNEL_ORDER_NATIVE && ch_layout->nb_channels <= 64) {
        return ch_layout->u.mask;
    }
    // Fall back to default layout for this channel count
    return av_get_default_channel_layout(ch_layout->nb_channels);
}

// Frame channel layout compatibility
static inline uint64_t get_frame_channel_layout(const AVFrame *frame)
{
    return channel_layout_from_ch_layout(&frame->ch_layout);
}

// Forward declaration for filter compatibility
#if CONFIG_AVFILTER
struct AVFilterContext;
// Buffersink compatibility functions  
static inline int av_buffersink_get_channels(const struct AVFilterContext *ctx)
{
    // This is a stub implementation for compatibility
    // In ff_ffplay.c, this should be handled differently with proper filter context
    return 2; // Default to stereo
}
#endif

// Audio open function parameter compatibility
static inline uint64_t get_valid_channel_layout(uint64_t channel_layout, int channels)
{
    if (channel_layout && av_get_channel_layout_nb_channels(channel_layout) == channels)
        return channel_layout;
    else
        return av_get_default_channel_layout(channels);
}

// SwrContext parameter setting compatibility for FFmpeg 7.x
static inline int swr_set_channel_layout(struct SwrContext *s, int64_t out_ch_layout, int64_t in_ch_layout)
{
    AVChannelLayout out_layout, in_layout;
    av_channel_layout_from_mask(&out_layout, out_ch_layout);
    av_channel_layout_from_mask(&in_layout, in_ch_layout);
    
    int ret = 0;
    ret |= av_opt_set_chlayout(s, "out_channel_layout", &out_layout, 0);
    ret |= av_opt_set_chlayout(s, "in_channel_layout", &in_layout, 0);
    
    av_channel_layout_uninit(&out_layout);
    av_channel_layout_uninit(&in_layout);
    
    return ret;
}

// Registration compatibility functions
static inline void avcodec_register_all(void)
{
    // In FFmpeg 7.x, all codecs are automatically registered
    // This function is no longer needed but we keep it for compatibility
}

// Lock manager compatibility - removed in FFmpeg 7.x
// Define AVLockOp for compatibility
enum AVLockOp {
    AV_LOCK_CREATE = 0,  ///< Create a mutex
    AV_LOCK_OBTAIN,      ///< Lock the mutex
    AV_LOCK_RELEASE,     ///< Unlock the mutex
    AV_LOCK_DESTROY,     ///< Free mutex resources
};

static inline int av_lockmgr_register(int (*cb)(void **mutex, enum AVLockOp op))
{
    // Lock manager functionality was removed in FFmpeg 7.x
    // Return 0 for compatibility
    return 0;
}

// Dictionary helper for pointer storage/retrieval
static inline int av_dict_set_intptr(AVDictionary **pm, const char *key, uintptr_t value, int flags)
{
    char str[32];
    snprintf(str, sizeof(str), "%p", (void *)value);
    return av_dict_set(pm, key, str, flags);
}

static inline uintptr_t av_dict_strtoptr(const char *str)
{
    if (!str || !*str)
        return 0;

    uintptr_t ptr;
    if (sscanf(str, "%p", (void **)&ptr) == 1)
        return ptr;

    return 0;
}

// VideoToolBox compatibility functions for FFmpeg 7.1.2
// These functions were deprecated and removed in FFmpeg 7.x

// Packet flags compatibility (these were removed)
#ifndef AV_PKT_FLAG_NEW_SEG
#define AV_PKT_FLAG_NEW_SEG                 0x0010  // Segment boundary flag for streaming
#endif

// Deprecated function compatibility for VideoToolBox
static inline int av_copy_packet(AVPacket *dst, const AVPacket *src)
{
    return av_packet_ref(dst, src);
}

static inline int av_packet_split_side_data(AVPacket *pkt)
{
    // In FFmpeg 7.x this functionality is handled internally
    return 0;
}

// Deprecated decode function compatibility
static inline int avcodec_decode_video2(AVCodecContext *avctx, AVFrame *picture,
                                       int *got_picture_ptr, const AVPacket *avpkt)
{
    int ret = avcodec_send_packet(avctx, avpkt);
    if (ret < 0)
        return ret;

    ret = avcodec_receive_frame(avctx, picture);
    if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF) {
        *got_picture_ptr = 0;
        return avpkt ? avpkt->size : 0;
    } else if (ret < 0) {
        return ret;
    }

    *got_picture_ptr = 1;
    return avpkt ? avpkt->size : 0;
}

// ISOM compatibility for VideoToolBox
static inline int ff_isom_write_avcc(AVIOContext *pb, const uint8_t *data, int len)
{
    // Write AVCC (avcC atom) header for H.264 extradata
    if (len < 6 || !data)
        return AVERROR_INVALIDDATA;

    avio_w8(pb, 1);      // configurationVersion
    avio_w8(pb, data[1]); // profile indication
    avio_w8(pb, data[2]); // profile compatibility
    avio_w8(pb, data[3]); // level indication
    avio_w8(pb, 0xff);    // length size minus one (4 bytes)
    avio_w8(pb, 0xe1);    // number of SPS (1)

    // Write remaining data
    avio_write(pb, data + 4, len - 4);

    return 0;
}

// Function alias for AVC parser
#define ff_avc_parse_nal_units ijk_avc_parse_nal_units

#ifdef __cplusplus
}
#endif

#endif /* IJK_INTERNAL_COMPAT_H */
