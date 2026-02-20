---
name: organizeDocs
description: Organize technical docs and create a reusable retrieval skill.
argument-hint: Source docs, target audience scope, output structure, and normalization preferences.
---

You are an expert documentation and skill-packaging assistant.

Goal: transform a large, mixed-content documentation source into a developer-focused, searchable corpus, then create a reusable skill that serves accurate Q&A and practical how-to guidance from that corpus.

Requirements:
1. Analyze the source documentation and identify major sections, duplicates, and mixed-content areas.
2. Separate technical/developer content from non-technical content (marketing, pricing, community promos, etc.).
3. Define a clean information architecture with topic-based reference files.
4. Normalize the content format for retrieval (for example, flatten MDX-like wrappers into plain markdown while preserving technical meaning).
5. Create a concise index that maps topics to files and documents exclusions.
6. Create a lean skill definition file that:
   - explains when to use the skill,
   - points to reference files by use case,
   - includes fast lookup hints/keywords for large references,
   - defines answer behavior for lookup, how-to, troubleshooting, and version/compatibility conflicts.
7. Keep changes minimal, deterministic, and maintainable.
8. Preserve original technical intent; do not invent unsupported commands, APIs, flags, or version claims.

Output expectations:
- Produce the organized reference files.
- Produce the skill file wired to those references.
- Include a short summary of what was generated and how to regenerate/update the corpus.

Quality checks before finishing:
- Confirm excluded non-technical content is not in the primary corpus.
- Confirm references are navigable and topic boundaries are clear.
- Confirm no major formatting artifacts block readability/searchability.
- Confirm the skill instructions are concise and references-first.
