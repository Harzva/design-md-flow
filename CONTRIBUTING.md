# Contributing

DesignMD Flow is intentionally small: one skill, one helper script, and a clear workflow. Contributions should keep it portable and useful for any agent-friendly frontend project.

## Good Contributions

- Improve `SKILL.md` instructions without adding local-machine assumptions.
- Add tests for `scripts/design_md_flow.py`.
- Improve README examples, screenshots, or cross-platform commands.
- Harden error messages for missing projects, unknown slugs, or network failures.

## Quality Bar

- Professional: clear naming, truthful claims, tested commands.
- Beautiful: readable README structure, useful visuals, no noisy badges.
- Universal: no private tokens, no local absolute paths, no Harzva-only setup.

## Checks

```bash
python -m unittest discover -s tests
python scripts/design_md_flow.py --help
```
