from .sessions import engine
from sqlmodel import SQLModel

def create_all_db_tables():
    SQLModel.metadata.create_all(engine)