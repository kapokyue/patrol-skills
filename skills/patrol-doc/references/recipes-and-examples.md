# Recipes And Examples


## Write your first test

Patrol is a powerful, open-source testing framework created by LeanCode that enhances Flutter's testing capabilities by enabling interaction with native platform features directly in Dart. It allows to handle permission dialogs, notifications, WebViews, and device settings—features previously unavailable in standard Flutter tests, making it truly possible to test the whole app.

This tutorial will take you through writing your first substantial Patrol test, interacting both with the Flutter app itself and also with native permission dialogs and notifications.

Before writing any tests, make sure you [install the Patrol CLI]. Then just clone the following repository from GitHub to follow along. The app we’re going to be testing is fully functional and ready to be tested, with Patrol already configured.

  To learn how to set up Patrol for your own project, check out the [Patrol Setup Docs].

  Clone the [STARTER PROJECT] to follow along.

### App Walkthrough

Before we can start writing automated Patrol tests, we need to know what the app does and to test it manually. Please, check out the video tutorial for a visual walkthrough.

The first screen of our app is for signing in. It’s not using any actual sign-in provider but it only validates the email address and password. In order to successfully “sign in” and get to the home screen, we need to input a valid email and a password that’s at least 8 characters long.

  You can test any real authentication providers that use WebView for signing in with the powerful Patrol native automation.

On the second screen, we’re greeted with a notifications permission dialog. Once we allow them, we can tap on the notification button in the app bar to manually trigger a local notification which will be displayed after 3 seconds both when the app is running in the foreground or in the background.

Once we open the native notification bar and tap on the notification from our app, we’re gonna see a snackbar on the bottom saying *"Notification was tapped!”*

### Testing the “Happy Path”

You’ve just seen the full walkthrough of the app, including errors that can show up if you input an invalid email or password. UI tests (integration tests), like the ones we’re going to write with Patrol, should only be testing the “happy path” of a UI flow. We only want them to fail if the app suddenly stops the user from doing what the app is for - in this case, that’s displaying a notification. Validation error messages are not “what the app is for”, they exist only to allow the user to successfully sign in with a proper email and password. That’s why we won’t be checking for them in the tests.

### Writing the Test

We have only one UI flow in this app, that is signing in, showing the notification and then tapping on that notification. This means, we’re going to have only a single test. Let’s create it in `/patrol_test/app_test.dart`.

Like any other test, we need to have a `main()` top-level function. Inside it we’re going to have our single `patrolTest` with a description properly describing what we’re about to test. An optional step is to set the frame policy to “fully live” to make sure all frames are shown, even those which are not pumped by our test code. Without it, we would see that our app stutters and animations are not played properly.

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:patrol/patrol.dart';

