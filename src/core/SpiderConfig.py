from datetime import datetime
import json
from time import sleep
from requests.cookies import RequestsCookieJar
import re
from random import randint
from typing import Mapping
import requests

from models.entities import Job

RawValueType = dict[str, str | list[str]]

user_Agent = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
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

class ZhiTongType(RawJobType):
    def __init__(self, rawValue: RawValueType) -> None:
        super().__init__(rawValue)

        try:
            self.__id__ = "102" + str(self.__raw_value__["posId"])
            self.__name__ = self.__raw_value__["posName"]
            self.__work_area__ = self.__raw_value__["cityName"]

            experience = self.__raw_value__["reqWorkYearStr"]
            if experience == "经验不限":
                self.__experience__ = "无需经验"
            elif re.compile("应届毕业生|在读学生").match(experience):
                self.__experience__ = "在校生/应届生"
            elif re.compile("经验[12]年").match(experience):
                self.__experience__ = "1-3年经验"
            elif re.compile("经验[3-5]年").match(experience):
                self.__experience__ = "3-5年经验"
            elif re.compile("经验[5-9]年").match(experience):
                self.__experience__ = "5-10年经验"
            elif re.compile("经验10年.*").match(experience):
                self.__experience__ = "10年及以上经验"

            degree = self.__raw_value__["reqDegreeStr"]
            if degree == "不限":
                self.__degree__ = "学历不限"
            elif degree == "中专":
                self.__degree__ = "中技/中专"
            elif degree == "硕士及以上":
                self.__degree__ = "硕士"
            else:
                self.__degree__ = degree

            self.__company_name__ = self.__raw_value__["comName"]
            self.__type__ = self.__raw_value__["comIndustryStr"].split("/")[0]

            self.__salary_min__ = float(self.__raw_value__["maxSalary"]) * 0.001
            self.__salary_max__ = float(self.__raw_value__["minSalary"]) * 0.001
            self.__salary_sys__ = 12
        except Exception as e:
            raise Exception("ERROR_INIT_DATA", e.args)

class HookType(RawJobType):
    def __init__(self, rawValue: RawValueType) -> None:
        super().__init__(rawValue)

        try:
            self.__id__ = "lg" + str(self.__raw_value__["positionId"])
            self.__name__ = self.__raw_value__["positionName"]
            self.__work_area__ = self.__raw_value__["city"]

            experience = self.__raw_value__["workYear"]
            if experience == "不限":
                self.__experience__ = "无需经验"
            else:
                self.__experience__ = experience + "经验"

            degree = self.__raw_value__["education"]
            if degree == "不限":
                self.__degree__ = "学历不限"
            else:
                self.__degree__ = degree

            self.__company_name__ = self.__raw_value__["companyFullName"]
            self.__type__ = self.__raw_value__["industryField"].split(",")[0]

            matches = re.compile("(\d*)k-(\d*)k").match(self.__raw_value__["salary"])
            if matches:
                self.__salary_min__ = float(matches[1])
                self.__salary_max__ = float(matches[2])
                
            self.__salary_sys__ = int(self.__raw_value__["salaryMonth"]) if self.__raw_value__["salaryMonth"] else 12
        except Exception as e:
            raise Exception("ERROR_INIT_DATA", e.args)


