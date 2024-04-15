from sqlalchemy import Column, DECIMAL, Date, DateTime, Integer, String, Table, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.orm.base import Mapped

Base = declarative_base()
metadata = Base.metadata


t_damai_show_concert_spider_20240415 = Table(
    'damai_show_concert_spider_20240415', metadata,
    Column('create_time', DateTime),
    Column('show_title', String(255, 'utf8mb4_general_ci'), nullable=False),
    Column('show_location', String(255, 'utf8mb4_general_ci')),
    Column('show_date', DateTime),
    Column('show_price', String(255, 'utf8mb4_general_ci')),
    Column('show_actor', String(255, 'utf8mb4_general_ci'))
)

