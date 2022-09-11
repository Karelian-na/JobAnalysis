from models.entities import Job, engine
from services.BaseService import BaseService
from sqlalchemy.orm import sessionmaker

session = sessionmaker(engine).__call__()


class JobService(BaseService):

    def getById(self, id: int) -> Job | None:
        """get a job from database

        Args:
            id (int): the job id

        Returns:
            Job | None: if the database has the job, return the job object, otherwise, None
        """
        return session.query(Job).filter(Job.id == id).one_or_none()

    def gedAllByName(self, name: str) -> list[Job] | None:
        """get all jobs from database which name is name

        Args:
            name (str): the job name

        Returns:
            typing.List[Job] | None: if has, return a list of Job, otherwise None
        """
        jobs = session.query(Job).filter(Job.name == name).all()
        if jobs.__len__ == 0:
            return None
        return jobs

    def getAll(self) -> list[Job] | None:
        """get all record from database, user with caution

        Returns:
            list[Job] | None: if database is empty, return None, otherwise the all jobs
        """
        jobs = session.query(Job).all()
        if jobs.__len__ == 0:
            return None
        return jobs

    def getAllBySalaryInterval(min: int, max: int) -> list[Job]:
        """get all jobs which salary between min and max

        Args:
            min (int): lower of the salary, in thousand, must gretter than 0
            max (int): upper of the salary, in thousand, must letter than 100

        Raises:
            Exception: raises when interval is not meet the criteria

        Returns:
            list[Job]: the jobs
        """

        if min < 0 or max < 0 or min < max or max > 100:
            raise Exception("不合法的薪资范围!")

        jobs = session.query(Job).filter(Job.salary_min >= min, Job.salary_min <= max).all()
        if jobs.__len__ == 0:
            return None
        return jobs

    def add(self, job: Job) -> bool:
        try:
            session.add(job, False)
            session.commit()
            print("{}:{}添加入库成功!".format(job.id, job.name))
            return True
        except:
            print("{}:{}添加入库失败!".format(job.id, job.name))
            return False
            
    def bulkAdd(self, jobs: list[Job]) -> None:
        for job in jobs:
            try:
                session.add(job, False)
                session.commit()
            except:
                continue