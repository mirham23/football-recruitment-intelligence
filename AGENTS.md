# AGENTS.md

## Project state

Late Phase 1 (Data Science MVP): modeling done, Day-5 README + push pending.

- `src/join/` — StatsBomb↔Transfermarkt entity resolution (normalize, club map, nicknames, cascade, fuzzy). Tested.
- `src/models/` — value-model prep/train/evaluate/artifact IO (pure functions; DB reads stay notebook-side). Tested.
- `sql/schema.sql` + `scripts/load_data.py` — Postgres `players` + `player_season` tables, idempotent loader.
- `notebooks/01–09` — committed with outputs; re-run downstream notebooks after any `src/` change before committing.

## Data

- `data/statsbomb/data/` — StatsBomb open data (JSON). Matches in `matches/<comp_id>/<season_id>.json`, events/lineups per match in `events/`/`lineups/`, 360-frame data in `three-sixty/`.
- StatsBomb license requires attribution and logo use if publishing insights. See `data/statsbomb/README.md`.
- CSV/parquet/xlsx under `data/` are gitignored.

## Commands

```bash
pip install -r requirements.txt
```

Tests: `pytest tests/ -q` (requires `pip install -r requirements.txt` for pytest + pandas).

No linter, formatter, or typecheck is configured yet.

## Conventions

- Python, pandas, scikit-learn, xgboost, shap stack.
- Notebooks for exploration (committed with outputs at milestones). `src/` for reusable modules.
- No build system, no CI, no pre-commit hooks.
