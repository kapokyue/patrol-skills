# Overview And Compatibility


## Patrol

Patrol is a powerful, open-source UI testing framework designed specifically for
Flutter apps and released in September 2022. Developed and maintained by [LeanCode][leancode],
one of the world’s leading Flutter development consultancies, Patrol builds upon
Flutter's core testing tools to enable developers to do things that were previously impossible.

## Why choose Patrol?

### Native Access, Redefined

Unlock [**native platform features**][native] right within your Flutter tests. With Patrol, you can:

* Interact with **permission dialogs**, **notifications**, and **WebViews**.
* Modify **device settings**, toggle **Wi-Fi**, and more.
* Achieve all this effortlessly using plain **Dart** code.

### Intuitive Test Writing

Say goodbye to complexity with Patrol’s custom finder system.

* Streamline your test code with a shorter, more readable, [**new custom finder system**][finders].
* Enjoy the speed and convenience of [**Hot Restart**][hot restart], which makes integration testing faster, easier, and more fun.
* Quickly inspect the currently visible Android/iOS views and discover their properties with the **Patrol DevTools extension**.

### Production-Ready Integration Testing

Patrol revolutionizes Flutter’s built-in `integration_test` plugin:

* Overcomes its limitations with **full test isolation** between tests and **sharding**.
* Delivers a robust, **production-grade solution** for your app testing needs.
* Offers **console logs** to get real-time insights during test execution.

### Compatible with Device Farms

With Patrol's native-like testing capabilities, you can  use popular device farms like:

* Firebase Test Lab
* BrowserStack
* LambdaTest
* Marathon
* emulator.wtf
* AWS Device Farm

## Trusted by LeanCode and the Flutter Community

Patrol is a fully open-source project, and we're proud to share it with the amazing
Flutter community. Patrol isn’t just a tool; it’s a commitment to quality. At LeanCode,
we use Patrol to test production-grade apps for clients across industries, and now, you can do the same!

  [Get Patrol from pub.dev now!][patrol_on_pubdev]

**Need expert help?** LeanCode offers end-to-end automated UI testing services tailored for your Flutter apps – check them out:

