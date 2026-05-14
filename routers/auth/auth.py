from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from starlette.responses import HTMLResponse
from starlette import status

from utils import dbDependency, fetchAndAuthenticateUserData, createAccessToken
from datetime import timedelta
import os

from pydantic import BaseModel

templates = Jinja2Templates(directory="./templates")

authRouter = APIRouter(tags=["Auth"], prefix="/auth", include_in_schema=False)

# Pages


@authRouter.get("/login-page", response_class=HTMLResponse)
async def loginPage(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@authRouter.get("/register-page", response_class=HTMLResponse)
async def registerPage(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")


# Auth Routes


class responseTokenModel(BaseModel):
    access_token: str
    token_type: str


@authRouter.post("/token", response_model=responseTokenModel)
async def generateToken(
    formData: Annotated[OAuth2PasswordRequestForm, Depends()], db: dbDependency
):
    user = fetchAndAuthenticateUserData(formData.username, formData.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    accessTokenExpiry = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_IN")))
    accessToken = createAccessToken(
        formData.username, user.id, user.role, accessTokenExpiry
    )
    return {"access_token": accessToken, "token_type": "bearer"}
