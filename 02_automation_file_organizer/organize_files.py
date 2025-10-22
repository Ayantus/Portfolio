#!/usr/bin/env python3
"""
File Organizer — Night‑shift friendly
------------------------------------
Renames or moves files in a folder by date and file type.

Usage:
  python organize_files.py --src "/path/to/downloads" --dst "/path/to/sorted" --dry-run
  python organize_files.py --src "/path/to/downloads" --dst "/path/to/sorted"

Features:
  - Groups files into folders by extension (e.g., images, docs, audio, video, other)
  - Adds a date prefix (YYYYMMDD) to filenames
  - Dry-run mode to preview changes
"""

import argparse, os, shutil, datetime, pathlib

GROUPS = {
    "images": {".png",".jpg",".jpeg",".gif",".webp",".bmp",".tiff"},
    "docs": {".pdf",".doc",".docx",".xls",".xlsx",".csv",".txt",".rtf",".md",".ppt",".pptx"},
    "audio": {".mp3",".wav",".m4a",".aac",".flac"},
    "video": {".mp4",".mov",".avi",".mkv",".webm"},
}

def group_for_extension(ext: str) -> str:
    ext = ext.lower()
    for g, exts in GROUPS.items():
        if ext in exts:
            return g
    return "other"

def organize(src: str, dst: str, dry_run: bool = True) -> list[tuple[str, str]]:
    src_p = pathlib.Path(src)
    dst_p = pathlib.Path(dst)
    actions = []
    today = datetime.date.today().strftime("%Y%m%d")

    if not src_p.exists():
        raise FileNotFoundError(f"Source folder not found: {src}")

    dst_p.mkdir(parents=True, exist_ok=True)

    for path in src_p.iterdir():
        if not path.is_file():
            continue
        group = group_for_extension(path.suffix)
        target_dir = dst_p / group
        target_dir.mkdir(parents=True, exist_ok=True)

        new_name = f"{today}_{path.name}"
        target_path = target_dir / new_name
        actions.append((str(path), str(target_path)))
        if not dry_run:
            shutil.move(str(path), str(target_path))

    return actions

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="Source folder to organize")
    ap.add_argument("--dst", required=True, help="Destination root folder")
    ap.add_argument("--dry-run", action="store_true", help="Preview only, do not move files")
    args = ap.parse_args()

    actions = organize(args.src, args.dst, dry_run=args.dry_run)
    if args.dry_run:
        print("Planned moves:")
        for a,b in actions:
            print(a, "=>", b)
    else:
        print(f"Moved {len(actions)} files.")

if __name__ == "__main__":
    main()
