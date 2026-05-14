from fastapi import APIRouter
from fastapi import status, HTTPException

from pydantic import BaseModel

from utils import dbDependency, userDependency, hashPassword, verifyPassword
from database.models import Users


class UserRequest(BaseModel):
    username: str
    email: str
    firstname: str
    lastname: str
    password: str
    isactive: bool
    role: str
    phone_number: str

usersRouter = APIRouter(
    tags=["Users"],
    prefix = "/users"
)

@usersRouter.get("/{userID}")
def getUser(db: dbDependency, user: userDependency, userID: int):
    
    if user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

    user = db.query(Users).filter(Users.id == userID).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"message": "User found successfully", "user": user}


@usersRouter.post("/create", status_code=status.HTTP_201_CREATED)
def createUser(db: dbDependency, usermodel: UserRequest):
    newUser = Users(username=usermodel.username, email=usermodel.email, firstname=usermodel.firstname, lastname=usermodel.lastname, hashedpassword=hashPassword(usermodel.password), isactive=usermodel.isactive, role=usermodel.role, phone_number=usermodel.phone_number)
    db.add(newUser)
    db.commit()
    return {"message": "User created successfully"}

@usersRouter.put("/update/password", status_code=status.HTTP_200_OK)
def updatePassword(db: dbDependency, currentUser: userDependency, userModel: UserRequest, newPassword: str):

    user = db.query(Users).filter(Users.username == userModel.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Ensure that the user trying to change their password is the same user
    if currentUser["username"] != user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

    if not verifyPassword(userModel.password, user.hashedpassword):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password")

    user.hashedpassword = hashPassword(newPassword)
    db.add(user)   
    db.commit()
    return {"message": "Password updated successfully"}


@usersRouter.put("/update/phoneNumber", status_code=status.HTTP_200_OK)
def updatePhoneNumber(db: dbDependency, currentUser: userDependency, userModel: UserRequest):
    
    user = db.query(Users).filter(Users.username == userModel.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Ensure that the user trying to change their phone number is the same user
    if currentUser["username"] != user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    
    if not verifyPassword(userModel.password, user.hashedpassword):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password")
    
    if userModel.phone_number == user.phone_number:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New phone number is same as old phone number")
    
    user.phone_number = userModel.phone_number
    db.add(user)
    db.commit()
    return {"message": "Phone number updated successfully"}