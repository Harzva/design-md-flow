# DesignMD Flow Reference

## What This Wraps

- Google Stitch design-md: generates semantic DESIGN.md files from Stitch projects and treats the file as a design-system source of truth for agents.
- Google stitch-skills: packages design work into agent skills such as `stitch-design`, `design-md`, `stitch-loop`, and `react-components`.
- VoltAgent awesome-design-md/getdesign.md: provides ready-to-use DESIGN.md examples extracted from public websites.

DesignMD Flow turns those pieces into an implementation loop:

```text
brief -> choose style -> install DESIGN.md -> implement UI -> screenshot QA -> revise DESIGN.md/code -> ship
```

## Installing A Style

Prefer the helper script:

```bash
python scripts/design_md_flow.py list
python scripts/design_md_flow.py show claude
python scripts/design_md_flow.py install claude --project .
```

Use a local source when available:

```bash
python scripts/design_md_flow.py install claude --project . --source /path/to/awesome-design-md
```

The script does not overwrite an existing DESIGN.md unless `--overwrite` is passed.

## Working With Existing Projects

1. Locate the project root by checking for package manifests, framework config, or app entry files.
2. Inspect existing design tokens, CSS variables, Tailwind config, theme providers, component libraries, and any current screenshots.
3. Install or adapt DESIGN.md at the root.
4. Map DESIGN.md tokens into the existing styling system instead of inventing a parallel one.
5. Build the requested screen/component.
6. Run the app, screenshot desktop and mobile, then fix visible mismatches.

## Creating A Custom DESIGN.md

Use this when the requested style is missing or the user wants a proprietary/local brand:

1. Gather official source pages, screenshots, existing app styles, and any brand notes.
2. Extract atmosphere, color roles, typography, component language, spacing, depth, motion, responsive behavior, and anti-patterns.
3. Write the result as a project-specific DESIGN.md. Include exact colors and concrete UI rules.
4. Avoid protected logos, names, and asset copying unless the user owns or supplies them.
5. Verify by implementing a representative screen and adjusting the file where the agent misunderstood the style.

## Visual QA Checklist

- Does the first viewport immediately communicate the selected visual language?
- Are primary, secondary, muted, danger, and success colors used according to documented roles?
- Do type scale, weights, line heights, and letter spacing match the file?
- Are buttons, inputs, cards, nav, tables, and modals using the documented geometry and states?
- Is spacing consistent across desktop and mobile?
- Are there overflow, clipping, low-contrast, or text-fit problems?
- Did the implementation avoid brand plagiarism while preserving useful design cues?

## Good User-Facing Names

Recommended repository name: `design-md-flow`.

Why it travels well:

- Includes the exact searchable standard name: `design-md`.
- Says what the wrapper adds: a flow/workflow, not another asset dump.
- Short enough for GitHub, npm packages, docs headings, and skill triggers.
- Easy tagline: "Pick a DESIGN.md, install it, build, screenshot-QA, iterate."
