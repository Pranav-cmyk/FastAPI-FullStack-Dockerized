from .database import engine, client, SessionLocal
from .models import Todos, Users

client.metadata.create_all(bind=engine)
