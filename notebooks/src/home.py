"""
Streamlit application for CO2 emission data exploration and prediction via regression model.
Provides an interactive interface with filters, charts, and an emissions calculator.
"""

import pandas as pd

import plotly.express as px
import streamlit as st

from joblib import load

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

from notebooks.src.config import CONSOLIDATED_DATA, PROCESSED_DATA, FINAL_MODEL


@st.cache_data
def load_data(file):
    """
    Loads data from a Parquet file with Streamlit caching.

    Args:
        file (str/Path): Path to the Parquet file.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    return pd.read_parquet(file)


@st.cache_resource
def load_trained_model(file):
    """
    Loads the trained model from a .joblib file with resource caching.

    Args:
        file (str/Path): Path to the model file.

    Returns:
        object: Loaded scikit-learn model.
    """
    return load(file)


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns.

    Link blog: https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


df_consolidated = load_data(CONSOLIDATED_DATA)
df_processed = load_data(PROCESSED_DATA)
model = load_trained_model(FINAL_MODEL)

columns_to_remove = [
    "co2_rating",
    "smog_rating",
    "combined_mpg",
    "engine_size_l",
    "cylinders",
    "city_l_100_km",
    "highway_l_100_km",
]

df_consolidated = df_consolidated.drop(columns=columns_to_remove)

df_consolidated = df_consolidated[
    [
        "model_year",
        "make",
        "model",
        "co2_emissions_g_km",
        "fuel_type",
        "vehicle_class",
        "combined_l_100_km",
    ]
]

fuel_map = {
    "X": "reg_gasoline",
    "Z": "premium_gasoline",
    "D": "diesel",
    "E": "ethanol",
    "N": "natural_gas",
}

df_consolidated["fuel_type"] = df_consolidated["fuel_type"].map(fuel_map)

tab1, tab2 = st.tabs(["Data", "Regression"])

with tab1:

    df_filtered = filter_dataframe(df_consolidated)
    
    st.dataframe(
        df_filtered.style.background_gradient(
            subset=["co2_emissions_g_km", "combined_l_100_km"],
            cmap="RdYlGn_r",
        )
    )

    cmin, cmax = (
        df_consolidated["co2_emissions_g_km"].min(),
        df_consolidated["co2_emissions_g_km"].max(),
    )

    fig1 = px.bar(
        df_consolidated[["make", "co2_emissions_g_km"]].groupby("make").mean().reset_index(),
        x="make",
        y="co2_emissions_g_km",
        title="Average CO<sub>2</sub> emission by manufacturer (g/km)",
        color="co2_emissions_g_km",
        color_continuous_scale="RdYlGn_r",
        hover_data={"co2_emissions_g_km": ":.2f"},
    )

    fig1.update_xaxes(categoryorder="total descending")

    fig1.data[0].update(marker_cmin=cmin, marker_cmax=cmax)

    fig1.add_hline(
        y=df_consolidated["co2_emissions_g_km"].mean(),
        line_dash="dot",
        line_color="purple",
    )

    fig1.add_annotation(
        xref="paper",
        x=0.95,
        y=df_consolidated["co2_emissions_g_km"].mean(),
        text=f"Average: {df_consolidated['co2_emissions_g_km'].mean():.2f} g/km",
        showarrow=False,
        yshift=10,
    )

    st.plotly_chart(fig1) 


    fig2 = px.bar(
        df_consolidated[["vehicle_class", "co2_emissions_g_km"]]
        .groupby("vehicle_class").mean().reset_index(),
        x="vehicle_class",
        y="co2_emissions_g_km",
        title="Average CO<sub>2</sub> emission by vehicle class (g/km)",
        color="co2_emissions_g_km",
        color_continuous_scale="RdYlGn_r",
        hover_data={"co2_emissions_g_km": ":.2f"},
        range_color=[cmin, cmax],
    )

    fig2.update_xaxes(categoryorder="total descending")

    fig2.data[0].update(marker_cmin=cmin, marker_cmax=cmax)

    fig2.add_hline(
        y=df_consolidated["co2_emissions_g_km"].mean(),
        line_dash="dot",
        line_color="purple",
    )

    fig2.add_annotation(
        xref="paper",
        x=0.95,
        y=df_consolidated["co2_emissions_g_km"].mean(),
        text=f"Average: {df_consolidated['co2_emissions_g_km'].mean():.2f} g/km",
        showarrow=False,
        yshift=10,
    )

    st.plotly_chart(fig2) 

    fig3 = px.bar(
        df_consolidated[["model_year", "co2_emissions_g_km"]]
        .groupby("model_year").mean().reset_index(),
        x="model_year",
        y="co2_emissions_g_km",
        title="Average CO<sub>2</sub> emission by year (g/km)",
        color="co2_emissions_g_km",
        color_continuous_scale="RdYlGn_r",
        hover_data={"co2_emissions_g_km": ":.2f"},
        range_color=[cmin, cmax],
    )

    fig3.data[0].update(marker_cmin=cmin, marker_cmax=cmax)

    fig3.add_hline(
        y=df_consolidated["co2_emissions_g_km"].mean(),
        line_dash="dot",
        line_color="purple",
    )

    fig3.add_annotation(
        xref="paper",
        x=0.95,
        y=df_consolidated["co2_emissions_g_km"].mean(),
        text=f"Average: {df_consolidated['co2_emissions_g_km'].mean():.2f} g/km",
        showarrow=False,
        yshift=10,
    )

    st.plotly_chart(fig3) 

    fig4 = px.scatter(
        df_consolidated,
        x="combined_l_100_km",
        y="co2_emissions_g_km",
        color="fuel_type",
        color_discrete_sequence=px.colors.qualitative.Set3,
        opacity=0.5,
        title="CO<sub>2</sub> Emission x Combined Consumption - Fuel Type",
        labels={
            "combined_l_100_km": "Combined Consumption (l/100 km)",
            "co2_emissions_g_km": "CO<sub>2</sub> Emission (g/km)"
        }
    )

    fig4.update_layout(
        legend=dict(
            title="Fuel Type",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        )
    )

    st.plotly_chart(fig4)
    
    fig5 = px.scatter(
        df_consolidated,
        x="combined_l_100_km",
        y="co2_emissions_g_km",
        color="vehicle_class",
        color_discrete_sequence=px.colors.qualitative.Light24,
        opacity=0.5,
        title="CO<sub>2</sub> Emission x Combined Consumption - Vehicle Class",
        labels={
            "combined_l_100_km": "Combined Consumption (l/100 km)",
            "co2_emissions_g_km": "CO<sub>2</sub> Emission (g/km)"
        }
    )
    
    st.plotly_chart(fig5)

    fig6 = px.treemap(
        df_consolidated,
        path=[
            px.Constant("co2_emissions_g_km"),
            "make",
            "vehicle_class",
            "fuel_type",
            "model_year",
            "model",
        ],
        color="co2_emissions_g_km",
        color_continuous_scale="RdYlGn_r",
        range_color=[cmin, cmax],
        title="CO<sub>2</sub> Emission Treemap",
        labels={
            "co2_emissions_g_km": "CO<sub>2</sub> Emission (g/km)"
        },
        hover_data={"co2_emissions_g_km": ":.2f"},
    )

    st.plotly_chart(fig6)

with tab2:
    years = sorted(df_processed["model_year"].unique())
    transmission = sorted(df_processed["transmission"].unique())
    fuel = sorted(df_processed["fuel_type"].unique())
    vehicle = sorted(df_processed["vehicle_class_grouped"].unique())
    engine_size = sorted(df_processed["engine_size_l_class"].unique())
    cylinders = sorted(df_processed["cylinders_class"].unique())

    slider_columns = (
        "city_l_100_km",
        "highway_l_100_km",
        "combined_l_100_km",
    )

    slider_columns_min_max = {
        column: {
            "min_value": df_processed[column].min(),
            "max_value": df_processed[column].max(),
        }
        for column in slider_columns
    }

    with st.form(key="model_form"):

        left_column, right_column = st.columns(2)

        with left_column:
            widget_year = st.selectbox("Year", years)
            widget_transmission = st.selectbox("Transmission", transmission)
            widget_fuel = st.selectbox("Fuel", fuel)

        with right_column:
            widget_vehicle = st.selectbox("Vehicle Type", vehicle)
            widget_engine_size = st.selectbox("Engine Size", engine_size)
            widget_cylinders = st.selectbox("Cylinders", cylinders)
    
        widget_city = st.slider(
            "Urban consumption (l/100 km)",
            **slider_columns_min_max["city_l_100_km"]
        )
    
        widget_highway = st.slider(
            "Highway consumption (l/100 km)",
            **slider_columns_min_max["highway_l_100_km"]
        )
    
        widget_combined = st.slider(
            "Combined consumption (l/100 km)",
            **slider_columns_min_max["combined_l_100_km"]
        )

        predict_button = st.form_submit_button("Predict emission")

    model_input = {
        "model_year": widget_year,
        "transmission": widget_transmission,
        "fuel_type": widget_fuel,
        "vehicle_class_grouped": widget_vehicle,
        "engine_size_l_class": widget_engine_size,
        "cylinders_class": widget_cylinders,
        "city_l_100_km": widget_city,
        "highway_l_100_km": widget_highway,
        "combined_l_100_km": widget_combined,
    }

    df_model_input = pd.DataFrame([model_input])

    if predict_button:
        emission = model.predict(df_model_input)
        st.metric(label="Predicted emission (g/km)", value=f"{emission[0]:.2f}")

