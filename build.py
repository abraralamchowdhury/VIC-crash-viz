#!/usr/bin/env python3
"""Build a self-contained HTML animation comparing two years of Victoria road crashes.

Usage:
    python build.py data/crashes.csv --years 2020 2025 --out docs/index.html
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

# Bounding box of Victoria (used to drop bad coordinates and to project to x/y)
LON0, LON1 = 140.9, 150.1
LAT0, LAT1 = -39.3, -33.9
COS_LAT = np.cos(np.radians(-37))  # simple equirectangular projection
COLS = ["ACCIDENT_DATE", "ACCIDENT_TIME", "SEVERITY", "LATITUDE", "LONGITUDE"]


def severity_code(text: str) -> int:
    """0 = fatal, 1 = serious injury, 2 = other."""
    text = text.lower()
    return 0 if "fatal" in text else 1 if "serious" in text else 2


def load(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path, usecols=COLS).dropna(subset=["LATITUDE", "LONGITUDE"])
    df = df[df.LATITUDE.between(LAT0, LAT1) & df.LONGITUDE.between(LON0, LON1)]
    return df


def encode_year(df: pd.DataFrame, year: int):
    d = df[df.ACCIDENT_DATE.str.startswith(str(year))]
    if d.empty:
        raise SystemExit(f"No crashes found for {year}")
    stamp = pd.to_datetime(d.ACCIDENT_DATE + " " + d.ACCIDENT_TIME)
    hour = ((stamp - pd.Timestamp(f"{year}-01-01")).dt.total_seconds() // 3600).astype(int).clip(0, 8759)
    sev = d.SEVERITY.map(severity_code)
    x = ((d.LONGITUDE - LON0) * COS_LAT * 1e3).round().astype(int)
    y = ((d.LATITUDE - LAT0) * 1e3).round().astype(int)
    rows = pd.DataFrame({"x": x, "y": y, "h": hour, "s": sev}).sort_values("h")
    daily = np.bincount(np.minimum(rows.h // 24, 364), minlength=365).tolist()
    return rows, daily, int((sev == 0).sum())


def compact(obj) -> str:
    return json.dumps(obj, separators=(",", ":"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", type=Path, help="CSV with " + ", ".join(COLS))
    ap.add_argument("--years", type=int, nargs=2, default=[2020, 2025], metavar=("A", "B"))
    ap.add_argument("--out", type=Path, default=Path("docs/index.html"))
    ap.add_argument("--template", type=Path, default=Path(__file__).parent / "templates" / "compare.html")
    args = ap.parse_args()

    df = load(args.csv)
    (ra, da, fa), (rb, db, fb) = (encode_year(df, y) for y in args.years)
    width = int(((df.LONGITUDE - LON0) * COS_LAT * 1e3).max())
    height = int(((df.LATITUDE - LAT0) * 1e3).max())

    html = args.template.read_text()
    for key, val in {
        "__DATA_A__": compact(ra.values.ravel().tolist()),
        "__DAY_A__": compact(da),
        "__DATA_B__": compact(rb.values.ravel().tolist()),
        "__DAY_B__": compact(db),
        "__YEAR_A__": str(args.years[0]),
        "__YEAR_B__": str(args.years[1]),
        "__W__": str(width),
        "__H__": str(height),
    }.items():
        html = html.replace(key, val)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html)
    print(f"{args.years[0]}: {len(ra):,} crashes, {fa} fatal")
    print(f"{args.years[1]}: {len(rb):,} crashes, {fb} fatal")
    print(f"Wrote {args.out} ({args.out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
