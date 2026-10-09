# Victoria Road Crashes: Year vs Year

An animated, glow-style map that replays two years of police-reported road crashes in Victoria, Australia, side by side on one shared clock.

- Each crash flashes at the hour it happened and fades over about 3 days
- Fatal crashes are the largest and brightest points
- Live crash and fatality counts for each year, plus a cumulative chart
- Output is a single self-contained HTML file: no server, no map tiles, works on a phone

## Quick start

```bash
pip install -r requirements.txt
# put your crash CSV in data/ (see below), then:
python build.py data/crashes.csv --years 2020 2025 --out docs/index.html
```

Open `docs/index.html` in a browser.

## Data

Crash data comes from the Victorian Government open data portal (search for "Victoria road crash data" at discover.data.vic.gov.au). Check the licence and attribution requirements on the dataset page before publishing.

`build.py` expects one CSV with these columns:

| Column | Example |
|---|---|
| `ACCIDENT_DATE` | `2025-03-14` |
| `ACCIDENT_TIME` | `17:42:00` |
| `SEVERITY` | `Fatal accident`, `Serious injury accident`, `Other injury accident` |
| `LATITUDE` | `-37.81` |
| `LONGITUDE` | `144.96` |

The raw crash file is large, so `data/` is git-ignored. Do not commit it.

## Publish with GitHub Pages

1. Build into `docs/index.html` (the default output).
2. Push to GitHub.
3. Repo **Settings > Pages**, source: **Deploy from a branch**, branch `main`, folder `/docs`.

## How it works

`build.py` filters the CSV to two years, projects latitude/longitude to a flat x/y grid, encodes each crash as `[x, y, hour_of_year, severity]`, and injects the arrays into `templates/compare.html`. The page draws everything on a canvas with additive blending to get the glow.

## Ideas

- Compare any two years with `--years`
- Fatal crashes only (filter in `encode_year`)
- A Melbourne close-up (narrow the bounding box constants)
- A 24-hour view that folds the whole year into one day

## Licence

Code: MIT. Data: see the licence on the source dataset.
