from pathlib import Path

from fastapi import FastAPI, Depends, Request
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


async def validate(db: Database, username: str, password: str) -> bool:
    expected_hash = await db.execute(
        "SELECT password_hash FROM `User` WHERE username = :username",
        {"username": username}
    )
    return sha256(password.encode()).hexdigest() == expected_hash


class PostModel(BaseModel):
    username: str
    password: str
    title: str
    content: str


class UserModel(BaseModel):
    username: str
    password: str


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})


@app.post("/test")
async def test(request: Request):
    return JSONResponse({"status": "success", "message": "Hello World"})


@app.get("/view/{username}")
async def view(username: int):
    ...


@app.post("/create/post")
async def create_post(req: PostModel, db: Database = Depends(get_db)):
    if not await validate(db, req.username, req.password):
        return {"error": "wrong password", "status_code": 403}

    author_id = await db.execute(
        "SELECT id FROM `User` WHERE username = :username",
        {"username": req.username})

    await db.execute(
        "INSERT INTO `Post`(title, content, author_id) VALUES (:title, :content, :author_id)",
        {'title': req.title, 'content': req.content, 'author_id': author_id[0][0]}
    )

    return {"status_code": 200, "message": "post created"}


@app.post("/create/user")
async def create_user(req: UserModel, db: Database = Depends(get_db)):
    await db.execute(
        "INSERT INTO `User`(username, password_hash) VALUES (:username, :password_hash)",
        {'username': req.username,
         'password_hash': sha256(req.password.encode()).hexdigest()}
    )

    return {"status_code": 200, "message": "user created"}
