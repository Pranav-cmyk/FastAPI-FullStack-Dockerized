from fastapi import APIRouter, Request
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates

from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse

from pydantic import BaseModel

from utils import dbDependency, userDependency, getCurrentUser

from database.models import Todos

todosRouter = APIRouter(tags=["Todos"], prefix="/todos")

templates = Jinja2Templates(directory="./templates")


def redirectToLogin():
    redirectResponse = RedirectResponse(
        url="/auth/login-page", status_code=status.HTTP_401_UNAUTHORIZED
    )
    redirectResponse.delete_cookie("access_token")
    return redirectResponse


# Pages


@todosRouter.get("/todo-page", response_class=HTMLResponse)
async def renderTodoPage(request: Request, db: dbDependency):
    try:
        user = await getCurrentUser(request.cookies.get("access_token"))
    except HTTPException as e:
        print(f"Error while fetching user | Token Error: {e}")
        return redirectToLogin()
    except Exception as e:
        print(f"Error while fetching user | General Error: {e}")
        return redirectToLogin()
    else:
        todos = db.query(Todos).filter(Todos.ownerid == user["userID"]).all()
        return templates.TemplateResponse(
            request=request, context={"todos": todos, "user": user}, name="todo.html"
        )


@todosRouter.get("/add-todo-page", response_class=HTMLResponse)
async def renderAddTodoPage(request: Request):
    try:
        user = await getCurrentUser(request.cookies.get("access_token"))
    except HTTPException as e:  
        print(f"Error while fetching user | Token Error: {e}")
        return redirectToLogin()
    except Exception as e:
        print(f"Error while fetching user | General Error: {e}")
        return redirectToLogin()
    else:
        return templates.TemplateResponse(
            request=request, context={"user": user}, name="add-todo.html"
        )


@todosRouter.get("/edit-todo-page/{todoID}", response_class=HTMLResponse)
async def renderEditTodoPage(request: Request, todoID: int, db: dbDependency):
    try:
        user = await getCurrentUser(request.cookies.get("access_token"))
    except HTTPException as e:
        print(f"Error while fetching user | Token Error: {e}")
        return redirectToLogin()
    except Exception as e:
        print(f"Error while fetching user | General Error: {e}")
        return redirectToLogin()
    else:
        todo = (
            db.query(Todos)
            .filter(Todos.ownerid == user["userID"])
            .filter(Todos.id == todoID)
            .first()
        )
        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        return templates.TemplateResponse(
            request=request, context={"todo": todo, "user": user}, name="edit-todo.html"
        )


# Routes


class TodoRequest(BaseModel):
    title: str
    description: str
    priority: int
    completed: bool


@todosRouter.get("/", status_code=status.HTTP_200_OK)
def getTodos(db: dbDependency, user: userDependency):
    return db.query(Todos).filter(Todos.ownerid == user["userID"]).all()


@todosRouter.get("/{todoID}", status_code=status.HTTP_200_OK)
def getTodo(db: dbDependency, todoID: int, user: userDependency):
    todo = (
        db.query(Todos)
        .filter(Todos.ownerid == user["userID"])
        .filter(Todos.id == todoID)
        .first()
    )
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@todosRouter.post("/create", status_code=status.HTTP_201_CREATED)
def createTodo(db: dbDependency, todo: TodoRequest, user: userDependency):
    newTodo = Todos(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        completed=todo.completed,
        ownerid=user["userID"],
    )
    db.add(newTodo)
    db.commit()
    return {"message": "Todo created successfully"}


@todosRouter.put("/update/{todoID}", status_code=status.HTTP_204_NO_CONTENT)
def updateTodo(
    db: dbDependency, todoID: int, todoRequest: TodoRequest, user: userDependency
):
    todo = (
        db.query(Todos)
        .filter(Todos.ownerid == user["userID"])
        .filter(Todos.id == todoID)
        .first()
    )
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    todo.title = todoRequest.title
    todo.description = todoRequest.description
    todo.priority = todoRequest.priority
    todo.completed = todoRequest.completed
    db.add(todo)
    db.commit()
    return {"message": "Todo updated successfully"}


@todosRouter.delete("/delete/{todoID}", status_code=status.HTTP_204_NO_CONTENT)
def deleteTodo(db: dbDependency, todoID: int, user: userDependency):
    todo = (
        db.query(Todos)
        .filter(Todos.ownerid == user["userID"])
        .filter(Todos.id == todoID)
        .first()
    )
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