[<img alt="Automated UI testing services" src={__img1} placeholder="blur" />](https://leancode.co/products/automated-ui-testing-in-flutter?utm_source=patrol_page\&utm_medium=banner\&utm_campaign=service)

## More about Patrol

* Blog Post: [How Patrol fixes Flutter's official integration\_test plugin deficiencies][blog_post].
* GitHub Repository: [leancodepl/patrol][github_repo]
* Discord Channel: [Join the Patrol channel][dc_invite]
* Get a quick introduction to Patrol and see the video:

[leancode]: https://leancode.co

[native]: https://patrol.leancode.co/documentation/native/overview

[finders]: https://patrol.leancode.co/documentation/finders/overview

[hot restart]: https://patrol.leancode.co/cli-commands/develop

[patrol_on_pubdev]: https://pub.dev/packages/patrol

[dc_invite]: https://discord.com/invite/ukBK5t4EZg

[blog_post]: https://leancode.co/blog/patrol-2-0-improved-flutter-ui-testing

[github_repo]: https://github.com/leancodepl/patrol

## Improved logging and reporting is here!

We’ve made some major improvements to how you can monitor and analyze your tests! With Patrol 3.13.0 and later, you’ll get:

* Verbose logging: Test names are now displayed in real time as they’re executed!
* Detailed step reporting: See every action Patrol takes during your test execution, giving you deeper insights into the process.
* Flutter logs in console: Now you can access Flutter logs directly within the patrol test output, streamlining debugging and analysis.
  These enhancements will make it easier than ever to understand what's happening behind the code.

For a full breakdown of these updates, check out the [Logs and test results][logs] page!

[logs]: https://patrol.leancode.co/documentation/logs

## New package - patrol_finders

We're introducing [`patrol_finders`] - a new package in Patrol framework! It was
created to make it easier to use Patrol finders in widget tests.

We decided to separate out our finders mechanism to another package, so
developers who would like to use Patrol's awesome finders in their widget tests
don't need to depend on whole Patrol package. This way you can conveniently use
Patrol finders in widget or golden tests, whichever platforms you need to
support in your project!

### How to use it?

We made a short tutorial on how to use `patrol_finders` package separately in
widget tests, you can find it in [Using Patrol finders in widget tests] section.

### Does this change affect my Patrol tests?

If you have already some Patrol tests in your project, there are no breaking
changes in this release - everything works the same as before. Though you may
see some deprecation warnings in your code - you can get your code aligned with
them to prepare for future changes.

[Using Patrol finders in widget tests]: https://patrol.leancode.co/documentation/finders/finders-setup

[`patrol_finders`]: https://pub.dev/packages/patrol_finders

## Patrol 3.0 is here

Patrol 3.0 is the new major version of Patrol.

## `patrol v3` and DevTools extension

The highlight of this release is the **Patrol DevTools Extension**. We created
it to enhance your UI test development experience with `patrol develop` by
making it much easier to explore the native view hierarchy. With Patrol's new
DevTools extension, you can effortlessly inspect the currently visible
Android/iOS views and discover their properties. This information can be then
used in native selectors like `$.native.tap()`, eliminating the need for
external tools.

Patrol is one of the first packages in the whole Flutter ecosystem to have a
DevTools extension. We have started working on it as soon as the Flutter team
has announced that they're working on making DevTools extensible. We immediately
realized how powerful this feature is and how it can enable us to deliver better
UI testing experience.

This is, of course, just the beginning, and we have plans to introduce more
features in future updates of our DevTools extension.

### Changes in `patrol` v3:

The DevTools extension is not the only new feature in this release. Other
changes include:

* **Minimum Flutter version**: The minimum supported Flutter version has been
  bumped to 3.16 to make it compatible with a few breaking changes that were
  introduced to the `flutter_test` package that `patrol` and `patrol_finders`
  depend on. We hope you'll have an easy time upgrading to 3.16, but if not, you
  can always use Patrol v2 until you're ready to upgrade.

* **A few breaking changes**:
  * The `bindingType` parameter has been removed from the `patrolTest()`
    function. Now, only `PatrolBinding` is used and it's also automatically
    initialized.
  * The `nativeAutomation` parameter has also been removed from the
    `patrolTest()` function. Now `patrolTest()` implies native automation and
    you can use `patrolWidgetTest()` if you don't need it.
  * `PatrolTester` class has been renamed to `PatrolIntegrationTester`. Now
    `PatrolTester` is used with `patrolWidgetTest()` *without* native automation
    and `PatrolIntegrationTester` is used with `patrolTest()` *with* native
    automation.

* **Patrol CLI version requirement**: Patrol v3 requires Patrol CLI v2.3.0 or
  newer, so make sure to `patrol update`!

## `patrol_finders` v2

Along with `patrol` v3, we are releasing the v2 of [patrol\_finders][patrol_finders]. In case you
missed it, we split `patrol_finders` from `patrol` a few months ago in response
to our community members who loved Patrol's lean finders syntax, but weren't
interested in developing integration tests. [Here's the docs
page][patrol_finders_docs] about `patrol_finders` in case you missed it.

### Changes in `patrol_finders` v2:

* **Minimum Flutter version**: The minimum supported Flutter version of
  `patrol_finders` has been bumped to 3.16, just like in `patrol`'s case.
* The deprecated `andSettle` method has been removed from all `PatrolTester` and
  `PatrolFinder` methods like `tap()`, `enterText()`, and so on. Developers
  should now use `settlePolicy` as a replacement, which has been available since
  June.
* The default `settlePolicy` has been changed to [SettlePolicy.trySettle].

## Wrapping up

As you can see, these updates have a little bit of everything - a large new
feature, support for the latest Flutter version, and a clean-up of a few
deprecations. We encourage you to explore our new DevTools extension and look
forward to your feedback and ideas for new features as we continue to evolve the
Patrol ecosystem. Meanwhile, we're getting back to work on Patrol, with a single
goal in mind – to make it the go-to UI testing framework for Flutter apps.

[patrol_finders]: https://pub.dev/packages/patrol_finders

[patrol_finders_docs]: https://patrol.leancode.co/patrol-finders-release

[SettlePolicy.trySettle]: https://pub.dev/documentation/patrol_finders/latest/patrol_finders/SettlePolicy.html#trySettle

## New major release - Patrol 4.0

Patrol 4.0 is live! Check out our [release article on Leancode's blog](https://leancode.co/blog/patrol-4-0-release).
Read more about new features coming in this release in deep-dives articles:

* [Simplifying Flutter Web Testing: Patrol Web](https://leancode.co/blog/patrol-web-support)
* [Patrol VS Code Extension - A Better Way to Run and Debug Flutter UI Tests](https://leancode.co/blog/patrol-vs-code-extension)

We also updated documentation if you're looking for guides and examples:

* [see how to test on Web with Patrol](https://patrol.leancode.co/documentation/web)
* [find out what features offers our VS Code extension](https://patrol.leancode.co/documentation/other/patrol-devtools-extension)
* [learn how to use `platform` instead of `native`](https://patrol.leancode.co/documentation/native/usage)

Run `patrol update` and upgrade `patrol` in your pubspec to use the newest version of Patrol.
You can find the VS Code extension in Marketplace inside VS Code.

We're hoping this early Christmas present will make your mobile testing easier!
If you have any questions or want to submit feedback, head on to [GitHub](https://github.com/leancodepl/patrol) or [our Discord server](https://discord.gg/ukBK5t4EZg). See you there!

## Compatibility table

The following table describes which versions of `patrol`
and `patrol_cli` are compatible with each other.
The simplest way to ensure that both packages are compatible
is by always using the latest version. However,
if for some reason that isn't possible, you can refer to
the table below to assess which version you should use.

This table shows the compatible versions between patrol\_cli and patrol packages.

| patrol\_cli version | patrol version  | Minimum Flutter version |
| ------------------- | --------------- | ----------------------- |
| 4.0.2+              | 4.1.0+          | 3.32.0                  |
| 4.0.0 - 4.0.1       | 4.0.0 - 4.0.1   | 3.32.0                  |
| 3.11.0              | 3.20.0          | 3.32.0                  |
| 3.9.0 - 3.10.0      | 3.18.0 - 3.19.0 | 3.32.0                  |
| 3.7.0 - 3.8.0       | 3.16.0 - 3.17.0 | 3.32.0                  |
| 3.5.0 - 3.6.0       | 3.14.0 - 3.15.2 | 3.24.0                  |
| 3.4.1               | 3.13.1 - 3.13.2 | 3.24.0                  |
| 3.4.0               | 3.13.0          | 3.24.0                  |
| 3.3.0               | 3.12.0          | 3.24.0                  |
| 3.2.1               | 3.11.2          | 3.24.0                  |
| 3.2.0               | 3.11.0 - 3.11.1 | 3.22.0                  |
| 3.1.0 - 3.1.1       | 3.10.0          | 3.22.0                  |
| 2.6.5 - 3.0.1       | 3.6.0 - 3.10.0  | 3.16.0                  |
| 2.6.0 - 2.6.4       | 3.4.0 - 3.5.2   | 3.16.0                  |
| 2.3.0 - 2.5.0       | 3.0.0 - 3.3.0   | 3.16.0                  |
| 2.2.0 - 2.2.2       | 2.3.0 - 2.3.2   | 3.3.0                   |
| 2.0.1 - 2.1.5       | 2.0.1 - 2.2.5   | 3.3.0                   |
| 2.0.0               | 2.0.0           | 3.3.0                   |
| 1.1.4 - 1.1.11      | 1.0.9 - 1.1.11  | 3.3.0                   |

## Notes

* Versions marked with `+` indicate compatibility with all later versions
* Ranges (e.g., `2.0.0 - 2.1.0`) indicate compatibility with all versions in that range
* The minimum Flutter version is required for both packages to work correctly

## Supported platforms

Patrol works on:

* Android 5.0 (API 21) and newer,
* iOS 13 and newer,
* macOS 10.14 and newer (alpha support).

Windows and Linux are not supported.

On mobile platforms it works on both physical and virtual devices.

If you want to check which native features are supported, see [feature parity].

[feature parity]: https://patrol.leancode.co/documentation/native/feature-parity
