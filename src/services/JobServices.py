from src.models.entities import Job, engine
from sqlalchemy.orm import sessionmaker, Query
from src.services.BaseService import BaseService
from sklearn.feature_extraction.text import TfidfVectorizer

maker = sessionmaker(engine)
session: maker = maker()


class JobService(BaseService):
    __categories__: dict[str, list[Job]]
    __jobs__: list[Job]


    def getById(self, id: int) -> Job | None:
        """get a job from database

        Args:
            id (int): the job id

        Returns:
            Job | None: if the database has the job, return the job object, otherwise, None
        """
        return session.query(Job).filter(Job.id == id).one_or_none()


    def get(self, amount: int, pageIdx: int):
        offset = (pageIdx - 1) * amount
        jobs = session.query(Job).offset(offset).limit(amount).all()
        return jobs


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


    def getAllBySalaryInterval(self, min: float, max: float, query: Query = None) -> list[Job]:
        """get all jobs which salary between min and max

        Args:
            min (int): lower of the salary, in thousand, must gretter than 0
            max (int): upper of the salary, in thousand, must letter than 100

        Raises:
            Exception: raises when interval is not meet the criteria

        Returns:
            list[Job]: the jobs
        """

        if min < 0 or min > max or max > 100:
            raise Exception("不合法的薪资范围!")

        if not query:
            query = session.query(Job)
        jobs = query.filter(Job.salary_min >= str(min), Job.salary_min <= str(max)).all()
        return jobs


    def add(self, job: Job) -> bool:
        try:
            session.add(job, False)
            session.commit()
            print("{}:{}添加入库成功!".format(job.id, job.name))
            return True
        except:
            session.rollback()
            print("{}:{}添加入库失败!".format(job.id, job.name))
            return False


    def bulkAdd(self, jobs: list[Job]) -> None:
        for job in jobs:
            try:
                session.add(job, False)
                session.commit()
            except:
                continue


    def getAllByArea(self, area: str):
        if area == "":
            jobs = session.query(Job)
        else:
            jobs = session.query(Job).filter(Job.work_area == area)
        return jobs


    def getAllAreas(self):
        areas = session.query(Job.work_area).group_by(Job.work_area).all()
        return areas


    def getAllIndustries(self, groupAmount):
        self.__jobs__ = self.getAll()
        types = [ job.type for job in self.__jobs__]

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
                    categories.get(topJobNames[_idx]).append(self.__jobs__[idx])
                    break

        self.__categories__ = categories
        return self.__categories__


    def getAllByIndustry(self, industryName):
        if industryName:
            return  self.__categories__.get(industryName)
        return self.__jobs__


    def getTotalCount(self) -> int:
        return session.query(Job).count()