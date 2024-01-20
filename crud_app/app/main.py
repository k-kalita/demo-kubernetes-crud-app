from typing import Dict
from hashlib import sha256
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from .db_connect import DatabaseConnection, DatabaseWrapper

# ----------------------------------------- app config ----------------------------------------- #

APP_ROOT_PATH = Path(__file__).parent
app = FastAPI()

# Templates configuration
templates = Jinja2Templates(directory=APP_ROOT_PATH / "templates")

# Static files configuration
app.mount("/static", StaticFiles(directory=APP_ROOT_PATH / "static"), name="static")


# ----------------------------------------- validation ----------------------------------------- #

async def validate(wrapper: DatabaseWrapper, username: str, password: str) -> None:
    await wrapper.cursor.execute("SELECT password_hash FROM `User` WHERE username = %s",
                                 (username,))
    expected_hash = await wrapper.cursor.fetchone()

    if expected_hash is None:
        raise HTTPException(status_code=400, detail="User does not exist")
    if sha256(password.encode()).hexdigest() != expected_hash[0]:
        raise HTTPException(status_code=403, detail="wrong password")


async def validation_response(wrapper: DatabaseWrapper,
                              username: str,
                              password: str) -> JSONResponse | None:
    try:
        await validate(wrapper, username, password)
    except HTTPException as e:
        return JSONResponse({"status_code": e.status_code,
                             "status": "failure",
                             "message": e.detail})
    return None


# -------------------------------------------- util -------------------------------------------- #

async def get_user_id(wrapper: DatabaseWrapper, username: str) -> int:
    await wrapper.cursor.execute("SELECT id FROM `User` WHERE username = %s", (username,))
    user_id = await wrapper.cursor.fetchone()
    if user_id is None:
        raise HTTPException(status_code=400, detail="User does not exist")
    return user_id[0]


def parse_user_record(user: tuple) -> Dict[str, str]:
    return {"id": user[0],
            "username": user[1],
            "first_name": user[3],
            "last_name": user[4],
            "email": user[5]}


def parse_post_record(post: tuple) -> Dict[str, str]:
    return {"id": post[0],
            "title": post[1],
            "content": post[2],
            "author_id": post[3],
            "created_on": post[4]}


# ----------------------------------------- post views ----------------------------------------- #

@app.get("/view/post/{id_}")
async def view_post(request: Request, id_: int):
    async with DatabaseConnection() as conn:
        await conn.cursor.execute("SELECT * FROM `Post` WHERE id = %s", (id_,))
        post = parse_post_record(await conn.cursor.fetchone())
        await conn.cursor.execute("SELECT * FROM `User` WHERE id = %s", (post["author_id"],))
        user = parse_user_record(await conn.cursor.fetchone())

    return templates.TemplateResponse("view_post.html", {"request": request,
                                                         "post": post,
                                                         "user": user})


@app.get("/create/post")
async def create_post(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})


@app.post("/create/post")
async def create_post(req: Request):
    data = await req.form()

    async with DatabaseConnection() as conn:
        response = await validation_response(conn, data.get('username'), data.get('password'))
        if response is not None:
            return response
        author_id = await get_user_id(conn, data.get('username'))

        await conn.cursor.execute(
            "INSERT INTO `Post`(title, content, author_id)"
            "VALUES (%s, %s, %s)",
            (data.get('title'), data.get('content'), author_id)
        )
        await conn.commit()

    return JSONResponse({"status_code": 200, "status": "success", "message": "Post created"})


@app.post("/update/post/{id_}")
async def delete_post(request: Request, id_: int) -> JSONResponse:
    data = await request.form()

    async with DatabaseConnection() as conn:
        user_id = await get_user_id(conn, data.get('username'))
        await conn.cursor.execute("SELECT author_id FROM `Post` WHERE id = %s", (id_,))
        author_id = (await conn.cursor.fetchone())[0]
        if user_id != author_id:
            return JSONResponse({"status_code": 403, "status": "failure",
                                 "message": "You cannot edit this post"})

        response = await validation_response(conn, data.get('username'), data.get('password'))
        if response is not None:
            return response

        title = data.get('title')
        content = data.get('content')

        if title is None or content is None:
            return JSONResponse({"status_code": 400, "status": "failure",
                                 "message": "Title and content must be provided"})

        await conn.cursor.execute("UPDATE `Post` SET title = %s, content = %s WHERE id = %s",
                                  (title, content, id_))
        await conn.commit()

    return JSONResponse({"status_code": 200,
                         "status": "success",
                         "message": "Post updated",
                         "post_id": id_,
                         "action": "update",
                         "title": title,
                         "content": content})


@app.post("/delete/post/{id_}")
async def delete_post(request: Request, id_: int) -> JSONResponse:
    data = await request.form()

    async with DatabaseConnection() as conn:
        user_id = await get_user_id(conn, data.get('username'))
        await conn.cursor.execute("SELECT author_id FROM `Post` WHERE id = %s", (id_,))
        author_id = (await conn.cursor.fetchone())[0]
        if user_id != author_id:
            return JSONResponse({"status_code": 403, "status": "failure",
                                 "message": "You cannot delete this post"})

        response = await validation_response(conn, data.get('username'), data.get('password'))
        if response is not None:
            return response

        await conn.cursor.execute("DELETE FROM `Post` WHERE id = %s", (id_,))
        await conn.commit()

    return JSONResponse({"status_code": 200,
                         "status": "success",
                         "message": "Post deleted",
                         "post_id": id_,
                         "action": "delete"})


# ----------------------------------------- user views ----------------------------------------- #

@app.get("/view/users")
async def view_users(request: Request) -> HTMLResponse:
    async with DatabaseConnection() as conn:
        await conn.cursor.execute("SELECT * FROM `User`")
        users = await conn.cursor.fetchall()
    users = [parse_user_record(user) for user in users]

    return templates.TemplateResponse("view_users.html", {"request": request, "users": users})


@app.get("/view/user/{username}")
async def view_user(request: Request, username: str) -> HTMLResponse:
    async with DatabaseConnection() as conn:
        await conn.cursor.execute("SELECT * FROM `User` WHERE username = %s", (username,))
        user = parse_user_record(await conn.cursor.fetchone())
        await conn.cursor.execute("SELECT * FROM `Post` WHERE author_id = %s", (user["id"],))
        posts = [parse_post_record(post) for post in await conn.cursor.fetchall()]

    return templates.TemplateResponse("view_user.html", {"request": request,
                                                         "user": user,
                                                         "posts": posts})


@app.get("/create/user")
def create_user(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("create_user.html", {"request": request})


@app.post("/create/user")
async def create_user(req: Request):
    data = await req.form()
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    async with DatabaseConnection() as conn:
        try:
            await conn.cursor.execute(
                "INSERT INTO `User`(username, password_hash, name, last_name, email) "
                "VALUES (%s, %s, %s, %s, %s)",
                (username, sha256(password.encode()).hexdigest(), first_name, last_name, email)
            )
            await conn.commit()
        except IntegrityError as e:
            return JSONResponse({"status_code": 400, "status": "failure", "message": str(e)})

    return JSONResponse({"status_code": 200, "status": "success", "message": "User created"})


@app.post("/delete/user")
async def delete_user(req: Request):
    data = await req.form()

    async with DatabaseConnection() as conn:
        response = await validation_response(conn, data.get('username'), data.get('password'))
        if response is not None:
            return response

        await conn.cursor.execute("DELETE FROM `User` WHERE username = %s", (data.get('username'),))
        await conn.commit()

    return JSONResponse({"status_code": 200, "status": "success", "message": "User deleted"})
