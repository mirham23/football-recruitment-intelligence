"""Model-module tests. Synthetic frames only -- properties, not accuracy.

Run with: pytest tests/ -q
"""

import numpy as np
import pandas as pd

from src.models.data import (
    MIN_MINUTES,
    SHORTLIST,
    position_group,
    prepare_frame,
    season_start_year,
    time_split,
)
from src.models.train import (
    MODEL_SPECS,
    build_model,
    cross_val_oof,
    evaluate,
    load_artifact,
    save_artifact,
    train_all,
)


def make_raw(n=40, seed=7):
    rng = np.random.default_rng(seed)
    positions = ["Center Forward", "Left Center Midfield", "Right Back", "Goalkeeper"]
    return pd.DataFrame({
        "league_season": rng.choice(["La Liga 2015/2016", "La Liga 2019/2020"], n),
        "sb_player": [f"Player {i % 12}" for i in range(n)],
        "sb_team": rng.choice(["Barcelona", "Sevilla FC"], n),
        "position": rng.choice(positions, n),
        "minutes": rng.integers(100, 3000, n).astype(float),
        "matches": rng.integers(1, 38, n),
        "starts": rng.integers(0, 30, n),
        "shots_p90": rng.uniform(0, 5, n).round(3),
        "goals_p90": rng.uniform(0, 1, n).round(3),
        "xg_p90": rng.uniform(0, 1, n).round(3),
        "passes_p90": rng.uniform(20, 90, n).round(3),
        "pass_pct": rng.uniform(60, 95, n).round(1),
        "drib_ok_p90": rng.uniform(0, 3, n).round(3),
        "carries_p90": rng.uniform(0, 100, n).round(3),
        "pressures_p90": rng.uniform(0, 60, n).round(3),
        "duels_w_p90": rng.uniform(0, 10, n).round(3),
        "interceptions_p90": rng.uniform(0, 5, n).round(3),
        "recoveries_p90": rng.uniform(0, 30, n).round(3),
        "market_value_in_eur": rng.integers(500_000, 50_000_000, n).astype(float),
        "value_date": "2016-06-30",
        "date_of_birth": rng.choice(["1990-01-01", "1995-06-15", None], n),
    })


# ---- prep ----

def test_position_group_buckets():
    assert position_group("Left Center Forward") == "Attack"
    assert position_group("Left Wing") == "Attack"
    assert position_group("Left Center Midfield") == "Midfield"
    assert position_group("Right Back") == "Defence"
    assert position_group("Goalkeeper") == "GK"


def test_season_start_year_handles_leagues_and_tournaments():
    assert season_start_year("La Liga 2015/2016") == 2015
    assert season_start_year("Euro 2020") == 2020


def test_prepare_frame_filters_squares_dummies():
    frame = prepare_frame(make_raw())
    assert (frame["minutes"] >= MIN_MINUTES).all()
    assert frame["age2"].equals(frame["age"] ** 2)
    assert frame["age"].notna().all()  # missing DOBs dropped, not imputed
    assert "pos_grp_Attack" in frame.columns or "pos_grp_Midfield" in frame.columns
    assert "ln_v" in frame.columns


def test_shortlist_matches_notebook_08():
    assert "goals_p90" in SHORTLIST and "xg_p90" in SHORTLIST
    assert "carries_p90" in SHORTLIST and "age" in SHORTLIST and "age2" in SHORTLIST


def test_time_split_is_forward_and_deterministic():
    frame = prepare_frame(make_raw())
    Xtr, Xte, ytr, yte, full = time_split(frame)
    assert (full.loc[Xtr.index, "start_yr"] < 2019).all()
    assert (full.loc[Xte.index, "start_yr"] >= 2019).all()
    assert "ln_v" not in Xtr.columns and "sb_player" not in Xtr.columns
    Xtr2, _, _, _, _ = time_split(frame)
    pd.testing.assert_frame_equal(Xtr, Xtr2)


# ---- train/evaluate ----

def _small_split():
    frame = prepare_frame(make_raw(n=60))
    return (frame, *time_split(frame))


def test_train_all_returns_four_fitted():
    frame, Xtr, Xte, ytr, yte, _ = _small_split()
    fitted = train_all(Xtr, ytr)
    assert set(fitted) == set(MODEL_SPECS)
    for model in fitted.values():
        assert hasattr(model, "predict")


def test_evaluate_keys_and_reproducibility():
    frame, Xtr, Xte, ytr, yte, _ = _small_split()
    first = evaluate(train_all(Xtr, ytr), Xte, yte)
    second = evaluate(train_all(Xtr, ytr), Xte, yte)
    assert list(first.columns) == ["MAE_log", "RMSE_log", "R2", "MAE_eur_M"]
    pd.testing.assert_frame_equal(first, second)


def test_unknown_model_rejected():
    try:
        build_model("messi")
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_cross_val_oof_shape_and_groups():
    frame, Xtr, Xte, ytr, yte, full = _small_split()
    X = pd.concat([Xtr, Xte])
    y = pd.concat([ytr, yte])
    groups = full["sb_player"]
    pred = cross_val_oof("xgboost", X, y, groups, n_splits=3)
    assert len(pred) == len(y)
    assert np.isfinite(pred).all()


def test_artifact_roundtrip(tmp_path):
    frame, Xtr, Xte, ytr, yte, _ = _small_split()
    fitted = train_all(Xtr, ytr)
    path = str(tmp_path / "model.joblib")
    save_artifact(fitted["xgboost"], list(Xtr.columns), path)
    model, columns = load_artifact(path)
    assert columns == list(Xtr.columns)
    assert len(model.predict(Xte)) == len(Xte)
