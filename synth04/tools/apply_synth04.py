#!/usr/bin/env python3
"""Integrate SYNTH 04 into a checked-out *existing* Hatchable public/ tree.

Dry-run by default. Never publishes. Does not touch live production.

Usage:
  python tools/apply_synth04.py /path/to/public
  python tools/apply_synth04.py /path/to/public --apply --backup /path/to/backup
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SRC_PUBLIC = PACKAGE_ROOT / "public"

# Relative paths this package is allowed to write under public/
MANAGED = [
    "app/projects/index.html",
    "app/projects/synth04.css",
    "app/projects/synth04.js",
    "app/projects/synth04-laptop.webp",
    "app/projects/synth04-phone.webp",
    "app/projects/synth04-ribbon.webp",
    "app/synth04-global.css",
    "app/synth04-global.js",
    "app/synth04-sf-overlay.css",
]


def die(msg: str, code: int = 1) -> None:
    print(f"[apply_synth04] ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def check_public_layout(public: Path) -> None:
    if not public.is_dir():
        die(f"Not a directory: {public}")
    app = public / "app"
    if not app.is_dir():
        die(f"Expected Hatchable layout with public/app/: missing {app}")
    # Soft checks — do not fail if some routes are absent in a partial checkout
    for name in ("mobile.css", "sections.css"):
        if not (app / name).exists():
            print(f"[apply_synth04] WARN: {app / name} not found (continuing)")


def plan(public: Path) -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    for rel in MANAGED:
        src = SRC_PUBLIC / rel
        dst = public / rel
        if not src.exists():
            # overlay is optional if only full CSS is present
            if rel.endswith("synth04-sf-overlay.css"):
                continue
            die(f"Package file missing: {src}")
        pairs.append((src, dst))
    return pairs


def backup_existing(pairs: list[tuple[Path, Path]], backup_root: Path) -> None:
    backup_root.mkdir(parents=True, exist_ok=True)
    for _src, dst in pairs:
        if dst.exists():
            target = backup_root / dst.name
            # keep relative structure lightly
            rel_parent = dst.parent.name
            target = backup_root / rel_parent / dst.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dst, target)
            print(f"  backup: {dst} -> {target}")


def apply_pairs(pairs: list[tuple[Path, Path]]) -> None:
    for src, dst in pairs:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  wrote: {dst}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Apply SYNTH 04 SF Humanoid to Hatchable public/")
    parser.add_argument("public", type=Path, help="Path to Hatchable public/ directory")
    parser.add_argument("--apply", action="store_true", help="Write files (default is dry-run)")
    parser.add_argument("--backup", type=Path, default=None, help="Backup dir for overwritten files")
    args = parser.parse_args(argv)

    public = args.public.resolve()
    check_public_layout(public)
    pairs = plan(public)

    print(f"[apply_synth04] target: {public}")
    print(f"[apply_synth04] package: {PACKAGE_ROOT}")
    print(f"[apply_synth04] files: {len(pairs)}")
    for src, dst in pairs:
        status = "UPDATE" if dst.exists() else "CREATE"
        print(f"  {status}  {dst.relative_to(public)}  <-  {src.relative_to(PACKAGE_ROOT)}")

    if not args.apply:
        print("[apply_synth04] dry-run only. Re-run with --apply to write.")
        return 0

    if args.backup:
        print(f"[apply_synth04] backing up to {args.backup}")
        backup_existing(pairs, args.backup.resolve())

    print("[apply_synth04] applying...")
    apply_pairs(pairs)
    print("[apply_synth04] done. Review on device before publishing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
