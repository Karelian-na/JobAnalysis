import re
from sklearn.feature_extraction.text import TfidfVectorizer
from .SpiderConfig import RawJobType
from models.entities import Job

class JobAnalysis:
    __jobs__: list[Job]
    __categories__: dict[str, list[Job]]

    @property
    def Categories(self):
        return self.__categories__

    @property
    def Jobs(self):
        return self.__jobs__

    @staticmethod
    def processRawJobs(rawJobs: list[RawJobType]) -> list[Job]:
        jobs: list[Job] = []
        for rawJob in rawJobs:
            job = Job()
            job.id = rawJob.id
            job.name = re.compile("((（|\(|\[).*(）|\]|\)))|((-|\+).*)|[\d]届?(.招)?").sub("", rawJob.name)
            
            # 处理薪水
            matches = re.compile("\d*-\d*K").match(rawJob)
            matches = re.compile("^(\d*(\.\d)?)(千?)-(\d*(\.\d)?)(千|万)(·(\d*)薪)?").match(rawJob.salary_text)
            if matches:
                if matches[3] == "":
                    rate = 1 if matches[6] == "千" else 10
                    job.salary_min = float(matches[1]) * rate
                    job.salary_max = float(matches[4]) * rate
                else:
                    job.salary_min = float(matches[1])
                    job.salary_max = float(matches[4]) * 10

                job.salary_sys = int(matches[8]) if matches[8] else 12
            else:
                matches = re.compile("(\d*)元/天").match(rawJob.salary_text)
                if matches:
                    daySal = int(matches[1])
                    job.salary_min = daySal * 0.022
                    job.salary_max = daySal * 0.03
                    job.salary_sys = 12
                else:
                    matches = re.compile("(\d*)千及以下").match(rawJob.salary_text)
                    if matches:
                        job.salary_min = float(matches[1])
                        job.salary_max = float(matches[1])
                        job.salary_sys = 12
                    else:
                        matches = re.compile("(\d*)-(\d*)万/年").match(rawJob.salary_text)
                        if matches:
                            job.salary_min = float(matches[1]) / 1.2
                            job.salary_max = float(matches[2]) / 1.2
                            job.salary_sys = 12

            job.work_area = rawJob.work_area
            job.experience = rawJob.experience
            job.degree = rawJob.degree
            job.company_name = rawJob.company_name
            job.type = rawJob.type

            jobs.append(job)
        return jobs

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
            result.setdefault(category, self.__categories__.get(category).__len__)

        return result

    @classmethod
    def statisticEducation(self) -> dict[str, dict[str, int]]:
        """statistic jobs' degree group under each category

        Returns: dict[str, dict[str, int]]: \n
                the result, str specified category name,\n
                dict[str, int] speicified degree array and amount in each item
        """
        result: dict[str, dict[str, int]] = dict()
        for category in self.__categories__:
            jobs = self.__categories__.get(category)
            groups: dict[str, int] = dict()
            for job in jobs:
                count = groups.get(job.degree)
                if count:
                    groups.update({ job.degree: count + 1 })
                else:
                    groups.setdefault(job.degree, 1)
            result.setdefault(category, groups)

        return result

    def statisticExperience(self) -> dict[str, dict[str, int]]:
        """statistic jobs' experience group under each category

        Returns: dict[str, dict[str, int]]: \n
                the result, str specified category name,\n
                dict[str, int] speicified experience array and amount in each item
        """
        result: dict[str, dict[str, int]] = dict()
        for category in self.__categories__:
            jobs = self.__categories__.get(category)
            groups: dict[str, int] = dict()
            for job in jobs:
                count = groups.get(job.experience)
                if count:
                    groups.update({ job.experience: count + 1 })
                else:
                    groups.setdefault(job.experience, 1)
            result.setdefault(category, groups)

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

            result.setdefault(category, "{:.1f}k-{:.1f}k".format(averageMinSalary, averageMaxSalary))

        return result

    def analysisRelation(self):
        pass