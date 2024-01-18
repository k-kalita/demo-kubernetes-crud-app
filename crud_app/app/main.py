from hashlib import sha256
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from mysql.connector.aio.connection import MySQLConnection
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.staticfiles import StaticFiles

from .db_connect import get_db

# ----------------------------------------- app config ----------------------------------------- #

APP_ROOT_PATH = Path(__file__).parent
app = FastAPI()

# Templates configuration
templates = Jinja2Templates(directory=APP_ROOT_PATH / "templates")

# Static files configuration
app.mount("/static", StaticFiles(directory=APP_ROOT_PATH / "static"), name="static")


# ----------------------------------------- validation ----------------------------------------- #

async def validate(db: MySQLConnection, username: str, password: str) -> None:
    cur = await db.cursor()
    await cur.execute(
        "SELECT password_hash FROM `User` WHERE username = %s",
        (username,)
    )
    expected_hash = (await cur.fetchone())[0]
    await cur.close()

    if expected_hash is None:
        raise HTTPException(status_code=400, detail="User does not exist")
    if sha256(password.encode()).hexdigest() != expected_hash[0]:
        raise HTTPException(status_code=403, detail="wrong password")


async def validation_response(db, username: str, password: str) -> JSONResponse | None:
    try:
        await validate(db, username, password)
    except HTTPException as e:
        return JSONResponse({"status_code": e.status_code,
                             "status": "failure",
                             "message": e.detail})
    return None


# ------------------------------------------ querying ------------------------------------------ #

async def get_user_id(db, username: str) -> int:
    cur = await db.cursor()
    await cur.execute("SELECT id FROM `User` WHERE username = %s",
                      (username,))
    user_id = (await cur.fetchone())[0]
    await cur.close()
    if user_id is None:
        raise HTTPException(status_code=400, detail="User does not exist")
    return user_id[0]


# ----------------------------------------- post crud ------------------------------------------ #

@app.get("/view/post/{id_}")
async def view_post(id_: int):
    ...


@app.get("/create/post")
async def create_post(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})


@app.post("/create/post")
async def create_post(req: Request):
    db = await get_db()
    data = await req.form()
    response = await validation_response(db, data.get('username'), data.get('password'))
    if response is not None:
        return response
    author_id = await get_user_id(db, data.get('username'))

    cur = await db.cursor()
    try:
        await cur.execute(
            "INSERT INTO `Post`(title, content, author_id)"
            "VALUES (%s, %s, %s)",
            (data.get('title'), data.get('content'), author_id)
        )
        await db.commit()
    except SQLAlchemyError as e:  # TODO: check if this is the right exception
        return JSONResponse({"status_code": 500, "status": "failure", "message": str(e)})
    await cur.close()

    return JSONResponse({"status_code": 200, "status": "success", "message": "Post created"})


@app.post("/delete/post")
async def delete_post(req: Request):
    db = await get_db()
    data = await req.form()
    response = await validation_response(db, data.get('username'), data.get('password'))
    if response is not None:
        return response
    author_id = await get_user_id(db, data.get('username'))

    cur = await db.cursor()
    try:
        await cur.execute("DELETE FROM `Post` WHERE id = %s AND author_id = %s",
                          (data.get('id'), author_id))
    except SQLAlchemyError as e:  # TODO: check if this is the right exception
        return JSONResponse({"status_code": 500, "status": "failure", "message": str(e)})
    await cur.close()

    return JSONResponse({"status_code": 200, "status": "success", "message": "Post deleted"})


# ----------------------------------------- user crud ------------------------------------------ #

@app.get("/view/{username}")
async def view_user(username: int):
    ...


@app.get("/create/user")
def create_user(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})


@app.post("/create/user")
async def create_user(req: Request):
    db = await get_db()
    data = await req.form()
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    cur = await db.cursor()
    try:
        await cur.execute(
            "INSERT INTO `User`(username, password_hash, name, last_name, email) "
            "VALUES (%s, %s, %s, %s, %s)",
            (username, sha256(password.encode()).hexdigest(), first_name, last_name, email)
        )
        await db.commit()
    except IntegrityError as e:
        return JSONResponse({"status_code": 400, "status": "failure", "message": str(e)})
    except SQLAlchemyError as e:
        return JSONResponse({"status_code": 500, "status": "failure", "message": str(e)})
    finally:
        await cur.close()

    return JSONResponse({"status_code": 200, "status": "success", "message": "User created"})


@app.post("/delete/user")
async def delete_user(req: Request):
    db = await get_db()
    data = await req.form()
    response = await validation_response(db, data.get('username'), data.get('password'))
    if response is not None:
        return response

    cur = await db.cursor()
    try:
        await cur.execute("DELETE FROM `User` WHERE username = %s",
                          (data.get('username'),))
    except SQLAlchemyError as e:
        return JSONResponse({"status_code": 500, "status": "failure", "message": str(e)})
    await cur.close()

    return JSONResponse({"status_code": 200, "status": "success", "message": "User deleted"})
