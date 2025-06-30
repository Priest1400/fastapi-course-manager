from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from fastapi.websockets import WebSocket
from db.database import base, engine
from db import models
from fastapi.requests import Request
from fastapi.responses import JSONResponse, HTMLResponse

from routers import R_Users

app = FastAPI()

app.include_router(R_Users.router)
models.base.metadata.create_all(engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def creat_user():
    return "hello"