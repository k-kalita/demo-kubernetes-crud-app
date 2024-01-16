from pathlib import Path

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from databases import Database
from pydantic import BaseModel
from hashlib import sha256

from .db_connect import get_db

APP_ROOT_PATH = Path(__file__).parent
app = FastAPI()

# Templates configuration
templates = Jinja2Templates(directory=APP_ROOT_PATH / "templates")

# Static files configuration
app.mount("/static", StaticFiles(directory=APP_ROOT_PATH / "static"), name="static")


async def validate(db: Database, username: str, password: str) -> None:
    expected_hash = await db.fetch_one(
        "SELECT password_hash FROM `User` WHERE username = :username",
        {"username": username}
    )
    if expected_hash is None:
        raise HTTPException(status_code=400, detail="User does not exist")
    if sha256(password.encode()).hexdigest() != expected_hash:
        raise HTTPException(status_code=403, detail="wrong password")


class PostModel(BaseModel):
    username: str
    password: str
    title: str
    content: str


class PostDeleteModel(BaseModel):
    username: str
    password: str
    id_: int


class UserModel(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})


@app.post("/test")
async def test(request: Request):
    data = await request.form()
    return JSONResponse({"status": "success", "message": "Hello World"})


@app.get("/view/{username}")
async def view(username: int):
    ...


@app.post("/create/post")
async def create_post(req: Request, db: Database = Depends(get_db)):
    data = await req.form()
    try:
        await validate(db, data.get('username'), data.get('password'))
    except HTTPException as e:
        return JSONResponse({"status_code": e.status_code,
                             "status": "failure",
                             "message": e.detail})

    author_id = await db.fetch_one(
        "SELECT id FROM `User` WHERE username = :username",
        {"username": data.get('username')}
    )
    author_id = author_id[0]

    await db.execute(
        "INSERT INTO `Post`(title, content, author_id) VALUES (:title, :content, :author_id)",
        {'title': data.get('title'), 'content': data.get('content'), 'author_id': author_id}
    )

    return JSONResponse({"status_code": 200, "status": "success", "message": "Post created"})


@app.post("/delete/post")
async def delete_post(req: Request, db: Database = Depends(get_db)):
    data = await req.form()
    try:
        await validate(db, data.get('username'), data.get('password'))
    except HTTPException as e:
        return JSONResponse({"status_code": e.status_code,
                             "status": "failure",
                             "message": e.detail})

    author_id = await db.fetch_one(
        "SELECT id FROM `User` WHERE username = :username",
        {"username": data.get('username')}
    )
    author_id = author_id[0]

    await db.execute(
        "DELETE FROM `Post` WHERE id = :id_ AND author_id = :author_id",
        {"id_": data.get('id_'), "author_id": author_id}
    )

    return JSONResponse({"status_code": 200, "status": "success", "message": "Post deleted"})


@app.get("/create/user")
def create_user(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})


@app.post("/create/user")
async def create_user(req: Request, db: Database = Depends(get_db)):
    data = await req.form()

    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    out = await db.fetch_all("SELECT id FROM `User` WHERE username = :username",
                             {'username': username})

    if len(out) > 0:
        return HTTPException(status_code=400, detail="User already exists")

    await db.execute("INSERT INTO `User`(username, password_hash, name, last_name, email) "
                     "VALUES (:username, :password_hash, :first_name, :last_name, :email)",
                     {'username': username, 'password_hash': sha256(password.encode()).hexdigest(),
                      'first_name': first_name, 'last_name': last_name, 'email': email})

    return JSONResponse({"status_code": 200, "status": "success", "message": "User created"})


@app.post("/delete/user")
async def delete_user(req: UserModel, db: Database = Depends(get_db)):
    out = await db.fetch_all("SELECT id FROM `User` WHERE username = :username",
                             {'username': req.username})

    if len(out) == 0:
        return HTTPException(status_code=400, detail="User does not exist")

    await db.execute("DELETE FROM `User` WHERE username = :username",
                     {'username': req.username})

    return JSONResponse({"status_code": 200, "status": "success", "message": "User deleted"})
