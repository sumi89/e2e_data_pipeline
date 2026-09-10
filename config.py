import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
dotenv_path = os.path.join(BASE_DIR, '.env')
#print(f"dotenv_path: {dotenv_path}")
load_dotenv(dotenv_path)

DB_DRIVER = os.getenv('MSSQL_DRIVER')
#print(f"DB_DRIVER: {DB_DRIVER}")
DB_SERVER = os.getenv('MSSQL_SERVER')
DB_DATABASE = os.getenv('MSSQL_DATABASE')
DB_TRUSTED_CONNECTION = os.getenv('MSSQL_TRUSTED_CONNECTION')


# Construct ODBC connection string
MSSQL_CONN_STR = (
    f"DRIVER={{{DB_DRIVER}}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_DATABASE};"
    f"Trusted_Connection={DB_TRUSTED_CONNECTION};"
)

###########
# Source Server
SOURCE_CONN_STR = (
    f"DRIVER={{{os.getenv('SOURCE_DRIVER')}}};"
    f"SERVER={os.getenv('SOURCE_SERVER')};"
    f"DATABASE={os.getenv('SOURCE_DATABASE')};"
    f"Trusted_Connection={os.getenv('SOURCE_TRUSTED_CONNECTION')};"
)


# Target Server
TARGET_CONN_STR = (
    f"DRIVER={{{os.getenv('TARGET_DRIVER')}}};"
    f"SERVER={os.getenv('TARGET_SERVER')};"
    f"DATABASE={os.getenv('TARGET_DATABASE')};"
    f"Trusted_Connection={os.getenv('TARGET_TRUSTED_CONNECTION')};"
)
