from requests.cookies import RequestsCookieJar
import re
from random import randint
from typing import Mapping

from models.entities import Job

RawValueType = dict[str, str | list[str]]

user_Agent = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
]

class RawJobType:
    __raw_value__: RawValueType
    __id__: str
    __name__: str
    __salary_min__: float
    __salary_max__: float
    __salary_sys__: float
    __work_area__: str
    __experience__: str
    __degree__: str
    __company_name__: str
    __type__: str

    @property
    def id(self) -> str: 
        return self.__id__

    @property
    def name(self) -> str:
        return self.__name__

    @property
    def salary_min(self) -> float:
        return self.__salary_min__

    @property
    def salary_max(self) -> float: 
        return self.__salary_max__

    @property
    def salary_sys(self) -> int: 
        return self.__salary_sys__

    @property
    def work_area(self) -> str: 
        return self.__work_area__

    @property
    def experience(self) -> str:
        return self.__experience__

    @property
    def degree(self) -> str: 
        return self.__degree__

    @property
    def company_name(self) -> str: 
        return self.__company_name__

    @property
    def type(self) -> str: 
        return self.__type__

    def __init__(self, rawValue: RawValueType) -> None:
        self.__raw_value__ = rawValue

    def toLocalJob(self) -> Job:
        job = Job()
        try:
            job.id = self.id
            job.name = self.name
            job.company_name = self.company_name
            job.salary_min = self.salary_min
            job.salary_max = self.salary_max
            job.salary_sys = self.salary_sys
            job.work_area = self.work_area
            job.experience = self.experience
            job.degree = self.degree
            job.company_name = self.company_name
            job.type = self.type
        except :
            return None
        return job

class FiveOneType(RawJobType):
    def __init__(self, rawValue: RawValueType) -> None:
        super().__init__(rawValue)
        
        try:
            self.__id__ = "51" + self.__raw_value__["jobid"]
            self.__name__ = re.compile("(((（|\(|\[).*(）|\]|\)))|((-|\+).*)|[\d]届?(.招)?)$").sub("", self.__raw_value__["job_name"])
            self.__work_area__ = re.compile("(-.*)").sub("", self.__raw_value__["workarea_text"])
            self.__degree__ = self.__raw_value__["attribute_text"][2] if len(self.__raw_value__["attribute_text"]) == 3 else "学历不限"
            self.__company_name__ = self.__raw_value__["company_name"]
            self.__type__ = self.__raw_value__["companyind_text"].split("/")[0]


            # 工作经验
            if len(self.__raw_value__["attribute_text"]) >= 2:
                experience = self.__raw_value__["attribute_text"][1]
                if re.compile("[12]年经验").match(experience):
                    self.__experience__ = "1-3年经验"
                elif re.compile("3-4年经验").match(experience):
                    self.__experience__ = "3-5年经验"
                elif re.compile("([5-9])-([6-9])年经验").match(experience):
                    self.__experience__ = "5-10年经验"
                else:
                    self.__experience__ = experience
            else:
                self.__experience__ = "无需经验"

            # 工资
            salary = self.__raw_value__["providesalary_text"]
            if not salary:
                raise Exception("ERROR_DATA")
            matches = re.compile("^(\d*(\.\d)?)(千?)-(\d*(\.\d)?)(千|万)(·(\d*)薪)?").match(salary)
            if matches:
                if matches[3] == "":
                    rate = 1 if matches[6] == "千" else 10
                    self.__salary_min__ = float(matches[1]) * rate
                    self.__salary_max__ = float(matches[4]) * rate
                else:
                    self.__salary_min__ = float(matches[1])
                    self.__salary_max__ = float(matches[4]) * 10

                self.__salary_sys__ = int(matches[8]) if matches[8] else 12
                return

            matches = re.compile("(\d*)元/天").match(salary)
            if matches:
                daySal = int(matches[1])
                self.__salary_min__ = daySal * 0.022
                self.__salary_max__ = daySal * 0.03
                self.__salary_sys__ = 12
                return

            matches = re.compile("(\d*)千及以下").match(salary)
            if matches:
                self.__salary_min__ = float(matches[1])
                self.__salary_max__ = float(matches[1])
                self.__salary_sys__ = 12
                return

            matches = re.compile("(\d*)-(\d*)万/年").match(salary)
            if matches:
                self.__salary_min__ = float(matches[1]) / 1.2
                self.__salary_max__ = float(matches[2]) / 1.2
                self.__salary_sys__ = 12
        except Exception as e:
            if e.args[0] == "ERROR_DATA":
                raise e
            raise Exception("ERROR_INIT_TYPE", e.args)

