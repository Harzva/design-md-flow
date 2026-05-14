# AGENTS.md

Use this repository as a portable Agent Skill plus a small Python CLI. Keep it lightweight and dependency-free unless a new dependency removes real operational friction.

## Development Commands

```bash
python -m unittest discover -s tests
python scripts/design_md_flow.py --help
python scripts/design_md_flow.py doctor --offline
```

## Editing Rules

- Keep `SKILL.md` concise and focused on agent behavior.
- Keep `scripts/design_md_flow.py` compatible with the Python standard library.
- Do not commit private tokens, local absolute paths, generated caches, or account-specific setup.
- Update README commands when CLI flags or workflow names change.
- Regenerate README assets only when `docs/preview.html` or the first-screen story changes.

## Release Checklist

- Tests pass on the local machine.
- `quick_validate.py` accepts the skill folder.
- README links point to repo-owned files or stable public URLs.
- GitHub Actions CI passes after push.
- If `docs/` changes, the Pages workflow should publish the updated preview.
