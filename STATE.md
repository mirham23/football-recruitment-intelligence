# Project State — Football Recruitment Intelligence

Last updated: 2026-09-20. Phase 1 (Data Science MVP) modeling complete; Day 5 (README story) done; public push is the remaining step.

## Question answered (handover §33)

**Yes — the datasets join into a player-season table with performance metrics and market value**, for men's senior football: 74–83% automatic match rate at high precision, all failure modes closed. Women's data has no Transfermarkt counterpart (accepted gap).

## Data (local, gitignored, ~16 GB)

- `data/statsbomb/data/` — StatsBomb open data: 4,235 event/lineup matches, 80 league-seasons. No market-value, transfer, or bio columns (proven by key scan). No age/height/foot.
- `data/transfermarkt/` — 12 CSVs: 50,149 players (bio: DOB, height, foot), 656k valuations (2000–2026, the target variable), 175k transfers, 1.9M appearances, 89k games.
- `data/processed/` — built artifacts: `player_season_value.csv` (6,454 rows), `player_season_features.csv` (6,454 rows, 44 cols).

## Database (local Postgres 17, db `fri`)

- `sql/schema.sql` — `players` (3,728 rows: ID, name, DOB, position, foot, height) + `player_season` (6,454 rows: features + value; PK covers team for January movers).
- `scripts/load_data.py` — idempotent loader (password via prompt, never stored).

## Code (`src/`, tested)

- `src/join/` — entity resolution graduated from notebooks: normalization (accents, hyphens, whitespace), 5-entry club map, 18-entry nickname dict, token-subset + club-gate cascade, difflib fuzzy (0.85). Principle: hardcode knowledge, never decisions — the dict proposes, the gate disposes.
- `tests/test_join.py` — 17 tests, all passing (`pytest tests/ -q`). Locks in: Llorente≠Torres, De Paul pick, Casimiro fuzzy hit, Dortmund/Gladbach rejection.

## Notebooks (`notebooks/`, committed with outputs)

| # | File | Result |
|---|---|---|
| 01 | StatsBomb inspection | IDs unique; no value/bio data; 80 league-seasons |
| 02 | Transfermarkt inspection | Target series + bio found; IDs disjoint; 937 name collisions; 12-league overlap |
| 03 | Join prototype (La Liga 15/16) | 57% auto; club gate proven load-bearing; failure modes characterized |
| 04 | Join resolution | 74% (442/601); cascade + nicknames + fuzzy; all classes closed |
| 05 | PL validation | 80% unchanged code; 0 new map entries — method generalizes |
| 06 | Bulk join (28 seasons) | +hyphen fix + Hertha entry; Dortmund/Gladbach rejection locked in |
| 07 | Per-90 features | Minutes engine, event counters, 0.00% unattributed; one merge-grain bug found and fixed (team key + tripwire) |
| 08 | Value analysis | Log target, age curve (age+age²), 500-min cutoff, feature shortlist |
| 09 | Price model | XGB CV R² 0.645 (player-grouped); forward time-split honestly negative (regime shift, n=66) |

## Key modeling facts

- Target: `ln(market_value_in_eur)`. Top single-feature correlations ~0.37–0.39 (carries, dribbles, goals, pass%, xG, shots).
- Time-split test R² negative for all models — reported as stress-test failure, not hidden. SHAP leader `pass_pct` flagged as Barcelona-confounding suspect.
- Hunt table uses out-of-fold predictions; "potentially undervalued *according to the model*" wording per handover rule.

## Repo hygiene (decided, do not regress)

- Raw data never commits (16 GB + redistribution licensing): `data/statsbomb/data/`, `data/transfermarkt/`, `data/**/*.csv|parquet` ignored.
- Notebooks committed with fresh outputs only (Restart & Run All before add).
- Short-lived branches, `--no-ff` merges, delete after. No push of `main` until Day-5 publication (repo is public).
- Identity: repo-local `mirham23 <belajarestudiar@gmail.com>`; `.mailmap` covers the initial commit.
- Rule: re-run notebooks downstream of any `src/` change before committing.

## Next (Day 5, then Phase 2)

1. README story (problem, data, method, results, limits, next) + public push.
2. Player similarity system (handover §8).
3. FastAPI → React → Docker → CI/CD per handover architecture (deferred, not started).

## Environment

Windows + Python 3.12 (pandas 3.0.5, sklearn 1.9, xgboost 3.4, shap 0.52, matplotlib 3.11, psycopg2-binary) + Postgres 17 on :5432. Planned: Fedora dual-boot as hobby project (after Day 5); code moves via git, data via NTFS copy or re-download.
