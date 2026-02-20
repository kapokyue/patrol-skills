# Installation And Setup


## Install Patrol

Check out our video version of this tutorial on YouTube!

  If you want to use Patrol finders in your existing widget or golden
  tests, go to [Using Patrol finders in widget tests].

## Setup

  
    Install `patrol_cli`:

    ```
      flutter pub global activate patrol_cli
    ```

    [Patrol CLI] (command-line interface) is a small program that enables running
    Patrol UI tests. It is necessary to run UI tests (`flutter test` won't work! [Here's why]).

    
      Make sure to add `patrol` to your `PATH` environment variable.
      It's explained in the [README].
    
  

  
    Verify that installation was successful and your environment is set up properly:

    ```
    patrol doctor
    ```

    Example output:

    ```
    Patrol CLI version: 2.3.1+1
    Android:
    • Program adb found in /Users/username/Library/Android/sdk/platform-tools/adb
    • Env var $ANDROID_HOME set to /Users/username/Library/Android/sdk
    iOS / macOS:
    • Program xcodebuild found in /usr/bin/xcodebuild
    • Program ideviceinstaller found in /opt/homebrew/bin/ideviceinstaller
    Web:
    • Program node found in /usr/bin/node
    • Program npm found in /usr/bin/npm
    ```

    Be sure that for the platform you want to run the test on, all the checks are green.

    
      Patrol CLI invokes the Flutter CLI for certain commands. To override the command used,
      pass the `--flutter-command` argument or set the `PATROL_FLUTTER_COMMAND` environment
      variable. This supports FVM (by setting the value to `fvm flutter`), puro (`puro flutter`)
      and potentially other version managers.
    
  

  
    Add a dependency on the `patrol` package in the
    `dev_dependencies` section of `pubspec.yaml`.  `patrol` package requires
    Android SDK version 21 or higher.

    ```
    flutter pub add patrol --dev
    ```
  

  
    Create `patrol` section in your `pubspec.yaml`:

    ```yaml title="pubspec.yaml"
    dependencies:
      # ...

    dev_dependencies:
      # ...

    patrol:
      app_name: My App
      android:
        package_name: com.example.myapp
      ios:
        bundle_id: com.example.MyApp
      macos:
        bundle_id: com.example.macos.MyApp
    ```

    
      **Test Directory Configuration**: By default, Patrol looks for tests in the `patrol_test/` directory.
      You can customize this by adding `test_directory: your_custom_directory` to your `patrol` section in `pubspec.yaml`.

      ```yaml title="pubspec.yaml (optional customization)"
      patrol:
        app_name: My App
        test_directory: integration_test  # Use custom directory
        android:
          package_name: com.example.myapp
        ios:
          bundle_id: com.example.MyApp
        macos:
          bundle_id: com.example.macos.MyApp
      ```
    

    
      In this tutorial, we are using example app, which has package name
      `com.example.myapp` on Android, bundle id `com.example.MyApp` on iOS,
      `com.example.macos.MyApp` on macOS and `My App` name on all platforms.
      Replace any occurences of those names with proper values.
    

    
      If you don't know where to get `package_name` and `bundle_id` from, see the [FAQ] section.
    
  

  
    Integrate with native side

    The 3 first steps were common across platforms. The rest is platform-specific.

    Psst... Android is a bit easier to set up, so we recommend starting with it!

    
        
          
            Go to **android/app/src/androidTest/java/com/example/myapp/** in your project
            directory. If there are no such folders, create them. **Remember to replace
            `/com/example/myapp/` with the path created by your app's package name.**
          

          
            Create a file named `MainActivityTest.java` and copy there the code below.

            ```java title="MainActivityTest.java"
            package com.example.myapp; // replace "com.example.myapp" with your app's package

            import androidx.test.platform.app.InstrumentationRegistry;
            import org.junit.Test;
            import org.junit.runner.RunWith;
            import org.junit.runners.Parameterized;
            import org.junit.runners.Parameterized.Parameters;
            import pl.leancode.patrol.PatrolJUnitRunner;

            @RunWith(Parameterized.class)
            public class MainActivityTest {
                @Parameters(name = "{0}")
                public static Object[] testCases() {
                    PatrolJUnitRunner instrumentation = (PatrolJUnitRunner) InstrumentationRegistry.getInstrumentation();
                    // replace "MainActivity.class" with "io.flutter.embedding.android.FlutterActivity.class" 
                    // if in AndroidManifest.xml in manifest/application/activity you have
                    //     android:name="io.flutter.embedding.android.FlutterActivity"
                    instrumentation.setUp(MainActivity.class);
                    instrumentation.waitForPatrolAppService();
                    return instrumentation.listDartTests();
                }

                public MainActivityTest(String dartTestName) {
                    this.dartTestName = dartTestName;
                }

                private final String dartTestName;

                @Test
                public void runDartTest() {
                    PatrolJUnitRunner instrumentation = (PatrolJUnitRunner) InstrumentationRegistry.getInstrumentation();
                    instrumentation.runDartTest(dartTestName);
                }
            }
            ```
          

          
            Go to the **build.gradle.kts** file, located in **android/app** folder in your
            project directory.
          

          
            Add these 2 lines to the `defaultConfig` section:

            ```kotlin title="android/app/build.gradle.kts"
              testInstrumentationRunner = "pl.leancode.patrol.PatrolJUnitRunner"
              testInstrumentationRunnerArguments["clearPackageData"] = "true"
            ```
          

          
            Add this section to the `android` section:

            ```kotlin title="android/app/build.gradle.kts"
              testOptions {
                execution = "ANDROIDX_TEST_ORCHESTRATOR"
              }
            ```
          

          
            Add this line to `dependencies` section:

            ```kotlin title="android/app/build.gradle.kts"
              androidTestUtil("androidx.test:orchestrator:1.5.1")
            ```
          
        

        
          Bear in mind that ProGuard can lead to some problems if not well configured, potentially causing issues such as `ClassNotFoundException`s.
          Keep all the Patrol packages or disable ProGuard in `android/app/build.gradle.kts`:

          ```kotlin title="android/app/build.gradle.kts"
            ...
            buildTypes {
              getByName("release") {
                  ...
              }
              getByName("debug") {
                  isMinifyEnabled = false
                  isShrinkResources = false
              }
            }
          ```
        
      

        
          
            Go to **android/app/src/androidTest/java/com/example/myapp/** in your project
            directory. If there are no such folders, create them. **Remember to replace
            `/com/example/myapp/` with the path created by your app's package name.**
          

          
            Create a file named `MainActivityTest.java` and copy there the code below.

            ```java title="MainActivityTest.java"
            package com.example.myapp; // replace "com.example.myapp" with your app's package

            import androidx.test.platform.app.InstrumentationRegistry;
            import org.junit.Test;
            import org.junit.runner.RunWith;
            import org.junit.runners.Parameterized;
            import org.junit.runners.Parameterized.Parameters;
            import pl.leancode.patrol.PatrolJUnitRunner;

            @RunWith(Parameterized.class)
            public class MainActivityTest {
                @Parameters(name = "{0}")
                public static Object[] testCases() {
                    PatrolJUnitRunner instrumentation = (PatrolJUnitRunner) InstrumentationRegistry.getInstrumentation();
                    // replace "MainActivity.class" with "io.flutter.embedding.android.FlutterActivity.class" 
                    // if in AndroidManifest.xml in manifest/application/activity you have
                    //     android:name="io.flutter.embedding.android.FlutterActivity"
                    instrumentation.setUp(MainActivity.class);
                    instrumentation.waitForPatrolAppService();
                    return instrumentation.listDartTests();
                }

                public MainActivityTest(String dartTestName) {
                    this.dartTestName = dartTestName;
                }

                private final String dartTestName;

                @Test
                public void runDartTest() {
                    PatrolJUnitRunner instrumentation = (PatrolJUnitRunner) InstrumentationRegistry.getInstrumentation();
                    instrumentation.runDartTest(dartTestName);
                }
            }
            ```
          

          
            Go to the **build.gradle** file, located in **android/app** folder in your
            project directory.
          

          
            Add these 2 lines to the `defaultConfig` section:

            ```groovy title="android/app/build.gradle"
              testInstrumentationRunner "pl.leancode.patrol.PatrolJUnitRunner"
              testInstrumentationRunnerArguments clearPackageData: "true"
            ```
          

          
            Add this section to the `android` section:

            ```groovy title="android/app/build.gradle"
              testOptions {
                execution "ANDROIDX_TEST_ORCHESTRATOR"
              }
            ```
          

          
            Add this line to `dependencies` section:

            ```groovy title="android/app/build.gradle"
              androidTestUtil "androidx.test:orchestrator:1.5.1"
            ```
          
        

        
          Bear in mind that ProGuard can lead to some problems if not well configured, potentially causing issues such as `ClassNotFoundException`s.
          Keep all the Patrol packages or disable ProGuard in `android/app/build.gradle`:

          ```groovy title="android/app/build.gradle"
            ...
            buildTypes {
              release {
                  ...
              }
              debug {
                  minifyEnabled false
                  shrinkResources false
              }
            }
          ```
        
      
    

    
        
          
            Open `ios/Runner.xcworkspace` in Xcode.
          

          
            Create a test target if you do not already have one (see the screenshot below
            for the reference). Select `File > New > Target...` and select `UI Testing Bundle`.
            Change the `Product Name` to `RunnerUITests`. Set the `Organization Identifier`
            to be the same as for the `Runner` (no matter if you app has flavors or not).
            For our example app, it's `com.example.MyApp` just as in the `pubspec.yaml` file.
            Make sure `Target to be Tested` is set to `Runner` and language is set to `Objective-C`.
            Select `Finish`.

          

          
            2 files are created: `RunnerUITests.m` and `RunnerUITestsLaunchTests.m`.
            Delete `RunnerUITestsLaunchTests.m` **through Xcode** by clicking on it and
            selecting `Move to Trash`.
          

          
            Make sure that the **iOS Deployment Target** of `RunnerUITests` within the
            **Build Settings** section is the same as `Runner`.
            The minimum supported **iOS Deployment Target** is `13.0`.

          

          
            Replace contents of `RunnerUITests.m` file with the following:

            ```objective-c title="ios/RunnerUITests/RunnerUITests.m"
            @import XCTest;
            @import patrol;
            @import ObjectiveC.runtime;

            PATROL_INTEGRATION_TEST_IOS_RUNNER(RunnerUITests)
            ```

            Add the newly created target to `ios/Podfile` by embedding in the existing
            `Runner` target.

            ```ruby title="ios/Podfile"
            target 'Runner' do
              # Do not change existing lines.
              ...

              target 'RunnerUITests' do
                inherit! :complete
              end
            end
            ```
          

          
            Create an empty file `patrol_test/example_test.dart` in the root of your Flutter project. From the command line, run
            the following command and make sure it completes with no errors:

            ```
            flutter build ios --config-only patrol_test/example_test.dart
            ```
          

          
            Go to your `ios` directory and run:

            ```
            pod install --repo-update
            ```
          

          
            Open your Xcode project and Make sure that for each build configuration,
            the `RunnerUITests` have the same Configuration Set selected as the `Runner`:

          

          
            Go to **RunnerUITests** -> **Build Phases** and add 2 new "Run Script Phase" Build Phases.
            Name them `xcode_backend build` and `xcode_backend embed_and_thin`.

          

          
            Arrange the newly created Build Phases in the order shown in the screenshot below.

          

          
            Paste this code into the `xcode_backend build` Build Phase:

            ```
            /bin/sh "$FLUTTER_ROOT/packages/flutter_tools/bin/xcode_backend.sh" build
            ```
          

          
            Paste this code into the `xcode_backend embed_and_thin` Build Phase:

            ```
            /bin/sh "$FLUTTER_ROOT/packages/flutter_tools/bin/xcode_backend.sh" embed_and_thin
            ```
          

          
            Xcode by default also enables a "parallel execution" setting, which
            breaks Patrol. Disable it **for all schemes** (if you have more than one):

          

          
            Go to **RunnerUITests** -> **Build Settings**, search for **User Script Sandboxing**
            and make sure it's set to **No**.
          

          You're ready to run tests on iOS simulator but using real devices is a bit
          more complicated.
          Check out [Setup for physical iOS Devices] to learn how to set up Patrol for physical iOS devices.
        
      

        
          Support for macOS is in alpha stage. Please be aware that some features
          may not work as expected. There is also no native automation support
          for macOS yet. If you encounter any issues, please report them on
          GitHub.
        

        
          
            Open `macos/Runner.xcworkspace` in Xcode.
          

          
            Create a test target if you do not already have one via `File > New > Target...`
            and select `UI Testing Bundle`. Change the `Product Name` to `RunnerUITests`. Make
            sure `Target to be Tested` is set to `Runner` and language is set to `Objective-C`.
            Select `Finish`.
          

          
            2 files are created: `RunnerUITests.m` and `RunnerUITestsLaunchTests.m`.
            Delete `RunnerUITestsLaunchTests.m` **through Xcode**.
          

          
            Make sure that the **macOS Deployment Target** of `RunnerUITests` within the
            **Build Settings** section is the same as `Runner`.
            The minimum supported **macOS Deployment Target** is `10.14`.

          

          
            Replace contents of `RunnerUITests.m` file with the following:

            ```objective-c title="macos/RunnerUITests/RunnerUITests.m"
            @import XCTest;
            @import patrol;
            @import ObjectiveC.runtime;

            PATROL_INTEGRATION_TEST_MACOS_RUNNER(RunnerUITests)
            ```

            Add the newly created target to `macos/Podfile` by embedding in the existing
            `Runner` target.

            ```ruby title="macos/Podfile"
            target 'Runner' do
              # Do not change existing lines.
              ...

              target 'RunnerUITests' do
                inherit! :complete
              end
            end
            ```
          

          
            Create an empty file `patrol_test/example_test.dart` in the root of your Flutter project. From the command line, run:

            ```
            flutter build macos --config-only patrol_test/example_test.dart
            ```
          

          
            Go to your `macos` directory and run:

            ```
            pod install --repo-update
            ```
          

          
            Go to **RunnerUITests** -> **Build Phases** and add 2 new "Run Script Phase" Build Phases.
            Rename them to `xcode_backend build` and `xcode_backend embed_and_thin` by double clicking
            on their names.

          

          
            Arrange the newly created Build Phases in the order shown in the screenshot below.

          

          
            Paste this code into the first `macos_assemble build` Build Phase:

            ```
            /bin/sh "$FLUTTER_ROOT/packages/flutter_tools/bin/macos_assemble.sh" build
            ```
          

          
            Paste this code into the second `macos_assemble embed` Build Phase:

            ```
            /bin/sh "$FLUTTER_ROOT/packages/flutter_tools/bin/macos_assemble.sh" embed
            ```
          

          
            Xcode by default also enables a "parallel execution" setting, which
            breaks Patrol. Disable it **for all schemes** (if you have more than one):

          

          
            Go to **RunnerUITests** -> **Build Settings**, search for **User Script Sandboxing**
            and make sure it's set to **No**.
          

          
            Go to **Runner** -> **Signing & Capabilities**. Make sure that in all **App Sandbox**
            sections, **Incoming Connections (Server)** and **Outgoing Connections (Client)** checkboxes
            are checked.

          

          
            **Copy** `DebugProfile.entitlements` and `Release.entitlements` files from `macos/Runner`
            to `macos/RunnerUITests` directory.
          

          
            Go to **RunnerUITests** -> **Build Settings** and set **Code Signing Entitlements** to
            `RunnerUITests/DebugProfile.entitlements` for **Debug** and **Profile** configuration and to
            `RunnerUITests/Release.entitlements` for **Release** configuration.

          
        
      
    
  

  
    Create a simple integration test

    Let's create a dummy Flutter integration test that you'll use to verify
    that Patrol is correctly set up.

    Paste the following code into `patrol_test/example_test.dart`:

    ```dart title="patrol_test/example_test.dart"
    import 'dart:io';

    import 'package:flutter/material.dart';
    import 'package:flutter_test/flutter_test.dart';
    import 'package:patrol/patrol.dart';

    void main() {
      patrolTest(
        'counter state is the same after going to home and switching apps',
        ($) async {
          // Replace later with your app's main widget
          await $.pumpWidgetAndSettle(
            MaterialApp(
              home: Scaffold(
                appBar: AppBar(title: const Text('app')),
                backgroundColor: Colors.blue,
              ),
            ),
          );

          expect($('app'), findsOneWidget);
          if (!Platform.isMacOS) {
            await $.platform.mobile.pressHome();
          }
        },
      );
    }
    ```

    It does only 2 things:

    * first, it finds a text `app`
    * then (on mobile platforms), it exits to home screen

    It's a very simple test, but it's enough to verify that Patrol is correctly set
    up. To run `patrol_test/example_test.dart` on a connected Android, iOS or macOS device:

    ```
    patrol test -t patrol_test/example_test.dart
    ```

    If the setup is successful, you should see a summary like one below.

    ```
    Test summary:
    📝 Total: 1
    ✅ Successful: 1
    ❌ Failed: 0
    ⏩ Skipped: 0
    📊 Report: <some path>
    ⏱️  Duration: 4s
    ```

    If something went wrong, please proceed to the [FAQ] section which might
    contain an answer to your issue.
  

  If you are looking for a working example of a Flutter app with Patrol tests,
  check out the [example app]
  in the patrol repository.

  Add test\_bundle.dart to .gitignore

  ```
  If you are using a custom test directory, replace `patrol_test` with your custom directory.
  patrol_test/test_bundle.dart
  ```

  This file is generated by Patrol and should not be committed.

## Initializing app inside a test

To be able to test your app, you need to initialize it and pump the app's root widget, so it appears on the screen.
It's very similar to what is done in main function of your app, but it has some key differences, that can break your tests.
Easy way to implement it is to copy main function of your app and then adjust it, so it works with Patrol.
Here's what to remove when running app inside a patrol test:

1. DO NOT call `WidgetsFlutterBinding.ensureInitialized()`.
2. DO NOT use `runApp()`. Instead, use `$.pumpWidget()` (or `$.pumpWidgetAndSettle()` to wait until the UI is rendered). Pass the same argument which was passed to `runApp()`.
3. DO NOT modify `FlutterError.onError`. Sometimes it is done by some monitoring tools (like Crashlytics). Those tools rely on intercepting errors by modifying `FlutterError.onError` callback and it causes that the test engine can't see any exceptions, thus can't end a test if it fails. One way is to move the code that would be common for both the test and the app into a method and leave the rest in main function of the app, or move whole app initialization to a function and define some arguments to enable or diable parts needed in a specific place.

For an example, look at `createApp` in [`common.dart`] in Patrol repository on GitHub.

## Flavors

If your app is using flavors, then you can pass them like so:

```
patrol test --target patrol_test/example_test.dart --flavor development
```

or you can specify them in `pubspec.yaml` (recommended):

```yaml title="pubspec.yaml"
patrol:
  app_name: My App
  flavor: development
  android:
    package_name: com.example.myapp
  ios:
    bundle_id: com.example.MyApp
    app_name: The Awesome App
  macos:
    bundle_id: com.example.macos.MyApp
```

## FAQ

    The reason is probably a mismatch of `patrol` and `patrol_cli` versions. Go to [Compatibility table]
    and make sure that the versions of `patrol` and `patrol_cli` you are using are compatible.
  

    To run your application within the patrol test, you need to call `$.pumpWidgetAndSettle()`,
    and pass your application's main widget to it. Be sure that you registered all the
    necessary services before calling `$.pumpWidgetAndSettle()`.
    Here's the example of running an app within the patrol test:

    ```dart

    void main() {
      patrolTest('real app test', ($) async {

      // Do all the necessary setup here (DI, services, etc.)

      await $.pumpWidgetAndSettle(const MyApp()); // Your's app main widget

      // Start testing your app here

      });
    }

    ```

    It's a good practice to create a setup wrapper function for your tests, so you don't have to
    repeat the same code in every test. Look at the [example]
    of a wrapper function. Find out more in [Initializing app inside a test] section above.
  

### Android

    Go to `android/app/build.gradle` and look for `applicationId` in `defaultConfig` section.
  

    It's most likely caused by using incompatible JDK version.
    Run `javac -version` to check your JDK version. Patrol officially works on JDK 17,
    so unexpected errors may occur on other versions.
    If you have AndroidStudio or Intellij IDEA installed, you can find the path to JDK by
    opening your project's android directory in AS/Intellij and going to
    **Settings** -> **Build, Execution, Deployment** -> **Build Tools** -> **Gradle** -> **Gradle JDK**.
    [Learn more]
  

### iOS

    For iOS go to `ios/Runner.xcodeproj/project.pbxproj` and look for `PRODUCT_BUNDLE_IDENTIFIER`.
    For macOS go to `macos/Runner.xcodeproj/project.pbxproj` and look for `PRODUCT_BUNDLE_IDENTIFIER`.
  

    Make sure that you disabled "Paralell execution" for **all schemes** in Xcode.
    See [this video] for details.
  

    Search for a `FLUTTER_TARGET` in your project files and remove it (both value and key)
    from \*.xcconfig and \*.pbxproj files.
  

    Search for a `FLUTTER_TARGET` in your project files and remove it (both value and key)
    from \*.xcconfig and \*.pbxproj files.
  

    Check if this line in `Podfile` is present and uncommented.

    ```
    platform :ios, '12.0'
    ```

    If yes, then check if **iOS deployment version** in Xcode project's **Build Settings**
    section for all targets (Runner and RunnerUITests) are set to the same value as in Podfile
    (in case presented in snippet above, all should be set to 12.0).
  

    After removing `FLUTTER_TARGET` from `*.xcconfig`, you need to run the following command to generate it:

    ```
    flutter build ios --config-only patrol_test/example_test.dart
    ```

    Make sure to replace `patrol_test/example_test.dart` with the path to your test file.
  

If you couldn't find an answer to your question/problem, feel free to ask on
[Patrol Discord Server].

## Going from here

To learn how to write Patrol tests, see [finders] and [native automation] sections.

[native automation]: https://patrol.leancode.co/documentation/native/usage

[Setup for physical iOS Devices]: https://patrol.leancode.co/documentation/physical-ios-devices-setup

[finders]: https://patrol.leancode.co/documentation/finders/usage

[Using Patrol finders in widget tests]: https://patrol.leancode.co/documentation/finders/finders-setup

[Here's why]: https://patrol.leancode.co/documentation/native/advanced#embrace-the-native-tests

[Patrol CLI]: https://pub.dev/packages/patrol_cli

[FAQ]: https://patrol.leancode.co/documentation#faq

[Compatibility table]: https://patrol.leancode.co/documentation/compatibility-table

[README]: https://pub.dev/packages/patrol_cli#installation

[example app]: https://github.com/leancodepl/patrol/tree/master/packages/patrol/example

[example]: https://github.com/leancodepl/patrol/blob/d2c7493f9399a028e39cb94fd204affdb932c5fc/dev/e2e_app/patrol_test/common.dart#L17-L33

[Learn more]: https://developer.android.com/build/jdks

[this video]: https://www.youtube.com/watch?v=9LdEJR59fW4

[Patrol Discord Server]: https://discord.gg/ukBK5t4EZg

[Initializing app inside a test]: https://patrol.leancode.co/documentation#initializing-app-inside-a-test

[`common.dart`]: https://github.com/leancodepl/patrol/blob/master/dev/e2e_app/integration_test/common.dart

## Physical iOS devices

Because of restrictions on JIT, "in iOS 14+, debug mode Flutter apps can only be launched from Flutter tooling,IDEs..." we need to build and run tests in release mode.
Going further, we need to sign the app and tests. Let's assume that your team joined Apple Developer Program and have already an App ID, profile and certificate for your app. We need to do the same for `RunnerUITests`.

  
    In [Apple Developer Portal](https://developer.apple.com) create a new Identifier (App ID) with your app's bundle ID and with `.RunnerUITests.xctrunner` ending. It should look like e.g.: `com.example.myapp.RunnerUITests.xctrunner` (Remember to swap `com.example.myapp` with your app's one).
  

  
    In [Apple Developer Portal](https://developer.apple.com) make sure that you have a Development Certificate. If not, create one.
  

  
    In [Apple Developer Portal](https://developer.apple.com) create a new Development Provisioning Profile that is linked to the new Identifier and includes the Development Certificate.
  

  
    Next three steps are needed only if you use [fastlane for codesigning](https://docs.fastlane.tools/codesigning/getting-started/).
  

  
    In Xcode disable automatic signing in `RunnerUITests` Target.
  

  
    Go to `ios/Runner.xcodeproj/project.pbxproj` and search for all occurrences of `PRODUCT_BUNDLE_IDENTIFIER = com.example.myapp.RunnerUITests;`. Then set the `PROVISIONING_PROFILE_SPECIFIER` to your specifier of newly created profile.
  

  
    Import the new profile for RunnerUITests manually in Xcode.

    
      You might see error or warning in Xcode about not matching bundle IDs. Don't worry about it, `RunnerUITests.xctrunner` bundle is generated while building tests and this is the bundle ID that we need to sign.
    
  

  
    Go to your IDE and try it out by running `patrol build ios --release`. If tests have been built successfully you're ready for action!
