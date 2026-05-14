from fastapi import APIRouter, HTTPException

from starlette import status
from database.models import Users, Todos

from utils import dbDependency, userDependency

adminRouter = APIRouter(
    prefix = '/admin',
    tags = ['Admin']
)

# GET Routes
@adminRouter.get("/users", status_code=status.HTTP_200_OK)
def getAllUsers(db: dbDependency, currentUser: userDependency):
    if currentUser is None or currentUser.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return db.query(Users).all()

@adminRouter.get("/todos", status_code = status.HTTP_200_OK)
def getAllTodos(db: dbDependency, currentUser: userDependency):
    if currentUser is None or currentUser.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return db.query(Todos).all()

@adminRouter.delete("/user/{username}", status_code=status.HTTP_200_OK)
def deleteUser(db: dbDependency, currentUser: userDependency, username: str):
    if currentUser is None or currentUser.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
        

@adminRouter.delete("/todo/{ownerID}", status_code=status.HTTP_200_OK)
def deleteTodo(db: dbDependency, currentUser: userDependency, ownerID: int, todoID: int):
    if currentUser is None or currentUser.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    todo = db.query(Todos).filter(Todos.ownerid == ownerID).filter(Todos.id == todoID).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}