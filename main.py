import sys
from db_connection import get_db_connection, run_diagnostics, test_table_read
from logger import get_logger
'''
from enrollment.extract import extract_data
from enrollment.transform import transform_data
from enrollment.load import load_data
'''

logger = get_logger("MainPipeline")

def main():
    logger.info("Starting Data Pipeline Execution...")
    source_conn = None
    target_conn = None

    try:
        # CONNECT TO SOURCE
        source_conn = get_db_connection("PeopleSoftCBM008Creation")
        run_diagnostics(source_conn)

        # READ FROM SOURCE
        source_cursor = source_conn.cursor()
        source_query = """
            SELECT *
            FROM dbo.CBM008_Sal_Manual
        """
        source_cursor.execute(source_query)

        rows = source_cursor.fetchall()

        logger.info(f"Retrieved {len(rows)} rows from source.")

        source_cursor.close()

        # CONNECT TO TARGET
        target_conn = get_db_connection("TestDatabase_Sumi")
        run_diagnostics(target_conn)

        # WRITE TO TARGET
        target_cursor = target_conn.cursor()

        target_query = """

        """
        target_cursor.execute(target_query)


        # COMMIT
        target_conn.commit()

        logger.info(f"Successfully inserted {len(rows)} rows.")

        target_cursor.close()

    except Exception as e:
        logger.critical(f"Pipeline failure: {e}", exc_info=True)
        sys.exit(1)

'''
def main():

    # 1. Establish Database Connection & Run Diagnostics
    logger.info("Starting Data Pipeline Execution...")

    try:
        conn = get_db_connection("TestDatabase_Sumi")
        run_diagnostics(conn)

        
        # Test table read
        #test_table_read(
        #    conn,
        #    schema="dbo",
        #    table="tst_load"
        #)
        

        logger.info("Database connection and diagno completed successfully.")


    #finally:
        if conn:
            conn.close()
            logger.info("Database connection closed.")

    
    except Exception as e:
        logger.critical(f"Pipeline failure: {e}", exc_info=True)
        sys.exit(1)
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