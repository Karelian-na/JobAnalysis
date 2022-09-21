from typing import Type

from models.entities import Job, engine
from sqlalchemy.orm import sessionmaker, Query
from services.BaseService import BaseService
from sklearn.feature_extraction.text import TfidfVectorizer

maker = sessionmaker(engine)
session: maker = maker()


class JobService(BaseService):
    __categories__: dict[str, list[Job]]
    __jobs__: list[Job]

    def getById(self, ID: int) -> Job | None:
        """get a job from database

        Args:
            ID (int): the job id

        Returns:
            Job | None: if the database has the job, return the job object, otherwise, None
        """
        return session.query(Job).filter(Job.id == id).one_or_none()

    @staticmethod
    def get(amount: int, pageIdx: int):
        offset = (pageIdx - 1) * amount
        jobs = session.query(Job).offset(offset).limit(amount).all()
        return jobs

    @staticmethod
    def gedAllByName(name: str) -> list[Job] | None:
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

    @staticmethod
    def getAllBySalaryInterval(salaryMin: float, salaryMax: float, query: Query = None) -> list[Job]:
        """get all jobs which salary between salaryMin and salaryMax

        Args:
            salaryMin (int): lower of the salary, in a thousand, must gretter than 0
            salaryMax (int): upper of the salary, in a thousand, must letter than 100
            query (Query): the orm query object

        Raises:
            Exception: raises when interval is not meet the criteria

        Returns:
            list[Job]: the jobs
        """

        if salaryMin < 0 or salaryMin > salaryMax or salaryMax > 100:
            raise Exception("不合法的薪资范围!")

        if not query:
            query = session.query(Job)
        jobs = query.filter(Job.salary_min >= str(
            salaryMin), Job.salary_min <= str(salaryMax)).all()
        return jobs

    @staticmethod
    def add(job: Job) -> bool:
        try:
            session.add(job, False)
            session.commit()
            print("{}:{}添加入库成功!".format(job.id, job.name))
            return True
        except Exception:
            session.rollback()
            print("{}:{}添加入库失败!".format(job.id, job.name))
            return False

    @staticmethod
    def bulkAdd(jobs: list[Job]) -> None:
        for job in jobs:
            try:
                session.add(job, False)
                session.commit()
            except Exception:
                continue

    @staticmethod
    def getAllByArea(area: str):
        if area == "":
            jobs = session.query(Job)
        else:
            jobs = session.query(Job).filter(Job.work_area == area)
        return jobs

    @staticmethod
    def getAllAreas():
        areas = session.query(Job.work_area).group_by(Job.work_area).all()
        return areas

    def getAllIndustries(self, groupAmount):
        self.__jobs__ = self.getAll()
        types = [job.type for job in self.__jobs__]

        vectorizer = TfidfVectorizer(max_features=groupAmount)
        matrix = vectorizer.fit_transform(types).toarray().tolist()
        topJobNames: list[str] = vectorizer.get_feature_names_out().tolist()

        categories: dict[str, list[Job]] = dict()
        for name in topJobNames:
            categories.setdefault(name, [])

        for idx in range(0, len(matrix)):
            item = matrix[idx]
            for _idx in range(0, len(item)):
                if item[_idx] > 0.8:
                    categories.get(topJobNames[_idx]).append(
                        self.__jobs__[idx])
                    break

        self.__categories__ = categories
        return self.__categories__

    def getAllByIndustry(self, industryName):
        if industryName:
            return self.__categories__.get(industryName)
        return self.__jobs__

    @staticmethod
    def getTotalCount() -> int:
        return session.query(Job).count()

    def getByField(slef, search_field: str, search_content: str, pageIdx: int, pageSize: int):
        # select_sql = "SELECT * FROM jobs WHERE search_field LIKE '%{}%' LIMIT(pageIdx - 1) * pageSize, pageSize".format(
        #     search_content)
        offset = (pageIdx - 1) * pageSize
        # search_field和search_content都为空
        if not search_field and not search_content:
            jobs = session.query(Job).offset(offset).limit(pageSize).all()
            jobList = [job.toDict() for job in jobs]
            return jobList
        # search_field和search_content都不为空
        elif search_field and search_content:
            jobs = session.execute("SELECT * FROM jobs WHERE {} LIKE '%{}%' LIMIT {}, {}".format(
                search_field, search_content, (pageIdx - 1) * pageSize, pageSize)).all()
            jobList = [dict(job._mapping) for job in jobs]
            return jobList
        else:
            return False

    def getCountByField(self, search_field: str, search_content: str, pageIdx: int, pageSize: int):
        # search_field和search_content都为空
        if not search_field and not search_content:
            count = list(session.execute("SELECT COUNT(*) FROM jobs".format(
                search_field, search_content)))[0][0]
            return session.query(Job).count()

         # search_field和search_content都不为空
        elif search_field and search_content:
            count = list(session.execute("SELECT COUNT(*) FROM jobs WHERE {} LIKE '%{}%'".format(
                search_field, search_content)))[0][0]
            return count
        else:
            return False
