/*
 * Simplified Demo Main View Controller Implementation
 * Uses native iOS components for simulator compatibility
 */

#import "SimpleDemoMainViewController.h"
#import "SimpleVideoViewController.h"

@interface SimpleDemoMainViewController () <UITableViewDataSource, UITableViewDelegate>

@property (nonatomic, strong) UITableView *tableView;
@property (nonatomic, strong) NSArray *options;

@end

@implementation SimpleDemoMainViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.title = @"IJKPlayer Demo (Simulator)";
    self.view.backgroundColor = [UIColor whiteColor];
    
    self.options = @[
        @"Play Sample Video (HTTP)",
        @"Play Local Test Video",
        @"About"
    ];
    
    [self setupTableView];
}

- (void)setupTableView {
    self.tableView = [[UITableView alloc] initWithFrame:self.view.bounds style:UITableViewStyleGrouped];
    self.tableView.dataSource = self;
    self.tableView.delegate = self;
    self.tableView.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
    [self.view addSubview:self.tableView];
}

#pragma mark - UITableViewDataSource

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return self.options.count;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    static NSString *cellIdentifier = @"DemoCell";
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:cellIdentifier];
    
    if (!cell) {
        cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:cellIdentifier];
        cell.accessoryType = UITableViewCellAccessoryDisclosureIndicator;
    }
    
    cell.textLabel.text = self.options[indexPath.row];
    
    return cell;
}

#pragma mark - UITableViewDelegate

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    [tableView deselectRowAtIndexPath:indexPath animated:YES];
    
    switch (indexPath.row) {
        case 0: {
            // Play sample HTTP video
            NSURL *videoURL = [NSURL URLWithString:@"https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"];
            SimpleVideoViewController *playerVC = [[SimpleVideoViewController alloc] initWithURL:videoURL];
            [self.navigationController pushViewController:playerVC animated:YES];
            break;
        }
        case 1: {
            // Try to play a local video (will show message if none available)
            [self showLocalVideoMessage];
            break;
        }
        case 2: {
            // Show about dialog
            [self showAboutDialog];
            break;
        }
        default:
            break;
    }
}

- (void)showLocalVideoMessage {
    UIAlertController *alert = [UIAlertController alertControllerWithTitle:@"Local Video"
                                                                   message:@"Local video playback would require video files in the app bundle. For simulator testing, use the HTTP sample video option."
                                                            preferredStyle:UIAlertControllerStyleAlert];
    
    UIAlertAction *okAction = [UIAlertAction actionWithTitle:@"OK" style:UIAlertActionStyleDefault handler:nil];
    [alert addAction:okAction];
    
    [self presentViewController:alert animated:YES completion:nil];
}

- (void)showAboutDialog {
    UIAlertController *alert = [UIAlertController alertControllerWithTitle:@"About IJKPlayer Demo"
                                                                   message:@"This is a simplified version of IJKPlayer demo for iOS Simulator testing.\n\nOriginal IJKPlayer by Bilibili\nSimplified for simulator compatibility"
                                                            preferredStyle:UIAlertControllerStyleAlert];
    
    UIAlertAction *okAction = [UIAlertAction actionWithTitle:@"OK" style:UIAlertActionStyleDefault handler:nil];
    [alert addAction:okAction];
    
    [self presentViewController:alert animated:YES completion:nil];
}

@end