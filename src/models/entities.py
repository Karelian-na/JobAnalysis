from database import DB_URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, SmallInteger

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

    def toDict(self) -> dict[str, str | int]:
        data: dict[str, str | int] = {
            "id": self.id,
            "name": self.name,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "salary_sys": self.salary_sys,
            "work_area": self.work_area,
            "experience": self.experience,
            "degree": self.degree,
            "company_name": self.company_name,
            "type": self.type,
        }
        return data
