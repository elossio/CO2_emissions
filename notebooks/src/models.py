"""
Module for building, training, and validating regression models.
Uses scikit-learn pipelines to integrate preprocessing and estimators.
"""

import pandas as pd


from sklearn.compose import TransformedTargetRegressor
from sklearn.model_selection import KFold, cross_validate, GridSearchCV
from sklearn.pipeline import Pipeline

RANDOM_STATE = 42


def build_regression_model_pipeline(
    regressor, preprocessor=None, target_transformer=None
):
    """
    Builds a scikit-learn pipeline or a TransformedTargetRegressor.

    Args:
        regressor (estimator): Base estimator (e.g., Ridge, Lasso, XGBoost).
        preprocessor (transformer, optional): ColumnTransformer for preprocessing.
        target_transformer (transformer, optional): Transformer for the target variable (e.g., Quantile).

    Returns:
        object: Configured Pipeline or TransformedTargetRegressor.
    """
    if preprocessor is not None:
        pipeline = Pipeline([("preprocessor", preprocessor), ("reg", regressor)])
    else:
        pipeline = Pipeline([("reg", regressor)])

    if target_transformer is not None:
        model = TransformedTargetRegressor(
            regressor=pipeline, transformer=target_transformer
        )
    else:
        model = pipeline
    return model


def train_and_validate_regression_model(
    X,
    y,
    regressor,
    preprocessor=None,
    target_transformer=None,
    n_splits=5,
    random_state=RANDOM_STATE,
):
    """
    Executes cross-validation for a configured model.

    Args:
        X (pd.DataFrame): Explanatory variables.
        y (pd.Series/array): Target.
        regressor (estimator): Base estimator.
        preprocessor (transformer, optional): Preprocessor.
        target_transformer (transformer, optional): Target transformer.
        n_splits (int, optional): Number of folds in KFold. Defaults to 5.
        random_state (int, optional): Random seed. Defaults to RANDOM_STATE.

    Returns:
        dict: Dictionary with R2, MAE, and RMSE scores from cross-validation.
    """

    model = build_regression_model_pipeline(
        regressor, preprocessor, target_transformer
    )

    kf = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    scores = cross_validate(
        model,
        X,
        y,
        cv=kf,
        scoring=[
            "r2",
            "neg_mean_absolute_error",
            "neg_root_mean_squared_error",
        ],
    )

    return scores


def run_grid_search_cv(
    regressor,
    param_grid,
    preprocessor=None,
    target_transformer=None,
    n_splits=5,
    random_state=RANDOM_STATE,
    return_train_score=False,
):
    """
    Configures and returns a GridSearchCV object for hyperparameter optimization.

    Args:
        regressor (estimator): Base estimator.
        param_grid (dict): Parameter grid for search.
        preprocessor (transformer, optional): Preprocessor.
        target_transformer (transformer, optional): Target transformer.
        n_splits (int, optional): Number of folds. Defaults to 5.
        random_state (int, optional): Random seed. Defaults to RANDOM_STATE.
        return_train_score (bool, optional): If True, includes training scores. Defaults to False.

    Returns:
        GridSearchCV: Configured object for parameter space search.
    """

    model = build_regression_model_pipeline(
        regressor, preprocessor, target_transformer
    )

    kf = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    grid_search = GridSearchCV(
        model,
        cv=kf,
        param_grid=param_grid,
        scoring=["r2", "neg_mean_absolute_error", "neg_root_mean_squared_error"],
        refit="neg_root_mean_squared_error",
        n_jobs=-1,
        return_train_score=return_train_score,
        verbose=1,
    )

    return grid_search


def organize_results(results):
    """
    Transforms the cross-validation results dictionary into a formatted DataFrame.

    Args:
        results (dict): Dictionary containing metrics from multiple models.

    Returns:
        pd.DataFrame: "Exploded" DataFrame (one row per fold/model) with numeric columns.
    """

    for key, value in results.items():
        results[key]["time_seconds"] = (
            results[key]["fit_time"] + results[key]["score_time"]
        )

    df_results = (
        pd.DataFrame(results).T.reset_index().rename(columns={"index": "model"})
    )

    df_results_exploded = df_results.explode(
        df_results.columns[1:].to_list()
    ).reset_index(drop=True)

    try:
        df_results_exploded = df_results_exploded.apply(pd.to_numeric)
    except ValueError:
        pass

    return df_results_exploded