void main() {
  patrolTest(
    'signs in, triggers a notification, and taps on it',
    ($) async {
      // Test code will go here
    },
  );
}
```

We could start writing the test right now and then re-run it from scratch every time we add a new line of test code by calling `patrol test --target patrol_test/app_test.dart` but since we’re writing a Patrol test that runs on an Android or iOS device, constantly building the whole Flutter app is not time effective. Thankfully, Patrol offers a different approach - hot restarting the tests! We can run the command `patrol develop --target patrol_test/app_test.dart` right now and anytime we add a new line of test code, we can just type “r” in the terminal to re-run the tests without the time-costly app building. Just make sure that you have an emulator running first - Patrol will select it automatically.

First, we need to perform any initializations that need to happen before the app is run and pump the top-level widget of our app. We’re effectively doing what the `main` function inside `main.dart` does - this time not for just running the app as usual but for running an automated Patrol test.

```dart
patrolTest(
  'signs in, triggers a notification, and taps on it',
  ($) async {
	  initApp();
    await $.pumpWidgetAndSettle(const MainApp());
  },
);
```

Hot-restarting the test by typing “r” into the terminal won’t really do much since we’re not yet performing any user-like actions but you will at least see the sign in page for a brief moment before the test finishes.

Let’s now perform some action! We know we have to sign in if we want to continue to the home screen. First, we have to type in both email and password. There are multiple ways to find widgets on the screen - by widget type, by text and lastly by key.

Although it’s not the best practice, we’re first going to find the fields by type. Both are of type `TextFormField` but there are two of them on the screen so the following won’t work.

```dart
patrolTest(
  'signs in, triggers a notification, and taps on it',
  ($) async {
	  initApp();
    await $.pumpWidgetAndSettle(const MainApp());
    await $(TextFormField).enterText('test@email.com');
    await $(TextFormField).enterText('password');
  },
);
```

That’s because finders always find the first matching widget so both the email address and password are entered into the same field - in this case, the email field.

If multiple widgets on a screen match the finder, we can tell Patrol which one we want by specifying its index in the list of all found widgets from top to bottom like this:

```dart
patrolTest(
  'signs in, triggers a notification, and taps on it',
  ($) async {
	  initApp();
    await $.pumpWidgetAndSettle(const MainApp());
    await $(TextFormField).enterText('test@email.com');
    await $(TextFormField).at(1).enterText('password');
  },
);
```

We can use a text finder to tap on the “Sign in” button.

```dart
patrolTest(
  'signs in, triggers a notification, and taps on it',
  ($) async {
	  initApp();
    await $.pumpWidgetAndSettle(const MainApp());
    await $(TextFormField).enterText('test@email.com');
    await $(TextFormField).at(1).enterText('password');
    await $('Sign in').tap();
  },
);
```

Hot-restarting the test will now take you all the way to the home page from which we will want to trigger the notification.

As you can imagine though, using type and text finders in any app that’s just a bit more complex will result in a huge mess. The recommended approach is to always find your widgets by their `Key`. There are currently no keys specified for these widgets so let’s change that. In `sign_in_page.dart` pass in the following into the `TextFormFields` and `ElevatedButton`:

```dart
class SignInPage extends StatelessWidget {
  const SignInPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      ...
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextFormField(
                key: const Key('emailTextField'),
                decoration: const InputDecoration(
                  labelText: 'Email',
                ),
                ...
              ),
              const SizedBox(height: 16),
              TextFormField(
                key: const Key('passwordTextField'),
                decoration: const InputDecoration(
                  labelText: 'Password',
                ),
                ...
              ),
              const SizedBox(height: 16),
              Builder(builder: (context) {
                return ElevatedButton(
                  key: const Key('signInButton'),
                  ...
                  child: const Text('Sign in'),
                );
              }),
            ],
          ),
        ),
      ),
    );
  }
}
```

With the keys in place, we can now rewrite our test code to use `Key` finders. The simplest approach is to prefix the key’s value with a hash symbol. For this approach to work, your keys mustn’t contain any invalid characters such as spaces.

```dart
patrolTest(
  'signs in, triggers a notification, and taps on it',
  ($) async {
	  initApp();
    await $.pumpWidgetAndSettle(const MainApp());
    await $(#emailTextField).enterText('test@email.com');
    await $(#passwordTextField).enterText('password');
    await $(#signInButton).tap();
  },
);
```

Looking at this test code again, it’s certain we can do better. Why? We’ve just added code duplication to our codebase! The key values in `sign_in_page.dart` and in `app_test.dart` are fully duplicated and if we change one, the other won’t be automatically updated, thus breaking our tests.

That’s why production-grade apps should have a single source for all the `Keys` exposed as a global final variable inside `integration_test_keys.dart`. That’s going to look as follows if we already take into account the home page which we want to test next.

```dart
import 'package:flutter/foundation.dart';

class SignInPageKeys {
  final emailTextField = const Key('emailTextField');
  final passwordTextField = const Key('passwordTextField');
  final signInButton = const Key('signInButton');
}

class HomePageKeys {
  final notificationIcon = const Key('notificationIcon');
  final successSnackbar = const Key('successSnackbar');
}

class Keys {
  final signInPage = SignInPageKeys();
  final homePage = HomePageKeys();
}

final keys = Keys();
```

  Feel free to put your page-specific key classes (e.g. `SignInPageKeys`) into separate files in more complex apps.

The updated `sign_in_page.dart` code will now look like this:

```dart
class SignInPage extends StatelessWidget {
  const SignInPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      ...
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextFormField(
                key: keys.signInPage.emailTextField,
                decoration: const InputDecoration(
                  labelText: 'Email',
                ),
                ...
              ),
              const SizedBox(height: 16),
              TextFormField(
                key: keys.signInPage.passwordTextField,
                decoration: const InputDecoration(
                  labelText: 'Password',
                ),
                ...
              ),
              const SizedBox(height: 16),
              Builder(builder: (context) {
                return ElevatedButton(
                  key: keys.signInPage.signInButton,
                  ...
                  child: const Text('Sign in'),
                );
              }),
            ],
          ),
        ),
      ),
    );
  }
}
```

The test code will now also use the `keys` global final variable instead of the hash symbol notation:

```dart
patrolTest(
  'signs in, triggers a notification, and taps on it',
  ($) async {
	  initApp();
    await $.pumpWidgetAndSettle(const MainApp());
    await $(keys.signInPage.emailTextField).enterText('test@email.com');
    await $(keys.signInPage.passwordTextField).enterText('password');
    await $(keys.signInPage.signInButton).tap();
  },
);
```

Hot-restarting the test won’t show any change in its functionality but it sure is more maintainable and easier to work with.

### Home Page

First, let’s add the keys we’ve already created to the `IconButton` and the `SnackBar` shown when the notification has been tapped.

```dart
class HomePage extends StatefulWidget {
  ...
}

