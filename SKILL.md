---
name: design-md-flow
description: Install, select, adapt, and apply DESIGN.md design-system files as a repeatable AI frontend workflow. Use when the user mentions DESIGN.md, getdesign.md, awesome-design-md, Google Stitch DESIGN.md, brand-inspired UI generation, installing a design style into a project, or turning a design reference into a workflow skill for agents.
---

# DesignMD Flow

## Purpose

Use DESIGN.md as a lightweight design contract for frontend agents: choose a visual language, install it at the project root, build against it, then visually verify the result. This wraps Google Stitch's DESIGN.md idea and VoltAgent's awesome-design-md sample library into a practical coding workflow.

## Quick Start

Run the helper from this skill when the user needs a DESIGN.md installed:

```bash
python scripts/design_md_flow.py list
python scripts/design_md_flow.py install claude --project /path/to/project
python scripts/design_md_flow.py verify --project /path/to/project
python scripts/design_md_flow.py doctor --project /path/to/project
```

If a local clone of `VoltAgent/awesome-design-md` exists, prefer it with `--source /path/to/awesome-design-md` for speed and reproducibility.

## Workflow

1. Identify the target product, audience, and UI surface before selecting a style. For vague requests, offer 2-3 good style candidates and say why each fits.
2. Check whether the project already has `DESIGN.md`. Do not overwrite it without explicit user intent; use `--overwrite` only after the user asks or after you have made a backup.
3. Install one primary style with `scripts/design_md_flow.py install <slug> --project <project-root>`. Avoid blending more than two style sources unless the user explicitly wants a hybrid.
4. Read the installed `DESIGN.md` before editing UI code. Extract concrete tokens, layout rules, typography, component states, spacing, and anti-patterns.
5. Implement within the repo's existing frontend conventions. Treat `DESIGN.md` as design direction, not permission to copy protected logos, names, or proprietary assets.
6. Run the app and perform visual QA. For web apps, capture at least desktop and mobile screenshots and fix mismatches in hierarchy, spacing, color roles, typography, overflow, and interaction states.
7. If the result diverges because the style file is too generic, revise `DESIGN.md` into a project-specific design contract and keep the selected source style as inspiration.

For deeper guidance, read `references/workflow.md`.

## Selection Heuristics

- Developer tools and SaaS: start with `vercel`, `linear.app`, `cursor`, `mintlify`, `raycast`, `resend`, or `supabase`.
- AI products: start with `claude`, `runwayml`, `mistral.ai`, `replicate`, `together.ai`, `x.ai`, or `voltagent`.
- Commerce and consumer: start with `apple`, `airbnb`, `nike`, `shopify`, `spotify`, or `pinterest`.
- Enterprise/data products: start with `ibm`, `hashicorp`, `mongodb`, `clickhouse`, `sentry`, or `intercom`.
- Luxury/editorial: start with `bugatti`, `ferrari`, `lamborghini`, `wired`, `theverge`, or `mastercard`.

If the user asks for an unavailable brand such as OpenAI, create a custom `DESIGN.md` by analyzing official pages, screenshots, and the existing codebase. Make the result "inspired by" the visual language rather than a clone.

## Prompt Pattern

After installing a style, use a compact implementation prompt:

```text
Use the project root DESIGN.md as the design contract. Build [surface].
Preserve existing app architecture. Match the documented color roles, typography,
component styling, spacing, responsive behavior, and do/don't guardrails.
Verify with screenshots on desktop and mobile, then iterate until the UI reads
as the selected visual language without copying protected brand assets.
```

## Scripts

- `scripts/design_md_flow.py list`: list available slugs from GitHub or a local clone.
- `scripts/design_md_flow.py show <slug>`: print source metadata and links.
- `scripts/design_md_flow.py install <slug> --project <path>`: copy or download a `DESIGN.md`.
- `scripts/design_md_flow.py verify --project <path>`: sanity-check the installed file.
- `scripts/design_md_flow.py doctor --project <path>`: check project path, optional local source, and remote catalog access.

Use `--json` on `list`, `show`, `install`, `verify`, and `doctor` when another script or agent needs structured output.

## Output Discipline

When reporting back to the user, include the chosen style slug, where `DESIGN.md` was installed, what visual QA was run, and any remaining design risks. Keep source attributions concise: Google Stitch defines the DESIGN.md/skills direction; awesome-design-md/getdesign.md supplies brand-style examples.
