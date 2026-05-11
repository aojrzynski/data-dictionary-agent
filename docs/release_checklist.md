# Release Checklist

Manual release readiness checklist for maintainers.

- Run full tests (`python -m pytest`).
- Run deterministic smoke command.
- Run config override smoke command.
- Run agent mode smoke command.
- Run LLM fallback smoke command (without API key).
- Inspect generated artifacts for expected files and readability.
- Check README links and key docs links.
- Confirm GitHub repo description text.
- Add/update GitHub topics/tags.
- Create release tag and GitHub release notes.
- Optional: prepare social/preview image.