class _HomePageState extends State<HomePage> {
  ...

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
        actions: [
          IconButton(
            key: keys.homePage.notificationIcon,
            icon: const Icon(Icons.notification_add),
            onPressed: () {
              triggerLocalNotification(
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      key: keys.homePage.successSnackbar,
                      content: const Text('Notification was tapped!'),
                    ),
                  );
                },
                onError: () {
                  ...
                },
              );
            },
          ),
        ],
      ),
      ...
    );
  }
}
```

The first thing the user sees when first navigating to the `HomePage` is a notifications permission dialog. We need to accept it from within the test. Patrol’s native automation makes this as easy as it gets.

  Native automation allows you to interact with the OS your Flutter app is running on. Patrol currently supports Android, iOS and macOS native interactions. [Learn more from the docs]

```dart
patrolTest(
  'signs in, triggers a notification, and taps on it',
  ($) async {
	  initApp();
    await $.pumpWidgetAndSettle(const MainApp());
    await $(keys.signInPage.emailTextField).enterText('test@email.com');
    await $(keys.signInPage.passwordTextField).enterText('password');
    await $(keys.signInPage.signInButton).tap();
    await $.platform.mobile.grantPermissionWhenInUse();
  },
);
```

Hot-restarting the test will work wonderfully the first time, however, once the permission has already been granted, calling `grantPermissionWhenInUse()` will fail. This is not going to be an issue if you use Patrol as a part of your CI/CD process since everytime you test with Patrol there, the app will be built from scratch and no permission will be granted yet. But when we’re writing the test locally with `patrol develop` command, we need to make sure that the permission dialog is visible before trying to accept it.

```dart
patrolTest(
  'signs in, triggers a notification, and taps on it',
  ($) async {
	  initApp();
    await $.pumpWidgetAndSettle(const MainApp());
    await $(keys.signInPage.emailTextField).enterText('test@email.com');
    await $(keys.signInPage.passwordTextField).enterText('password');
    await $(keys.signInPage.signInButton).tap();
    if (await $.platform.mobile.isPermissionDialogVisible()) {
      await $.platform.mobile.grantPermissionWhenInUse();
    }
  },
);
```

  It’s generally a bad practice to add any branching logic within your tests and you should be 100% certain that it cannot introduce any test flakiness before doing so. Checking if a permission dialog is visible is an example of a proper use of branching logic.

Next up, we want to tap on the notification icon button and then go to the device home screen to test the notification while the app is running in the background.

```dart
patrolTest(
  'signs in, triggers a notification, and taps on it',
  ($) async {
	  initApp();
    await $.pumpWidgetAndSettle(const MainApp());
    await $(keys.signInPage.emailTextField).enterText('test@email.com');
    await $(keys.signInPage.passwordTextField).enterText('password');
    await $(keys.signInPage.signInButton).tap();
    if (await $.platform.mobile.isPermissionDialogVisible()) {
      await $.platform.mobile.grantPermissionWhenInUse();
    }
    await $(keys.homePage.notificationIcon).tap();
    await $.platform.mobile.pressHome();
  },
);
```

Once we’re on the home screen, we want to open the notification shade and tap on the notification we get from our app. You can either tap on a notification by index or by finding a text. We know that the title of our notification is “Patrol says hello!” so let’s do the latter.

```dart
patrolTest(
  'signs in, triggers a notification, and taps on it',
  ($) async {
    initApp();
    await $.pumpWidgetAndSettle(const MainApp());
    await $(keys.signInPage.emailTextField).enterText('test@email.com');
    await $(keys.signInPage.passwordTextField).enterText('password');
    await $(keys.signInPage.signInButton).tap();
    if (await $.platform.mobile.isPermissionDialogVisible()) {
      await $.platform.mobile.grantPermissionWhenInUse();
    }
    await $(keys.homePage.notificationIcon).tap();
    await $.platform.mobile.pressHome();
    await $.platform.mobile.openNotifications();
    await $.platform.mobile.tapOnNotificationBySelector(
      Selector(textContains: 'Patrol says hello!'),
    );
  },
);
```

Since the notification is delayed by 3 seconds, we have to provide a timeout that’s at least as long in order to wait for the notification to appear - 5 seconds should do the trick here.

```dart
patrolTest(
  'signs in, triggers a notification, and taps on it',
  ($) async {
    ...
    await $.platform.mobile.openNotifications();
    await $.platform.mobile.tapOnNotificationBySelector(
      Selector(textContains: 'Patrol says hello!'),
      timeout: const Duration(seconds: 5),
    );
  },
);
```

Lastly, we want to check if the snackbar has been shown after tapping on a notification. We can call `waitUntilVisible()` after selecting it with its key.

```dart
patrolTest(
  'signs in, triggers a notification, and taps on it',
  ($) async {
    initApp();
    await $.pumpWidgetAndSettle(const MainApp());
    await $(keys.signInPage.emailTextField).enterText('test@email.com');
    await $(keys.signInPage.passwordTextField).enterText('password');
    await $(keys.signInPage.signInButton).tap();
    if (await $.platform.mobile.isPermissionDialogVisible()) {
      await $.platform.mobile.grantPermissionWhenInUse();
    }
    await $(keys.homePage.notificationIcon).tap();
    await $.platform.mobile.pressHome();
    await $.platform.mobile.openNotifications();
    await $.platform.mobile.tapOnNotificationBySelector(
      Selector(textContains: 'Patrol says hello!'),
      timeout: const Duration(seconds: 5),
    );
    $(keys.homePage.successSnackbar).waitUntilVisible();
  },
);
```

And just like that, we have now tested the whole flow of the app with Patrol! If any part of the logic breaks, this test will notify us about that sooner than our real users do and that’s what we’re all after!

[install the Patrol CLI]: https://pub.dev/packages/patrol_cli#installation

[Patrol Setup Docs]: https://patrol.leancode.co/documentation

[STARTER PROJECT]: https://github.com/ResoCoder/patrol-basics-tutorial

[Learn more from the docs]: https://patrol.leancode.co/documentation/native/overview

## Disabling/enabling Bluetooth

In this video we show you how to toggle Bluetooth using Patrol framework.

Here you can find the code of this test and try it out by yourself.

```dart title="patrol_test/bluetooth_test.dart"
import 'package:example/main.dart';
import 'package:patrol/patrol.dart';

