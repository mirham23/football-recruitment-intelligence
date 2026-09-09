# AGENTS.md

## Project state

Early Phase 1 (Data Science MVP). Empty `src/` and `tests/` packages — no production code yet. Active work is in Jupyter notebooks (gitignored).

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
- Notebooks for exploration (`.ipynb` — gitignored). `src/` for reusable modules.
- No build system, no CI, no pre-commit hooks.