class SpiderConfig:
    __name__: str
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
    __json_data__: dict[str, ]

    def getRawJobsList(self, text: str) -> list[RawJobType]: 
        """get all raw job list from the http response text
            this is a virtual function, sub class must implement it
        Args:
            text (str): the http response text

        Returns:
            list[RawJobType]: the list
        """
        ...

    @property
    def name(self) -> str:
        return self.__name__

    @property
    def cities(self) -> list[str] | None:
        return self.__cities__

    @property
    def lastAccessCity(self) -> list[str] | None:
        return self.__last_city__
    
    @property
    def headers(self) -> Mapping[str, str | bytes] | None:
        return self.__headers__

    @property
    def cookies(self):
        return self.__cookie__

    @cookies.setter
    def cookies(self, cookies: dict[str, ] | str):
        """parse to RequestsCookieJar from a string or a dict with a string key and any value

        Args:
            cookies (dict[str, ] | str): the value
        """
        if isinstance(cookies, str):
            items = cookies.replace(" ", "").split(";")
            for item in items:
                name, value = item.split("=", 1)
                self.__cookie__.set(name, value)

    def __init__(self, name: int) -> None:
        self.__name__ = name
        self.__text_except_data__ = None
        self.__cookie__ = RequestsCookieJar()
        self.__last_city__ = self.__cities__[0]
        self.__cities_pages_info__ = {}
        for city in self.__cities__:
            info = {}
            info.setdefault("unAccessedPages", list(range(1, 11)))
            info.setdefault("maxPage", 10)
            self.__cities_pages_info__.setdefault(city, info)

    def __update_request_msg__(self, randomCity: str, currentPageIdx: int) -> str:
        """update current config's request msg use the passed value randomCity, currentPageIdx
            like headers' referer, headers' userAgent, request url etc.
        Args:
            randomCity (str): current random city
            currentPageIdx (int): current random pageIdx

        Returns:
            str: the new random request url, new headers can be gotten by calling property headers
        Note:
            the implementer must update the request url to return it aside for method randUrl
        """
        self.__last_city__ = randomCity
        self.__headers__["User-Agent"] = user_Agent[randint(0, len(user_Agent) - 1)]
        
    def __update_max_page__(self, pageAmount: int) -> None:
        """update last city's max pageAmount

        Args:
            pageAmount (int): new pageAmount
        """
        if self.__cities_pages_info__[self.__last_city__]["maxPage"] != pageAmount:
            self.__cities_pages_info__[self.__last_city__]["maxPage"] = pageAmount
            self.__cities_pages_info__[self.__last_city__]["unAccessedPages"] = list(range(1, int(pageAmount) + 1))

    def randUrl(self) -> str:
        """generate a new random request url

        Raises:
            Exception: when all url have been used, it will raise an exception with ERROR_NO_MORE_ITEM

        Returns:
            str: the generated random url
        """
        while len(self.__cities_pages_info__) != 0:
            currentPageIdx: int
            randomCity = self.__cities__[randint(0, len(self.__cities__) - 1)]
            unAccessedPages = self.__cities_pages_info__[randomCity]["unAccessedPages"]
            while len(unAccessedPages) != 0:
                idx = randint(0, len(unAccessedPages) - 1)
                currentPageIdx = unAccessedPages[idx]
                unAccessedPages.pop(idx)
                return self.__update_request_msg__(randomCity, currentPageIdx)
            else:
                self.__cities_pages_info__.pop(randomCity)
                self.__cities__.pop(randomCity)
        else:
            raise Exception("ERROR_NO_MORE_ITEM", "No more Url to get!")
        
    def updateCookies(self, cookies: RequestsCookieJar):
        """update current sessions' cookies by the response cookies

        Args:
            cookies (RequestsCookieJar): the response cookie
        """
        for name, value in cookies.items():
            self.__cookie__.set(name, value)

    def getCookieString(self) -> str:
        """transfom the cookie to a string

        Returns:
            str: the result string like 'PHPSESSION=129r51fioqwgt0u1tg321ggq; ssid=12r12btfgq1g12g'
        """
        items = [name + "=" + value for name, value in self.__cookie__.items()]
        return ";".join(items)

    def createRawJobInstance(self, rawValue: RawValueType) -> RawJobType:
        """create an instance matched current config's RawJobType

        Args:
            rawValue (RawValueType): the rawValue from the request response's datalist

        Returns:
            RawJobType: the instance of the RawJobType
        """
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
    
    def __init__(self, name: int) -> None:
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
        super().__init__(name)

    def __update_request_msg__(self, randomCity: str, pageIdx: int): 
        super().__update_request_msg__(randomCity, pageIdx)
        self.__headers__["Referer"] = self.__referer__.format(randomCity, pageIdx)
        return self.__url__.format(randomCity, pageIdx)
    
    def getRawJobsList(self, text: str) -> list[RawJobType]:
        try:
            data = json.loads(text)
            self.__json_data__ = data
            self.__update_max_page__(data["total_page"])
            return data["engine_jds"]
        except:
            raise Exception("ERROR_GET_DATA_LIST")

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
        'token': 'cGbsHkNO1v2lUY23',
        'traceid': '72C6F6CA-566C-42A6-8EE0-2705570620BE',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'zp_token': 'V1RN4vGeD00ltiVtRvyR4YKi606TLRxyo~',
    }
    __type__ = BossType
    __referer__ = 'https://www.zhipin.com/web/geek/job?query=&city={}&page={}'

    def __init__(self, name: int) -> None:
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
        super().__init__(name)

    def __update_request_msg__(self, randomCity: str, pageIdx: int) -> None:
        super().__update_request_msg__(randomCity, pageIdx)
        self.__headers__["Referer"] = self.__referer__.format(randomCity, pageIdx)
        return self.__url__.format(randomCity, pageIdx)
    
    def updateCookies(self, cookies: RequestsCookieJar):
        """update current sessions' cookies by the response cookies

        Args:
            cookies (RequestsCookieJar): the response cookie
        """
        seed = cookies.get("__zp_sseed__")
        s = cookies.get("__zp_sname__")
        timestamp = cookies.get("__zp_sts__")
        res = requests.get("http://127.0.0.1:5000/getBossNewCookie/seed={}&timestamp={}".format(seed, timestamp))
        while True:
            with open("./src/newCookie.txt", encoding="utf-8") as file:
                cookieValue = file.readline()
                if cookieValue:
                    self.__cookie__.set("__zp_stoken__", cookieValue)
                    break
                sleep(0.5)

    def getRawJobsList(self, text: str) -> list[RawJobType]:
        try:
            data = json.loads(text)
            self.__json_data__ = data
            self.__update_max_page__(int(int(data["zpData"]["totalCount"]) / self.__page_size__))
            return data["zpData"]["jobList"]
        except:
            raise Exception("ERROR_GET_DATA_LIST")