void main() {
  patrolTest(
    'disable and enable bluetooth',
    ($) async {
      await $.pumpWidgetAndSettle(const MyApp());

      await Future<void>.delayed(const Duration(seconds: 2));
      await $.platform.mobile.openQuickSettings();
      await $.platform.mobile.disableBluetooth();
      await Future<void>.delayed(const Duration(seconds: 4));
      await $.platform.mobile.enableBluetooth();
      await Future<void>.delayed(const Duration(seconds: 4));
    },
  );
}
```

## Granting camera permission

In this video we show you how to grant camera permission using Patrol framework.

Here you can find the code of this test and try it out by yourself.

```dart title="patrol_test/grant_camera_permission_test.dart"
import 'package:permission_handler/permission_handler.dart';
import './common.dart';

void main() {
  patrolTest('grants camera permission', ($) async {
    await createApp($);

    await $('Open permissions screen').scrollTo().tap();

    if (!await Permission.camera.isGranted) {
      await $('Request camera permission').tap();

      if (await $.platform.mobile.isPermissionDialogVisible()) {
        await Future<void>.delayed(const Duration(seconds: 1));
        await $.platform.mobile.grantPermissionWhenInUse();
        await $.pump();
      }
    }

    await Future<void>.delayed(const Duration(seconds: 4));
  });
}

