import pandas as pd
from logger import get_logger

logger = get_logger("Extract Data . . . ")



import pyodbc
import pandas as pd

from config import SOURCE_CONN_STR
from logger import get_logger

logger = get_logger(__name__)



def extract_data(conn, source_db: str, source_table: str) -> pd.DataFrame:
    """
    Extract data from a source SQL Server table into a DataFrame.
    """

    sql = f"""
    SELECT Top 10 *
    FROM [{source_db}].dbo.[{source_table}]
    """

    try:
        logger.info(
            f"Extracting data from {source_db}.dbo.{source_table}"
        )

        df = pd.read_sql(sql, conn)

        logger.info(
            f"Extracted {len(df):,} rows."
        )

        return df
    
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise