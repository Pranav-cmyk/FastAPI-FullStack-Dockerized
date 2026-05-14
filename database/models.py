from .database import client
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Todos(client):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(Integer, index=True)
    completed = Column(Boolean, default=False)
    ownerid = Column(Integer, ForeignKey("users.id"))

class Users(client):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    hashedpassword = Column(String, index=True)
    isactive = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)
