from csv import excel
import json
from random import randint
import requests
from time import sleep
from models.entities import Job
from services.JobServices import JobService
from .SpiderConfig import SpiderConfig, FiveOneConfig


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
            FiveOneConfig(2000)
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

        for config in self.__configs__:
            accessedPageAmount: int = 0
            while accessedPageAmount < pageAmountEachConfig:
                while True:
                    try:
                        url = config.randUrl()
                        break
                    except Exception as e:
                        if e.args[0] == "ERROR_NO_MORE_ITEM":
                            return jobs
                        continue
                    
                accessedPageAmount = accessedPageAmount + 1
                res = requests.get(url, headers=config.headers, cookies=config.cookies, timeout=2)

                if res.status_code == 200:
                    config.updateCookies(res.cookies)
                    try:
                        data = json.loads(res.text)
                        items = config.getRawJobsList(data)
                        config.updateMaxPage(config.__last_city__, data)
                        for item in items:
                            job = config.createRawJobInstance(item).toLocalJob()
                            if job:
                                jobService.add(job)
                                jobs.append(job)
                    except Exception as e:
                        if e.args[0] == "ERROR_INIT_TYPE":
                            print("\n转换{}时异常! 原因:{}\n".format(item, e.args))
                            continue
                        elif e.args[0] == "ERROR_DATA":
                            print("\n数据{}无效!\n".format(item))
                            continue
                        print("\n爬取{}时中断! 原因:{} 服务器回复:{}\n".format(config.__class__.__name__, e.args, res.text))
                        break

                timeout = randint(5, self.__frequency__)
                print("\n爬取{}的第{}个数据包成功!延迟{}s\n".format(config.__class__.__name__, accessedPageAmount, timeout))
                sleep(timeout)
        return jobs