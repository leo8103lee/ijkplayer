/*
 * Simple Video View Controller Implementation
 * Uses native AVPlayer for iOS simulator compatibility
 */

#import "SimpleVideoViewController.h"

@interface SimpleVideoViewController ()

@property (nonatomic, strong) UIButton *playButton;
@property (nonatomic, strong) UIButton *pauseButton;
@property (nonatomic, strong) UILabel *statusLabel;

@end

@implementation SimpleVideoViewController

- (instancetype)initWithURL:(NSURL *)url {
    if (self = [super init]) {
        self.player = [AVPlayer playerWithURL:url];
        self.title = @"Simple Video Player";
    }
    return self;
}

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.view.backgroundColor = [UIColor blackColor];
    
    // Setup player layer
    self.playerLayer = [AVPlayerLayer playerLayerWithPlayer:self.player];
    self.playerLayer.frame = self.view.bounds;
    self.playerLayer.videoGravity = AVLayerVideoGravityResizeAspect;
    [self.view.layer addSublayer:self.playerLayer];
    
    // Setup controls
    [self setupControls];
}

- (void)setupControls {
    // Play button
    self.playButton = [UIButton buttonWithType:UIButtonTypeSystem];
    [self.playButton setTitle:@"Play" forState:UIControlStateNormal];
    [self.playButton setTitleColor:[UIColor whiteColor] forState:UIControlStateNormal];
    self.playButton.frame = CGRectMake(50, self.view.frame.size.height - 100, 80, 44);
    [self.playButton addTarget:self action:@selector(playVideo) forControlEvents:UIControlEventTouchUpInside];
    [self.view addSubview:self.playButton];
    
    // Pause button
    self.pauseButton = [UIButton buttonWithType:UIButtonTypeSystem];
    [self.pauseButton setTitle:@"Pause" forState:UIControlStateNormal];
    [self.pauseButton setTitleColor:[UIColor whiteColor] forState:UIControlStateNormal];
    self.pauseButton.frame = CGRectMake(150, self.view.frame.size.height - 100, 80, 44);
    [self.pauseButton addTarget:self action:@selector(pauseVideo) forControlEvents:UIControlEventTouchUpInside];
    [self.view addSubview:self.pauseButton];
    
    // Status label
    self.statusLabel = [[UILabel alloc] initWithFrame:CGRectMake(50, 100, 300, 44)];
    self.statusLabel.text = @"Ready to play";
    self.statusLabel.textColor = [UIColor whiteColor];
    [self.view addSubview:self.statusLabel];
    
    // Back button
    UIBarButtonItem *backButton = [[UIBarButtonItem alloc] initWithTitle:@"Back" style:UIBarButtonItemStylePlain target:self action:@selector(goBack)];
    self.navigationItem.leftBarButtonItem = backButton;
}

- (void)playVideo {
    [self.player play];
    self.statusLabel.text = @"Playing";
}

- (void)pauseVideo {
    [self.player pause];
    self.statusLabel.text = @"Paused";
}

- (void)goBack {
    [self.navigationController popViewControllerAnimated:YES];
}

- (void)viewWillLayoutSubviews {
    [super viewWillLayoutSubviews];
    self.playerLayer.frame = self.view.bounds;
}

@end