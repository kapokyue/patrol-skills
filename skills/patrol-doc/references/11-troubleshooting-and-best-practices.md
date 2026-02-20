# 11 Troubleshooting And Best Practices

Generated from curated sections of `patrol-llms-full.txt`.

# Effective Patrol

Over the past months, we've written many Patrol tests and often learned the hard
way what works well and what doesn't. We're sharing our findings hoping that
they'll help you write robust tests.

  This document follows 

  [RFC 2119][rfc2119]

  .

### PREFER using keys to find widgets

Patrol's custom finders are very powerful, and you might often be inclined to
find the widget you want in a variety of ways. While we're encouraging you to
explore and play with Patrol's custom finders, we are quite confident that keys
are the best way to find widgets.

**Why not strings?**

At first, strings might seem like a good way to find widgets.

They'll get increasingly annoying to work with as your app grows and changes,
for example, when the strings in your app change.

Using strings stops making any sense when you have more than 1 language in your
app. Using strings in such case is asking for trouble.

**Why not classes?**

There are 2 problems with using classes.

First is that they hurt your test's readability. You want to tap on *the* login
button or enter text into *the* username field. You don't want to tap on, say,
the third button and enter text into the second text field.

The second problem is that classes are almost always an implementation detail.
As a tester, you shouldn't care if something is a `TextButton` or an
`OutlineButton`. You care that it is *the* login button, and you want to tap on
it. In most cases, that login button should have a key.

Let's consider this simple example:

```dart
await $(LoginForm).$(Button).at(1).tap(); // taps on the second ("login") button
```

This works, but the code is not very self-explanatory. To make it understandable
at glance, you had to add a comment.

But if you assigned a key to the login button, the above could be simplified to:

```dart
await $(#loginButton).tap();
```

Much better!

Let's see another example:

```dart
await $(Select<String>).tap(); // taps on the first Select<String>
```

If the type parameter is changed from `String` to, for example, some specialized
`PersonData` model, that finder won't find anything. You'd have to update it to:

```dart
await $(Select<PersonTile>).tap();
```

You had to change your test, even though nothing changed from the user's
perspective. This is usually a sign that you rely too much on classes to find
widgets.

This whole section could be summed up to the simple maxim:

> Have tester's mindset.

Treat your finders as if they were the tester's eyes.

### CONSIDER having a file where all keys are defined

The number of keys will get bigger as your app grows and you write more tests.
To keep track of them, it's a good idea to keep all keys in, say,
`lib/keys.dart` file.

```dart title="lib/keys.dart"
import 'package:flutter/foundation.dart';

typedef K = Keys;

class Keys {
  const Keys();

  static const usernameTextField = Key('usernameTextField');
  static const passwordTextField = Key('passwordTextField');
  static const loginButton = Key('loginButton');
  static const forgotPasswordButton = Key('forgotPasswordButton');
  static const privacyPolicyLink = Key('privacyPolicyLink');
}
```

Then you can use it in your app's and tests' code:

```dart title="In app UI code"
@override
Widget build(BuildContext context) {
  return Column(
    children: [
      /// some widgets
      TextField(
        key: K.usernameTextField,
        // some other TextField properties
      ),
      // more widgets
    ],
  );
}
```

```dart title="In app test code"
void main() {
  patrolTest('logs in', (PatrolIntegrationTester $) {
    // some code
    await $(K.usernameTextField).enterText('CoolGuy');
    // more code
  });
}
```

This is a good way to make sure that the same keys are used in app and tests. No
more typos!

### PREFER having one test path

Good tests test one feature, and test it well (this applies to all tests, not
only Patrol tests). This is often called the "main path". Try to introduce as
little condional logic as possible to help keep the main path straight. In
practice, this usually comes down to having as few `if`s as possible.

Keeping your test code simple and to the point will also help you in debugging
it.

### DO add a good test description explaining the test's purpose

If your app is non-trivial, your Patrol test will become long pretty quickly.
You may be sure now that you'll always remember what the 200 line long test
you've just written does and are (rightfully) very proud of it.

Believe us, in 3 months you will not remember what your test does. This is why
the first argument to `patrolTest` is the test description. Use it well!

```dart
// GOOD
import 'package:awesome_app/main.dart';
import 'package:patrol/patrol.dart';

void main() {
  patrolTest(
    'signs up for the newsletter and receives a reward',
    ($) async {
      await $.pumpWidgetAndSettle(AwesomeApp());

      await $(#phoneNumber).enterText('800-555-0199');
      await $(#loginButton).tap();

      // more code
    },
  );
}
```

```dart
// BAD
void main() {
  patrolTest(
    'test',
    ($) async {
      await $.pumpWidgetAndSettle(AwesomeApp());

      await $(#phoneNumber).enterText('800-555-0199');
      await $(#loginButton).tap();

      // more code
    },
  );
}
```

[rfc2119]: https://www.ietf.org/rfc/rfc2119.txt

# Tips and tricks

### Inspecting native view hierarchy

It's hard to tap on or enter text into a view you don't know how to refer to. In
such situation we recommend doing a native view hierarchy dump and finding the
properties of the view you want to act on.

**Android**

First, perform a native view hierarchy dump using `adb`:

```
adb shell uiautomator dump
```

Then, copy the dump file from the device to your machine:

```
adb pull /sdcard/window_dump.xml .
```

**iOS**

The easiest way to perform the native view hierarchy dumb on iOS is to use the
[idb] tool.

Once you have [idb] installed, perform a dump:

```
idb ui describe-all
```

