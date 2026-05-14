# Security

DesignMD Flow does not require secrets, API keys, or privileged local access.

## Reporting

Open a GitHub issue for low-risk documentation or CLI hardening problems. If a report includes private credentials, private repository details, or exploitable security impact, contact the repository owner privately instead of posting the secret publicly.

## Scope

In scope:

- Accidental secret exposure in examples, docs, or workflows.
- Unsafe overwrite behavior in the helper CLI.
- Network handling that could mislead users about downloaded `DESIGN.md` files.

Out of scope:

- Third-party website design ownership disputes.
- Vulnerabilities in upstream repositories or GitHub-hosted services.

## Safety Notes

- The helper downloads public `DESIGN.md` files from `VoltAgent/awesome-design-md` unless `--source` points to a local clone.
- The helper refuses to overwrite an existing `DESIGN.md` unless `--overwrite` is explicitly provided.
- Treat third-party visual systems as design inspiration, not permission to copy protected brand assets.
