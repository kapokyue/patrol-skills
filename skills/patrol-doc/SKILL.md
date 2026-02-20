---
name: patrol-doc
description: Serve Patrol framework docs with fast lookup and practical how-to guidance. Use when users ask setup, CLI, finders, native/web automation, CI/device farms, reporting, VS Code extension, tags, or troubleshooting questions.
---

# Patrol Doc

Answer Patrol documentation questions using the curated corpus in `references/`.
Live documentation is available at [https://patrol.leancode.co/](https://patrol.leancode.co/).

## Workflow

1. Identify user intent: lookup, how-to, migration/compatibility, troubleshooting, or command usage.
2. Open only the most relevant reference files listed below.
3. Prefer exact command/flag snippets and explicit caveats from references.
4. Keep responses concise and action-oriented.

## Reference Map

- [references/overview-and-compatibility.md](references/overview-and-compatibility.md) — project overview, release notes, platform support, compatibility table.
- [references/cli-commands.md](references/cli-commands.md) — `patrol build|devices|doctor|develop|test|update` usage and options.
- [references/installation-and-setup.md](references/installation-and-setup.md) — install + Android/iOS/macOS setup and FAQ-level setup issues.
- [references/web-testing.md](references/web-testing.md) — web testing architecture, prerequisites, and web flags.
- [references/finders-and-widget-tests.md](references/finders-and-widget-tests.md) — `patrol_finders`, finder syntax, widget-test usage.
- [references/native-automation.md](references/native-automation.md) — `platform.mobile|android|ios|web` actions, feature parity, `native2`.
- [references/logging-reporting-and-allure.md](references/logging-reporting-and-allure.md) — logs, native reports, Allure integration.
- [references/ci-and-device-farms.md](references/ci-and-device-farms.md) — CI strategies and device farm options.
- [references/recipes-and-examples.md](references/recipes-and-examples.md) — first-test flow, practical platform recipes, tags examples.
- [references/vscode-and-devtools.md](references/vscode-and-devtools.md) — Patrol DevTools + VS Code extension usage.
- [references/troubleshooting-and-best-practices.md](references/troubleshooting-and-best-practices.md) — test stability, keying strategy, tips/tricks.

## Fast Lookup Hints

For large files, grep for high-signal tokens before reading fully:

- CLI: `patrol test`, `--target`, `--tags`, `--full-isolation`, `--coverage`, `--web-headless`
- Setup: `MainActivityTest.java`, `RunnerUITests`, `testInstrumentationRunner`, `pod install`
- Compatibility: `patrol_cli version`, `Minimum Flutter version`
- Native/web automation: `$.platform.mobile`, `$.platform.web`, `native2`, `NativeSelector`
- Reporting: `Test summary`, `Report:`, `allure`, `printLogs`
- Troubleshooting: `FLUTTER_TARGET`, `Unsupported class file major version`, `parallel execution`

## Response Contract

- For lookup requests: give direct answer + minimal context.
- For how-to requests: provide ordered steps and exact commands.
- For troubleshooting: include likely cause, checks, and concrete fix steps.
- When docs disagree across versions, call out version assumptions explicitly and cite the compatibility table.

## Scope Rules

- Primary corpus is developer-focused (setup, CLI, automation, CI, troubleshooting).
- Excluded content: Articles & Resources, Marketing/Services/Pricing, Consultation/Training programs.
- Preserve source meaning; do not invent undocumented flags or APIs.
- Formatting note: MDX-specific wrapper components are flattened into plain Markdown.
