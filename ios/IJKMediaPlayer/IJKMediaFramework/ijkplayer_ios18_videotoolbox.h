//
// ijkplayer_ios18_videotoolbox.h  
// iOS 18 VideoToolbox Integration
//

#ifndef ijkplayer_ios18_videotoolbox_h
#define ijkplayer_ios18_videotoolbox_h

#import <VideoToolbox/VideoToolbox.h>
#import <CoreFoundation/CoreFoundation.h>
#import <CoreVideo/CoreVideo.h>

#ifdef __cplusplus
extern "C" {
#endif

// iOS 18 VideoToolbox session configuration
typedef struct {
    VTDecompressionSessionRef session;
    CMVideoFormatDescriptionRef formatDesc;
    VTDecompressionOutputCallbackRecord callback;
    CFDictionaryRef decoderConfig;
    CFDictionaryRef destinationPixelBufferAttributes;
    BOOL useHardwareAcceleration;
    BOOL enableHDRSupport;
} IJKVideoToolboxContext;

// Initialize VideoToolbox for iOS 18
OSStatus ijkVT_InitializeForIOS18(IJKVideoToolboxContext *context, 
                                 int width, int height,
                                 CMVideoCodecType codecType);

// Configure iOS 18 specific properties  
OSStatus ijkVT_ConfigureIOS18Properties(IJKVideoToolboxContext *context);

// Enhanced decode function for iOS 18
OSStatus ijkVT_DecodeFrameIOS18(IJKVideoToolboxContext *context,
                               CMSampleBufferRef sampleBuffer,
                               VTDecodeFrameFlags decodeFlags,
                               void *sourceFrameRefCon,
                               VTDecodeInfoFlags *infoFlagsOut);

// Clean up iOS 18 VideoToolbox session
void ijkVT_CleanupIOS18Session(IJKVideoToolboxContext *context);

// iOS 18 HDR support detection
BOOL ijkVT_SupportsHDROnIOS18(void);

// iOS 18 ProRes support detection  
BOOL ijkVT_SupportsProResOnIOS18(void);

// Get optimal decoder configuration for iOS 18
CFDictionaryRef ijkVT_CreateIOS18DecoderConfig(int width, int height, 
                                              CMVideoCodecType codecType);

// Create pixel buffer attributes optimized for iOS 18
CFDictionaryRef ijkVT_CreateIOS18PixelBufferAttributes(int width, int height);

// iOS 18 Metal integration
#if TARGET_OS_IOS
#import <Metal/Metal.h>
#import <MetalKit/MetalKit.h>

// Convert VideoToolbox buffer to Metal texture for iOS 18
id<MTLTexture> ijkVT_CreateMetalTextureFromPixelBufferIOS18(CVPixelBufferRef pixelBuffer,
                                                          id<MTLDevice> device);
#endif

#ifdef __cplusplus
}
#endif

#endif /* ijkplayer_ios18_videotoolbox_h */
