# Native Automation

## Overview

Flutter's [integration\_test][integration_test] does a good job at providing
basic support for integration testing Flutter apps. What it can't do is
interaction with the OS your Flutter app is running on. This makes it impossible
to test many critical business features:

* granting runtime permissions
* signing into the app which uses WebView or OAuth (like Google) as the login
  page
* listing and tapping on notifications
* exiting the app, coming back, and verifying that state is preserved
* enabling and disabling features such as Wi-Fi, mobile data, location, or dark
  mode

Patrol's *platform automation* feature finally solves these problems. Here's a
tiny snippet to spice things up:

```dart title="patrol_test/demo_test.dart"
void main() {
  patrolTest('demo', (PatrolIntegrationTester $) async {
    await $.pumpWidgetAndSettle(AwesomeApp());
    // prepare network conditions
    await $.platform.mobile.enableCellular();
    await $.platform.mobile.disableWifi();

    // toggle system theme
    await $.platform.mobile.enableDarkMode();

    // handle native location permission request dialog
    await $.platform.mobile.selectFineLocation();
    await $.platform.mobile.grantPermissionWhenInUse();

    // tap on the first notification
    await $.platform.mobile.openNotifications();
    await $.platform.mobile.tapOnNotificationByIndex(0);
  });
}
```

For web applications, Patrol provides browser-specific automation capabilities. You can
interact with browser dialogs, manage cookies, handle file uploads, and more:

```dart title="patrol_test/web_demo_test.dart"
void main() {
  patrolTest('web demo', (PatrolIntegrationTester $) async {
    await $.pumpWidgetAndSettle(AwesomeWebApp());

    // grant browser permissions
    await $.platform.web.grantPermissions(permissions: ['clipboard-read']);

    // manage cookies
    await $.platform.web.addCookie(name: 'session', value: 'abc123');

    // handle browser dialogs
    await $.platform.web.acceptNextDialog();
  });
}
```

  Platform automation is currently available on Android, iOS, and Web.

[integration_test]: https://github.com/flutter/flutter/tree/master/packages/integration_test

## Usage

Once set up, interacting with the native UI using Patrol is very easy!

### Basics

After you've got your `PlatformAutomator` object via `$.platform`, you simply call methods on it
and it does the magic. For cross-platform mobile actions, use `$.platform.mobile`.

To tap on a native view (for example, a button in a WebView):

```dart
await $.platform.mobile.tap(Selector(text: 'Sign up for newsletter'));
```

To enter text into a native view (for example, a form in a WebView):

```dart
await $.platform.mobile.enterText(
  Selector(text: 'Enter your email'),
  text: 'charlie@root.me',
);
```

You can also enter text into the n-th currently visible text field (counting from 0):

```dart
await $.platform.mobile.enterTextByIndex('charlie_root', index: 0); // enter username
await $.platform.mobile.enterTextByIndex('ny4ncat', index: 1); // enter password
```

The above are the simplest, most common actions, but they already make it
possible to test scenarios that were impossible to test before, such as
WebViews.

### Platform-specific selectors

When you need different selectors for Android and iOS, use `MobileSelector`:

```dart
await $.platform.mobile.tap(
  MobileSelector(
    android: AndroidSelector(resourceName: 'com.example:id/button'),
    ios: IOSSelector(identifier: 'myButton'),
  ),
);
```

### Android-specific actions

For Android-only actions, use `$.platform.android`:

```dart
// Press the hardware back button (Android only)
await $.platform.android.pressBack();

// Double press the recent apps button to switch to the previous app
await $.platform.android.pressDoubleRecentApps();

// Tap on a native view using Android-specific selector
await $.platform.android.tap(
  AndroidSelector(resourceName: 'com.example:id/submit_button'),
);

// Open a specific Android app
await $.platform.android.openPlatformApp(androidAppId: 'com.android.settings');
```

### iOS-specific actions

For iOS-only actions, use `$.platform.ios`:

```dart
// Tap on a native view using iOS-specific selector
await $.platform.ios.tap(
  IOSSelector(identifier: 'submitButton'),
);

// Close a heads-up notification
await $.platform.ios.closeHeadsUpNotification();

// Swipe back gesture (iOS edge swipe)
await $.platform.ios.swipeBack();

// Open a specific iOS app
await $.platform.ios.openPlatformApp(iosAppId: 'com.apple.Preferences');
```

  To tap, enter text, or perform generally any UI interaction with an iOS app
  that is not your Flutter app under test, you need to pass its bundle
  identifier. For example, to tap on the "Add" button in the iPhone contacts app:

  ```dart
  await $.platform.ios.tap(
    IOSSelector(text: 'Add'),
    appId: 'com.apple.MobileAddressBook',
  );
  ```

