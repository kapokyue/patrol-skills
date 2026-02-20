# Ci And Device Farms


# Overview

This section of the documentation is focused on running Patrol tests as part of
your Continuous Integration workflows.

Having tests doesn't bring you any benefits if you don't automatically verify
that they pass. We know this too well, and we're putting a lot of work into
making it easy to do so.

# Platforms

In this document, we'll outline a few ways to run Patrol UI tests of Flutter
apps.

Generally, the solutions for running UI tests of mobile apps can be divided into
2 groups:

* Device labs - platforms that provide access to mobile devices in the cloud. You
  upload an app binary with tests to the device lab, which runs the tests and
  reports the results back to you.

* Traditional – containers or VMs, either managed or self-hosted. In this
  approach, you get access to the shell, so everything is possible. You manually
  script what you want to achieve, which is usually: installing the Android/iOS
  SDK tools, creating a virtual device, running tests, and collecting results.

There are quite a few solutions in each of these groups, and each is unique, but
generally, **device labs trade flexibility for ease of use**. They're a good fit
for most apps but make certain more complicated scenarios impossible.

# Device labs

### Firebase Test Lab

[Firebase Test Lab] is one of the most popular device labs. It is a good choice
for most projects.

You upload the app main app, the test app, select devices to run on, and after a
while, test results along with a video recording are available.

Firebase Test Lab has a large pool of physical and virtual devices.

See also:

* [Firebase Test Lab pricing]

### emulator.wtf

[emulator.wtf] is a fairly new solution created by Madis Pink and Tauno Talimaa. It
claims to provide a 2-5x speedup compared to Firebase Test Lab, and 4-20x
speedup compared to spawning emulators on CI machines. It works similarly to
Firebase Test Lab - you upload your main apk, test apk, select emulators to run
on, and the rest is up to emulator.wtf - it runs the tests and outputs results.

The emulators are indeed rock stable. Emulator.wtf automatically records videos
from test runs, and it presents the test results nicely.

It's a solid choice if you can accept that your tests will run only on Android
emulator.

Reports are available in JUnit.

See also:

* [emulator.wtf pricing]

### Xcode Cloud

[Xcode Cloud] is a CI/CD platform built into Xcode and designed expressly for
Apple developers. It doesn't support testing on Android.

Since integration tests written with Patrol are also native `XCTest`s, it should
be possible to run Patrol on Xcode Cloud. We plan to research it soon and share
our findings here.

### Other

Another popular device lab is [AWS Device Farm].

If your use-case is highly specific, you might want to build an in-house device
farm. A project that helps with this is [Simple Test Farm].

### Limitations

We mentioned above that device labs make certain scenarios impossible to
accomplish.

