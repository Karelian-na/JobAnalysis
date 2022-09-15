import requests
from time import sleep
from random import randint
from src.models.entities import Job
from src.services.JobServices import JobService
from src.core.SpiderConfig import SpiderConfig, FiveOneConfig


class Spider:
    __frequency__: int
    __configs__: list[SpiderConfig]

    @property
    def configs(self):
        return self.__configs__

    @property
    def frequency(self):
        return self.__frequency__

    @frequency.setter
    def frequency(self, frequency: int):
        if self.__frequency__ != frequency and frequency >= 5:
            self.__frequency__ = frequency

    def __init__(self, spiderFrequency: int = 10, configs: list[SpiderConfig] = None) -> None:
        """init an instance by specified spider frequency and configs,
            if spiderFrequency is not specified, then it will be set a default value 10, 
            means the service will spidy the data every 10 second;
            if configs is not specified, then it will be set a default list only contains a _51Config,
            means it wiil spidy data from 51job.com

        Args:
            spiderFrequency (int): the spidy frequency 

        Args:
            configs (list[SpiderConfig]): the spidy condfigs/source

        Returns:
            list[RawJobType]: the acquired jobs
        """
        self.__frequency__ = 5 if spiderFrequency < 5 else spiderFrequency
        self.__configs__ = configs if configs else [
            FiveOneConfig("前程无忧")
        ]

    def addConfig(self, config: SpiderConfig) -> None:
        self.__configs__.append(config)

    def get(self, pageAmountEachConfig: int) -> list[Job]:
        jobService = JobService()
        """get rawJobs from configs with specified amount

        Args:
            pageAmountEachConfig (int): the job amount will be get in each config

        Returns:
            list[Job]: the acquired jobs
        """
        jobs: list[Job] = []
        job: Job

        eachConfigAccessedPageAmount = {config.name: 0 for config in self.__configs__}
        while len(self.__configs__) != 0:
            config = self.__configs__[randint(0, len(self.__configs__) - 1)]

            # 专门针对boos直聘, 搞死它:
            # if isinstance(config, BossConfig):
            #     with open("./src/cookie.json", encoding="utf-8", mode="r") as file:
            #         cookies = json.loads(file.read())
            #         config.cookies = cookies.get(config.__class__.__name__)

            if eachConfigAccessedPageAmount[config.name] > pageAmountEachConfig:
                self.__configs__.remove(config)
                continue

            url = ""
            while True:
                try:
                    url = config.randUrl()
                    break
                except Exception as e:
                    if e.args[0] == "ERROR_NO_MORE_ITEM":
                        return jobs
                    continue

            eachConfigAccessedPageAmount[config.name] = eachConfigAccessedPageAmount[config.name] + 1
            res = requests.get(url, headers=config.headers, cookies=config.cookies, timeout=2)

            if res.status_code != 200:
                print("\n请求{}的第{}个数据包失败!".format(config.name, eachConfigAccessedPageAmount[config.name]))
            else:
                config.updateCookies(res.cookies)
                try:
                    items = config.getRawJobsList(res.text)
                except Exception:
                    print("\n爬取{}的第{}个数据包失败! 服务器回复:{} ".format(config.name, eachConfigAccessedPageAmount[config.name], res.text))
                    self.__configs__.remove(config)
                    continue
                else:
                    print("\n爬取{}的第{}个数据包成功!".format(config.name, eachConfigAccessedPageAmount[config.name]))

                for item in items:
                    try:
                        job = config.createRawJobInstance(item).toLocalJob()
                        if job:
                            jobService.add(job)
                            jobs.append(job)
                    except Exception as e:
                        if e.args[0] == "ERROR_INIT_TYPE":
                            print("\n转换{}时异常! 原因:{} ".format(item, e.args))
                        elif e.args[0] == "ERROR_DATA":
                            print("\n数据{}无效! ".format(item))
                        else:
                            print("\n转换数据{}时出现未知错误! ".format(item))
            timeout = randint(5, self.__frequency__)
            print("\n延迟{}s\n".format(timeout))
            sleep(timeout)
        return jobs
