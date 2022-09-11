from database import DB_URL
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, SmallInteger
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(DB_URL)
EntityBase = declarative_base(engine)

class Job(EntityBase):
    __tablename__ = "jobs"
    id = Column(String(28), primary_key=True, autoincrement=True)
    name = Column(String(255))
    salary_min = Column(Float)
    salary_max = Column(Float)
    salary_sys = Column(SmallInteger)
    work_area = Column(String(255))
    experience = Column(String(255))
    degree = Column(String(255))
    company_name = Column(String(255))
    type = Column(String(255))