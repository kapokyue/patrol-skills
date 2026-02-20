# 07 Logging Reporting And Allure

Generated from curated sections of `patrol-llms-full.txt`.

# Logs and test results

Once you've written and executed your tests, it's essential to monitor their results. Patrol provides two main methods for reporting test outcomes: **console logs** and **native test reports**.

## Logging test steps

  This feature is available starting from version `3.13.0`.

  If you're using this version but don't see logs for test steps, check if you're passing a custom `PatrolTesterConfig` to `patrolTest()`. If so, ensure the `printLogs: true` argument is included in the constructor.

During test execution, every test step (e.g., `tap` or `enterText`) is logged to the console along with its status. Additionally, the test name, status, and execution time are displayed.

**Example console output:**

```
...
🧪 denies various permissions
        ✅   1. scrollTo widgets with text "Open permissions screen".
        ✅   2. scrollTo widgets with text "Open permissions screen".
        ✅   3. tap widgets with text "Open permissions screen".
        ✅   4. tap widgets with text "Request camera permission".
        ✅   5. isPermissionDialogVisible (native)
        ✅   6. tap widgets with text "Request camera permission".
        ✅   7. isPermissionDialogVisible (native)
        ⏳   8. denyPermission (native)
❌ denies various permissions (patrol_test/permissions/deny_many_permissions_twice_test.dart) (9s)
══╡ EXCEPTION CAUGHT BY FLUTTER TEST FRAMEWORK ╞═════════════════
The following PlatformException was thrown running a test:
PlatformException(PermissionHandler.PermissionManager, A request
for permissions is already running, please wait for it to finish
before doing another request (note that you can request multiple
permissions at the same time)., null, null)

When the exception was thrown, this was the stack:
#0      StandardMethodCodec.decodeEnvelope (package:flutter/src/services/message_codecs.dart:648:7)
#1      MethodChannel._invokeMethod (package:flutter/src/services/platform_channel.dart:334:18)
<asynchronous suspension>
#2      MethodChannelPermissionHandler.requestPermissions (package:permission_handler_platform_interface/src/method_channel/method_channel_permission_handler.dart:79:9)
<asynchronous suspension>
#3      PermissionActions.request (package:permission_handler/permission_handler.dart:52:31)
<asynchronous suspension>
#4      _PermissionsScreenState._requestCameraPermission (package:e2e_app/permissions_screen.dart:21:20)
<asynchronous suspension>

The test description was:
  denies various permissions
═════════════════════════════════════════════════════════════════

✅ taps on notification (patrol_test/permissions/notifications_test.dart) (16s)
✅ taps on notification native2 (patrol_test/permissions/notifications_test.dart) (14s)
✅ grants various permissions (patrol_test/permissions/permissions_many_test.dart) (15s)
...
```

## Test summary

Once the tests are complete, a summary is printed:

```
Test summary:
📝 Total: 8
✅ Successful: 3
❌ Failed: 5
  - taps on notification (patrol_test/permissions/notifications_test.dart)
  - taps on notification native2 (patrol_test/permissions/notifications_test.dart)
  - accepts location permission (patrol_test/permissions/permissions_location_test.dart)
  - accepts location permission native2 (patrol_test/permissions/permissions_location_test.dart)
  - grants various permissions (patrol_test/permissions/permissions_many_test.dart)
⏩ Skipped: 0
📊 Report: file:///Users/user/patrol/dev/e2e_app/build/app/reports/androidTests/connected/index.html
⏱️  Duration: 227s
```

## Customizing log behavior

You can customize which logs are displayed by using the following flags. These can be passed to the `patrol test` or `patrol develop` commands:

| Flag                      | Description                                | Available in                                      | Default value |
| ------------------------- | ------------------------------------------ | ------------------------------------------------- | ------------- |
| --\[no-]show-flutter-logs | Show Flutter logs while running the tests. | `patrol test`, in `patrol develop` it's always on | `false`       |
| --\[no-]hide-test-steps   | Hide test steps while running the tests.   | `patrol test` and `patrol develop`                | `false`       |
| --\[no-]clear-test-steps  | Clear test steps after the test finishes.  | `patrol test`                                     | `true`        |

## Native test reports

In addition to console logs, you can review test results in a **native test report**. The report's file path is provided in the test summary, for example:

### Android:

Path without flavor, so just build mode (debug, release, profile):

```
📊 Report: file:///Users/user/patrol/dev/e2e_app/build/app/reports/androidTests/connected/debug/index.html
```

Path with flavor:

```
📊 Report: file:///Users/user/patrol/dev/e2e_app/build/app/reports/androidTests/connected/debug/flavors/dev/index.html
```

### iOS:

Open `.xcresult` file in Xcode, to see logs and videos.
Path:

```
📊 Report: file:///Users/user/patrol/dev/e2e_app/build/ios_results_1754923033891.xcresult
```

## Logs in `patrol_finders`

By default, enhanced logs are disabled when using `patrol_finders` without the `patrol` package. To enable them, pass the `printLogs: true` argument to the `PatrolTesterConfig` constructor:

```dart
patrolWidgetTest(
  'throws exception when no widget to tap on is found',
  config: const PatrolTesterConfig(printLogs: true),
  (tester) async {
    // test body
    // ...
  },
);
```

```dart
testWidgets(
  'description',
  (widgetTester) async {
    final $ = PatrolTester(
      tester: widgetTester,
      config: PatrolTesterConfig(printLogs: true),
    );
    // test body
    // ...
  },
);
```

# Allure

## Overview

If you're using [Allure] to report your test results, you can use the
alternative test runner to get more detailed test report.

We decided not to package this alternative runner together with Patrol because
it'd make Patrol depend on Allure, which is not desirable. Instead, you can
easily do it yourself.

