from copy import copy
from src.models.entities import Job
from sklearn.feature_extraction.text import TfidfVectorizer

class JobAnalysis:
    __jobs__: list[Job]
    __categories__: dict[str, list[Job]]


    @property
    def Categories(self):
        return self.__categories__


    @property
    def Jobs(self):
        return self.__jobs__


    @classmethod
    def group(self, jobs: list[Job], groupAmount: int) -> None:
        """Categorize the jobs by job'name 

        Args:
            jobs (list[Job]): the jobs will be categorized

        Raises:
            Exception: raises when jobs is not an instance of type list[Job]!
        """
        if not isinstance(jobs, list):
            raise Exception("Type Error! jobs is not an instance of type list[Job]!")
        self.__jobs__ = jobs
        
        names = [ job.name for job in jobs]

        vectorizer = TfidfVectorizer(max_features=groupAmount)
        matrix = vectorizer.fit_transform(names).toarray().tolist()
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

        self.__categories__ = categories


    @classmethod
    def statistic(self) -> dict[str, int]:
        """statistic jobs' amount under each category

        Returns:
            dict[str, int]: the result, str specified category name, int specified its jobs' amount
        """
        result: dict[str, int] = dict()
        for category in self.__categories__:
            result.setdefault(category, len(self.__categories__.get(category)))

        return result


    @classmethod
    def statisticDegree(self, isCategory: bool) -> dict[str, dict[str, int]] | dict[str, int]:
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
        result: dict[str, dict[str, int]] | dict[str, int]
        if isCategory:
            result = { category: copy(degrees) for category in self.__categories__ }
            for category in result:
                jobs = self.__categories__.get(category)
                groups = result.get(category)
                for job in jobs:
                    count = groups.get(job.degree)
                    groups.update({ job.degree: count + 1 })
        else:
            result = degrees
            for job in self.__jobs__:
                count = result.get(job.degree)
                result.update({ job.degree: count + 1 })

        return result


    def statisticExperience(self, isCategory: bool) -> dict[str, dict[str, int]] | dict[str, int]:
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
            "10年及以上经验": 0,
        }
        result: dict[str, dict[str, int]] | dict[str, int]
        if isCategory:
            result = { category: copy(experiences) for category in self.__categories__ }
            for category in result:
                jobs = self.__categories__.get(category)
                groups = result.get(category)
                for job in jobs:
                    count = groups.get(job.experience)
                    groups.update({ job.experience: count + 1 })
        else:
            result = experiences
            for job in self.__jobs__:
                count = result.get(job.experience)
                result.update({ job.experience: count + 1 })
        return result


    def statisticSalary(self) -> dict[str, str]:
        """statistic jobs' salary interval under each category

        Returns:
            dict[str, str]: str specified category name, str specified interval like "6.5k-8.5k"
        """
        result: dict[str, str] = dict()
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


    def analysisRelation(self):
        pass