class BossType(RawJobType):
    def __init__(self, rawValue: RawValueType) -> None:
        super().__init__(rawValue)

        try:
            self.__id__ = self.__raw_value__["encryptJobId"]
            self.__name__ = re.compile("(((（|\(|\[).*(）|\]|\)))|((-|\+).*)|[\d]届?(.招)?)$").sub("", self.__raw_value__["jobName"])
            self.__work_area__ = self.__raw_value__["cityName"]
            self.__company_name__ = self.__raw_value__["brandName"]
            self.__type__ = self.__raw_value__["brandIndustry"].split("/")[0]

            experience = self.__raw_value__["jobExperience"]
            if experience == "经验不限":
                self.__experience__ = "无需经验"
            elif re.compile("在校生|应届生|在校\/应届").match(experience):
                self.__experience__ = "在校生/应届生"
            else:
                self.__experience__ = self.__raw_value__["jobExperience"] + "经验" if self.__raw_value__["jobExperience"] else "无需经验"

            if self.__raw_value__["jobDegree"] == "中专/中技":
                self.__degree__ = "中技/中专"
            else:
                self.__degree__ = self.__raw_value__["jobDegree"] or "无需学历"
            salary = self.__raw_value__["salaryDesc"]
            matches = re.compile("(\d*)-(\d*)K(·(\d*)薪)?").match(salary)
            if matches:
                self.__salary_min__ = float(matches[1])
                self.__salary_max__ = float(matches[2])
                self.__salary_sys__ = int(matches[4]) if matches[4] else 12
                return

            matches = re.compile("(\d*)-(\d*)元/月").match(salary)
            if matches:
                self.__salary_min__ = int(matches[1]) * 0.001
                self.__salary_max__ = int(matches[2]) * 0.001
                self.__salary_sys__ = 12
                return
            
            matches = re.compile("(\d*)-(\d*)元/天").match(salary)
            if matches:
                daySal = int(matches[1])
                self.__salary_min__ = daySal * 0.022
                self.__salary_max__ = daySal * 0.03
                self.__salary_sys__ = 12
                return

        except Exception as e:
            raise Exception("ERROR_INIT_TYPE", e.args)




