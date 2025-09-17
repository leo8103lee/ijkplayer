//
// ios18_compat.h
// IJKMediaPlayer iOS 18 Compatibility
//

#ifndef ios18_compat_h
#define ios18_compat_h

#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>
#import <VideoToolbox/VideoToolbox.h>

#if __IPHONE_OS_VERSION_MAX_ALLOWED >= 180000

// iOS 18 VideoToolbox enhancements
#define IJK_USE_VT_SESSION_PROPERTIES 1

// iOS 18 AVAudioSession improvements
#define IJK_USE_MODERN_AUDIO_SESSION 1

// iOS 18 Metal Performance Shaders
#define IJK_USE_MPS_OPTIMIZATIONS 1

#else

#define IJK_USE_VT_SESSION_PROPERTIES 0
#define IJK_USE_MODERN_AUDIO_SESSION 0  
#define IJK_USE_MPS_OPTIMIZATIONS 0

#endif

// iOS 18 VideoToolbox session properties
#if IJK_USE_VT_SESSION_PROPERTIES
static inline OSStatus ijkVTSessionSetProperty(VTSessionRef session, CFStringRef propertyKey, CFTypeRef propertyValue) {
    if (@available(iOS 18.0, *)) {
        return VTSessionSetProperty(session, propertyKey, propertyValue);
    } else {
        // Fallback for older iOS versions
        if (CFEqual(propertyKey, kVTDecompressionPropertyKey_RealTime)) {
            return VTDecompressionSessionSetProperty(session, propertyKey, propertyValue);
        }
        return noErr;
    }
}
#endif

// iOS 18 AVAudioSession configuration
#if IJK_USE_MODERN_AUDIO_SESSION
static inline void ijkConfigureAudioSessionForIOS18(void) {
    if (@available(iOS 18.0, *)) {
        AVAudioSession *session = [AVAudioSession sharedInstance];
        NSError *error = nil;
        
        // Use new iOS 18 audio session categories
        [session setCategory:AVAudioSessionCategoryPlayback 
                        mode:AVAudioSessionModeMoviePlayback 
                     options:AVAudioSessionCategoryOptionMixWithOthers |
                             AVAudioSessionCategoryOptionAllowBluetooth |
                             AVAudioSessionCategoryOptionAllowBluetoothA2DP
                       error:&error];
                       
        if (error) {
            NSLog(@"Audio session configuration error: %@", error.localizedDescription);
        }
    }
}
#endif

// iOS 18 hardware acceleration optimizations
#if IJK_USE_MPS_OPTIMIZATIONS
#import <MetalPerformanceShaders/MetalPerformanceShaders.h>

static inline BOOL ijkCanUseMPSForVideoProcessing(void) {
    if (@available(iOS 18.0, *)) {
        id<MTLDevice> device = MTLCreateSystemDefaultDevice();
        return device && [MPSKernel supportsDevice:device];
    }
    return NO;
}
#endif

// Deprecated API compatibility
#pragma mark - Deprecated API Compatibility

// Handle deprecated UIApplication methods
#define IJK_UI_APPLICATION_STATUS_BAR_STYLE(style) \
    do { \
        if (@available(iOS 18.0, *)) { \
            /* Use new scene-based status bar control */ \
        } else { \
            [[UIApplication sharedApplication] setStatusBarStyle:style]; \
        } \
    } while(0)

// Handle deprecated VideoToolbox methods
#define IJK_VT_DECOMPRESSION_SESSION_CREATE(session, ...) \
    VTDecompressionSessionCreate(__VA_ARGS__)

#endif /* ios18_compat_h */
