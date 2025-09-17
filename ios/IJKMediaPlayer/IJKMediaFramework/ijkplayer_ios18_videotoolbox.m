//
// ijkplayer_ios18_videotoolbox.m
// iOS 18 VideoToolbox Implementation  
//

#import "ijkplayer_ios18_videotoolbox.h"
#import <os/log.h>

static os_log_t ijkVT_log(void) {
    static os_log_t log;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        log = os_log_create("com.ijkplayer.videotoolbox", "ios18");
    });
    return log;
}

OSStatus ijkVT_InitializeForIOS18(IJKVideoToolboxContext *context, 
                                 int width, int height,
                                 CMVideoCodecType codecType) {
    if (!context) return kVTParameterErr;
    
    memset(context, 0, sizeof(IJKVideoToolboxContext));
    
    OSStatus status;
    
    // Create format description
    status = CMVideoFormatDescriptionCreate(kCFAllocatorDefault,
                                          codecType,
                                          width, height,
                                          NULL,
                                          &context->formatDesc);
    if (status != noErr) {
        os_log_error(ijkVT_log(), "Failed to create format description: %d", status);
        return status;
    }
    
    // Create decoder configuration
    context->decoderConfig = ijkVT_CreateIOS18DecoderConfig(width, height, codecType);
    
    // Create pixel buffer attributes
    context->destinationPixelBufferAttributes = ijkVT_CreateIOS18PixelBufferAttributes(width, height);
    
    context->useHardwareAcceleration = YES;
    context->enableHDRSupport = ijkVT_SupportsHDROnIOS18();
    
    os_log_info(ijkVT_log(), "VideoToolbox initialized for iOS 18: %dx%d, codec: %d", 
                width, height, codecType);
    
    return noErr;
}

OSStatus ijkVT_ConfigureIOS18Properties(IJKVideoToolboxContext *context) {
    if (!context || !context->session) return kVTParameterErr;
    
    OSStatus status = noErr;
    
    if (@available(iOS 18.0, *)) {
        // Enable hardware acceleration
        status = VTSessionSetProperty(context->session,
                                    kVTDecompressionPropertyKey_UsingHardwareAcceleratedVideoDecoder,
                                    kCFBooleanTrue);
        if (status != noErr) {
            os_log_error(ijkVT_log(), "Failed to enable hardware acceleration: %d", status);
        }
        
        // Configure real-time decoding
        status = VTSessionSetProperty(context->session,
                                    kVTDecompressionPropertyKey_RealTime,
                                    kCFBooleanTrue);
        if (status != noErr) {
            os_log_error(ijkVT_log(), "Failed to enable real-time decoding: %d", status);
        }
        
        // Enable HDR support if available
        if (context->enableHDRSupport) {
            CFStringRef hdrKey = CFSTR("EnableHDRSupport");
            status = VTSessionSetProperty(context->session, hdrKey, kCFBooleanTrue);
            if (status != noErr) {
                os_log_info(ijkVT_log(), "HDR support configuration failed (may not be available): %d", status);
            }
        }
        
        os_log_info(ijkVT_log(), "iOS 18 VideoToolbox properties configured");
    }
    
    return status;
}

BOOL ijkVT_SupportsHDROnIOS18(void) {
    if (@available(iOS 18.0, *)) {
        // Check for HDR10 and Dolby Vision support
        CFArrayRef supportedTypes = NULL;
        OSStatus status = VTCopyVideoDecoderList(NULL, &supportedTypes);
        
        if (status == noErr && supportedTypes) {
            CFIndex count = CFArrayGetCount(supportedTypes);
            for (CFIndex i = 0; i < count; i++) {
                CFDictionaryRef decoderInfo = CFArrayGetValueAtIndex(supportedTypes, i);
                CFStringRef codecName = CFDictionaryGetValue(decoderInfo, 
                                                           kVTVideoDecoderList_DisplayName);
                if (codecName) {
                    CFStringRef codecStr = CFStringCreateCopy(kCFAllocatorDefault, codecName);
                    if (CFStringFind(codecStr, CFSTR("HEVC"), 0).location != kCFNotFound ||
                        CFStringFind(codecStr, CFSTR("HDR"), 0).location != kCFNotFound) {
                        CFRelease(codecStr);
                        CFRelease(supportedTypes);
                        return YES;
                    }
                    CFRelease(codecStr);
                }
            }
            CFRelease(supportedTypes);
        }
    }
    return NO;
}

CFDictionaryRef ijkVT_CreateIOS18DecoderConfig(int width, int height, 
                                              CMVideoCodecType codecType) {
    CFMutableDictionaryRef config = CFDictionaryCreateMutable(
        kCFAllocatorDefault, 0,
        &kCFTypeDictionaryKeyCallBacks,
        &kCFTypeDictionaryValueCallBacks);
    
    // Hardware acceleration preference
    CFDictionarySetValue(config, 
                        kVTVideoDecoderSpecification_EnableHardwareAcceleratedVideoDecoder,
                        kCFBooleanTrue);
    
    if (@available(iOS 18.0, *)) {
        // iOS 18 specific optimizations
        CFDictionarySetValue(config,
                            kVTVideoDecoderSpecification_RequireHardwareAcceleratedVideoDecoder,
                            kCFBooleanFalse);  // Allow software fallback
    }
    
    return config;
}

void ijkVT_CleanupIOS18Session(IJKVideoToolboxContext *context) {
    if (!context) return;
    
    if (context->session) {
        VTDecompressionSessionInvalidate(context->session);
        CFRelease(context->session);
        context->session = NULL;
    }
    
    if (context->formatDesc) {
        CFRelease(context->formatDesc);
        context->formatDesc = NULL;
    }
    
    if (context->decoderConfig) {
        CFRelease(context->decoderConfig);
        context->decoderConfig = NULL;
    }
    
    if (context->destinationPixelBufferAttributes) {
        CFRelease(context->destinationPixelBufferAttributes);
        context->destinationPixelBufferAttributes = NULL;
    }
    
    os_log_info(ijkVT_log(), "iOS 18 VideoToolbox session cleaned up");
}
