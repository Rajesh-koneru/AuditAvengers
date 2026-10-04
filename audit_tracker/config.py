import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

def get_connection():
    db_host = os.getenv("DB_HOST", "interchange.proxy.rlwy.net")
    db_port = int(os.getenv("DB_PORT", "20639"))
    db_user = os.getenv("DB_USER", "root")
    db_pass = os.getenv("DB_PASSWORD", "nwPKmzXjMQOHkjlaGLndEYiCwXuOOBTa")
    db_name = os.getenv("DB_NAME", "railway")

    try:
        return mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_pass,
            database=db_name,
            autocommit=True,
            connection_timeout=5
        )
    except Exception as err:
        raise err