### Configuring test directory

By default, Patrol looks for tests in the `patrol_test/` directory.
This default was changed from `integration_test/` to avoid conflicts with Flutter's official integration testing plugin
and to give Patrol tests their own dedicated space. This change was introduced in Patrol 4.0.0.

#### Using custom test directory

You can configure Patrol to use a different directory by adding `test_directory` to your `pubspec.yaml`:

```yaml title="pubspec.yaml"
patrol:
  app_name: My App
  test_directory: my_custom_tests  # Custom directory
  android:
    package_name: com.example.myapp
  ios:
    bundle_id: com.example.MyApp
```

#### Migrating from integration\_test directory

If you have existing Patrol tests in the `integration_test/` directory, you have two options:

**Option 1: Rename integration\_test directory to patrol\_test**

**Option 2: Configure Patrol to use integration\_test**

```yaml title="pubspec.yaml"
patrol:
  app_name: My App
  test_directory: integration_test  # Keep using old directory
  android:
    package_name: com.example.myapp
  ios:
    bundle_id: com.example.MyApp
```

  Non-patrol integration tests should remain in the integration\_test directory.

### Avoiding hardcoding credentials in tests

It's a bad practice to hardcode data such as emails, usernames, and passwords in
test code.

```dart
await $(#nameTextField).enterText('Bartek'); // bad!
await $(#passwordTextField).enterText('ny4ncat'); // bad as well!
```

To fix this, we recommend removing the hardcoded credentials from test code and
providing them through the environment:

```dart
await $(#nameTextField).enterText(const String.fromEnvironment('USERNAME'));
await $(#passwordTextField).enterText(const String.fromEnvironment('PASSWORD'));
```

> Make sure that you're using `const` here because of [issue #55870][55870].

To set `USERNAME` and `PASSWORD`, use `--dart-define`:

```
patrol test --dart-define 'USERNAME=Bartek' --dart-define 'PASSWORD=ny4ncat'
```

Alternatively you can create a `.patrol.env` file in your project's root. Comments
are supported using the `#` symbol and can be inline or on their own line. Here's
an example:

```
$ cat .patrol.env
# Add your username here
EMAIL=user@example.com
PASSWORD=ny4ncat # The password for the API
```

### Granting sensitive permission through the Settings app

Some particularly sensitive permissions (such as access to background location
or controlling the Do Not Disturb feature) cannot be requested in the permission
dialog like most of the common permissions. Instead, you have to ask the user to
go to the Settings app and grant your app the permission you need.

Testing such flows is not as simple as simply granting normal permission, but
it's totally possible with Patrol.

Below we present you with a snippet that will make the built-in Camera app have
access to the Do Not Disturb feature on Android. Let's assume that the Settings
app on the device we want to run the tests on looks like this:

And here's the code:

```dart
await $.platform.mobile.tap(Selector(text: 'Camera')); // tap on the list tile
await $.platform.mobile.tap(Selector(text: 'ALLOW')); // handle the confirmation dialog
await $.platform.mobile.pressBack(); // go back to the app under test
```

Please note that the UI of the Settings app differs across operating systems,
their versions, and OEM flavors (in case of Android). You'll have to handle all
edge cases yourself.

### Ignoring exceptions

If an exception is thrown during a test, it is marked as failed. This is
Flutter's default behavior and it's usually good – after all, it's better to fix
the cause of a problem instead of ignoring it.

That said, sometimes you do have a legitimate reason to ignore an exception.
This can be accomplished with the help of the
[WidgetTester.takeException()][take_exception] method, which returns the last
exception that occurred and removes it from the internal list of uncaught
exceptions, so that it won't mark the test as failed. To use it, just call it
once:

```dart
final widgetTester = $.tester;
widgetTester.takeException();
```

If more than a single exception is thrown during the test and you want to ignore
all of them, the below snippet should come in handy:

```dart
var exceptionCount = 0;
dynamic exception = $.tester.takeException();
while (exception != null) {
  exceptionCount++;
  exception = $.tester.takeException();
}
if (exceptionCount != 0) {
  $.log('Warning: $exceptionCount exceptions were ignored');
}
```

### Handling permission dialogs before the main app widget is pumped

Sometimes you might want to manually request permissions in the test before the
main app widget is pumped. Let's say that you're using the [geolocator] package:

```dart
final permission = await Geolocator.requestPermission();
final position = await Geolocator.getCurrentPosition();
await $.pumpWidgetAndSettle(MyApp(position: position));
```

In such case, first call the `requestPermission()` method, but instead of
awaiting it, assign the `Future` it returns to some `final`. Then, use Patrol to
grant the permissions, and finally, await the `Future` from the first step:

```dart
// 1. request the permission
final permissionRequestFuture = Geolocator.requestPermission();
// 2. grant the permission using Patrol
await $.platform.mobile.grantPermissionWhenInUse();
// 3. wait for permission being granted
final permissionRequestResult = await permissionRequestFuture;
expect(permissionRequestResult, equals(LocationPermission.whileInUse));
final position = await Geolocator.getCurrentPosition();
await $.pumpWidgetAndSettle(MyApp(position: position));
```

See also:

* [Patrol issue #628]

[patrol issue #628]: https://github.com/leancodepl/patrol/issues/628

[geolocator]: https://pub.dev/packages/geolocator

[idb]: https://github.com/facebook/idb

[take_exception]: https://api.flutter.dev/flutter/flutter_test/WidgetTester/takeException.html

[55870]: https://github.com/flutter/flutter/issues/55870
