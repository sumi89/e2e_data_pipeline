import pandas as pd

from logger import get_logger

logger = get_logger(__name__)


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and transform data before loading.
    """

    logger.info(f"Initial rows: {len(df):,}")
    logger.info(f"Initial columns: {len(df.columns):,}")

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove completely empty columns
    #df = df.dropna(axis=1, how="all")

    # Remove duplicate rows
    df = df.drop_duplicates()

    logger.info(f"Rows after cleaning: {len(df):,}")
    logger.info(f"Columns after cleaning: {len(df.columns):,}")

    return df