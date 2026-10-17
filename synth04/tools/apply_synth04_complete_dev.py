#!/usr/bin/env python3
"""Build a *local DEV copy* of the existing Hatchable mobile web app using the
full, approved SYNTH04 archive and Grok's optional SF Humanoid visual overlay.
DRY RUN by default. Does not contact Hatchable, GitHub, or production.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
ZIP_SHA256 = "bac708d9f2f4e4b6a342157c3e7dfbdb3e56f054aab8dd2196092102b2aa9810"
MANAGED = {
    "app/projects/index.html": "bbbd9c65e8deb90caf54461a6f9eaaecd5abf9eea79a4bea8a9844d10d9120ed",
    "app/projects/synth04-laptop.webp": "a93e8fc3eddc8f562f9955b2df2426fe2dabb18f34dec978016745d6c0fdf62b",
    "app/projects/synth04-phone.webp": "347999a2d302d3cf21318e1371713f3ca1f0f7a7d8eeff1a19b2fb8e6b830453",
    "app/projects/synth04-ribbon.webp": "86cfc5a4b5557ef894df8a5977da4501ae2741c1b42b59f0a3ed36e90db0ecdf",
    "app/projects/synth04.css": "e05eea789987440ade01b2bf9f1078e95bacd1225482ee7d7bc5d08ef9112e5b",
    "app/projects/synth04.js": "1c53f8e1c89f294410fc5f798c4792bdb0580149f0294d89c076953a5937902b",
    "app/synth04-global.css": "5a1296571c55f8cbf973d00739e81fb54f8fa8ac4ba290041210f60138ae24b3",
    "app/synth04-global.js": "46b0e484b746a88a893968f6de2131251e72f4ca25da2bb4dcbc536b751c2186",
}
ROUTES = ["app/index.html", "app/projects/index.html", "app/ai/index.html",
          "app/forum/index.html", "app/account/index.html"]
OVERLAY = "app/synth04-sf-overlay.css"
ADD_TO_CACHE = [
    "/app/synth04-global.css", "/app/synth04-global.js",
    "/app/synth04-sf-overlay.css", "/app/projects/synth04.css",
    "/app/projects/synth04.js", "/app/projects/synth04-laptop.webp",
    "/app/projects/synth04-phone.webp", "/app/projects/synth04-ribbon.webp",
]


def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def stop(message: str) -> None:
    raise SystemExit("STOP (no files applied): " + message)


def inject_once(html: str, tag: str, where: str) -> str:
    if tag in html:
        return html
    if where not in html:
        stop("Expected HTML insertion point is missing: " + where)
    return html.replace(where, tag + "\n" + where, 1)


def main() -> None:
    p = argparse.ArgumentParser(description="SYNTH04 integration for local Hatchable DEV checkout only")
    p.add_argument("public", type=Path, help="An OFFLINE / DEV checkout's public/ directory")
    p.add_argument("--package", type=Path, required=True, help="Full BUXY_DIGITAL_SYNTH04_5_PAGINI_DEV_COMPLET.zip")
    p.add_argument("--apply", action="store_true", help="Opt-in to local writes, requires DEV sentinel and backup")
    p.add_argument("--backup", type=Path, help="Required with --apply; must be outside the public directory")
    p.add_argument("--no-sf-overlay", action="store_true", help="Leave out Grok's extra grid / scanlines")
    args = p.parse_args()
    dest = args.public.resolve()
    if dest.name != "public" or not dest.is_dir():
        stop("Point to an existing DEV checkout folder ending in /public.")
    if args.apply:
        if not (dest.parent / ".buxy-synth04-dev").is_file():
            stop("Missing .buxy-synth04-dev sentinel next to public/; refuses writes.")
        if not args.backup:
            stop("--apply requires --backup with a separate destination.")
        backup = args.backup.resolve()
        if backup == dest or dest in backup.parents or backup == dest.parent:
            stop("Backup cannot be in/at the live target public/ tree.")
        if backup.exists() and any(backup.iterdir()):
            stop("Backup directory must not already contain files.")
    for rel in ROUTES + ["app/app.js", "app/sw.js", "app/mobile.css",
                         "app/sections.css", "app/ai.js", "app/forum.js", "app/account.js"]:
        if not (dest / rel).is_file():
            stop("Source checkout is incomplete: " + rel)
    if not args.package.is_file():
        stop("Missing full source archive: " + str(args.package))
    archive = args.package.read_bytes()
    if digest(archive) != ZIP_SHA256:
        stop("The provided ZIP differs from the reviewed full SYNTH04 package (SHA-256).")
    planned: dict[str, bytes] = {}
    with ZipFile(args.package) as z:
        for rel, sha in MANAGED.items():
            src = "public/" + rel
            if src not in z.namelist():
                stop("Source archive is incomplete: " + src)
            payload = z.read(src)
            if digest(payload) != sha:
                stop("Asset or component hash mismatch: " + src)
            planned[rel] = payload

    if not args.no_sf_overlay:
        sf = ROOT / "public" / OVERLAY
        if not sf.is_file():
            stop("Missing Grok's overlay CSS in the source branch.")
        planned[OVERLAY] = sf.read_bytes()

    # Replace Projects from complete archive (NOT truncated Projects from Grok).
    projects = planned["app/projects/index.html"].decode("utf-8")
    if not args.no_sf_overlay:
        projects = inject_once(projects,
            '<link rel="stylesheet" href="/app/synth04-sf-overlay.css">',
            "</head>")
    planned["app/projects/index.html"] = projects.encode("utf-8")

    # Preserve existing authenticated pages and their JS. Add only a themed body
    # class and local CSS/JS imports; no replacement of API/auth/live logic.
    for rel in ROUTES:
        if rel == "app/projects/index.html":
            continue
        html = (dest / rel).read_text(encoding="utf-8")
        if '<body>' in html:
            html = html.replace('<body>', '<body class="s04-mobile-page">', 1)
        elif "s04-mobile-page" not in html:
            stop("Existing page body layout differs: " + rel)
        html = inject_once(html,
            '<link rel="stylesheet" href="/app/synth04-global.css">', "</head>")
        if not args.no_sf_overlay:
            html = inject_once(html,
                '<link rel="stylesheet" href="/app/synth04-sf-overlay.css">', "</head>")
        html = inject_once(html,
            '<script src="/app/synth04-global.js" defer></script>', "</body>")
        planned[rel] = html.encode("utf-8")

    # Update *static* service-worker asset cache only. No API or client records
    # are precached; network-only behavior remains unchanged.
    sw = (dest / "app/sw.js").read_text(encoding="utf-8")
    if "buxy-mobile-v4" in sw:
        sw = sw.replace("buxy-mobile-v4", "buxy-mobile-v5-synth04")
    elif "buxy-mobile-v5-synth04" not in sw:
        stop("Unexpected service worker cache version; review before changing.")
    missing = [s for s in ADD_TO_CACHE if ("'" + s + "'") not in sw]
    if args.no_sf_overlay:
        missing = [s for s in missing if s != "/app/synth04-sf-overlay.css"]
    if missing:
        marker = "const OPTIONAL=["
        if marker not in sw:
            stop("Unknown SW structure, cannot safely inject static resources.")
        sw = sw.replace(marker, marker + "\n  " +
                        ",\n  ".join(repr(s) for s in missing) + ",", 1)
    planned["app/sw.js"] = sw.encode("utf-8")

    for rel in ROUTES:
        html = planned[rel].decode("utf-8")
        for route in ("/app/", "/app/projects/", "/app/ai/",
                      "/app/forum/", "/app/account/"):
            if 'href="' + route + '"' not in html:
                stop("Mobile navigation would lose " + route + " in " + rel)
    if "id=\"aiBuild\"" not in planned["app/ai/index.html"].decode("utf-8"):
        stop("AI action is missing; refusing a destructive substitution.")

    print("SYNTH04 DEV integration | files:", len(planned))
    for rel, payload in sorted(planned.items()):
        target = dest / rel
        before = target.read_bytes() if target.exists() else None
        state = "UNCHANGED" if before == payload else ("UPDATE" if before is not None else "ADD")
        print("%9s  %s  (%s bytes)" % (state, rel, len(payload)))
    if not args.apply:
        print("DRY RUN: no files modified. Pass --apply --backup <empty-dir> for local DEV only.")
        return

    # All validation is finished. Make a faithful backup (relative paths).
    backup.mkdir(parents=True, exist_ok=False)
    for rel in planned:
        src = dest / rel
        if src.is_file():
            target = backup / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
    for rel, payload in planned.items():
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, tempname = tempfile.mkstemp(dir=target.parent, prefix=".s04-")
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(payload)
            os.replace(tempname, target)
        finally:
            if os.path.exists(tempname):
                os.unlink(tempname)
    print("Applied to local DEV checkout; backups in:", backup)
    print("NOT DEPLOYED. Test locally and obtain owner approval before any deployment.")


if __name__ == "__main__":
    main()
