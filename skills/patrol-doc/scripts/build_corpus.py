from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
CORPUS_SOURCE = ROOT / 'patrol-llms-full.txt'
OUT_DIR = ROOT / 'skills' / 'patrol-doc' / 'references'


def heading_index(lines: list[str]) -> tuple[list[tuple[str, int]], dict[str, list[int]]]:
    headings: list[tuple[str, int]] = []
    in_code = False
    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith('```'):
            in_code = not in_code
        if not in_code and line.startswith('# '):
            headings.append((line[2:].strip(), idx))

    starts: dict[str, list[int]] = defaultdict(list)
    for title, line_no in headings:
        starts[title].append(line_no)
    return headings, starts


def section_ranges(headings: list[tuple[str, int]], max_line: int) -> dict[int, tuple[int, int]]:
    heading_lines = [line for _, line in headings]
    ranges: dict[int, tuple[int, int]] = {}
    for start in heading_lines:
        next_lines = [line for line in heading_lines if line > start]
        end = min(next_lines) - 1 if next_lines else max_line
        ranges[start] = (start, end)
    return ranges


def clean_mdx(text: str) -> str:
    replacements = {
        '<Info>': '',
        '</Info>': '',
        '<Warning>': '',
        '</Warning>': '',
        '<Success>': '',
        '</Success>': '',
        '<Accordions>': '',
        '</Accordions>': '',
        '<Steps>': '',
        '</Steps>': '',
        '<Step>': '',
        '</Step>': '',
        '</Tabs>': '',
        '</Accordion>': '',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r'^<(img|YouTube|Tweet|div|FirebaseStudioButton)\b', stripped):
            continue
        if re.match(r'^</(div)>$', stripped):
            continue
        if re.match(r'^<(Tabs|Accordion)\b', stripped):
            continue
        lines.append(line)

    text = '\n'.join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip() + '\n'


def main() -> None:
    if not CORPUS_SOURCE.exists():
        raise FileNotFoundError(f'Source file not found: {CORPUS_SOURCE}')

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_lines = CORPUS_SOURCE.read_text(encoding='utf-8').splitlines()
    headings, starts = heading_index(raw_lines)
    ranges = section_ranges(headings, len(raw_lines))

    def get(title: str, occurrence: int = 1) -> int:
        items = starts.get(title, [])
        if len(items) < occurrence:
            raise KeyError(f'Missing heading occurrence: {title} ({occurrence})')
        return items[occurrence - 1]

    topics: dict[str, list[int]] = {
        'overview-and-compatibility.md': [
            get('Patrol'),
            get('Improved logging and reporting is here!'),
            get('New package - patrol_finders'),
            get('Patrol 3.0 is here'),
            get('New major release - Patrol 4.0'),
            get('Supported platforms'),
            get('Compatibility table'),
        ],
        'cli-commands.md': [
            get('build'),
            get('devices'),
            get('doctor'),
            get('develop'),
            get('test'),
            get('update'),
        ],
        'installation-and-setup.md': [
            get('Install Patrol'),
            get('Physical iOS devices'),
        ],
        'web-testing.md': [
            get('Flutter Web Testing'),
        ],
        'finders-and-widget-tests.md': [
            get('Using Patrol finders in widget tests'),
            get('Overview', 2),
            get('Usage', 1),
        ],
        'native-automation.md': [
            get('Feature parity'),
            get('Native Automation 2.0 (native2)'),
            get('Overview', 3),
            get('Usage', 2),
        ],
        'logging-reporting-and-allure.md': [
            get('Logs and test results'),
            get('Allure'),
        ],
        'ci-and-device-farms.md': [
            get('Overview', 1),
            get('Platforms'),
            get('Device labs'),
            get('Traditional'),
            get('BrowserStack'),
            get('Firebase Test Lab'),
            get('LambdaTest'),
            get('LambdaTest overview'),
        ],
        'recipes-and-examples.md': [
            get('Write your first test'),
            get('Disabling/enabling Bluetooth'),
            get('Granting camera permission'),
            get('Pick images from gallery'),
            get('Pull to refresh'),
            get('Take photo using camera'),
            get('Patrol tags'),
        ],
        'vscode-and-devtools.md': [
            get('Patrol DevTools Extension'),
            get('Guide for Patrol VS Code extension'),
            get('Debugging Patrol tests'),
        ],
        'troubleshooting-and-best-practices.md': [
            get('Effective Patrol'),
            get('Tips and tricks'),
        ],
    }

    for file_name, starts_for_topic in topics.items():
        sections: list[str] = []
        for start in sorted(set(starts_for_topic)):
            start_line, end_line = ranges[start]
            body = '\n'.join(raw_lines[start_line - 1:end_line]).rstrip() + '\n'
            sections.append(body)

        merged = '\n\n'.join(sections)
        content = clean_mdx(merged)
        title = file_name.removesuffix('.md').replace('-', ' ').title()
        header = f'# {title}\n\n'
        (OUT_DIR / file_name).write_text(header + content, encoding='utf-8')

    print(f'Generated {len(topics)} topic files at {OUT_DIR}')


if __name__ == '__main__':
    main()
