from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Postgres@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency (Everytime a request comes, we establish a session so that we can interact with the database. This function does that)
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
