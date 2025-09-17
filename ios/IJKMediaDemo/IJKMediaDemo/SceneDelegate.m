//
// SceneDelegate.m
// IJKMediaDemo iOS 18 Scene Support  
//

#import "SceneDelegate.h"

@interface SceneDelegate ()

@end

@implementation SceneDelegate

- (void)scene:(UIScene *)scene willConnectToSession:(UISceneSession *)session options:(UISceneConnectionOptions *)connectionOptions {
    if (@available(iOS 18.0, *)) {
        // iOS 18 specific scene configuration
        UIWindowScene *windowScene = (UIWindowScene *)scene;
        self.window = [[UIWindow alloc] initWithWindowScene:windowScene];
        
        // Configure window for media playback
        self.window.backgroundColor = [UIColor blackColor];
        [self.window makeKeyAndVisible];
        
        NSLog(@"Scene connected with iOS 18 optimizations");
    } else {
        // Fallback for iOS < 18
        UIWindowScene *windowScene = (UIWindowScene *)scene;
        self.window = [[UIWindow alloc] initWithWindowScene:windowScene];
        [self.window makeKeyAndVisible];
    }
}

- (void)sceneDidDisconnect:(UIScene *)scene {
    // Clean up media resources
    NSLog(@"Scene disconnected, cleaning up media resources");
}

- (void)sceneDidBecomeActive:(UIScene *)scene {
    // Resume media playback if needed
    if (@available(iOS 18.0, *)) {
        // iOS 18 optimized media resumption
        [[NSNotificationCenter defaultCenter] postNotificationName:@"IJKMediaPlayerSceneDidBecomeActive" 
                                                            object:nil];
    }
}

- (void)sceneWillResignActive:(UIScene *)scene {
    // Pause media playback
    [[NSNotificationCenter defaultCenter] postNotificationName:@"IJKMediaPlayerSceneWillResignActive" 
                                                        object:nil];
}

- (void)sceneWillEnterForeground:(UIScene *)scene {
    // Prepare for active use
}

- (void)sceneDidEnterBackground:(UIScene *)scene {
    // Save application state and pause media
    if (@available(iOS 18.0, *)) {
        // iOS 18 background task management
        UIApplication *app = [UIApplication sharedApplication];
        __block UIBackgroundTaskIdentifier bgTask = [app beginBackgroundTaskWithExpirationHandler:^{
            [app endBackgroundTask:bgTask];
            bgTask = UIBackgroundTaskInvalid;
        }];
        
        // Clean up background task after a short delay
        dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2.0 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
            if (bgTask != UIBackgroundTaskInvalid) {
                [app endBackgroundTask:bgTask];
                bgTask = UIBackgroundTaskInvalid;
            }
        });
    }
}

@end
