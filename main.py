import sys
from db_connection import get_db_connection, run_diagnostics
from logger import get_logger

from enrollment.extract import extract_data
from enrollment.transform import transform_data
from enrollment.load import load_data

logger = get_logger("MainPipeline")

def main():

    # 1. Establish Database Connection & Run Diagnostics
    logger.info("Starting Data Pipeline Execution...")

    try:
        # with get_db_connection() as conn:
        #     run_diagnostics(conn)
        conn = get_db_connection()
        run_diagnostics(conn)
        logger.info("Database connection and diagno completed successfully.")

        # 2. Extract Data from Source Table
        df = extract_data(conn, "Goldmine Extracts", "PartTerms")
        logger.info(f"Extracted DataFrame shape: {df.shape}")

        # 3. Transform Data
        df = transform_data(df)

        # 4. Load Data into Target Table
        load_data(conn, df, "TestDatabase_Sumi", "tst_load")

    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed.")

    '''
    except Exception as e:
        logger.critical(f"Pipeline failure: {e}", exc_info=True)
        sys.exit(1)
    '''

    '''
    # 2. Extract Data from Source Table
    df = extract_data(conn, "Goldmine Extracts", "PartTerms")
    print(df.head())  # Display the first few rows of the extracted DataFrame

    # 3. Load Data into Target Table

    load_data(conn, df, "tst_load")
    '''

if __name__ == "__main__":
    main()






'''
import pyodbc
import logging
from sqlalchemy import text


logger = logging.getLogger("MSSQL_WinAuth_Test")
logging.basicConfig(level=logging.INFO)

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"+
    "SERVER=CIERPSRVSQL01;"+
    "DATABASE=TestDatabase_Sumi;"+
    "Trusted_Connection=yes;"
)

logger.info("Connection established to MS SQL Server using Windows Authentication.")

# Execute a basic diagnostic query
query = """
        SELECT
            @@SERVERNAME AS server_name,
            DB_NAME() AS current_database,
            SYSTEM_USER AS connected_user,
            @@VERSION AS sql_version;
    """
print(type(query))

logger.info("Executing diagnostic query to retrieve server information...")

result = conn.execute(query).fetchone()



logger.info("Successfully connected to MS SQL Server!")
logger.info(f"Host Server Name : {result.server_name}")
logger.info(f"Active Database  : {result.current_database}")
logger.info(f"Authenticated As : {result.connected_user}")
'''