import os
from mysql.connector.aio import connect

DB_HOST = os.getenv("MYSQL_HOST")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DB")
DB_PORT = os.getenv("MYSQL_PORT")

# if not DB_PORT:
#     DB_PORT = '3306'

if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT]):
    raise Exception("Please set the environment variables for the database")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(DATABASE_URL)


async def get_db():
    db = await connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    return db
