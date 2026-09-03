import sys
from db_connection import get_db_connection, run_diagnostics
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

logger = logging.getLogger("MainPipeline")


def main():
    logger.info("Starting Data Pipeline Execution...")
    
    try:
        # 1. Establish Database Connection & Run Diagnostics
        # with get_db_connection() as conn:
        #     run_diagnostics(conn)
        conn = get_db_connection()
        run_diagnostics(conn)
            
        logger.info("Pipeline completed successfully.")
        
    except Exception as e:
        logger.critical(f"Pipeline failure: {e}", exc_info=True)
        sys.exit(1)

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