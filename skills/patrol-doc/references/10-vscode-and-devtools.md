# 10 Vscode And Devtools


# Debugging Patrol tests

If you want to debug your application during patrol tests,
you can do in Visual Studio Code by attaching a debugger to the running process.
Here is how you can do it:

1. In your `launch.json` file, add a new configuration for attaching debugger to a process:

```json
{
      "name": "attach debugger",
      "request": "attach",
      "type": "dart",
      "cwd": "patrol_test",
      "vmServiceUri": "${command:dart.promptForVmService}"
}
```

2. Run your patrol tests using `develop` command with the same arguments as you would normally do.

3. When the tests will start running, at some point you will see a message with a link to Patrol devtools extension.
   Copy the last part of the URI from the message.
   Eg. for this link:

   `Patrol DevTools extension is available at http://127.0.0.1:9104/patrol_ext?uri=http://127.0.0.1:52263/F2-CH29gR1k=/`

   copy `http://127.0.0.1:52263/F2-CH29gR1k=/`.

   
     You'll see 2 similar logs. First one looks like this:
     `The Dart VM service is listening on http://127.0.0.1:63725/57XmBI_pwSA=/`

     Ignore it - this link is incorrect, wait for the one that says about devtools extension.
   

4. From "Run and Debug" tab in Visual Studio Code, select the configuration you have created in step 1.
   You will be prompted to enter the VM service URI. Paste the URI you copied in step 3.

5. Once the debugger is attached, you can set breakpoints and debug your application as you would normally do.

  Intellij/Android Studio does not support attaching a debugger to a running process via Observatory Uri.
  Therefore you cannot achieve the same behavior in those IDEs (See this [issue]).

[issue]: https://github.com/flutter/flutter-intellij/issues/2250

# Patrol DevTools Extension

A powerful Flutter DevTools extension that allows you to **inspect native UI elements** on Android and iOS devices while developing your Patrol tests. This extension provides a tree view of native UI components, making it easier to write accurate selectors for your integration tests.

## Features

* **Native UI Tree Inspection**: Browse the complete hierarchy of native UI elements on your device
* **Element Details**: View detailed information about each native element (bounds, text, accessibility properties, etc.)
* **Cross-platform Support**: Works with both Android and iOS applications
* **Live Updates**: Refresh the UI tree to see real-time changes
* **Test Integration**: Copy element selectors directly for use in your Patrol tests

## Quick Start

  
    Launch Your app with test in Development Mode

    To use the DevTools extension, start your app in Patrol development mode:

    ```bash
    patrol develop -t patrol_test/example_test.dart
    ```

    This command will:

    * Launch your test on the connected device/simulator in develop mode
    * Start the Flutter DevTools server
    * Print a clickable link to the DevTools interface in your terminal
  

  
    Open the DevTools Extension

    When `patrol develop -t` is running, look for output similar to this in your terminal:

    ```
    Patrol DevTools extension is available at:
    http://127.0.0.1:9102/patrol_ext?uri=http://127.0.0.1:58463/MOAGppLU9BU=/
    ```

    **Click on this link** to open Flutter DevTools in your browser.

    
      If logs are cluttering your terminal and making it hard to find the DevTools link, you can use the `--open-devtools` flag to automatically open DevTools:
    

    > ```bash
    > patrol develop -t patrol_test/example_test.dart  --open-devtools
    > ```
  

  
    Navigate to the Patrol Extension

    Once DevTools opens:

    * By first time you need to Enable extension, just click the button that will shows up
    * Look for the **"Patrol"** tab in the top navigation bar
    * Click on it to open the Patrol DevTools Extension
  

  
    Load the UI Tree

    * Make sure that your wanted native view is visible on your device/simulator
    * Click the **Refresh** button (🔄) in the Patrol extension
    * You should see the native UI tree populate in the left panel
  

### Flutter DevTools

After opening the Patrol DevTools link, you can also use the Flutter Inspector to see widgets and their
properties in your Flutter app. To make it work, you need to add the path to your app's lib folder (e.g., user/my\_example\_app/lib) under settings (⚙️) on the DevTools page.

### DevTools Interface

#### Tree View Controls

* **RAW button**: Shows native tree detailed information (You need to refresh native tree after toggle)
* **📱 Full node names**: Shows full node names
* **🔄 Refresh tree**: Load current UI tree

## Using Discovered Elements in Tests

When you find elements in the inspector, you can create cross-platform selectors that work on both Android and iOS:

```dart
// Cross-platform button using unique identifiers
await $.platform.mobile.tap(NativeSelector(
  android: AndroidSelector(resourceId: 'com.example:id/login_btn'),
  ios: IOSSelector(identifier: 'loginButton'),
));

// Using class name (Android) and element type (iOS)
await $.platform.mobile.tap(NativeSelector(
  android: AndroidSelector(className: 'android.widget.Button'),
  ios: IOSSelector(elementType: 'XCUIElementTypeButton'),
));

```

### Key Properties Reference

#### Android Properties

| Property             | Description                        | Example                 |
| -------------------- | ---------------------------------- | ----------------------- |
| `resourceName`       | Unique resource ID (most reliable) | `com.app:id/login_btn`  |
| `text`               | Visible text content               | `"Sign In"`             |
| `className`          | UI element type                    | `android.widget.Button` |
| `contentDescription` | Accessibility description          | `"Login button"`        |
| `applicationPackage` | App package name                   | `com.example.app`       |

