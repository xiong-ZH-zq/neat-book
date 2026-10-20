# Changelog

## Unreleased

- Fix missing CJK italics with explicit per-character oblique transforms, preserving bold weight and native Latin italics. Add `cjk-oblique` to adjust or disable synthesis.
- Verify all default families against Typst's live web font inventory; add asset and license notices, a reproducible font check, and publishing audit. Include linked documentation in the Universe submission directory.

## 0.1.0 — 2026-10-20

- Initial book design with a minimal cover, running headers and three-level contents.
- Configurable open CJK, Latin, monospace and math fonts; explicit language spans.
- Theorion 0.6.0 Fancy theorem frames and square QEDs for proofs and solutions.
- Algorithmic 1.0.7 pseudocode with ruled captions, input/output and line numbers.
- Codly 2.0.0 code blocks with language badges and syntax highlighting.
- Chapter-based equation and figure numbering, including appendix-aware references.
- Chicago author-date bibliography before lettered appendices.
- Universe starter, packaging scripts, regression checks and CI configuration.
