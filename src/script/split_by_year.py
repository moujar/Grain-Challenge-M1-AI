#!/usr/bin/env python3
import argparse
import os
import re
import shutil
import sys
from typing import Optional, Iterable, Tuple

YEAR_RE = re.compile(r"_(20\d{2})-")


def parse_year_from_filename(filename: str) -> Optional[str]:
    """
    Extract a 4-digit year (e.g., 2020, 2021) from dataset filename.
    Expected pattern examples:
      - grain12205_x45y19-var4_11000_us_2x_2020-12-02T111648_corr.npz
      - grain26027_var8-x75y12_7000_us_2x_2021-10-20T111433_corr.npz
    """
    m = YEAR_RE.search(filename)
    if not m:
        return None
    return m.group(1)


def iter_npz_files(folder: str) -> Iterable[str]:
    for entry in os.scandir(folder):
        if not entry.is_file():
            continue
        if entry.name.endswith(".npz"):
            yield entry.path


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def action_apply(src: str, dst: str, mode: str, dry_run: bool) -> None:
    if dry_run:
        print(f"[DRY] {mode:7s} {src} -> {dst}")
        return
    if mode == "move":
        shutil.move(src, dst)
    elif mode == "copy":
        shutil.copy2(src, dst)
    elif mode == "symlink":
        # Overwrite if exists and points elsewhere
        if os.path.islink(dst) or os.path.exists(dst):
            try:
                os.remove(dst)
            except OSError:
                pass
        os.symlink(os.path.abspath(src), dst)
    else:
        raise ValueError(f"Unknown mode: {mode}")


def split_one_directory(
    src_dir: str,
    out_strategy: str,
    mode: str,
    years: Optional[Tuple[str, ...]],
    dry_run: bool,
) -> None:
    """
    Split files in src_dir by year into:
      - out_strategy == 'inplace': create subdirs inside src_dir: {src_dir}/2020, {src_dir}/2021
      - out_strategy == 'sibling': create sibling dir {src_dir}-{year}
    Action mode: 'symlink' (default), 'copy', or 'move'
    """
    if not os.path.isdir(src_dir):
        print(f"[WARN] Skipping non-existent directory: {src_dir}", file=sys.stderr)
        return

    # Collect targets and ensure output dirs
    detected_years = set()
    for f in iter_npz_files(src_dir):
        y = parse_year_from_filename(os.path.basename(f))
        if y:
            detected_years.add(y)
    if years:
        target_years = set(years)
    else:
        target_years = detected_years

    if not target_years:
        print(f"[INFO] No year tags found in: {src_dir}")
        return

    # Prepare output directories depending on strategy
    out_dirs = {}
    for y in sorted(target_years):
        if out_strategy == "inplace":
            od = os.path.join(src_dir, y)
        elif out_strategy == "sibling":
            od = f"{src_dir}-{y}"
        else:
            raise ValueError("out_strategy must be 'inplace' or 'sibling'")
        out_dirs[y] = od
        if not dry_run:
            ensure_dir(od)
        else:
            print(f"[DRY] mkdir -p {od}")

    # Apply split
    total = 0
    matched = 0
    for f in iter_npz_files(src_dir):
        total += 1
        y = parse_year_from_filename(os.path.basename(f))
        if not y or y not in out_dirs:
            continue
        dst = os.path.join(out_dirs[y], os.path.basename(f))
        action_apply(f, dst, mode=mode, dry_run=dry_run)
        matched += 1

    print(f"[DONE] {src_dir}: matched {matched}/{total} files into {sorted(target_years)} using mode={mode}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Split Grain dataset files by year (2020/2021) based on filename date tags."
    )
    p.add_argument(
        "--dirs",
        nargs="+",
        required=True,
        help="One or more source directories containing .npz files (e.g., data/Grain-Data-RGB data/Grain-Data).",
    )
    p.add_argument(
        "--out-strategy",
        choices=["inplace", "sibling"],
        default="inplace",
        help="Where to place year-split outputs: 'inplace' creates {dir}/{year}; 'sibling' creates {dir}-{year}.",
    )
    p.add_argument(
        "--mode",
        choices=["symlink", "copy", "move"],
        default="symlink",
        help="How to materialize split files. Default: symlink (non-destructive).",
    )
    p.add_argument(
        "--years",
        nargs="+",
        choices=["2020", "2021"],
        help="Restrict to specific years (default: auto-detect from filenames).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without making changes.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    for d in args.dirs:
        split_one_directory(
            src_dir=d,
            out_strategy=args.out_strategy,
            mode=args.mode,
            years=tuple(args.years) if args.years else None,
            dry_run=args.dry_run,
        )


if __name__ == "__main__":
    main()

