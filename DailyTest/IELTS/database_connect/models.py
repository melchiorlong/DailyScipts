from sqlalchemy import Column, DECIMAL, Date, DateTime, Integer, String, Table, text, VARCHAR
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.orm.base import Mapped

# sqlacodegen_v2 --generator tables mysql+pymysql://root:12345678@localhost/local_database --outfile=model1.py

Base = declarative_base()
metadata = Base.metadata

t_ielts_vocabulary = Table(
    'ielts_vocabulary', metadata,
    Column('id', Integer, primary_key=True),
    Column('vocabulary', VARCHAR(255)),
    Column('parts_of_speech', VARCHAR(255)),
    Column('parts_of_speech_eng', VARCHAR(255)),
    Column('parts_of_speech_chn', VARCHAR(255)),
    Column('meaning', VARCHAR(255)),
    Column('example_sentence', VARCHAR(255)),
    Column('sort', VARCHAR(255))
)
