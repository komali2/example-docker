import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI

username = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_ROOT_PASSWORD')
host = os.getenv('MYSQL_HOST')
port = os.getenv('MYSQL_PORT')
DB_NAME = os.getenv('MYSQL_DB')

print(username)
print(password)
print(host)
print(port)

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}"

print('about to create engine')
engine = create_engine( SQLALCHEMY_DATABASE_URL, connect_args={'auth_plugin': 'mysql_native_password'})
print('successfully create engine')

print('about to make session')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print('successfully make session')

print('about to make base')
Base = declarative_base()
print('successfully make base')

try:
    print('attempt 1')
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        result = conn.execute(text("select 'hello world'"))
        print(result.all())

except Exception as inst:
    print(f"try SLEEPING, error was {inst}")
    time.sleep(14)
    try:
        Base.metadata.create_all(bind=engine)
        with engine.connect() as conn:
            result = conn.execute(text("select 'hello world'"))
            print(result.all())

    except:
        print('try AGIAN SLEEPING')
        time.sleep(14)
        Base.metadata.create_all(bind=engine)
        with engine.connect() as conn:
            result = conn.execute(text("select 'hello world'"))
            print(result.all())


app = FastAPI()
