# Football Recruitment Intelligence

> An analytics-driven football recruitment platform that identifies statistically similar, tactically suitable and potentially undervalued players.

**Status: Phase 1 (Data Science MVP) complete.** This repository contains the full modeling pipeline: inspection → entity resolution → Postgres → features → value model. API, frontend, and deployment are planned later phases, not started.

## The question

> **Can historical performance statistics predict a player's transfer-market value — and who looks potentially undervalued?**

Answer: yes, within market regimes (cross-validated R² 0.65), with a documented failure mode across regimes (see Limits). The join path is proven at 74–83% automatic match rate with every failure class closed and tested.

## Pipeline

```text
StatsBomb events + Transfermarkt values
    ↓  notebooks 01–02 (inspection)
entity resolution (src/join, notebooks 03–06)
    ↓  74–83% automatic, tested
Postgres (sql/schema.sql, scripts/load_data.py)
    ↓  players + player_season tables
per-90 features (notebook 07)
    ↓  44 columns, 6,454 rows
analysis (notebook 08) → feature shortlist
    ↓
price model (src/models, notebook 09)
    ↓  XGB, CV R² 0.645
undervalued-player hunt (out-of-fold gaps)
```

## Data (not included — see each notebook for layout)

- **StatsBomb Open Data** (15 GB locally, gitignored): 4,235 matches, 80 league-seasons. Event-level performance. No market-value or bio columns. Used under StatsBomb's terms: data source credited, logo in `data/statsbomb/img/`. Full terms in `data/statsbomb/README.md`.
- **Transfermarkt export** (CSVs, gitignored): 50k players (bio: birth date, height, foot), 656k dated valuations 2000–2026 (the target variable), 175k transfers, 1.9M appearances.
- Overlap used for modeling: 23 league-seasons (La Liga ×9, UCL ×7, Ligue 1 ×3, PL/BL/SA + tournaments thin). Women's football has no Transfermarkt counterpart — accepted, documented gap.

## Method (each step evidenced in-notebook, decided logic in `src/`)

1. **Join** — normalized names, 5-entry club map, 18-entry nickname dict, token-subset + club-gate cascade, difflib fuzzy (0.85). The gate is load-bearing: it rejects real traps (Llorente/Torres, two Sergio Álvarezes, Dortmund/Gladbach).
2. **Features** — minutes from lineup stints; per-90 rates for shots/goals/xG, passing, dribbles, carries, pressures, duels, defensive actions. Assists out of scope (no direct field).
3. **Model** — target `ln(value)`; shortlist + age² + position/league dummies; baseline → Linear → Random Forest → XGBoost. Time-split test *and* player-grouped 5-fold CV (no identity leakage).

## Results

Cross-validated (grouped by player, out-of-fold):

| Model | CV R² | CV MAE (log) |
|---|---|---|
| XGBoost | **0.645** | 0.641 |
| Random Forest | 0.636 | 0.658 |

Forward time-split test (train ≤2018/19, test 66 rows after): all R² negative (XGB −0.74 best). Reported, not hidden — see Limits.

- SHAP leader `pass_pct` investigated per-league: #1 only in La Liga/Barcelona (#3–4 elsewhere) — documented confounding, not celebrated. Universal signals: carries, age.
- Hunt table uses out-of-fold gaps with "potentially undervalued *according to the model*" wording throughout.

## Notebooks (each: what it does → what came out)

- **01 — StatsBomb checkup.** Looked inside the match data: player/match/team ID numbers exist and are unique across 80 league-seasons, but there are no prices and no player bio data anywhere.
- **02 — Transfermarkt checkup.** Found the missing pieces: 656k dated price records (2000–2026) plus birth dates and heights. But the two datasets share no ID numbers, and 937 names belong to multiple players — so linking needs care.
- **03 — First join test (Spain 2015/16).** Tried matching players by name on one season. Exact matching only got 14% (full legal names vs short common names); word-matching plus a club-agreement check reached 57% with prices — and the club check caught real mix-ups between different players.
- **04 — Fixing every failure type.** Club-name map, tie-breaking rules, nickname list, spelling tolerance → 74% matched with prices. Every leftover case reviewed, nothing decided silently.
- **05 — Same method, England.** Ran the unchanged code on the Premier League: 80% matched, zero confusion cases, zero new fixes needed. The method works generally, not just in Spain.
- **06 — All 28 shared seasons.** Produced the master table (6,454 player-season rows with prices). The audit added two small fixes and locked in a Dortmund/Gladbach non-match as a regression test.
- **07 — Performance stats.** Turned raw match events into per-90 numbers (goals, xG, passes, duels…) plus minutes: 44 columns, every event traced to a player, one data-merging bug found and fixed along the way.
- **08 — What moves prices?** Prices skew wildly (log scale chosen); value peaks mid-to-late 20s (age + age²); only 500+ minute players trusted for rates (977 rows); no single stat explains more than ~40% alone.
- **09 — The price model.** Four models compared two honest ways: 0.65 skill within market eras, failure across eras (reported, not hidden). Top price driver (pass completion) proven Barcelona-skewed by a per-league check. Hunt table flags *potentially* undervalued players only.

## Limits (read before reusing anything)

- Forward generalization fails across market regimes (COVID, PL money boom); model is within-regime.
- Thin samples: UCL seasons are ~1 match each; tournaments yielded no joined rows; test set is 66 rows.
- Training on minutes ≥ 500 only (~977 rows); women's game uncovered; no assists, no injuries/contracts/wages anywhere in the data.

## Reproduce

```bash
pip install -r requirements.txt        # python deps incl. pytest
# place data: data/statsbomb/data/ + data/transfermarkt/*.csv (see notebooks 01-02)
psql -U postgres -c "CREATE DATABASE fri;"
psql -U postgres -d fri -f sql/schema.sql
python scripts/load_data.py           # password prompt; idempotent
pytest tests/ -q                      # 27 passed
```

Notebooks run 01→09 in order (Restart & Run All each). Key outputs: `data/processed/player_season_value.csv`, `player_season_features.csv` (both gitignored build artifacts).

## Next (not started)

Player similarity system → FastAPI → React → Docker → CI/CD → deployment, per `HANDOVER.md`.

## License

MIT. Data retains its original licenses and is not redistributed here.
