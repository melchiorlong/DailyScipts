from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_session():
    engine = create_engine('mysql+pymysql://root:12345678@localhost/local_database')

    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def session_close(session):
    session.close()
