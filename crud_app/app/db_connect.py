import os
from mysql.connector.aio import connect, MySQLConnection

DB_HOST = os.getenv("MYSQL_HOST")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DB")
DB_PORT = os.getenv("MYSQL_PORT")

if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT]):
    raise Exception("Please set the environment variables for the database")


class DatabaseWrapper:

    def __init__(self, db: MySQLConnection, cursor: MySQLConnection.cursor):
        self._db = db
        self.cursor = cursor

    async def commit(self):
        await self._db.commit()


class DatabaseConnection:

    def __init__(self):
        self.db = None
        self.cursor = None
        self.wrapper = None

    @staticmethod
    async def get_db():
        db = await connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        return db

    async def __aenter__(self) -> DatabaseWrapper:
        self.db = await self.get_db()
        self.cursor = await self.db.cursor()
        self.wrapper = DatabaseWrapper(self.db, self.cursor)
        return self.wrapper

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cursor.close()
        await self.db.close()
