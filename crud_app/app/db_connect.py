import os
from sqlalchemy import create_engine, MetaData
from databases import Database

DB_HOST = os.getenv("POSTAPP_DB_HOST")
DB_USER = os.getenv("POSTAPP_DB_USER")
DB_PASSWORD = os.getenv("POSTAPP_DB_PASSWORD")
DB_NAME = os.getenv("POSTAPP_DB_NAME")
DB_PORT = os.getenv("POSTAPP_DB_PORT")

if not DB_PORT:
    DB_PORT = '3306'

if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
    raise Exception("Please set the environment variables for the database")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


engine = create_engine(DATABASE_URL)
metadata = MetaData()
database = Database(DATABASE_URL)


async def db_init():
    await database.connect()
    return database


async def db_destroy(db):
    await db.disconnect()


async def get_db():
    db = await db_init()
    try:
        yield db
    finally:
        await db_destroy(db)
