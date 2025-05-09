import time
from sqlalchemy import text

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "mysql+pymysql://user:password@127.0.0.1:3306/webshop"

for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # test actual connection
        print("Database connected.")
        break
    except OperationalError:
        print("Waiting for database...")
        time.sleep(2)
else:
    raise Exception("Could not connect to database after retries.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()