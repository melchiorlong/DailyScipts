from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import models

Base = declarative_base()

engine = create_engine('mysql+pymysql://root:12345678@localhost/local_database')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

res = session.query(models.Users).all()
for user in res:
    print(user.id)
    print(user.username)
    print(user.email)
    print(user.birthdate)
    print(user.is_active)

session.close()
