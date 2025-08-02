from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from fastapi.websockets import WebSocket
from db.database import base, engine
from db import models
from fastapi.requests import Request
from fastapi.responses import JSONResponse, HTMLResponse

from routers import R_Users, R_Login, R_Admin, R_Course, R_Students

app = FastAPI()

app.include_router(R_Users.router)
app.include_router(R_Login.router)
app.include_router(R_Admin.router)
app.include_router(R_Course.router)
app.include_router(R_Students.router)
models.base.metadata.create_all(engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def hello():
    return "hello"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)