Full list of Android properties can be found:
[https://pub.dev/documentation/patrol/latest/patrol/AndroidSelector-class.html](https://pub.dev/documentation/patrol/latest/patrol/AndroidSelector-class.html)

#### iOS Properties

| Property      | Description                       | Example                 |
| ------------- | --------------------------------- | ----------------------- |
| `identifier`  | Unique identifier (most reliable) | `loginButton`           |
| `elementType` | UI element type                   | `XCUIElementTypeButton` |
| `label`       | Accessibility label               | `"Sign In"`             |
| `title`       | Element title                     | `"Login"`               |

Full list of iOS properties can be found:
[https://pub.dev/documentation/patrol/latest/patrol/IOSSelector-class.html](https://pub.dev/documentation/patrol/latest/patrol/IOSSelector-class.html)

# Guide for Patrol VS Code extension

## How to setup

  
    Install the extension from [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=LeanCode.patrol-vscode)
    or [Open VSX Registry for other VSCode-like editors, eg. Cursor](https://open-vsx.org/extension/LeanCode/patrol-vscode).
    It requires Dart extension - if you don't have it, you'll be prompted to install it.
  

  
    
      This step is only required if your tests are not located in the `patrol_test` directory.
    

    In your project's pubspec.yaml, add a new line to patrol section:

    ```yaml title=pubspec.yaml
    patrol:
      test_directory: <your-test-directory> # default: patrol_test
    ```

    Set this value to the directory where your patrol tests are located. Default value for `test_directory` is `patrol_test`.
  

  
    If you have a method wrapping `patrolTest()`, you need to add an annotation to it:

    ```dart title=patrol_wrapper.dart
    import 'package:meta/meta.dart';

    @isTest // add this annotation here
    void patrolWrapper(
        String testName, Future<void> Function(PatrolIntegrationTester) test) {
      patrolTest(testName, test);
    }
    ```

    
      The `@isTest` annotation comes from the `meta` package. If `meta` is not in your `pubspec.yaml`, add it as a dev dependency:

      ```
      flutter pub add meta --dev
      ```
    
  

You should now see patrol tests in the Test Explorer tab in VS Code. They should
be in Patrol section. Also you should see a green play button next to
`patrolTest` method invocation (or your wrapper invocation). See a screenshot below for a reference.

## Features

Let's go through features of our extension, that can help you developing and running Patrol tests.

### Test Explorer

Test Explorer is a tab on the left sidebar of VS Code. You can find there a list
of tests discovered in the opened project. You should see there all kinds of
tests in the project - unit, widget and integration - which comes from the Dart
extension. Our extension adds a section with Patrol tests.

You can use it to:

* run a single test file with the play button (1) next to test file name
* run all tests with play button at the top (2)
* debug a single test file (3)

You can see logs and result of the latest test run started through VS Code in
Test results tab (4). You'll also see there live logs from the current tests execution.

Running and debugging use the device chosen in VS Code.

The test execution can be stopped using stop button at the top. (5)

Keep in mind that running and debugging tests use commands from `patrol_cli` under
the hood, and you still have to have `patrol_cli` installed on your machine - activated
globally through pub or added to the project as a dependency in `pubspec.yaml`.

### Running tests from file

Now you can run the tests by clicking the green play button beside first line of the test, as shown on the screenshot below.

Be aware that if you have more than one test in the file, this button will run the whole test file.

### Debugging tests

We combined Patrol's `develop` command with debugging feature of VS Code - now
you can debug your tests easier in our extension!

To start debugging, click on debug icon in the Test explorer tab (as shown on
screenshot above, by no. 3). It will start the test in `develop` mode. This
means that:

* only one test file can be debugged at once - do not use the button
  to debug all tests (available at the very top, works only for widget and unit
  tests),
* debugging will continue after the test is finished. This allows you to
  hot restart the test.

After the test is built, it will start executing and debugger inside VS Code
will attach to it. It takes a while, you'll see a debugging toolbar when it's ready.

The buttons on the toolbar are from the left:

* 4 buttons to navigate debugging (pause/continue, step over, step into, step out)
* 2 buttons that don't work - they do nothing in this mode and are added by Flutter extension
* disconnect button, which disconnects the debugger but leave the test running
* hot restart button - use it to hot restart the test
* stop button - stops the test and closes the app on the device
* Widget inspector button - opens Widget inspector inside VS Code. More about
  devtools in general in the next section.

### Devtools

You can open devtools in many ways:

* from a popup that appears at the start of debugging session (1)
* from command palette (2)

Both those ways lead to this dropdown, where you can choose the tab of devtools
that you want to open or choose to open them in web browser.

  Patrol's devtools extension which allows you to inspect native elements
  tree is available only in web version of devtools. 

### Additional arguments to patrol commands

Since test execution through the extension is using patrol\_cli commands under the hood,
you may want to pass more arguments to those commands beside the target file and the device.
You can modify those in VS Code settings.

## Troubleshooting

    Reload the window: open Command palette > Show and Run Commands > Developer: Reload Window.
  

    Enable "Show implementation widgets" switch placed on the top bar of Widget inspector.
  

    Make sure you completed the setup from the first section of this page.
  

    It's a bug in some versions of VS Code resulting in PATH env var not being imported. Update your VS Code to the newest version.
