#!/usr/bin/env python3
"""Fix broken asset paths in HTML/CSS by matching filenames found under ./assets/

Usage:
  python3 fix_assets.py /path/to/site-root

What it does:
- Scans the site's assets directory recursively.
- Builds a filename -> relative path map (prefers paths containing "common/products" if multiple matches).
- Rewrites:
    - HTML: src/href values that contain "assets/img/..." (or "../img/...") to the matched asset path.
    - CSS:  url(...) references that contain "../img/..." or "/img/..." to the matched asset path.
- Writes files in-place (creates .bak backups).
"""

from __future__ import annotations
import argparse
import os
import re
from pathlib import Path

IMG_EXTS = {".png",".jpg",".jpeg",".svg",".webp",".gif"}
MEDIA_EXTS = IMG_EXTS | {".mp4",".webm",".mov"}

def build_asset_map(site_root: Path) -> dict[str,str]:
    assets_dir = site_root / "assets"
    if not assets_dir.exists():
        raise SystemExit(f"assets/ 폴더를 찾을 수 없습니다: {assets_dir}")
    by_name: dict[str,list[Path]] = {}
    for p in assets_dir.rglob("*"):
        if p.is_file() and p.suffix.lower() in MEDIA_EXTS:
            by_name.setdefault(p.name, []).append(p)

    def choose(name: str) -> str:
        cands = by_name[name]
        rels = [p.relative_to(site_root).as_posix() for p in cands]
        # Prefer "common/products" if present (your zip structure)
        rels.sort(key=lambda r: (0 if "common/products" in r else 1, len(r)))
        return rels[0]

    return {name: choose(name) for name in by_name.keys()}

def fix_html(text: str, name_map: dict[str,str]) -> str:
    # assets/img/.../file.ext  -> matched path
    def repl_assets_img(m: re.Match) -> str:
        fname = m.group(2)
        return name_map.get(fname, m.group(0))

    text = re.sub(r'assets/img/([A-Za-z0-9_\-/]+)/([A-Za-z0-9_\-]+\.(?:png|jpg|jpeg|svg|webp|gif))',
                  repl_assets_img, text)

    # ../img/.../file.ext -> matched path (for HTML)
    def repl_dotdot_img(m: re.Match) -> str:
        fname = m.group(2)
        return name_map.get(fname, m.group(0))

    text = re.sub(r'\.\./img/([A-Za-z0-9_\-/]+)/([A-Za-z0-9_\-]+\.(?:png|jpg|jpeg|svg|webp|gif))',
                  repl_dotdot_img, text)

    return text

def fix_css(text: str, name_map: dict[str,str]) -> str:
    # Replace url(../img/.../file.ext) etc.
    def repl(m: re.Match) -> str:
        raw = m.group(1).strip().strip('"'')

        # Skip data: and http(s):
        if raw.startswith("data:") or raw.startswith("http"):
            return m.group(0)

        # Extract filename
        fname = Path(re.split(r"[?#]", raw)[0]).name
        if fname in name_map:
            new = name_map[fname]
            return f"url('{new}')"
        return m.group(0)

    return re.sub(r"url\(([^)]+)\)", repl, text)

def process_files(site_root: Path, name_map: dict[str,str]) -> None:
    targets = list(site_root.rglob("*.html")) + list(site_root.rglob("*.css"))
    for p in targets:
        try:
            original = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            original = p.read_text(encoding="utf-8", errors="ignore")

        if p.suffix.lower() == ".html":
            fixed = fix_html(original, name_map)
        else:
            fixed = fix_css(original, name_map)

        if fixed != original:
            backup = p.with_suffix(p.suffix + ".bak")
            if not backup.exists():
                backup.write_text(original, encoding="utf-8")
            p.write_text(fixed, encoding="utf-8")
            print(f"FIXED: {p}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site_root", nargs="?", default=".", help="사이트 루트( index.html, assets/ 가 있는 폴더 )")
    args = ap.parse_args()

    site_root = Path(args.site_root).resolve()
    name_map = build_asset_map(site_root)
    process_files(site_root, name_map)
    print("Done.")

if __name__ == "__main__":
    main()
