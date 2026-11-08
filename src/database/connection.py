
import os

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


DATABASE = os.getenv("SQL_DATABASE", "Test")
SQL_USERNAME = os.getenv("SQL_USERNAME")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

if SQL_USERNAME and SQL_PASSWORD:
    # Airflow / Docker: SQL Server Authentication
    SERVER = os.getenv("SQL_SERVER", "host.docker.internal")
    PORT = int(os.getenv("SQL_PORT", "51879"))
    DRIVER = os.getenv("SQL_DRIVER", "ODBC Driver 17 for SQL Server")

    connection_url = URL.create(
        "mssql+pyodbc",
        username=SQL_USERNAME,
        password=SQL_PASSWORD,
        host=SERVER,
        port=PORT,
        database=DATABASE,
        query={
            "driver": DRIVER,
            "TrustServerCertificate": "yes",
        },
    )
else:
    # Local Windows execution: existing Windows authentication
    SERVER = r"DESKTOP-L7EUBBM\SQLEXPRESS"

    connection_url = URL.create(
        "mssql+pyodbc",
        host=SERVER,
        database=DATABASE,
        query={
            "driver": "ODBC Driver 17 for SQL Server",
            "trusted_connection": "yes",
        },
    )

engine = create_engine(
    connection_url,
    pool_pre_ping=True,
)


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(
                    "SELECT @@SERVERNAME AS server_name, "
                    "DB_NAME() AS database_name"
                )
            )
            row = result.fetchone()

            print("Database connection successful!")
            print(f"SQL Server: {row.server_name}")
            print(f"Database: {row.database_name}")

    except Exception as e:
        print("Database connection failed.")
        print(f"Error type: {type(e).__name__}")
        print(f"Details: {e}")
        raise


if __name__ == "__main__":
    try:
        test_connection()
    finally:
        engine.dispose()