This guide assumes basic familiarity with Allure. To get started, see:

* [official Allure documentation]
* [allure-framework/allure2 repository]

  This integration is currently Android-only.

  Before you proceed with the steps listed below, make sure that you've
  completed the [native setup] guide.

### Add dependencies and change runner

First, you have to modify the **app-level build.gradle**:

```groovy title="android/app/build.gradle"
android {
  // ...
  defaultConfig {
    // ...

    // Replace the existing "testInstrumentationRunner" line with:
    testInstrumentationRunner "pl.leancode.patrol.example.AllurePatrolJUnitRunner"
  }
  // ...
}

dependencies {
  androidTestImplementation "io.qameta.allure:allure-kotlin-model:2.4.0"
  androidTestImplementation "io.qameta.allure:allure-kotlin-commons:2.4.0"
  androidTestImplementation "io.qameta.allure:allure-kotlin-junit4:2.4.0"
  androidTestImplementation "io.qameta.allure:allure-kotlin-android:2.4.0"
}
```

  Replace `pl.leancode.patrol.example` with your app's package name.

See also:

* [the README of allure-kotlin library][allure_kotlin]

### Create alternative runner

Create a new Kotlin file in the same directory as **MainActivityTest.java** and
paste the following code, replacing the package:

```kotlin title="AllurePatrolJUnitRunner.kt"
package pl.leancode.patrol.example // replace "pl.leancode.patrol.example" with your app's package

import android.os.Bundle
import io.qameta.allure.android.AllureAndroidLifecycle
import io.qameta.allure.android.listeners.ExternalStoragePermissionsListener
import io.qameta.allure.android.writer.TestStorageResultsWriter
import io.qameta.allure.kotlin.Allure
import io.qameta.allure.kotlin.junit4.AllureJunit4
import io.qameta.allure.kotlin.util.PropertiesUtils
import pl.leancode.patrol.PatrolJUnitRunner

class AllurePatrolJUnitRunner : PatrolJUnitRunner() {
    override fun onCreate(arguments: Bundle) {
        Allure.lifecycle = createAllureAndroidLifecycle()
        val listenerArg = listOfNotNull(
            arguments.getCharSequence("listener"),
            AllureJunit4::class.java.name,
            ExternalStoragePermissionsListener::class.java.name.takeIf { useTestStorage }
        ).joinToString(separator = ",")
        arguments.putCharSequence("listener", listenerArg)
        super.onCreate(arguments)
    }

    private fun createAllureAndroidLifecycle() : AllureAndroidLifecycle {
      return createDefaultAllureAndroidLifecycle()
    }

    private fun createDefaultAllureAndroidLifecycle() : AllureAndroidLifecycle {
        if (useTestStorage) {
            return AllureAndroidLifecycle(TestStorageResultsWriter())
        }

        return AllureAndroidLifecycle()
    }

    private val useTestStorage: Boolean
        get() = PropertiesUtils.loadAllureProperties()
            .getProperty("allure.results.useTestStorage", "true")
            .toBoolean()
}
```

  In the snippet above, remember to replace the `package
    pl.leancode.patrol.example` line at the top of the file with your app's
  package name!

### Create allure.properties

This is required if you enabled the `clearPackageData` option for Android Test
Orchestrator. If you enabled that option but don't create the
`allure.properties` file as below, your tests reports will be cleared after each
test.

```txt title="android/app/src/main/res/allure.properties"
allure.results.useTestStorage=true
```

### Add rules to MainActivityTest

Finally, modify the **MainActivityTest.java**. You'll add a 3 rules, which add
the following features:

* automatically take a screenshot at the end of each test
* automatically dump the window hierarchy at the end of each test
* automatically embed the logcat into the report

You can simply copy-paste the following code (remember to replace the package
name):

```java title="MainActivityTest.java"
package pl.leancode.patrol.example; // replace "pl.leancode.patrol.example" with your app's package

import androidx.test.platform.app.InstrumentationRegistry;

import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;

import io.qameta.allure.android.rules.LogcatRule;
import io.qameta.allure.android.rules.ScreenshotRule;
import io.qameta.allure.android.rules.WindowHierarchyRule;
import pl.leancode.patrol.PatrolJUnitRunner;

@RunWith(Parameterized.class)
public class MainActivityTest {
    @Rule
    public ScreenshotRule screenshotRule = new ScreenshotRule(ScreenshotRule.Mode.END, "ss_end");

    @Rule
    public WindowHierarchyRule windowHierarchyRule = new WindowHierarchyRule();

    @Rule
    public LogcatRule logcatRule = new LogcatRule();

    @Parameters(name = "{0}")
    public static Object[] testCases() {
        PatrolJUnitRunner instrumentation = (PatrolJUnitRunner) InstrumentationRegistry.getInstrumentation();
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

  In the snippet above, remember to replace the `package
    pl.leancode.patrol.example` line at the top of the file with your app's
  package name!

### Retrieve the report

Run the tests with `patrol test` as usual.

After the tests are complete, create a directory for them, for example:

```bash
mkdir -p ./build/reports
```

and then retrieve the results from the device:

```bash
adb exec-out sh -c 'cd /sdcard/googletest/test_outputfiles && tar cf - allure-results' | tar xvf - -C build/reports
```

Finally, serve the results with Allure:

```bash
allure serve ./build/reports/allure-results
```

  If you're using Homebrew, `brew install allure` is the quickest way to get
  Allure.

[native setup]: /documentation

[allure]: https://qameta.io/allure-report

[allure_kotlin]: https://github.com/allure-framework/allure-kotlin/blob/master/README.md

[official Allure documentation]: https://docs.qameta.io/allure-report

[allure-framework/allure2 repository]: https://github.com/allure-framework/allure2
