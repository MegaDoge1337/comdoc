import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get("DB_CONNECTION_STRING"))
SessionFactory = sessionmaker(bind=engine)