An example of such a scenario scanning a QR code. One of the apps we worked on had
this feature, and we wanted to test it because it was a critical part of the user
flow. When you have access to the shell filesystem (which you do have in the
"manual" approach, and don't have in the "device lab" approach), you can easily
[replace the scene that is visible in the camera's viewfinder][so_viewfinder].

This is not possible on device labs.

# Traditional

### Codemagic

[Codemagic] is a popular CI/CD platform that integrates with Azure DevOps, GitHub, GitLab, Bitbucket, and
other self-hosted or cloud-based Git repositories.

It's also possible to run integration tests on Android directly on a Codemagic machine.
Here's a blog post about it: [Running Android integration tests on Codemagic].

However, this is generally not the recommended way to run your patrol tests. We recommend using device farms like [firebase test lab], [emulator.wtf] or others.
Codemagic will be great for preparing .apk files that you can upload to the device farms. To see documentation about using patrol in Codemagic workflows, please visit [codemagic/patrol documentation].
The full app example with all files is available in [codemagic/patrol-example-repository].

### GitHub Actions

[GitHub Actions] is a very popular CI/CD platform, especially among open-source
projects thanks to unlimited minutes.

Unfortunately, running Flutter integration tests on GitHub Actions is not a
pleasant experience.

**Android**

We used the [ReactiveCircus/android-emulator-runner] GitHub Action to run
Android emulator on GitHub Actions. Our takeaway is this: Running an Android
emulator on the default GitHub Actions runner is a bad idea. It is slow to start and
unstable (apps crash randomly) and very slow. Really, really slow. We tried to
mitigate its instability by using [Test Butler], but it comes with its own
restrictions, most notably, it doesn't allow for Google Play Services.

**iOS**

We use the [futureware-tech/simulator-action] GitHub Action to run iOS simulator
on GitHub Actions is stable. But given that the iOS simulator is just that – a
simulator, not an emulator – the range of cases it can be used for is reduced.
For example, there's no easy way to disable an internet connection, which makes it
very hard to test the behavior of an app when offline.

Bear in mind that to run an iOS simulator on GitHub Actions, you have to use a
macOS runner. 1 minute on macos-latest counts as 10 minutes on ubuntu-latest.
You can also use a custom runner – more on that below.

Custom Runners Workflows on GitHub Actions can run on external runners, in
addition to default runners such as ubuntu-latest and macos-latest.

One example of such a custom runner provider is BuildJet. We tried running
Android emulator on it, hoping that the performance benefits it brings would
help with the abysmal stability, but we've found that, even though the emulator
works faster and is more stable, it sometimes just crashes with no actionable
error message.

### Other

There are many more CI/CD platforms. Some of the most popular include
[CircleCI], [CirrusCI], and [GitLab CI/CD]. There are also CI providers that are
focused specifically on mobile apps, for example [Bitrise] and [Codemagic]. If
you used these platforms, we (and other Patrol users) will be happy to hear
about your experiences!

[github actions]: https://github.com/features/actions

[aws device farm]: https://aws.amazon.com/device-farm

[emulator.wtf]: https://emulator.wtf

[emulator.wtf pricing]: https://emulator.wtf/pricing

[firebase test lab]: https://firebase.google.com/docs/test-lab

[firebase test lab pricing]: https://firebase.google.com/docs/test-lab/usage-quotas-pricing

[xcode cloud]: https://developer.apple.com/xcode-cloud

[test butler]: https://github.com/linkedin/test-butler

[reactivecircus/android-emulator-runner]: https://github.com/ReactiveCircus/android-emulator-runner

[futureware-tech/simulator-action]: https://github.com/futureware-tech/simulator-action

[simple test farm]: https://github.com/DeviceFarmer/stf

[so_viewfinder]: https://stackoverflow.com/questions/13818389/android-emulator-camera-custom-image

[circleci]: https://circleci.com

[cirrusci]: https://cirrus-ci.org

[gitlab ci/cd]: https://docs.gitlab.com/ee/ci

[bitrise]: https://bitrise.io

[codemagic]: https://codemagic.io/start

[codemagic/patrol documentation]: https://docs.codemagic.io/integrations/patrol-integration/

[codemagic/patrol-example-repository]: https://github.com/codemagic-ci-cd/codemagic-sample-projects/tree/main/integrations/patrol-demo-project

[running android integration tests on codemagic]: https://blog.codemagic.io/how-to-test-native-features-in-flutter-apps-with-patrol-and-codemagic/

# BrowserStack

## Setup

[BrowserStack App Automate] is a popular cloud device farm. You can use it to run your tests on real devices.

    
      
        ### Change runner

        Modify the **app-level build.gradle**:

        ```groovy title="android/app/build.gradle"
        android {
          // ...
          defaultConfig {
            //...
            testInstrumentationRunner "pl.leancode.patrol.BrowserstackPatrolJUnitRunner"
          }
          // ...
        }

        // ...
        ```
      
    

    That's it! You can now use `bs_android` to schedule a test run.
  

    
      You need to do a [Setup for physical iOS devices] first.
    

    We need to convert your tests to use [Xcode test plans].

    
      Make sure that the project name is "Runner" and the scheme is named "Runner" - this is the default name for the Flutter project.
    

    
      
        Open your project in Xcode and edit the scheme:
      

      
        Go to the **Test** tab and convert your tests to use test plans:

      

      
        Create from scheme:
      

      
        Rename to "TestPlan" and save:

        
          It has to be named "TestPlan" to work with the `bs_ios` script.
        
      

      Now, you can schedule a test run using the `bs_ios` script.
    
  

You can choose between running tests in a recommended way using scripts or manually:

    ## Schedule tests using scripts

    We recommend using the [bs\_android][bs_android] and [bs\_ios][bs_ios] scripts to schedule test runs.
    They are part of LeanCode's [mobile-tools]. If you're using Homebrew, you can install it with:

    ```bash
    brew tap leancodepl/tools
    brew install mobile-tools
    ```

    The scripts require the `BS_CREDENTIALS` environment variable
    to be set so it can authenticate with BrowserStack:

    ```bash
    export BS_CREDENTIALS="YOUR_USERNAME:YOUR_ACCESS_KEY"
    ```

    Get your username and access on [BrowserStack's account page][bs_account].

    Now reload your shell (e.g. `exec zsh`)

    ### Usage

    The scripts forward all its options and flags to `patrol build`, so you can use it like this:

    ```bash
    bs_android \
      --target patrol_test/example_test.dart,patrol_test/another_test.dart \
      --verbose \
      --dart-define 'KEY_EXAMPLE=VALUE_EXAMPLE'
    ```

    Full example:

    ```
    $ export BS_PROJECT=AwesomeApp # optional
    $ export BS_ANDROID_DEVICES="[\"Google Pixel 4-10.0\"]" # optional
    $ bs_android
    • Building apk with entrypoint test_bundle.dart...
    ✓ Completed building apk with entrypoint test_bundle.dart (11.0s)
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100 87.4M  100   235  100 87.4M      7  2857k  0:00:33  0:00:31  0:00:02 2052k
    Uploaded app, url: bs://fb61a714e1a0c60e2578d940dad52b74da244d54
    Uploaded test, url: bs://a715b1231d41ac627bd683f1b16c28476babd72e
    {"message":"Success","build_id":"a30440db559fcab65554ab0273437f3bd45d761b"}
    Scheduled test execution
    ```

    That's all! "Success" means that the test execution was scheduled successfully.
  

    You can follow BrowserStack's docs and/or follow the code of `bs_android` and `bs_ios` scripts:

    1. Build the app under test and the instrumentation app ([see docs][patrol build])
    2. Upload the app under test APK to BrowserStack ([see Android docs][bs_android_app_docs]) ([see iOS docs][bs_ios_app_docs])
    3. Upload the instrumentation app APK to BrowserStack ([see Android docs][bs_android_test_docs]) ([see iOS docs][bs_ios_test_docs])
    4. Start test execution on BrowserStack ([see Android docs][bs_execute_android_docs]) ([see iOS docs][bs_execute_ios_docs])
  

After scheduling the test execution, you can check the status of the test execution in the [App Automate dashboard][bs_app_automate_dashboard].

If you need to change the test configuration, check out full list of available devices and OS versions in the [BrowserStack Browsers & Devices][bs_devices].

[BrowserStack App Automate]: https://www.browserstack.com/app-automate

[mobile-tools]: https://github.com/leancodepl/mobile-tools

[bs_account]: https://www.browserstack.com/accounts/profile

[bs_app_automate_dashboard]: https://app-automate.browserstack.com/dashboard/v2

[Setup for physical iOS devices]: /documentation/physical-ios-devices-setup

[Xcode test plans]: https://developer.apple.com/documentation/xcode/organizing-tests-to-improve-feedback

[bs_android]: https://github.com/leancodepl/mobile-tools/blob/master/bin/bs_android

[bs_ios]: https://github.com/leancodepl/mobile-tools/blob/master/bin/bs_ios

[bs_devices]: https://www.browserstack.com/list-of-browsers-and-platforms/app_automate

[patrol build]: /cli-commands/build

[bs_android_app_docs]: https://www.browserstack.com/docs/app-automate/api-reference/espresso/apps#upload-an-app

[bs_android_test_docs]: https://www.browserstack.com/docs/app-automate/api-reference/espresso/tests#upload-a-test-suite

[bs_execute_android_docs]: https://www.browserstack.com/docs/app-automate/api-reference/espresso/builds#execute-a-build

[bs_ios_app_docs]: https://www.browserstack.com/docs/app-automate/api-reference/xcuitest/apps#upload-an-app

[bs_ios_test_docs]: https://www.browserstack.com/docs/app-automate/api-reference/xcuitest/tests#upload-a-test-suite

[bs_execute_ios_docs]: https://www.browserstack.com/docs/app-automate/api-reference/xcuitest/builds#execute-a-build

# Firebase Test Lab

There are many device lab providers. Below we're showing how to run Patrol tests
on [Firebase Test Lab], because it's popular in the Flutter community, but the
instructions should be similar for other device farms, such as [AWS Device
Farm][aws_device_farm].

  Before you proceed with the steps listed below, make sure that you've
  completed the [native setup] guide.

  <Tab value="Android">
    To run the integration tests on Android, you need 2 apps: the app itself
    (often called the "app under test") and the test intrumentation app.

    To build these apps, run:

    ```
    patrol build android --target patrol_test/example_test.dart
    ```

    Once you have built the apks, use the [gcloud] tool to run them on Firebase
    Test Lab:

    ```
    gcloud firebase test android run \
        --type instrumentation \
        --use-orchestrator \
        --app build/app/outputs/apk/debug/app-debug.apk \
        --test build/app/outputs/apk/androidTest/debug/app-debug-androidTest.apk \
        --timeout 1m \
        --device model=MediumPhone.arm,version=34,locale=en,orientation=portrait \
        --record-video \
        --environment-variables clearPackageData=true
    ```

    
      You must [install the gcloud tool] first. [Here][gcloud_android] you can learn
      more about all available options and flags.
    

    
      The environment variable `clearPackageData=true` tells orchestrator to clear the
      package data between test runs. Keep in mind that it clears only the data of your
      app, not other data on the device, e.g. Chrome.
    

    It's convenient to create a shell script to avoid typing that long command
    every time. You might want to take a look at Patrol example app's
    [run\_android\_testlab script][example_android_script].

    
      On Android, all permissions are granted by default. This behavior can be
      changed using the [alpha version of the gcloud tool].
    
  </Tab>

  <Tab value="iOS">
    To run the integration tests on iOS, you need 2 apps: the app itself
    (often called the "app under test") and the test intrumentation app.

    First, build your Flutter app, choosing the integration test file as target:

    For simulations:

    ```
    patrol build ios --target patrol_test/example_test.dart --debug --simulator
    ```

    For physical devices:

    ```
    patrol build ios --target patrol_test/example_test.dart --release
    ```

    `patrol build ios` outputs paths to the built app binaries, for example:

    ```
    $ patrol build ios -t patrol_test/example_test.dart --release
    • Building app with entrypoint example_test.dart for iOS device (release)...
    ✓ Completed building app with entrypoint example_test.dart for iOS device (31.5s)
    build/ios_integ/Build/Products/Release-iphoneos/Runner.app (app under test)
    build/ios_integ/Build/Products/Release-iphoneos/RunnerUITests-Runner.app (test instrumentation app)
    build/ios_integ/Build/Products/Runner_iphoneos16.2-arm64.xctestrun (xctestrun file)
    ```

    Firebase Test Lab requires these files to be packaged together in a zip
    archive. To create the archive:

    ```
    pushd build/ios_integ/Build/Products
    zip -r ios_tests.zip Release-iphoneos Runner_iphoneos16.2-arm64.xctestrun
    popd
    ```

    Finally, upload the `ios_tests.zip` to Firebase Test Lab for execution:

    ```
    gcloud firebase test ios run \
      --test build/ios_integ/Build/Products/ios_tests.zip \
      --device model=iphone8,version=16.2,locale=en_US,orientation=portrait
    ```

    
      You must [install the gcloud tool] first. [Here][gcloud_ios] you can learn
      more about all available options and flags.
    

    If your `.xctestrun` file has different iOS version in its name than the
    device you're running on, simply rename the `.xctestrun` so that the version
    matches.

    It's convenient to create a shell script to avoid typing that long command
    every time. You might want to take a look at Patrol example app's
    [run\_ios\_testlab script][example_ios_script].
  </Tab>

[native setup]: /documentation

[gcloud]: https://cloud.google.com/sdk/gcloud

[example_android_script]: https://github.com/leancodepl/patrol/blob/master/dev/e2e_app/run_android_testlab

[example_ios_script]: https://github.com/leancodepl/patrol/blob/master/dev/e2e_app/run_ios_testlab

[firebase test lab]: https://firebase.google.com/products/test-lab

[aws_device_farm]: https://aws.amazon.com/device-farm

[install the gcloud tool]: https://cloud.google.com/sdk/docs/install

[gcloud_android]: https://cloud.google.com/sdk/gcloud/reference/firebase/test/android/run

[gcloud_ios]: https://cloud.google.com/sdk/gcloud/reference/firebase/test/ios/run

[alpha version of the gcloud tool]: https://cloud.google.com/sdk/gcloud/reference/alpha/firebase/test/android/run#--grant-permissions

# LambdaTest

# LambdaTest overview

[LambdaTest App Test Automation] is a popular cloud device farm.

  This integration is currently Android-only.

### Change runner

Modify the **app-level build.gradle**:

```groovy title="android/app/build.gradle"
android {
  // ...
  defaultConfig {
    //...
    testInstrumentationRunner "pl.leancode.patrol.LambdaTestPatrolJUnitRunner"
  }
  // ...
}

// ...
```

### Upload to LambdaTest

To run Android UI tests on LambdaTest:

1. Upload the app under test APK to LambdaTest ([see docs][LT_app_docs])
2. Upload the instrumentation app APK to LambdaTest ([see docs][LT_test_docs])
3. Start test execution on LambdaTest ([see docs][LT_execute_docs])

```
$ export LAMBDATEST_PROJECT=AwesomeApp # optional
$ export LAMBDATEST_DEVICES="[\"Pixel 7 Pro-13\"]" # optional
• Building apk with entrypoint test_bundle.dart...
✓ Completed building apk with entrypoint test_bundle.dart (11.0s)
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 82.4M  100   255  100 82.4M      7  2897k  0:00:31  0:00:36  0:00:02 2051k
Uploaded app, "app_id": "lt://APP1016047291733313441063634",
Uploaded testsuite, "app_id": "lt://APP1016047291733312896265135",
{
    "status": [
        "Success"
    ],
    "buildId": [
        "5875687"
    ],
    "message": [
        ""
    ]
}
```

[LT_app_docs]: https://www.lambdatest.com/support/docs/getting-started-with-espresso-testing/#running-your-first-test-a-step-by-step-guide

[LT_test_docs]: https://www.lambdatest.com/support/docs/getting-started-with-espresso-testing/#step-2-upload-your-test-suite

[LT_execute_docs]: https://www.lambdatest.com/support/docs/getting-started-with-espresso-testing/#step-3-executing-the-test

[LambdaTest App Test Automation]: https://www.lambdatest.com/app-test-automation
