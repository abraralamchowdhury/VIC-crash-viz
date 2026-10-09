# Victoria Road Crashes: Year vs Year

An animated map that replays two years of police-reported road crashes in Victoria, Australia, side by side on a shared clock.

**[Live demo](https://vic-crash-viz.netlify.app/)**

## Features

- Two years play simultaneously, so seasonal patterns and year-on-year changes are easy to compare
- Each crash appears at the hour it occurred and fades over about three days
- Fatal crashes are drawn largest and brightest, followed by serious injury and other injury crashes
- Live crash and fatality counts for each year, with the running difference between them
- Cumulative line chart, play/pause control and a scrubbable timeline
- Output is a single self-contained HTML file: no server, no map tiles, no external dependencies
- Responsive layout: maps stack on portrait screens and sit side by side in landscape

## Requirements

- Python 3.8 or later
- `pandas` and `numpy`

```bash
pip install -r requirements.txt
```

## Usage

1. Download the Victoria road crash data (see [Data](#data)) and place the CSV in the `data/` folder.
2. Build the visualisation:

```bash
python build.py data/crashes.csv --years 2020 2025 --out docs/index.html
```

3. Open `docs/index.html` in any browser.

### Options

| Argument | Description | Default |
|---|---|---|
| `csv` | Path to the crash CSV (required) | n/a |
| `--years A B` | The two years to compare | `2020 2025` |
| `--out` | Output HTML file | `docs/index.html` |
| `--template` | HTML template to use | `templates/compare.html` |

## Data

Crash records come from the Victorian Government open data portal. Search for "Victoria road crash data" at [discover.data.vic.gov.au](https://discover.data.vic.gov.au). Review the licence and attribution requirements on the dataset page before publishing or redistributing any output.

`build.py` expects a single CSV containing these columns:

| Column | Example |
|---|---|
| `ACCIDENT_DATE` | `2025-03-14` |
| `ACCIDENT_TIME` | `17:42:00` |
| `SEVERITY` | `Fatal accident`, `Serious injury accident`, `Other injury accident` |
| `LATITUDE` | `-37.81` |
| `LONGITUDE` | `144.96` |

Rows without coordinates, or with coordinates outside Victoria, are dropped. The raw crash file is large, so `data/` is excluded from version control. Do not commit it.

## Project structure

```
vic-crash-viz/
├── build.py              Data processing and HTML generation
├── templates/
│   └── compare.html      Visualisation page (placeholders filled in by build.py)
├── docs/
│   └── index.html        Pre-built output (2020 vs 2025)
├── data/                 Place the crash CSV here (git-ignored)
├── requirements.txt
└── LICENSE
```

## How it works

`build.py` filters the CSV to the two selected years and projects latitude and longitude onto a flat grid. Each crash is encoded as `[x, y, hour_of_year, severity]`, and the arrays are injected into `templates/compare.html`. The page renders on an HTML canvas using additive blending to produce the glow effect. Because the output is one static file, it can be hosted anywhere.

## Deployment

The `docs/` folder contains everything needed to host the visualisation.

**Netlify:** go to [app.netlify.com/drop](https://app.netlify.com/drop) and drag the `docs` folder onto the page.

**GitHub Pages:** in the repository, open **Settings > Pages**, set the source to **Deploy from a branch**, then select branch `main` and folder `/docs`.

## Limitations

- The page shows crash locations only. There is no street basemap or place labels, although the road network becomes visible when many crashes are plotted.
- Only police-reported crashes that appear in the source dataset are included.
- A crash that occurs in the final hours of a leap year is shown at the end of the timeline.

## Ideas for extension

- Compare any two years with `--years`
- Show fatal crashes only (filter inside `encode_year`)
- Zoom to Melbourne by narrowing the bounding box constants in `build.py`
- Add a 24-hour view that folds a full year into a single day

## Licence

Code is released under the [MIT Licence](LICENSE). Data is subject to the licence of the source dataset.