### Web-specific actions

For Flutter Web apps, use `$.platform.web` to interact with browser elements and features:

```dart
// Tap on a web element by text
await $.platform.web.tap(WebSelector(text: 'Submit'));

// Tap on a web element using CSS selector
await $.platform.web.tap(WebSelector(cssOrXpath: 'css=#submit-button'));

// Tap on a web element by test ID
await $.platform.web.tap(WebSelector(testId: 'login-button'));

// Enter text into a form field
await $.platform.web.enterText(
  WebSelector(placeholder: 'Email address'),
  text: 'user@example.com',
);

// Scroll to an element
await $.platform.web.scrollTo(WebSelector(text: 'Load more'));
```

Web automation also supports advanced browser interactions:

```dart
// Handle browser dialogs
await $.platform.web.acceptNextDialog();
await $.platform.web.dismissNextDialog();

// Manage cookies
await $.platform.web.addCookie(name: 'session', value: 'abc123');
await $.platform.web.clearCookies();

// Control dark mode
await $.platform.web.enableDarkMode();
await $.platform.web.disableDarkMode();

// Browser navigation
await $.platform.web.goBack();
await $.platform.web.goForward();

// Keyboard interactions
await $.platform.web.pressKey(key: 'Enter');
await $.platform.web.pressKeyCombo(keys: ['Control', 'a']);

// Clipboard operations
await $.platform.web.setClipboard(text: 'Copied text');
final clipboardContent = await $.platform.web.getClipboard();

// Browser permissions
await $.platform.web.grantPermissions(permissions: ['geolocation', 'notifications']);
await $.platform.web.clearPermissions();

// File uploads
await $.platform.web.uploadFile(files: [UploadFileData(name: 'test.txt', content: 'Hello')]);

// Verify file downloads
final downloadedFiles = await $.platform.web.verifyFileDownloads();

// Resize browser window
await $.platform.web.resizeWindow(size: Size(1920, 1080));
```

Working with iframes:

```dart
// Tap on an element inside an iframe
await $.platform.web.tap(
  WebSelector(text: 'Submit'),
  iframeSelector: WebSelector(cssOrXpath: 'css=#payment-iframe'),
);
```

### Cross-platform mobile actions

For actions that work on both Android and iOS, use `$.platform.mobile`. This is the recommended
approach when you don't need platform-specific behavior, as it keeps your tests clean and
maintainable across both platforms.

The `$.platform.mobile` automator automatically routes calls to the appropriate platform
implementation based on where your test is running. You can use the unified `Selector` class
for simple cases, or `MobileSelector` when you need different selectors per platform.

### Notifications

To open the notification shade:

```dart
await $.platform.mobile.openNotifications();
```

To tap on the second notification:

```dart
await $.platform.mobile.tapOnNotificationByIndex(1);
```

You can also tap on notification by its content:

```dart
await $.platform.mobile.tapOnNotificationBySelector(
  Selector(textContains: 'Someone liked your recent post'),
);
```

### Permissions

To handle the native permission request dialog:

```dart
await $.platform.mobile.grantPermissionWhenInUse();
await $.platform.mobile.grantPermissionOnlyThisTime();
await $.platform.mobile.denyPermission();
```

If the permission request dialog visible is the location dialog, you can also
select the accuracy:

```dart
await $.platform.mobile.selectFineLocation();
await $.platform.mobile.selectCoarseLocation();
```

The test will fail if the permission request dialog is not visible. You can
check if it is with:

```dart
if (await $.platform.mobile.isPermissionDialogVisible()) {
  await $.platform.mobile.grantPermissionWhenInUse();
}
```

By default, `isPermissionDialogVisible()` waits for a short amount of time and
then returns `false` if the dialog is not visible. To increase the timeout:

```dart
if (await $.platform.mobile.isPermissionDialogVisible(timeout: Duration(seconds: 5))) {
  await $.platform.mobile.grantPermissionWhenInUse();
}
```

  Patrol can handle permissions on iOS only if the device language is set to
  English (preferably US). That's because there's no way to refer to a specific
  view in a language-independent way (like resourceId on Android).

  If you want to handle permissions on iOS device with non-English locale, do it
  manually:

  ```dart
  await $.platform.ios.tap(
    IOSSelector(text: 'Allow'),
    appId: 'com.apple.springboard',
  );
  ```

### Device information

Get information about the device running the tests:

