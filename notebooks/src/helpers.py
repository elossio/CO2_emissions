"""
Helper functions for data manipulation and result preparation.
"""

import pandas as pd


def get_coefficients_dataframe(coefs, columns):
    """
    Creates an organized DataFrame with model coefficients and their column names.

    Args:
        coefs (list/array): Coefficients extracted from the trained model.
        columns (list/array): Column names corresponding to the coefficients.

    Returns:
        pd.DataFrame: DataFrame sorted by coefficients in ascending order.
    """
    return pd.DataFrame(data=coefs, index=columns, columns=["coefficient"]).sort_values(
        by="coefficient"
    )


