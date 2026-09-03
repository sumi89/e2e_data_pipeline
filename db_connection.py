import logging
import pyodbc
from config import MSSQL_CONN_STR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

logger = logging.getLogger("DatabaseConnection")

logger.info("Starting database connection...")

def get_db_connection() -> pyodbc.Connection:
    """Establishes and returns a pyodbc connection object."""
    try:
        logger.info("Connecting to MS SQL Server...")
        conn = pyodbc.connect(MSSQL_CONN_STR)
        logger.info("Connection established successfully.")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to MS SQL Server: {e}")
        raise

def run_diagnostics(conn) -> None:
    """Executes a diagnostic check against the active SQL connection."""
    query = """
        SELECT 
            @@SERVERNAME AS server_name,
            DB_NAME() AS current_database,
            SYSTEM_USER AS connected_user,
            @@VERSION AS sql_version;
    """
    logger.info("Executing diagnostic query to retrieve server information...")
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()

    if result is None:
        logger.warning("Diagnostic query returned no results.")
        cursor.close()
        return
    
    logger.info("Successfully retrieved server diagnostics:")
    logger.info(f"Host Server Name : {result.server_name}")
    logger.info(f"Active Database  : {result.current_database}")
    logger.info(f"Authenticated As : {result.connected_user}")
    logger.info(f"SQL Engine       : {result.sql_version.splitlines()[0]}")
    cursor.close()