```

## Pick images from gallery

Patrol provides functionality to pick one or many images from the Android and iOS gallery using the `pickImageFromGallery` or `pickMultipleImagesFromGallery` methods from the native automator.

  Due to differences between devices and gallery apps, this method may not work on 100% of devices, but it should work on most. If the device you are testing on is not working with the default selectors, you can provide your own selectors.
  To get native selectors, you can use the [Patrol DevTools Extension](https://patrol.leancode.co/documentation/patrol-devtools-extension).

## Pick an image from gallery

This method performs the following actions:

1. Selects an image (by default, the first image or the one at the provided index).
2. Confirm the selection if needed (some android devices require this step).

| Platform                   | Selector (default)                                                                                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Physical/Emulator Android  | `com.google.android.documentsui:id/icon_thumb` (API \< 34) or `com.google.android.providers.media.module:id/icon_thumbnail` (API 34+)                        |
| Simulator and Physical iOS | `IOSElementType.image` (we add +2 for simulators and +1 for physical devices to the index, as image finders start from index 1 or 2 depending on the device) |

  This method should work without custom selectors on iOS devices. For Android, it should work with most emulators and Pixel physical devices.

### Examples

When you are using supported devices, you can use this method without any additional arguments:

```dart
import 'package:example/main.dart';
import 'package:patrol/patrol.dart';

