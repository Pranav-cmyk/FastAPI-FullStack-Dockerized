from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from starlette import status

from database import SessionLocal
from database.models import Users
from sqlalchemy.orm import Session


from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

import os


# DataBase Connections
def databaseConnection():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


dbDependency = Annotated[Session, Depends(databaseConnection)]

# Password Hashing

bcryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashPassword(password: str):
    return bcryptContext.hash(password)


def verifyPassword(password: str, hashedPassword: str):
    return bcryptContext.verify(password, hashedPassword)


# User Authentication Functions


def fetchAndAuthenticateUserData(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user or not verifyPassword(password, user.hashedpassword):
        return False

    return user


# Creating Token


def createAccessToken(username: str, userID: int, role: str, expiresDelta: timedelta):
    encode = {"sub": username, "id": userID, "role": role}
    expires = datetime.now(timezone.utc) + expiresDelta
    encode.update({"exp": expires})
    return jwt.encode(encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))


# Decoding Token

oauth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def getCurrentUser(token: Annotated[str, Depends(oauth2PasswordBearer)]):
    try:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided"
            )

        secret_key = os.getenv("SECRET_KEY")
        algorithm = os.getenv("ALGORITHM")

        if not secret_key or not algorithm:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server configuration error",
            )

        payload = jwt.decode(token, secret_key, algorithms=[algorithm])

        username = payload.get("sub")
        userID = payload.get("id")
        role = payload.get("role")

        if username is None or userID is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
            )

        return {"username": username, "userID": userID, "role": role}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Error decoding token"
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}"
        )


userDependency = Annotated[dict, Depends(getCurrentUser)]