```dart
// Check if running on an emulator/simulator
final isVirtual = await $.platform.mobile.isVirtualDevice();

// Get OS version (e.g., 30 for Android 11)
final osVersion = await $.platform.mobile.getOsVersion();
if (osVersion >= 30) {
  // Android 11+ specific behavior
}
```

### More resources

To see more integration tests demonstrating Patrol's various features, check out
our [example app][example_app].

[example_app]: https://github.com/leancodepl/patrol/tree/master/packages/patrol/example

## Feature parity

Here you can see what you can already do with Patrol's `PlatformAutomator`, and what
is yet to be implemented. We hope that it will help you evaluate Patrol.

We strive for high feature parity across platforms, but in some cases it's
impossible to reach 100%. Web support is available for browser-specific automation.

  macOS support is still in alpha and does not have platform automation implemented yet.

## Native Automation 2.0 (native2)

> **Warning**
> `native2` is deprecated starting from Patrol version `4.0.0` and will be removed in a future release.
  Please migrate to the new [Platform Automation API](https://patrol.leancode.co/documentation/native/overview) using `$.platform.mobile` instead.

  `native2` is available starting from Patrol version `3.6.0`.

## Mobile features

These features are available via `$.platform.mobile` and work on both Android and iOS:

| **Feature**                    | **Android**  | **iOS**         |
| ------------------------------ | ------------ | --------------- |
| [Press home]                   | ✅            | ✅               |
| [Open app]                     | ✅            | ✅               |
| [Open notifications]           | ✅            | ✅               |
| [Close notifications]          | ✅            | ✅               |
| [Open quick settings]          | ✅            | ✅               |
| [Open URL]                     | ✅            | ✅               |
| [Enable/disable dark mode]     | ✅            | ✅               |
| [Enable/disable airplane mode] | ✅            | ✅               |
| [Enable/disable cellular]      | ✅            | ✅               |
| [Enable/disable Wi-Fi]         | ✅            | ✅               |
| [Enable/disable Bluetooth]     | ✅            | ✅               |
| [Press volume up]              | ✅            | ✅ (simulator ❌) |
| [Press volume down]            | ✅            | ✅ (simulator ❌) |
| [Handle permission dialogs]    | ✅            | ✅               |
| [Set mock location]            | ✅ (device ❌) | ✅               |
| [Get OS version]               | ✅            | ✅               |
| [Check virtual device]         | ✅            | ✅               |

## Android-specific features

These features are available via `$.platform.android`:

| **Feature**                | **Android**   |
| -------------------------- | ------------- |
| [Press back]               | ✅             |
| [Double press recent apps] | ✅             |
| [Tap]                      | ✅             |
| [Double tap]               | ✅             |
| [Tap at coordinate]        | ✅             |
| [Enter text]               | ✅             |
| [Enter text by index]      | ✅             |
| [Swipe]                    | ✅             |
| [Swipe back]               | ✅             |
| [Pull to refresh]          | ✅             |
| [Tap on notification]      | ✅             |
| [Enable/disable location]  | ✅             |
| [Take camera photo]        | ✅             |
| [Pick image from gallery]  | ✅             |
| [Pick multiple images]     | ✅             |
| Interact with WebView      | ⚠️ see [#244] |

## iOS-specific features

These features are available via `$.platform.ios`:

| **Feature**                   | **iOS** |
| ----------------------------- | ------- |
| [iOS Tap]                     | ✅       |
| [iOS Double tap]              | ✅       |
| [iOS Tap at coordinate]       | ✅       |
| [iOS Enter text]              | ✅       |
| [iOS Enter text by index]     | ✅       |
| [iOS Swipe]                   | ✅       |
| [iOS Swipe back]              | ✅       |
| [iOS Pull to refresh]         | ✅       |
| [iOS Tap on notification]     | ✅       |
| [Close heads-up notification] | ✅       |
| [iOS Take camera photo]       | ✅       |
| [iOS Pick image from gallery] | ✅       |
| [iOS Pick multiple images]    | ✅       |
| Interact with WebView         | ✅       |

## Web-specific features

These features are available via `$.platform.web` for Flutter Web apps:

| **Feature**                      | **Web** |
| -------------------------------- | ------- |
| [Web Tap]                        | ✅       |
| [Web Enter text]                 | ✅       |
| [Scroll to]                      | ✅       |
| [Enable/disable dark mode (web)] | ✅       |
| [Grant/clear permissions]        | ✅       |
| [Manage cookies]                 | ✅       |
| [Upload files]                   | ✅       |
| [Handle dialogs]                 | ✅       |
| [Press key/key combo]            | ✅       |
| [Browser navigation]             | ✅       |
| [Clipboard operations]           | ✅       |
| [Resize window]                  | ✅       |
| [Verify file downloads]          | ✅       |

{/* Issue links */}

[#244]: https://github.com/leancodepl/patrol/issues/244

{/* MobileAutomator links */}

[Press home]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/pressHome.html

[Open app]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/openApp.html

[Open notifications]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/openNotifications.html

[Close notifications]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/closeNotifications.html

[Open quick settings]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/openQuickSettings.html

[Open URL]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/openUrl.html

[Enable/disable dark mode]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/enableDarkMode.html

[Enable/disable airplane mode]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/enableAirplaneMode.html

[Enable/disable cellular]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/enableCellular.html

[Enable/disable Wi-Fi]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/enableWifi.html

[Enable/disable Bluetooth]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/enableBluetooth.html

[Press volume up]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/pressVolumeUp.html

[Press volume down]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/pressVolumeDown.html

[Handle permission dialogs]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/grantPermissionWhenInUse.html

[Set mock location]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/setMockLocation.html

[Get OS version]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/getOsVersion.html

[Check virtual device]: https://pub.dev/documentation/patrol/latest/patrol/MobileAutomator/isVirtualDevice.html

{/* AndroidAutomator links */}

[Press back]: https://pub.dev/documentation/patrol/latest/patrol/AndroidAutomator/pressBack.html

[Double press recent apps]: https://pub.dev/documentation/patrol/latest/patrol/AndroidAutomator/pressDoubleRecentApps.html

[Tap]: https://pub.dev/documentation/patrol/latest/patrol/AndroidAutomator/tap.html

[Double tap]: https://pub.dev/documentation/patrol/latest/patrol/AndroidAutomator/doubleTap.html

[Tap at coordinate]: https://pub.dev/documentation/patrol/latest/patrol/AndroidAutomator/tapAt.html

[Enter text]: https://pub.dev/documentation/patrol/latest/patrol/AndroidAutomator/enterText.html

[Enter text by index]: https://pub.dev/documentation/patrol/latest/patrol/AndroidAutomator/enterTextByIndex.html

[Swipe]: https://pub.dev/documentation/patrol/latest/patrol/AndroidAutomator/swipe.html

[Swipe back]: https://pub.dev/documentation/patrol/latest/patrol/AndroidAutomator/swipeBack.html

[Pull to refresh]: https://pub.dev/documentation/patrol/latest/patrol/AndroidAutomator/pullToRefresh.html

[Tap on notification]: https://pub.dev/documentation/patrol/latest/patrol/AndroidAutomator/tapOnNotificationBySelector.html

[Enable/disable location]: https://pub.dev/documentation/patrol/latest/patrol/AndroidAutomator/enableLocation.html

[Take camera photo]: https://pub.dev/documentation/patrol/latest/patrol/AndroidAutomator/takeCameraPhoto.html

[Pick image from gallery]: https://pub.dev/documentation/patrol/latest/patrol/AndroidAutomator/pickImageFromGallery.html

[Pick multiple images]: https://pub.dev/documentation/patrol/latest/patrol/AndroidAutomator/pickMultipleImagesFromGallery.html

{/* IOSAutomator links */}

[iOS Tap]: https://pub.dev/documentation/patrol/latest/patrol/IOSAutomator/tap.html

[iOS Double tap]: https://pub.dev/documentation/patrol/latest/patrol/IOSAutomator/doubleTap.html

[iOS Tap at coordinate]: https://pub.dev/documentation/patrol/latest/patrol/IOSAutomator/tapAt.html

[iOS Enter text]: https://pub.dev/documentation/patrol/latest/patrol/IOSAutomator/enterText.html

[iOS Enter text by index]: https://pub.dev/documentation/patrol/latest/patrol/IOSAutomator/enterTextByIndex.html

[iOS Swipe]: https://pub.dev/documentation/patrol/latest/patrol/IOSAutomator/swipe.html

[iOS Swipe back]: https://pub.dev/documentation/patrol/latest/patrol/IOSAutomator/swipeBack.html

[iOS Pull to refresh]: https://pub.dev/documentation/patrol/latest/patrol/IOSAutomator/pullToRefresh.html

[iOS Tap on notification]: https://pub.dev/documentation/patrol/latest/patrol/IOSAutomator/tapOnNotificationBySelector.html

[Close heads-up notification]: https://pub.dev/documentation/patrol/latest/patrol/IOSAutomator/closeHeadsUpNotification.html

[iOS Take camera photo]: https://pub.dev/documentation/patrol/latest/patrol/IOSAutomator/takeCameraPhoto.html

[iOS Pick image from gallery]: https://pub.dev/documentation/patrol/latest/patrol/IOSAutomator/pickImageFromGallery.html

[iOS Pick multiple images]: https://pub.dev/documentation/patrol/latest/patrol/IOSAutomator/pickMultipleImagesFromGallery.html

{/* WebAutomator links */}

[Web Tap]: https://pub.dev/documentation/patrol/latest/patrol/WebAutomator/tap.html

[Web Enter text]: https://pub.dev/documentation/patrol/latest/patrol/WebAutomator/enterText.html

[Scroll to]: https://pub.dev/documentation/patrol/latest/patrol/WebAutomator/scrollTo.html

[Enable/disable dark mode (web)]: https://pub.dev/documentation/patrol/latest/patrol/WebAutomator/enableDarkMode.html

[Grant/clear permissions]: https://pub.dev/documentation/patrol/latest/patrol/WebAutomator/grantPermissions.html

[Manage cookies]: https://pub.dev/documentation/patrol/latest/patrol/WebAutomator/addCookie.html

[Upload files]: https://pub.dev/documentation/patrol/latest/patrol/WebAutomator/uploadFile.html

[Handle dialogs]: https://pub.dev/documentation/patrol/latest/patrol/WebAutomator/acceptNextDialog.html

[Press key/key combo]: https://pub.dev/documentation/patrol/latest/patrol/WebAutomator/pressKey.html

[Browser navigation]: https://pub.dev/documentation/patrol/latest/patrol/WebAutomator/goBack.html

[Clipboard operations]: https://pub.dev/documentation/patrol/latest/patrol/WebAutomator/getClipboard.html

[Resize window]: https://pub.dev/documentation/patrol/latest/patrol/WebAutomator/resizeWindow.html

[Verify file downloads]: https://pub.dev/documentation/patrol/latest/patrol/WebAutomator/verifyFileDownloads.html

## What is `native2`?

`native2` was created to address fundamental limitations in the original native automation approach. The original native API was primarily designed for Android, and attempts to make a single `Selector` work across both
platforms proved problematic because **iOS and Android use different selector arguments** (eg. Android's `resourceName` vs iOS's `identifier`) and a single selector approach couldn't effectively handle the fundamental differences
between iOS and Android element identification. **`native2` provides platform-specific selectors that work with both Android and iOS, giving you more accurate selectors instead of one shared selector.**

### Before `native2`

```dart
// You were forced to use flaky text-based selectors that work on both platforms
await $.native.tap(Selector(textContains: 'Login'));
```

```dart
// Before: Sometimes you needed to use platform-specific if statements in your test code.
if (Platform.isAndroid) {
  await $.native.tap(Selector(resourceId: 'com.android.camera2:id/shutter_button'));
} else {
  await $.native.tap(Selector(text: 'Take Picture'));
}
```

### With `native2`

`native2` provides a single method call that works across both platforms:

```dart
// After: Single method call with platform-specific selectors
await $.native2.tap(
  NativeSelector(
    android: AndroidSelector(
      resourceName: 'com.android.camera2:id/shutter_button',
    ),
    ios: IOSSelector(label: 'Take Picture'),
  ),
);
```

### Text Input Operations

```dart
// Enter password in secure field
await $.native2.enterText(
  NativeSelector(
    android: AndroidSelector(
      contentDescription: 'Password',
    ),
    ios: IOSSelector(
      elementType: IOSElementType.secureTextField,
    ),
  ),
  text: 'secretpassword',
);
```

### More platform-specific attributes like elementType for iOS

```dart
// Find elements by instance (when multiple elements match)
await $.native2.tap(
  NativeSelector(
    android: AndroidSelector(
      className: 'android.widget.Button',
      instance: 2, // Third button (0-indexed)
    ),
    ios: IOSSelector(
      elementType: IOSElementType.button,
      instance: 2, // Third button (0-indexed)
    ),
  ),
);
```

### Specifying App ID (iOS)

When working with iOS, you may need to specify the `appId` parameter to interact with elements in specific applications. This is particularly useful when your test needs to interact with system apps like Safari, Settings, or other third-party applications.

  The `appId` parameter is used for iOS. On Android, it will be ignored.

```dart
await $.native2.tap(
  appId: 'com.apple.mobilesafari',
  NativeSelector(
    ios: IOSSelector(elementType: IOSElementType.button, label: 'Open'),
  ),
);
```

  Remember that if you don't provide a platform-specific selector (iOS or Android) and run the command on that platform, the command will fail.