class ZhiTongConfig(SpiderConfig):
    __method__ = "GET"
    __page_size__ = 10
    __url__ = "https://www.job5156.com/s/result?t={}&keyword=&keywordType=0&posTypeList=&locationList={}&taoLabelList=免费培训&degreeFrom=&propertyList=&industryList=&sortBy=0&urgentFlag=&comIdList=&locationAddrStr=&maxSalary=&salary=&workyearFrom=&workyearTo=&degreeTo&pn={}"
    __headers__ = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'AppType': 'pc',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.job5156.com',
        'isAsync': 'true',
        'posTypeNewFlag': 'true',
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
    __type__ = ZhiTongType
    __referer__ = 'https://www.job5156.com/s/result/kt0_wl14090000/?keywordFromSource=&recommendFromKeyword=&keywordType=0&keyword=&locationList={}'

    def __init__(self, name: int) -> None:
        self.__cities__ = [
            '14010000',
            '14010100',
            '14010200',
            '14010300',
            '14010400',
            '14013300',
            '14010500',

            '14080000',
            '14080100',
            '14080200',

            '14090000',

            '14040000',
            '14020000',
            '14030000',
            '14070000',
            '28070000',
            '28010000',
        ]
        super().__init__(name)

    def __update_request_msg__(self, randomCity: str, pageIdx: int) -> None:
        super().__update_request_msg__(randomCity, pageIdx)
        self.__headers__["Referer"] = self.__referer__.format(randomCity)
        return self.__url__.format(str(datetime.now().timestamp()).replace(".", "")[:13], randomCity, pageIdx)
    
    def getRawJobsList(self, text: str) -> list[RawJobType]:
        try:
            data = json.loads(text)
            self.__json_data__ = data
            self.__update_max_page__(int(data["posData"]["pageCount"]))
            return data["posData"]["posItems"]
        except:
            raise Exception("ERROR_GET_DATA_LIST")

class HookConfig(SpiderConfig):
    __method__ = "GET"
    __page_size__ = 15
    __url__ = "https://www.lagou.com/wn/jobs?pn={}&fromSearch=true&city={}"
    __headers__ = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.lagou.com',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    __type__ = HookType

    def __init__(self, name: int) -> None:
        self.__cities__ = [
            '北京',
            '上海',
            '深圳',
            '广州',
            '杭州',
            '成都',
            '南京',
            '武汉',
            '西安',
            '厦门',
            '长沙',
            '苏州',
            '天津',
        ]
        super().__init__(name)

    def __update_request_msg__(self, randomCity: str, pageIdx: int) -> None:
        super().__update_request_msg__(randomCity, pageIdx)
        return self.__url__.format(pageIdx, randomCity)

    def getRawJobsList(self, text: str) -> list[RawJobType]:
        try:
            matches = re.compile('.*<script id="__NEXT_DATA__".*?type="application\/json">(.*?)<\/script>').match(text)
            if matches:
                data = json.loads(matches[1])
            else:
                data = json.loads(text)
            self.__json_data__ = data
            self.__update_max_page__(int(int(data["props"]["pageProps"]["initData"]["content"]["positionResult"]["totalCount"]) / self.__page_size__))
            return data["props"]["pageProps"]["initData"]["content"]["positionResult"]["result"]
        except:
            raise Exception("ERROR_GET_DATA_LIST")