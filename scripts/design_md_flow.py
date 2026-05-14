#!/usr/bin/env python3
"""Small helper for installing DESIGN.md files from awesome-design-md."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path
from typing import Iterable


API_URL = "https://api.github.com/repos/VoltAgent/awesome-design-md/contents/design-md?ref=main"
RAW_URL = "https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/{slug}/DESIGN.md"
PAGE_URL = "https://getdesign.md/{slug}/design-md"
USER_AGENT = "design-md-flow/0.1"


class FlowError(RuntimeError):
    pass


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        raise FlowError(f"HTTP {exc.code} while fetching {url}") from exc
    except urllib.error.URLError as exc:
        raise FlowError(f"Network error while fetching {url}: {exc.reason}") from exc


def fetch_text(url: str) -> str:
    return fetch_bytes(url).decode("utf-8")


def source_design_root(source: str | None) -> Path | None:
    if not source:
        return None
    root = Path(source).expanduser().resolve()
    design_root = root / "design-md"
    if design_root.is_dir():
        return design_root
    if root.name == "design-md" and root.is_dir():
        return root
    raise FlowError(f"Source does not look like awesome-design-md: {root}")


def list_local(source: str) -> list[str]:
    design_root = source_design_root(source)
    assert design_root is not None
    return sorted(
        child.name
        for child in design_root.iterdir()
        if child.is_dir() and (child / "DESIGN.md").is_file()
    )


def list_remote() -> list[str]:
    payload = json.loads(fetch_text(API_URL))
    return sorted(item["name"] for item in payload if item.get("type") == "dir")


def read_design(slug: str, source: str | None) -> bytes:
    if source:
        design_root = source_design_root(source)
        assert design_root is not None
        path = design_root / slug / "DESIGN.md"
        if not path.is_file():
            raise FlowError(f"No DESIGN.md for slug '{slug}' in {design_root}")
        return path.read_bytes()
    return fetch_bytes(RAW_URL.format(slug=slug))


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    match = re.match(r"---\s*\n(.*?)\n---", text, re.S)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def command_list(args: argparse.Namespace) -> int:
    slugs = list_local(args.source) if args.source else list_remote()
    for slug in slugs:
        print(slug)
    print(f"\n{len(slugs)} styles")
    return 0


def command_show(args: argparse.Namespace) -> int:
    data = read_design(args.slug, args.source)
    text = data.decode("utf-8", errors="replace")
    fields = parse_frontmatter(text)
    print(f"slug: {args.slug}")
    if fields.get("name"):
        print(f"name: {fields['name']}")
    if fields.get("description"):
        print(f"description: {fields['description']}")
    print(f"page: {PAGE_URL.format(slug=args.slug)}")
    print(f"raw: {RAW_URL.format(slug=args.slug)}")
    print(f"bytes: {len(data)}")
    return 0


def command_install(args: argparse.Namespace) -> int:
    project = Path(args.project).expanduser().resolve()
    if not project.exists():
        raise FlowError(f"Project path does not exist: {project}")
    if not project.is_dir():
        raise FlowError(f"Project path is not a directory: {project}")

    dest = project / args.dest
    data = read_design(args.slug, args.source)

    if args.dry_run:
        print(f"would install: {args.slug}")
        print(f"destination: {dest}")
        print(f"bytes: {len(data)}")
        return 0

    if dest.exists() and not args.overwrite:
        raise FlowError(f"{dest} already exists. Re-run with --overwrite if intended.")

    dest.write_bytes(data)
    print(f"installed {args.slug} -> {dest}")
    print(f"page: {PAGE_URL.format(slug=args.slug)}")
    return 0


def iter_checks(text: str) -> Iterable[tuple[bool, str]]:
    lowered = text.lower()
    yield ("color" in lowered or "palette" in lowered), "colors or palette"
    yield ("typography" in lowered or "fontfamily" in lowered), "typography"
    yield ("component" in lowered or "buttons" in lowered), "components"
    yield ("layout" in lowered or "spacing" in lowered), "layout or spacing"
    yield ("responsive" in lowered or "breakpoint" in lowered), "responsive behavior"


def command_verify(args: argparse.Namespace) -> int:
    path = Path(args.project).expanduser().resolve() / args.dest
    if not path.is_file():
        raise FlowError(f"Missing {path}")

    text = path.read_text(encoding="utf-8", errors="replace")
    missing = [label for ok, label in iter_checks(text) if not ok]
    print(f"file: {path}")
    print(f"bytes: {path.stat().st_size}")
    if missing:
        print("status: warning")
        print("missing signals: " + ", ".join(missing))
        return 1
    print("status: ok")
    return 0


def command_open(args: argparse.Namespace) -> int:
    url = PAGE_URL.format(slug=args.slug)
    webbrowser.open(url)
    print(url)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install and inspect DESIGN.md styles.")
    sub = parser.add_subparsers(dest="command", required=True)

    list_p = sub.add_parser("list", help="List available style slugs.")
    list_p.add_argument("--source", help="Path to a local awesome-design-md clone.")
    list_p.set_defaults(func=command_list)

    show_p = sub.add_parser("show", help="Show metadata for one style.")
    show_p.add_argument("slug")
    show_p.add_argument("--source", help="Path to a local awesome-design-md clone.")
    show_p.set_defaults(func=command_show)

    install_p = sub.add_parser("install", help="Install a DESIGN.md into a project root.")
    install_p.add_argument("slug")
    install_p.add_argument("--project", default=".", help="Project root. Defaults to cwd.")
    install_p.add_argument("--source", help="Path to a local awesome-design-md clone.")
    install_p.add_argument("--dest", default="DESIGN.md", help="Destination filename.")
    install_p.add_argument("--overwrite", action="store_true")
    install_p.add_argument("--dry-run", action="store_true")
    install_p.set_defaults(func=command_install)

    verify_p = sub.add_parser("verify", help="Sanity-check a project DESIGN.md.")
    verify_p.add_argument("--project", default=".", help="Project root. Defaults to cwd.")
    verify_p.add_argument("--dest", default="DESIGN.md", help="Destination filename.")
    verify_p.set_defaults(func=command_verify)

    open_p = sub.add_parser("open", help="Open the getdesign.md page for a style.")
    open_p.add_argument("slug")
    open_p.set_defaults(func=command_open)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except FlowError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
