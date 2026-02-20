# Cli Commands


## build

### Synopsis

Build app binaries for integration testing.

```
patrol build android
patrol build ios
```

To see all available options and flags, run `patrol build android --help` or
`patrol build ios --help`.

  For `patrol build` to work, you must complete [native setup].

### Description

`patrol build` is useful if you want to run test on CI, for example on Firebase
Test Lab. It works the same as `patrol test`, except that it does not run tests.

`patrol build` builds apps in debug mode by default.

  To run tests on a physical iOS device on a device farm, the apps have to be
  built in release mode. To do so, pass the `--release` flag.

### Examples

**To build a single test for Android in debug mode**

```
patrol build android --target patrol_test/example_test.dart
```

or alternatively (but redundantly):

```
patrol build android --target patrol_test/example_test.dart --debug
```

**To build all tests for Android in debug mode**

```
patrol build android
```

**To build a single test for iOS device in release mode**

```
patrol build ios --target patrol_test/example_test.dart --release
```

**To build a single test for iOS simulator in debug mode**

```
patrol build ios --target patrol_test/example_test.dart --debug
```

**To build with custom build name and number**

```
patrol build android --build-name=1.2.3 --build-number=123
patrol build ios --build-name=1.2.3 --build-number=123  --release
```

**To build with full isolation between tests**

```
patrol build ios --full-isolation
```

The `--full-isolation` flag enables full isolation between test runs on iOS Simulator.

### Under the hood

The `patrol build` command walks through hierarchy of the `patrol_test`
directory and finds all files that end with `_test.dart`, and then creates an
additional "test bundle" file that references all the tests it found. Thanks to
this, all tests are built into a single app binary - only a single build is
required, which greatly reduces time spent on building. Then, it runs a new app
process for every test, improving isolation between tests and enabling sharding.

We call this feature **advanced test bundling**. It provides deep and seamless
integration with existing Android and iOS testing tools. It also fixes some
long-standing Flutter issues:

