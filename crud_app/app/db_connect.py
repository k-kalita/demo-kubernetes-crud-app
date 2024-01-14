from sqlalchemy import create_engine, MetaData
from databases import Database

DB_HOST = "127.0.0.1"
DB_USER = "db_user"
DB_PASSWORD = "db_password"
DB_NAME = "PostDB"

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
