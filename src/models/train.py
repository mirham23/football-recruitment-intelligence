"""Train/evaluate/compare. Fixed seeds and settings from notebook 09.

Winner selection lives notebook-side (comparison needs human judgment about
regime shift); this module only produces the scored table.
"""

import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold, cross_val_predict
from xgboost import XGBRegressor

MODEL_SPECS = ("baseline_median", "linear", "random_forest", "xgboost")


def build_model(name: str):
    """Fixed-setting constructors, identical to notebook 09 Cells 2-3."""
    if name == "baseline_median":
        return DummyRegressor(strategy="median")
    if name == "linear":
        return LinearRegression()
    if name == "random_forest":
        return RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
    if name == "xgboost":
        return XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=4,
                            subsample=0.8, random_state=42, n_jobs=-1)
    raise ValueError(f"unknown model: {name}")


def train_all(Xtr: pd.DataFrame, ytr: pd.Series) -> dict:
    """Fit every spec. Returns {name: fitted model}."""
    fitted = {}
    for name in MODEL_SPECS:
        fitted[name] = build_model(name).fit(Xtr, ytr)
    return fitted


def evaluate(fitted: dict, Xte: pd.DataFrame, yte: pd.Series) -> pd.DataFrame:
    """Test-set MAE/RMSE/R² in log units plus MAE back in euros. Higher R² wins."""
    rows = {}
    for name, model in fitted.items():
        pred = model.predict(Xte)
        rows[name] = {
            "MAE_log": round(mean_absolute_error(yte, pred), 3),
            "RMSE_log": round(float(np.sqrt(mean_squared_error(yte, pred))), 3),
            "R2": round(r2_score(yte, pred), 3),
            "MAE_eur_M": round(mean_absolute_error(np.expm1(yte), np.expm1(pred)) / 1e6, 2),
        }
    return pd.DataFrame(rows).T.sort_values("R2", ascending=False)


def cross_val_oof(name: str, X: pd.DataFrame, y: pd.Series,
                  groups: pd.Series, n_splits: int = 5) -> np.ndarray:
    """Out-of-fold predictions with player-grouped folds (no identity leakage)."""
    model = build_model(name)
    gkf = GroupKFold(n_splits=n_splits)
    return cross_val_predict(model, X, y, cv=gkf.split(X, y, groups=groups))


def save_artifact(model, feature_columns: list, path: str) -> None:
    """Persist winner + its expected columns (joblib ships with scikit-learn)."""
    joblib.dump({"model": model, "columns": list(feature_columns)}, path)


def load_artifact(path: str):
    """Returns (model, feature_columns)."""
    blob = joblib.load(path)
    return blob["model"], blob["columns"]