* [#115751](https://github.com/flutter/flutter/issues/115751)
* [#101296](https://github.com/flutter/flutter/issues/101296)
* [#117386](https://github.com/flutter/flutter/issues/117386)

We think that **this is huge** (even though it may not look like it at first
glance). To learn more, read [the in-depth technical article][patrol_v2_article]
explaining the nuts and bolts.

[patrol_v2_article]: https://leancode.co/blog/patrol-2-0-improved-flutter-ui-testing

[native setup]: https://patrol.leancode.co/documentation

## devices

### Synopsis

List attached devices, simulators and emulators

```
patrol devices
```

To see all available options and flags, run `patrol devices --help`.

### Description

It's intended to be a simpler, Patrol-aware alternative to `flutter devices`.

## doctor

### Synopsis

Show information about installed tooling.

```
patrol doctor
```

To see all available options and flags, run `patrol doctor --help`.

## develop

### Synopsis

Develop integration tests with Hot Restart.

```
patrol develop
```

To see all available options and flags, run `patrol develop --help`.

### Description

`patrol develop` makes the development of integration tests faster and more fun,
thanks to Flutter's Hot Restart feature.

To run a test file with Hot Restart, specify the `--target` option:

```
patrol develop --target patrol_test/example_test.dart
```

This performs a build of your app, so it's usually slow.

When the build completes and the app starts, Hot Restart becomes active after a
short while. Once it is active, type **R** to trigger a Hot Restart.

You can specify custom build number and build name using the `--build-name` and `--build-number` flags.

```
patrol develop --target patrol_test/example_test.dart --build-name=1.2.3 --build-number=123
```

### Demo

### Caveats

`patrol develop` is powerful, but it has some limitations. It's important to
understand them to write correct tests.

Flutter apps consist of 2 parts: the native part and the Flutter part. **Hot
Restart restarts only the Flutter part of your app**.

When you press **R**, the Flutter part of your app is restarted – your `main()`
function is run again.

It's important to note that:

* The native part of your app is not restarted
* The app's data is not cleared
* The app is not uninstalled

Below are a few common scenarios when state of your app will probably differ
between the first and later Hot Restarts.

**No support for physical iOS**

Patrol's Hot Restart is very unreliable when running on physical iOS devices, to
the point that we consider it completely broken. This is unfortunate, but it's a
[bug on the Flutter's side](https://github.com/flutter/flutter/issues/122698).

**Permissions**

Once granted, a permissions cannot be revoked.

You have to work around this by handling both cases (of granted and not granted
permissions) in your tests.

Removing all permissions at the beginning of each test won't work - both iOS and
Android kill the app when any permission is revoked, and when the app dies, Hot
Restart stops.

**File system**

The files your app creates in its internal storage aren't cleared between hot
restarts.

For example, when some data is saved to SharedPreferences during the first
restart, it will stay around in subsequent restarts (unless it's manually
cleared).

The same goes for any data the app creates during test - photos, documents, etc.
It's your responsibility to clean them up at the right time to have a stable
environment during `patrol develop`.

**Native state**

If your app has some native code that runs only when the app is first run, it
won't be re-executed on hot restarts.

These cases are quite specific and it's hard to give advice without knowing the
context.

See also:

* [The difference between Hot Restart and Hot Reload in Flutter][so_question]

[so_question]: https://stackoverflow.com/q/61787776/7009800

## test

### Synopsis

Run integration tests.

```
patrol test
```

To see all available options and flags, run `patrol test --help`.

### Description

This command is the one use you'll be using most often.

`patrol test` does the following things:

1. Builds the app under test (AUT) and the instrumentation app
2. Installs the AUT and the instrumentation on the selected device
3. Runs the tests natively, and reports results back in native format.

Under the hood, it calls Gradle (when testing on Android) and `xcodebuild` (when
testing on iOS).

### Discussion

By default, `patrol test` runs all integration tests (files ending with
`_test.dart` located in the `patrol_test` directory). You can customize the test directory by setting `test_directory` in your `pubspec.yaml` under the `patrol` section.

To run a single test, use `--target`:

```
patrol test --target patrol_test/login_test.dart
```

You can use `--target` more than once to run multiple tests:

```
patrol test \
  --target patrol_test/login_test.dart \
  --target patrol_test/app_test.dart
```

Or alternatively:

```
patrol test --targets patrol_test/login_test.dart,patrol_test/app_test.dart
```

Test files must end with `_test.dart`. Otherwise the file is not considered a
test and is not run.

  There's no difference between 

  `--target`

   and 

  `--targets`

  .

### Tags

You can use tags to run only tests with specific tags.

First specify tags in your patrol tests:

```dart
  patrol(
    'example test with tag',
    tags: ['android'],
    ($) async {
      await createApp($);

      await $(FloatingActionButton).tap();
      expect($(#counterText).text, '1');
    },
  );

  patrol(
    'example test with two tags',
    tags: ['android', 'ios'],
    ($) async {
      await createApp($);

      await $(FloatingActionButton).tap();
      expect($(#counterText).text, '1');
    },
  );
```

Then you can run tests with the tags you specified:

```bash
patrol test --tags android
patrol test --tags=android
patrol test --tags='android||ios'
patrol test --tags='(android || ios)'
patrol test --tags='(android && tablet)'
```

You can also use `--exclude-tags` to exclude tests with specific tags:

```bash
patrol test --exclude-tags android
patrol test --exclude-tags='(android||ios)'
```

  For comprehensive information about tag syntax, complex expressions, and advanced usage, see
  the [Patrol tags documentation](https://patrol.leancode.co/documentation/patrol-tags).

### Coverage

  Coverage collection is currently not supported on macOS.

To collect coverage from patrol tests, use `--coverage`.

```
patrol test --coverage
```

The LCOV report will be saved to `/coverage/patrol_lcov.info`.

Additionally, you can exclude certain files from the report using glob patterns and `--coverage-ignore` option.
For instance,

```
patrol test --coverage --coverage-ignore="**/*.g.dart"
```

excludes all files ending with `.g.dart`.

### Build versioning

You can specify custom build number and build name using the `--build-name` and `--build-number` flags. These work
the same as in Flutter CLI:

* `--build-name`: Version name of the app. (e.g. `1.2.3`)
* `--build-number`: Version code of the app. (e.g. `123`)

```
patrol test --build-name=1.2.3 --build-number=123
patrol test --target patrol_test/login_test.dart --build-name=1.2.3 --build-number=123
```

### Isolation of test runs

To achieve full isolation between test runs:

* On Android: set `clearPackageData` to `true` in your `build.gradle` file,
* On iOS Simulator: use the `--full-isolation` flag

  This functionality is experimental on iOS and might be removed in the future releases.

```bash
patrol test --full-isolation
```

### Web Platform

Patrol supports running tests on Flutter web using Playwright. To run tests on web:

```bash
patrol test --device chrome
```

When running on web:

* Tests execute in Chromium browser via Playwright
* CLI arguments can be used to configure Playwright
* Test results are generated in `test-results/`

#### Arguments

Playwright configuration is updated with values passed to the command. This allows direct control over Playwright
features such as reporting. To see the full list of supported arguments, run `patrol test --help`.

**Note:** Some arguments are not supported on web:

* `--flavor`: Flavors are not supported for Flutter web
* `--uninstall`: Not applicable to web platform
* `--clear-permissions`: Not applicable to web platform
* `--full-isolation`: Not applicable to web platform

### Under the hood

`patrol test` basically calls `patrol build` and then runs the built app
binaries. For more info, read [docs of `patrol build`][patrol_build].

[patrol_build]: https://patrol.leancode.co/cli-commands/build

## update

### Synopsis

Update Patrol CLI to the latest version.

```
patrol update
```

To see all available options and flags, run `patrol update --help`.
