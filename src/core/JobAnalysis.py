import re
from copy import copy
from models.entities import Job
from sklearn.feature_extraction.text import TfidfVectorizer


class JobAnalysis:
    __jobs__: list[Job] = None
    __categories__: dict[str, list[Job]] = None
    __categoried_jobs__: list[Job] = None

    @property
    def Categories(self):
        return self.__categories__

    @property
    def Jobs(self):
        return self.__jobs__

    @classmethod
    def group(cls, jobs: list[Job], groupAmount: int) -> None:
        """Categorize the jobs by job'name 

        Args:
            jobs (list[Job]): the jobs will be categorized

        Args:
            groupAmount (int): the group amount

        Raises:
            Exception: raises when jobs are not an instance of type list[Job]!
        """
        if not isinstance(jobs, list):
            raise Exception(
                "Type Error! jobs is not an instance of type list[Job]!")
        cls.__jobs__ = jobs

        names = [job.name or "" for job in jobs]

        vectorizer: TfidfVectorizer = TfidfVectorizer(max_features=groupAmount)
        matrix: list[list[float]] = vectorizer.fit_transform(
            names).toarray().tolist()
        topJobNames: list[str] = vectorizer.get_feature_names_out().tolist()

        categories: dict[str, list[Job]] = dict()
        for name in topJobNames:
            categories.setdefault(name, [])

        for idx in range(0, len(matrix)):
            item = matrix[idx]
            for _idx in range(0, len(item)):
                if item[_idx] > 0.8:
                    categories.get(topJobNames[_idx]).append(jobs[idx])
                    break

        cls.__categories__ = {}
        cls.__categoried_jobs__ = []
        for category in categories:
            if not re.compile(".*(吃住|薪|休|五险一金)").match(category) and len(categories.get(category)) != 0:
                cls.__categories__.setdefault(
                    category, categories.get(category))
                cls.__categoried_jobs__.extend(categories.get(category))

    @classmethod
    def statistic(cls) -> dict[str, int]:
        """statistic jobs' amount under each category

        Returns:
            dict[str, int]: the result, str specified category name, int specified its jobs' amount
        """
        result: dict[str, int] = dict()
        for category in cls.__categories__:
            result.setdefault(category, len(cls.__categories__.get(category)))

        return result

    @classmethod
    def statisticDegree(cls, isCategory: bool | str) -> dict[str, dict[str, int]] | dict[str, int]:
        """statistic jobs' degree group under each category

        Args:
            isCategory (bool): specified wherther statistic category

        Returns: dict[str, dict[str, int]] | dict[str, int]: \n
                if isCategory equals true, returns type of dict[str, int]: str specified category/name, int specified amount\n
                otherwise returns type of dict[str, dict[str, int]]: str specified category/name, dict[str, int] specified each amount of degree\n
        """
        degrees = {
            "学历不限": 0,
            "初中及以下": 0,
            "中技/中专": 0,
            "高中": 0,
            "大专": 0,
            "本科": 0,
            "硕士": 0,
            "博士": 0,
        }
        result: dict[str, int | dict[str, int]] | dict[str, int]
        if isinstance(isCategory, str) or not isCategory:
            result = degrees

            jobs = cls.__categories__.get(
                isCategory) if isCategory else cls.__categoried_jobs__
            for job in jobs:
                count = result.get(job.degree)
                result.update({job.degree: count + 1})
        else:
            result = {category: copy(degrees)
                      for category in cls.__categories__}
            for category in result:
                jobs = cls.__categories__.get(category)
                groups = result.get(category)
                for job in jobs:
                    count = groups.get(job.degree)
                    groups.update({job.degree: count + 1})

        return result

    def statisticExperience(self, isCategory: bool | str) -> dict[str, dict[str, int]] | dict[str, int]:
        """statistic jobs' experience group under each category

        Args:
            isCategory (bool): specified wherther statistic category

        Returns: dict[str, dict[str, int]] | dict[str, int]: \n
                if isCategory equals true, returns type of dict[str, int]: str specified category/name, int specified amount\n
                otherwise returns type of dict[str, dict[str, int]]: str specified category/name, dict[str, int] specified each amount of experience\n
        """
        experiences = {
            "无需经验": 0,
            "在校生/应届生": 0,
            "1年以内经验": 0,
            "1-3年经验": 0,
            "3-5年经验": 0,
            "5-10年经验": 0,
            "10年以上经验": 0,
        }
        result: dict[str, dict[str, int]] | dict[str, int]
        if isinstance(isCategory, str) or not isCategory:
            result = experiences

            jobs = self.__categories__.get(
                isCategory) if isCategory else self.__categoried_jobs__
            for job in jobs:
                count = int(result.get(job.experience))
                result.update({job.experience: count + 1})
        else:
            result = {category: copy(experiences)
                      for category in self.__categories__}
            for category in result:
                jobs = self.__categories__.get(category)
                groups = result.get(category)
                for job in jobs:
                    count = groups.get(job.experience)
                    groups.update({job.experience: count + 1})
        return result

    def statisticSalaryAverage(self) -> dict[str, dict[str, float]]:
        """statistic jobs' salary interval under each category

        Returns:
            dict[str, str]: str specified category name, str specified interval like "6.5k-8.5k"
        """
        result: dict[str, dict[str, float]] = dict()
        for category in self.__categories__:
            jobs = self.__categories__.get(category)
            averageMinSalary: int = 0
            averageMaxSalary: int = 0

            for job in jobs:
                averageMinSalary += job.salary_min
                averageMaxSalary += job.salary_max
            averageMinSalary /= len(jobs)
            averageMaxSalary /= len(jobs)

            result.setdefault(category, {
                "min": averageMinSalary.__round__(1),
                "mid": ((averageMinSalary + averageMaxSalary) / 2).__round__(1),
                "max": averageMaxSalary.__round__(1),
            })

        return result

    def statisticSalaryInterval(self, categoryName: str, salaryMin: float, salaryMax: float, groupAmount: int = None) -> dict[str, int]:
        delta = salaryMax - salaryMin
        if salaryMax < 0 or delta < 0:
            raise Exception("分段错误!")

        groupAmount = groupAmount or 5
        stepLength = (delta / groupAmount).__round__(1)

        interval = [salaryMin + (stepLength * idx).__round__(1)
                    for idx in range(0, groupAmount)]
        interval.append(salaryMax)

        result: dict[str, int] = {}
        for idx in range(0, len(interval) - 2):
            result.setdefault(
                "{}k-{}k".format(interval[idx], interval[idx + 1]), 0)
        result.setdefault(
            "{}k-{}k".format(interval[groupAmount - 1], salaryMax), 0)

        jobs = self.__categories__.get(
            categoryName) if categoryName else self.__categoried_jobs__
        for job in jobs:
            ave = ((job.salary_min + job.salary_max) / 2).__round__(1)
            if ave < salaryMin or ave > salaryMax:
                continue

            for idx in range(0, len(interval) - 1):
                if ave < interval[idx + 1]:
                    key = list(result.keys())[idx]
                    result.update({key: result[key] + 1})
                    break

        return result

    def analysisRelation(self):
        pass
