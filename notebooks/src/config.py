"""
Global project path and file configuration.
Uses pathlib to ensure compatibility across different operating systems.
"""

from pathlib import Path

# Project root path (two levels above this file)
PROJECT_PATH = Path(__file__).resolve().parents[2]

# Base directory for all data
DATA_PATH = PROJECT_PATH / "data"

# Specific paths for different year datasets (CSV)
DATA_2005_2014 = DATA_PATH / "canada_2005_2014.csv"
DATA_2015_2019 = DATA_PATH / "canada_2015_2019.csv"
DATA_2020 = DATA_PATH / "canada_2020.csv"
DATA_2021 = DATA_PATH / "canada_2021.csv"
DATA_2022 = DATA_PATH / "canada_2022.csv"
DATA_2023 = DATA_PATH / "canada_2023.csv"
DATA_2024 = DATA_PATH / "canada_2024.csv"

# Processed data files (Parquet for higher efficiency)
CONSOLIDATED_DATA = DATA_PATH / "canada_consolidated.parquet"
PROCESSED_DATA = DATA_PATH / "canada_processed.parquet"

# Model configurations
MODELS_PATH = PROJECT_PATH / "models"
FINAL_MODEL = MODELS_PATH / "ridge.joblib"

# Paths for generated reports and exported images
REPORTS_PATH = PROJECT_PATH / "reports"
IMAGES_PATH = REPORTS_PATH / "images"