void main() {
  patrolTest(
    'Pick an image from gallery on Android or iOS',
    ($) async {
      await $.pumpWidgetAndSettle(const MyApp());
      await $.tap(#addPhotoFromGalleryButton); // Opens the gallery picker in your app
      await $.platform.mobile.grantPermissionWhenInUse(); // Some devices require permission to be granted before picking an image
      await $.platform.mobile.pickImageFromGallery(index: 0); // Picks the first image from the gallery
    },
  );
}
```

When you are using unsupported devices, you can provide your own selectors:

```dart
import 'package:example/main.dart';
import 'package:patrol/patrol.dart';

void main() {
  patrolTest(
    'Pick an image from gallery with custom selectors',
    ($) async {
      await $.pumpWidgetAndSettle(const MyApp());
      await $.tap(#addPhotoFromGalleryButton); // Opens the gallery picker in your app
      await $.platform.mobile.grantPermissionWhenInUse(); // Some devices require permission to be granted before picking an image
      await $.platform.mobile.pickImageFromGallery(
        index: 1,
        imageSelector: NativeSelector(
          android: AndroidSelector(
            resourceName: 'com.oplus.gallery:id/image',
          ),
          ios: IOSSelector(label: 'Photo'),
        ),
      );
    },
  );
}
```

## Pick multiple images from gallery

This method performs the following actions:

1. Selects multiple images (user needs to specify indexes of images to select).
2. Confirm the selection.

The table below shows the default native selectors that the `pickMultipleImagesFromGallery()` method uses internally for each platform:

| Platform                          | Selector (default)                                                                                                                        |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Physical/Emulator Android images  | `com.google.android.documentsui:id/icon_thumb` (API \< 34) or `com.google.android.providers.media.module:id/icon_thumbnail` (API 34+)     |
| Simulator and Physical iOS images | `IOSElementType.image`                                                                                                                    |
| iOS Confirm button                | `IOSElementType.button` with label `"Add"`                                                                                                |
| Android Confirm button            | `com.google.android.providers.media.module:id/button_add` (API 34+) or `com.google.android.documentsui:id/action_menu_select` (API \< 34) |

  This method should work without custom selectors on iOS devices. For Android, it should work with most emulators and Pixel physical devices.

### Examples

When you are using supported devices, you can use this method without any additional arguments:

```dart
import 'package:example/main.dart';
import 'package:patrol/patrol.dart';

void main() {
  patrolTest(
    'Pick multiple images from gallery',
    ($) async {
      await $.pumpWidgetAndSettle(const MyApp());
      await $.tap(#addMultiplePhotosFromGalleryButton); // Opens the gallery picker in your app
      await $.platform.mobile.grantPermissionWhenInUse(); // Some devices require permission to be granted before picking an image
      await $.platform.mobile.pickMultipleImagesFromGallery(imageIndexes: [0, 1]); // Picks the first and second images from the gallery
    },
  );
}
```

When you are using unsupported devices, you can provide your own selectors:

```dart
import 'package:example/main.dart';
import 'package:patrol/patrol.dart';

void main() {
  patrolTest(
    'Pick multiple images from gallery with custom selectors',
    ($) async {
      await $.pumpWidgetAndSettle(const MyApp());
      await $.tap(#addMultiplePhotosFromGalleryButton); // Opens the gallery picker in your app
      await $.platform.mobile.grantPermissionWhenInUse(); // Some devices require permission to be granted before picking an image
      await $.platform.mobile.pickMultipleImagesFromGallery(
        imageIndexes: [0, 1],
        imageSelector: NativeSelector(
          android: AndroidSelector(
            resourceName: 'com.oplus.gallery:id/image',
          ),
          ios: IOSSelector(label: 'Photo'),
        ),
      );
    },
  );
}
```

## Pull to refresh

Patrol provides a function for pull-to-refresh gesture (`pullToRefresh`), allowing you to use refresh functionality in your tests.

## Basic usage

The `pullToRefresh` method is available through the platform automator:

```dart
await $.platform.mobile.pullToRefresh();
```

By default, this performs a pull-to-refresh gesture from the center of the screen (0.5, 0.5) to the bottom center (0.5, 0.9).

## Simulating real scenarios

Sometimes you need to pull to refresh multiple times until a specific element appears. Here's how you can do it:

```dart
const maxAttempts = 5;
var attempt = 0;
while (attempt < maxAttempts) {
  // Perform pull to refresh
  await $.platform.mobile.pullToRefresh();

  // Wait for the refresh to complete
  await $.pumpAndSettle();

  // Check if the target element exists
  if ($(K.awaitedElement).exists) {
    break;
  }
  
  attempt++;
}
// Verify if the element is visible
await $(K.awaitedElement).waitUntilVisible();
```

## Tips

* Increase the `steps` value for a slower gesture
* Since this function is native, it does not benefit from the default `pumpAndSettle` being performed automatically.
* Adjust coordinates based on your app's layout (e.g., when the center of the screen is not part of the scrollable area, or when testing horizontal lists that implement pull-to-refresh)

```dart
// Pull to refresh horizontally (swipe left)
await $.platform.mobile.pullToRefresh(
  start: Offset(0.5, 0.5),
  end: Offset(0.1, 0.5),
);
```

## Take photo using camera

Patrol provides functionality to take a photo using the Android and iOS camera.

  Due to many differences between devices, this method will not work on 100% of devices but should work on most of them. If the device that you are testing on is not working with this command, you can provide your own selectors. To get native selectors, you can use [Patrol DevTools Extension](https://patrol.leancode.co/documentation/patrol-devtools-extension).

## How it works

This method does two actions:

1. Tap on shutter button
2. Tap on confirm button

The table below shows the native selectors that the `takeCameraPhoto()` method uses internally for each platform:

| Platform                   | Shutter Button                                      | Confirm Button                                   |
| -------------------------- | --------------------------------------------------- | ------------------------------------------------ |
| Physical Android           | `com.google.android.GoogleCamera:id/shutter_button` | `com.google.android.GoogleCamera:id/done_button` |
| Emulator Android           | `com.android.camera2:id/shutter_button`             | `com.android.camera2:id/done_button`             |
| Simulator and Physical iOS | `PhotoCapture`                                      | `Done`                                           |

  This method should work without custom selectors on iOS devices. For Android, it should work with most emulators and Pixel physical devices.

## Examples

When you are using supported devices, you can use this method without any additional arguments:

```dart
import 'package:example/main.dart';
import 'package:patrol/patrol.dart';

void main() {
  patrolTest(
    'Take a photo using android or iOS camera',
    ($) async {
      await $.pumpWidgetAndSettle(const MyApp());
      await $.tap(#addPhotoButton); // Clicks a photo button inside your app to open camera
      await $.platform.mobile.grantPermissionWhenInUse(); // Some devices require permission to be granted before taking a photo
      await $.platform.mobile.takeCameraPhoto(); // Takes a photo using the camera
    },
  );
}
```

When you are using unsupported devices, you can provide your own selectors:

```dart
import 'package:example/main.dart';
import 'package:patrol/patrol.dart';

void main() {
  patrolTest(
    'Take a photo using android or iOS camera with custom selectors',
    ($) async {
      await $.pumpWidgetAndSettle(const MyApp());
      await $.tap(#addPhotoButton); // Clicks a photo button inside your app to open camera
      await $.platform.mobile.grantPermissionWhenInUse(); // Some devices require permission to be granted before taking a photo
      await $.platform.mobile.takeCameraPhoto(shutterButtonSelector: NativeSelector(
        android: AndroidSelector(
          resourceName: 'com.oplus.camera:id/shutter_button',
        ),
        ios: IOSSelector(label: 'Take Picture'),
      ),
      doneButtonSelector: NativeSelector(
        android: AndroidSelector(
          resourceName: 'com.oplus.camera:id/done_button',
        ),
        ios: IOSSelector(label: 'Done'),
      ),
      );
    },
  );
}
```

## Patrol tags

Patrol tags allow you to organize and selectively run your patrol tests. You can assign tags to individual tests and then use those tags to filter which tests to run or exclude.
By design, patrol tags should work the same as flutter test tags.

## Defining tags in tests

You can assign tags to your Patrol tests using the `tags` parameter. Tags are defined as a list of strings:

```dart title="patrol_test/example_test.dart"
import 'package:flutter/material.dart';
import 'package:patrol/patrol.dart';

void main() {

  patrolTest(
    'short test with two tags',
    tags: ['smoke', 'regression'],
    ($) async {
      await createApp($);

      await $(FloatingActionButton).tap();
      expect($(#counterText).text, '1');
      await $(FloatingActionButton).tap();
      expect($(#counterText).text, '2');
    },
  );

  patrolTest(
    'short test with tag',
    tags: ['smoke'],
    ($) async {
      await createApp($);

      await $(FloatingActionButton).tap();
      expect($(#counterText).text, '1');

      await $(#textField).enterText('Hello, Flutter!');
      expect($('Hello, Flutter!'), findsOneWidget);
    },
  );
}
```

## Running tests with tags

Use the `--tags` option to run only tests that have specific tags:

```bash
## Run tests with the 'smoke' tag
patrol test --tags smoke

## Run tests with either 'smoke' or 'regression' tag
patrol test --tags='smoke||regression'

## Run tests with both 'login' and 'smoke' tags
patrol test --tags='(login && smoke)'
```

## Excluding tests with tags

Use the `--exclude-tags` option to exclude tests that have specific tags:

```bash
## Exclude tests with the 'regression' tag
patrol test --exclude-tags regression

## Exclude tests with either 'smoke' or 'regression' tag
patrol test --exclude-tags='(smoke||regression)'
```

## Tag expression syntax

Patrol supports complex tag expressions using logical operators:

### Basic operators

* `||` - OR operator (run tests with either tag)
* `&&` - AND operator (run tests with both tags)
* `!` - NOT operator (exclude tests with this tag)

Note that tags must be valid Dart identifiers, although they may also contain hyphens.
For more information about tag rules, see: [https://pub.dev/packages/test#tagging-tests](https://pub.dev/packages/test#tagging-tests)

### Examples

```bash
## Run tests that have either 'smoke' OR 'regression' tag
patrol test --tags='smoke||regression'

## Run tests that have BOTH 'login' AND 'smoke' tags
patrol test --tags='(login && smoke)'

## Run tests with 'payment' OR 'navigation' tag, but NOT 'regression'
patrol test --tags='(payment || navigation) && !regression'

## Combine --tags with --exclude-tags
patrol test --tags='smoke||regression' --exclude-tags='slow'

## Complex expression: (login OR payment) AND (smoke OR regression)
patrol test --tags='((login || payment) && (smoke || regression))'
```

## Combining with other options

You can combine tag filtering with other Patrol CLI options:

```
patrol test --target patrol_test/login_test.dart --tags smoke
```
