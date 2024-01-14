import uvicorn
from app.fastapi_app import app

APP_HOST = "127.0.0.1"
APP_PORT = 8000

if __name__ == "__main__":
    uvicorn.run('main:app', host=APP_HOST, port=APP_PORT, reload=True)
