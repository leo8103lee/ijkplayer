/*
 * Simple Video View Controller for iOS Simulator Testing
 * This replaces the complex IJKMediaPlayer with a simple interface
 */

#import <UIKit/UIKit.h>
#import <AVFoundation/AVFoundation.h>

@interface SimpleVideoViewController : UIViewController

@property (nonatomic, strong) AVPlayer *player;
@property (nonatomic, strong) AVPlayerLayer *playerLayer;

- (instancetype)initWithURL:(NSURL *)url;

@end