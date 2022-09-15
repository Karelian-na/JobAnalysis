import json
from flask import Flask, render_template, request
from core.JobAnalysis import JobAnalysis
from services.JobServices import JobService
from core.Spider import Spider
from core.SpiderConfig import FiveOneConfig, BossConfig, ZhiTongConfig, HookConfig
from src.models.entities import Job
from selenium import webdriver

app = Flask(__name__)
jobService = JobService()
jobAnalysis = JobAnalysis()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/welcome")
def welcome():
    content = "hello World!"
    return render_template("welcome.html", **{"content": content})


@app.route("/analysis/<mode>", methods=["GET", "POST"])
def analysis(mode):
    if request.method == "GET":
        if mode == "total":
            categories = list(map(lambda area: area.work_area, jobService.getAllAreas()))
            filterTitle = "地区"
        elif mode == "industry":
            categories = jobService.getAllIndustries(10)
            filterTitle = "行业"
        elif mode == "professional":
            jobAnalysis.group(jobService.getAll(), 10)
            categories = jobAnalysis.__categories__
            return render_template("professionalAnalysis.html", **{
                "categories": categories,
            })
        else:
            return render_template("404.html", **{
                "msg": "您所访问的页面不存在!"
            })

        return render_template("analysis.html", **{
            "filterTitle": filterTitle,
            "categories": categories,
            "filter": mode,
        })
    elif request.method == "POST":
        filterValue = request.form.get("filterValue") if request.form.get("filterValue") else ""
        groupAmount = int(request.form.get("groupAmount")) if request.form.get("groupAmount") else 10
        minSalary = float(request.form.get("minSalary")) if request.form.get("minSalary") else 1.0
        maxSalary = float(request.form.get("maxSalary")) if request.form.get("maxSalary") else 100.0

        data: dict[str, dict[str, float] | dict[str, dict[str, float]]] = {}

        allJobs: list[Job] = []
        if mode == "total":
            query = jobService.getAllByArea(filterValue)
            allJobs = jobService.getAllBySalaryInterval(minSalary, maxSalary, query)
        elif mode == "industry":
            allJobs = jobService.getAllByIndustry(filterValue)
        elif mode == "professional":
            maxSalary = 20 if maxSalary == 100 else maxSalary
            data.setdefault("salaryIntervalProportion", jobAnalysis.statisticSalaryInterval(filterValue, minSalary, maxSalary, groupAmount))
            data.setdefault("degreeProportion", jobAnalysis.statisticDegree(filterValue))
            data.setdefault("experienceProportion", jobAnalysis.statisticExperience(filterValue))
            jsonValue = json.dumps(data)
            return jsonValue

        jobAnalysis.group(allJobs, groupAmount)

        data.setdefault("groupProportion", jobAnalysis.statistic())
        data.setdefault("salaryProportion", jobAnalysis.statisticSalaryAverage())
        data.setdefault("degreeProportion", jobAnalysis.statisticDegree(False))
        data.setdefault("categoryDegreeProportion", jobAnalysis.statisticDegree(True))
        data.setdefault("experienceProportion", jobAnalysis.statisticExperience(False))
        data.setdefault("categoryExperienceProportion", jobAnalysis.statisticExperience(True))

        jsonValue = json.dumps(data)
        return jsonValue
    else:
        return render_template("404.html", **{
            "msg": "您所请求方式错误!"
        })


@app.route("/jobs", methods=["GET", "POST"])
def jobLists():
    if request.method == "GET":
        return render_template("jobs.html")
    elif request.method == "POST":
        pageIdx = int(request.form.get("pageIdx"))
        pageSize = int(request.form.get("pageSize"))

        jobs = jobService.get(pageSize, pageIdx)
        count = jobService.getTotalCount()
        jobList = [ job.toDict() for job in jobs ]
        return json.dumps({
            "code": 0,
            "count": count,
            "data": jobList
        })
    else:
        return render_template("404.html", **{
            "msg": "您所请求方式错误!"
        })


@app.route("/spidy", methods=["GET", "POST"])
def spidy():
    amount = int(request.args.get("pageAmount")) if request.args.get("pageAmount") else None
    if not amount or amount < 1:
        amount = 1
    elif amount > 100:
        amount = 100

    cookies: dict[str, str]
    with open("./src/cookie.json", encoding="utf-8", mode="r") as file:
        cookies = json.loads(file.read())

    fiveOneConfig = FiveOneConfig("前程无忧")
    fiveOneConfig.cookies = cookies.get(fiveOneConfig.__class__.__name__)

    hookConfig = HookConfig("拉钩招聘")
    hookConfig.cookies = cookies.get(hookConfig.__class__.__name__)

    # bossConfig = BossConfig("Boss直聘")
    # bossConfig.cookies = cookies.get(bossConfig.__class__.__name__)

    zhiTongConfig = ZhiTongConfig("智通人才网")
    zhiTongConfig.cookies = cookies.get(zhiTongConfig.__class__.__name__)

    spilder = Spider(20, configs=[fiveOneConfig, hookConfig, zhiTongConfig])
    spilder.get(amount)

    for config in spilder.configs:
        cookies.setdefault(config.__class__.__name__, config.getCookieString())

    with open("./src/cookie.json", encoding="utf-8", mode="w+") as file:
        file.write(json.dumps(cookies))
    
    # try:
    #     driverer = webdriver.Edge()
    #     # driverer.get("http://127.0.0.1:5000/getBossNewCookie?seed={}&timestamp={}".format(seed, timestamp))
    #     driverer.get("http://127.0.0.1:5000/getBossNewCookie?seed=f9a3eaXo1PjlvITEvNWwZIlI8MSVvMSg4X1hHXgw4EHRcUng8Jz1hTCxuUixiDA48Fx8JB2xCfi07SkUAeHI/VBpgTAgEfwpKXxgbT0EFMxwueE0SNEBINwBFdw8YCHt3VSY7Dj9EXVVyeTk=&timestamp=1663238962260")
    # except Exception:
    #     return "fail"
    return "success"


@app.route("/getBossNewCookie/", methods=["GET"])
def getBossNewCookie():
    seed = request.args.get("seed")
    timestamp = request.args.get("timestamp")
    return render_template("bossCookie.html", **{
        "seed": seed,
        "timeStamp": timestamp})


@app.route("/setBossNewCookie/", methods=["GET"])
def setBossNewCookie():
    newValue = request.args.get("value")
    with open("./src/newCookie.txt", encoding="utf-8", mode="w+") as file:
        file.write(newValue)
    return ""


if __name__ == "__main__":
    app.run("localhost", 5000, True)
