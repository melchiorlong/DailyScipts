from sqlalchemy import Column, DECIMAL, Date, DateTime, Integer, String, Table, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.orm.base import Mapped

Base = declarative_base()
metadata = Base.metadata


t_cube_burial_point_simulation = Table(
    'cube_burial_point_simulation', metadata,
    Column('event_id', String(255, 'utf8mb4_general_ci')),
    Column('event_name', String(255, 'utf8mb4_general_ci')),
    Column('point_id', String(255, 'utf8mb4_general_ci')),
    Column('point_name', String(255, 'utf8mb4_general_ci')),
    Column('launch_duration', DECIMAL(10, 2))
)


t_damai_show_concert_spider_20240415 = Table(
    'damai_show_concert_spider_20240415', metadata,
    Column('create_time', DateTime),
    Column('show_title', String(255, 'utf8mb4_general_ci'), nullable=False),
    Column('show_location', String(255, 'utf8mb4_general_ci')),
    Column('show_date', DateTime),
    Column('show_price', String(255, 'utf8mb4_general_ci'))
)


class Users(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(50, 'utf8mb4_general_ci'), nullable=False)
    email = mapped_column(String(100, 'utf8mb4_general_ci'), nullable=False)
    birthdate = mapped_column(Date)
    is_active = mapped_column(TINYINT(1), server_default=text("'1'"))
