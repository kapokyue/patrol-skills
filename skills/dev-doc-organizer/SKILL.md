---
name: dev-doc-organizer
description: Organize developer documentation for searchability, scannability, and quick problem-solving. Use when creating or restructuring technical docs so engineers can find APIs, code examples, configuration, constraints, and known issues without business-noise.
---

# Dev Doc Organizer

Organize developer-facing documentation so engineers can quickly query and ship.

## Workflow

1. Separate technical content from non-technical context.
2. Standardize feature pages with predictable sections.
3. Prioritize copy-paste code examples and explicit outputs.
4. Surface warnings, caveats, and known issues with consistent callouts.
5. Optimize headings and keywords for search.
6. Keep shared concepts DRY and linked from a single source.

## Phase 1: Separate Signal from Noise

- Create clear separation between Product/Business docs and Engineering docs.
- Keep product context to 1 sentence and link out to PRD or user-story sources.
- If a unified docs system is required, enforce strict tags such as `dev-spec`, `api`, `architecture`.
- Filter out non-dev tags (for example `marketing`, `sales-enablement`, `ux-research`) in engineering views.
- Use progressive disclosure (`<details>`) for non-essential background that should not interrupt implementation flow.

## Phase 2: Structure the Developer Hub

For each feature page, use one predictable template. Do not reorder sections unless required by platform constraints.

Required sections:

1. Feature Name and TL;DR
2. Architecture and Flow
3. Dependencies and Integrations
4. API or Interfaces
5. Configuration and Environment Variables
6. Usage and Code Examples
7. Known Issues and Gotchas

Use the canonical template in [references/developer-feature-template.md](references/developer-feature-template.md).

## Phase 3: Optimize for Query-First Usage

- Write action-oriented headings (for example: `Connecting to Postgres`, `Creating a New User`).
- Include likely search synonyms in the first paragraph (for example: `user creation`, `register`, `sign up`).
- Maintain a central glossary/index for acronyms and domain terms.
- Document cross-cutting concepts once (for example authentication) and link to that page from feature pages.
- Remove duplicated and stale copies of shared instructions.

## Callout Rules

Use consistent severity and keep wording explicit:

- `🛑 WARNING` for destructive or breaking behavior.
- `⚠️ NOTE` for caveats, edge cases, cache behavior, and known non-obvious constraints.
- `💡 TIP` for best practices and performance optimizations.

## Quality Checklist

Before finalizing docs updates, confirm:

1. Non-dev context is linked, not embedded as long prose.
2. Feature pages follow a consistent template.
3. Every code sample is executable with realistic payloads.
4. Expected output is shown immediately after each main example.
5. Known Issues section exists and is visible.
6. Keywords and synonyms are present in intro and headings.
7. Shared topics are referenced, not duplicated.

## Output Requirements

When asked to produce or refactor docs:

- Return updated markdown files with standardized sections.
- Preserve existing technical meaning unless the user asks for semantic edits.
- Prefer minimal, mechanical restructuring over rewriting technical behavior.
