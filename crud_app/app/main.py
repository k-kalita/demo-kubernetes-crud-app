from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from databases import Database
from pydantic import BaseModel
from hashlib import sha256

from .db_connect import (get_db)

app = FastAPI()

# Templates configuration
templates = Jinja2Templates(directory="app/templates")

# Static files configuration
app.mount("/static", StaticFiles(directory="app/static"), name="static")


async def validate(db: Database, username: str, password: str) -> bool:
    expected_hash = await db.execute(
        "SELECT password_hash FROM `User` WHERE username = :username",
        {"username": username})
    return sha256(password.encode()).hexdigest() == expected_hash


class PostModel(BaseModel):
    username: str
    password: str
    title: str
    content: str


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})


@app.get("/view/{username}")
async def view(username: int):
    ...


@app.get("/create/post", response_model=PostModel, response_class=HTMLResponse)
async def create_post(req: PostModel, db: Database = Depends(get_db)):
    if not await validate(db, req.username, req.password):
        return {"error": "wrong password", "status_code": 403}

    author_id = await db.execute(
        "SELECT id FROM `User` WHERE username = :username",
        {"username": req.username})

    await db.execute("INSERT INTO `Post`(title, content, author_id) VALUES (:title, :content, :author_id)",
                     {'title': req.title, 'content': req.content, 'author_id': author_id[0][0]})

    return {"status_code": 200, "message": "post created"}
