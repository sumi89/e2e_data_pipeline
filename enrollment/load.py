import logging
from logger import get_logger

logger = get_logger("Load Data . . . ")

def load_data(conn, df, target_db: str, target_table: str):
    """
    Load DataFrame into target SQL Server table.
    """

    cursor = conn.cursor()

    try:

        logger.info(
            f"Loading {len(df):,} rows into {target_db}.dbo.{target_table}"
        )

        # Remove existing target data
        cursor.execute(
            f"TRUNCATE TABLE {target_db}.dbo.{target_table}"
        )


        columns = ",".join(
            f"[{col}]" for col in df.columns
        )

        placeholders = ",".join(
            ["?"] * len(df.columns)
        )

        insert_sql = f"""
        INSERT INTO {target_db}.dbo.{target_table}
        ({columns})
        VALUES ({placeholders})
        """


        '''
        insert_sql = f"""
        INSERT INTO {target_table}
        VALUES ({','.join(['?'] * len(df.columns))})
        """
        '''

        cursor.fast_executemany = True


        logger.info(insert_sql)

        logger.info(
            f"DataFrame shape: {df.shape}"
        )

        logger.info(
            f"DataFrame columns: {df.columns.tolist()}"
        )

        cursor.executemany(
            insert_sql,
            df.values.tolist()
        )

        conn.commit()

        logger.info("Load completed successfully.")

    except Exception:

        conn.rollback()

        logger.exception(
            "Load failed. Transaction rolled back."
        )

        raise

    finally:
        cursor.close()