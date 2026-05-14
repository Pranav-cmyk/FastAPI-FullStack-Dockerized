from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import HTMLResponse, RedirectResponse
from starlette import status

from routers.todos import todosRouter
from routers.users import usersRouter
from routers.auth import authRouter
from routers.admin import adminRouter

app = FastAPI(title="Todo App", description="Todo App", version="0.0.1")

CORSMiddleware(
    app,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")




@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Redirect to login page if not authenticated
    return RedirectResponse("/auth/login-page", status_code=status.HTTP_302_FOUND)



app.include_router(todosRouter)
app.include_router(usersRouter)
app.include_router(authRouter)
app.include_router(adminRouter)
