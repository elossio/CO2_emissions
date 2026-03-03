"""
Data visualization and model performance module.
Contains functions for plotting coefficients, residuals, and metric comparisons.
"""

import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.ticker import EngFormatter
from sklearn.metrics import PredictionErrorDisplay

from .models import RANDOM_STATE

sns.set_theme(palette="bright")

# Global plotting configurations
PALETTE = "coolwarm"
SCATTER_ALPHA = 0.2


def plot_coefficients(df_coefs, title="Coefficients"):
    """
    Plots a horizontal bar chart with the model coefficients.

    Args:
        df_coefs (pd.DataFrame): DataFrame containing coefficients (indexed by names).
        title (str, optional): Chart title. Defaults to "Coefficients".
    """
    df_coefs.plot.barh()
    plt.title(title)
    plt.axvline(x=0, color=".5")
    plt.xlabel("Coefficients")
    plt.gca().get_legend().remove()
    plt.show()


def plot_residuals(y_true, y_pred):
    """
    Plots a residual analysis panel (Histogram, Residual vs Predicted, Actual vs Predicted).

    Args:
        y_true (array-like): Actual values.
        y_pred (array-like): Predicted values by the model.
    """
    residuals = y_true - y_pred

    fig, axs = plt.subplots(1, 3, figsize=(12, 6))

    # Residuals distribution
    sns.histplot(residuals, kde=True, ax=axs[0])
    axs[0].set_title("Residuals Distribution")

    # Residual vs Predicted (homoscedasticity evaluation)
    error_display_01 = PredictionErrorDisplay.from_predictions(
        y_true=y_true, y_pred=y_pred, kind="residual_vs_predicted", ax=axs[1]
    )

    # Actual vs Predicted (bias evaluation)
    error_display_02 = PredictionErrorDisplay.from_predictions(
        y_true=y_true, y_pred=y_pred, kind="actual_vs_predicted", ax=axs[2]
    )

    plt.tight_layout()
    plt.show()


def plot_estimator_residuals(estimator, X, y, eng_formatter=False, sample_fraction=0.25):
    """
    Generates residual analysis directly from an estimator and input data.

    Args:
        estimator: Trained scikit-learn estimator.
        X (pd.DataFrame/array): Features.
        y (pd.Series/array): Actual target.
        eng_formatter (bool, optional): If True, uses engineering notation on axes. Defaults to False.
        sample_fraction (float, optional): Data fraction for the scatter plot (subsampling). Defaults to 0.25.
    """
    fig, axs = plt.subplots(1, 3, figsize=(12, 6))

    error_display_01 = PredictionErrorDisplay.from_estimator(
        estimator,
        X,
        y,
        kind="residual_vs_predicted",
        ax=axs[1],
        random_state=RANDOM_STATE,
        scatter_kwargs={"alpha": SCATTER_ALPHA},
        subsample=sample_fraction,
    )

    error_display_02 = PredictionErrorDisplay.from_estimator(
        estimator,
        X,
        y,
        kind="actual_vs_predicted",
        ax=axs[2],
        random_state=RANDOM_STATE,
        scatter_kwargs={"alpha": SCATTER_ALPHA},
        subsample=sample_fraction,
    )

    residuals = error_display_01.y_true - error_display_01.y_pred

    sns.histplot(residuals, kde=True, ax=axs[0])
    axs[0].set_title("Residuals Distribution")

    if eng_formatter:
        for ax in axs:
            ax.yaxis.set_major_formatter(EngFormatter())
            ax.xaxis.set_major_formatter(EngFormatter())

    plt.tight_layout()
    plt.show()


def plot_model_metrics_comparison(df_results):
    """
    Generates comparative boxplots for different performance metrics between models.

    Args:
        df_results (pd.DataFrame): DataFrame with organized results (multiple CV rounds).
    """
    fig, axs = plt.subplots(2, 2, figsize=(8, 8), sharex=True)

    compare_metrics = [
        "time_seconds",
        "test_r2",
        "test_neg_mean_absolute_error",
        "test_neg_root_mean_squared_error",
    ]

    metric_names = [
        "Time (s)",
        "R²",
        "MAE",
        "RMSE",
    ]

    for ax, metric, name in zip(axs.flatten(), compare_metrics, metric_names):
        sns.boxplot(
            x="model",
            y=metric,
            data=df_results,
            ax=ax,
            showmeans=True,
        )
        ax.set_title(name)
        ax.set_ylabel(name)
        ax.tick_params(axis="x", rotation=90)

    plt.tight_layout()
    plt.show()


