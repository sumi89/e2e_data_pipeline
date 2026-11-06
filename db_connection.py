
import pyodbc
from config import DB_DRIVER, DB_SERVER, DB_TRUSTED_CONNECTION
from logger import get_logger

logger = get_logger("DatabaseConnection")

def get_db_connection(database: str) -> pyodbc.Connection:
    """Establishes and returns a connection to the specified SQL Server database."""

    connection_string = (
        f"DRIVER={{{DB_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={database};"
        f"Trusted_Connection={DB_TRUSTED_CONNECTION};"
    )

    try:
        logger.info(f"Connecting to server '{DB_SERVER}', database '{database}'...")
        conn = pyodbc.connect(connection_string)
        logger.info(f"Connection established successfully to '{database}'.")
        return conn

    except pyodbc.Error as e:
        logger.error(
            f"Failed to connect to database '{database}': {e}"
        )
        raise
        
    '''
    except Exception as e:
        logger.error(f"Failed to connect to MS SQL Server: {e}")
        raise
    '''

def run_diagnostics(conn: pyodbc.Connection) -> None:
    """
    Executes a diagnostic check against the active SQL connection.
    """
    query = """
        SELECT
            @@SERVERNAME AS server_name,
            DB_NAME() AS current_database,
            SYSTEM_USER AS connected_user,
            @@VERSION AS sql_version;
    """

    logger.info(
        "Executing diagnostic query to retrieve server information..."
    )

    cursor = conn.cursor()

    try:
        cursor.execute(query)
        result = cursor.fetchone()
        if result is None:
            logger.warning("Diagnostic query returned no results.")
            return
        logger.info("Successfully retrieved server diagnostics:")
        logger.info(f"Host Server Name : {result.server_name}")
        logger.info(f"Active Database : {result.current_database}")
        logger.info(f"Authenticated As : {result.connected_user}")
        logger.info(
            f"SQL Engine : {result.sql_version.splitlines()[0]}"
        )

    finally:
        cursor.close()


'''
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
'''


'''
This tests several things at once:

-the database exists
-the table exists
-Windows account has SELECT permission
-SQL Server can execute the query
-pyodbc can retrieve the results
'''

def test_table_read(
    conn: pyodbc.Connection,
    schema: str,
    table: str
) -> None:
    """Tests whether a table can be read from the active database connection."""

    query = f"SELECT TOP (5) * FROM [{schema}].[{table}];"

    logger.info(f"Testing read access to [{schema}].[{table}]...")

    cursor = conn.cursor()

    try:
        cursor.execute(query)

        rows = cursor.fetchall()

        if not rows:
            logger.warning(
                f"Table [{schema}].[{table}] is accessible but returned no rows."
            )
            return

        # Get column names
        columns = [column[0] for column in cursor.description]

        logger.info(
            f"Successfully read table [{schema}].[{table}]."
        )

        logger.info(f"Columns: {columns}")
        logger.info(f"Rows retrieved: {len(rows)}")

        for row in rows:
            logger.info(row)

    finally:
        cursor.close()