class SpiderConfig:
    __url__: str
    __method__: str
    __cookie__: RequestsCookieJar
    __referer__: str
    __headers__: Mapping[str, str | bytes] | None

    __type__: type[RawJobType]

    __cities__: list[str]
    __last_city__: str
    __cities_pages_info__: dict[str, dict[str, int | list[int]]]

    __page_size__: int
    

    def getRawJobsList(self, data: dict[str, ]) -> list[RawJobType]: ...
    
    @property
    def headers(self) -> Mapping[str, str | bytes] | None:
        return self.__headers__

    @property
    def cookies(self):
        return self.__cookie__

    @cookies.setter
    def cookies(self, cookies: dict[str, ] | str):
        if isinstance(cookies, str):
            items = cookies.replace(" ", "").split(";")
            for item in items:
                name, value = item.split("=", 1)
                self.__cookie__.set(name, value)

    def __init__(self, initMaxPage: int) -> None:
        self.__cookie__ = RequestsCookieJar()
        self.__last_city__ = self.__cities__[0]
        self.__cities_pages_info__ = {}
        for city in self.__cities__:
            info = {}
            info.setdefault("unAccessedPages", list(range(1, initMaxPage + 1)))
            info.setdefault("initMaxPage", initMaxPage)
            info.setdefault("maxPage", initMaxPage)
            self.__cities_pages_info__.setdefault(city, info)

    def __update_headers__(self) -> None:
        self.__headers__["User-Agent"] = user_Agent[randint(1, len(user_Agent) + 1)]
        pass

    def randUrl(self) -> str:
        while len(self.__cities_pages_info__) != 0:
            currentPageIdx: int
            randomCity = self.__cities__[randint(1, len(self.__cities__))]
            unAccessedPages = self.__cities_pages_info__[randomCity]["unAccessedPages"]
            while len(unAccessedPages) != 0:
                idx = randint(1, len(unAccessedPages))
                currentPageIdx = unAccessedPages[idx]
                unAccessedPages.pop(idx)
                self.__last_city__ = randomCity
                self.__update_headers__(randomCity, currentPageIdx)
                return self.__url__.format(randomCity, currentPageIdx)
            else:
                self.__cities_pages_info__.pop(randomCity)
                self.__cities__.pop(randomCity)
        else:
            raise Exception("ERROR_NO_MORE_ITEM", "No more Url to get!")
        
    def updateCookies(self, cookies: RequestsCookieJar):
        for name, value in cookies.items():
            self.__cookie__.set(name, value)

    def getCookieString(self) -> str:
        items = [name + "=" + value for name, value in self.__cookie__.items()]
        return ";".join(items)

    def updateMaxPage(self, city: str, pageAmount: int) -> None:
        if self.__cities_pages_info__[city]["initMaxPage"] != pageAmount:
            self.__cities_pages_info__[city]["maxPage"] = pageAmount
            self.__cities_pages_info__[city]["unAccessedPages"] = list(range(1, pageAmount + 1))

    def createRawJobInstance(self, rawValue: RawValueType) -> RawJobType:
        return self.__type__(rawValue)

class FiveOneConfig(SpiderConfig):
    __method__ = "GET"
    __page_size__ = 50
    __url__ = "https://search.51job.com/list/{},000000,0000,00,9,99,+,2,{}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
    __headers__ =  {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'search.51job.com',
        'Pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    __type__ = FiveOneType
    __referer__ = __url__
    
    def __init__(self, initMaxPage: int) -> None:
        self.__cities__ = [
            '010000',
            '020000',
            '030200',
            '040000',
            '180200',
            '200200',
            '080200',
            '070200',
            '090200',
            '060000',
            '030800',
            '230300',
            '230200',
            '070300',
            '250200',
            '190200',
            '150200',
            '080300',
            '170200',
            '050000',
            '120300',
            '120200',
            '220200',
            '240200',
            '110200'
        ]
        super().__init__(initMaxPage)

    def __update_headers__(self, randomCity: str, pageIdx: int): 
        super().__update_headers__()
        self.__headers__["Referer"] = self.__referer__.format(randomCity, pageIdx)

    def updateMaxPage(self, city: str, data: dict[str, ]) -> None:
        super().updateMaxPage(city, int(data["total_page"]))

    def getRawJobsList(self, data: dict[str, ]) -> list[RawJobType]:
        return data["engine_jds"]


class BossConfig(SpiderConfig):
    __method__ = "GET"
    __page_size__ = 30
    __url__ = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=&city={}&experience=&degree=&industry=&scale=&stage=&position=&salary=&multiBusinessDistrict=&page={}&pageSize=30"
    __headers__ = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    __type__ = BossType
    __referer__ = 'https://www.zhipin.com/web/geek/job?city={}&page={}'

    def __init__(self, initMaxPage: int) -> None:
        self.__cities__ = [
            "100010000",
            "101010100",
            "101020100",
            "101280100",
            "101280600",
            "101210100",
            "101030100",
            "101110100",
            "101190400",
            "101200100",
            "101230200",
            "101250100",
            "101270100",
            "101180100",
            "101040100",
        ]
        super().__init__(initMaxPage)

    def __update_headers__(self, randomCity: str, pageIdx: int) -> None:
        super().__update_headers__()
        self.__headers__["Referer"] = self.__referer__.format(randomCity, pageIdx)

    def updateMaxPage(self, city: str, data: dict[str, ]) -> None:
        super().updateMaxPage(city, int(int(data["zpData"]["totalCount"]) / self.__page_size__))


    def getRawJobsList(self, data: dict[str, ]) -> list[RawJobType]:
        return data["zpData"]["jobList"]
