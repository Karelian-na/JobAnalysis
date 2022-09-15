import re
import json
from flask import Flask, render_template, request
from core.JobAnalysis import JobAnalysis
from services.JobServices import JobService
from core.Spider import Spider
from core.SpiderConfig import FiveOneConfig, BossConfig, ZhiTongConfig, HookConfig

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


@app.route("/analysis/<type>", methods=["GET", "POST"])
def analysis(type):
    if request.method == "GET":
        if type == "total":
            categories = list(map(lambda area: area.work_area, jobService.getAllAreas()))
            filterTitle = "地区"
        elif type == "industry":
            categories = jobService.getAllIndustries(10)
            filterTitle = "行业"
        elif type == "professional":
            jobs = jobService.getAll()
            jobAnalysis.group(jobs, 10)
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
            "filter": type,
        })
    elif request.method == "POST":
        filter = request.form.get("filter") if request.form.get("filter") else ""
        groupAmount = int(request.form.get("groupAmount")) if request.form.get("groupAmount") else 10
        minSalary = float(request.form.get("minSalary")) if request.form.get("minSalary") else 1.0
        maxSalary = float(request.form.get("maxSalary")) if request.form.get("maxSalary") else 100.0

        if type == "total":
            query = jobService.getAllByArea(filter)
            jobs = jobService.getAllBySalaryInterval(minSalary, maxSalary, query)
        elif type == "industry":
            jobs = jobService.getAllByIndustry(filter)

        jobAnalysis.group(jobs, groupAmount)

        data: dict[str, int | dict[str, int | str]] = {}
        data.setdefault("groupProportion", jobAnalysis.statistic())
        data.setdefault("salaryProportion", jobAnalysis.statisticSalary())
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
def jobs():
    if request.method == "GET":
        return render_template("jobs.html")
    elif request.method == "POST":
        pageIdx = int(request.form.get("pageIdx"))
        pageSize = int(request.form.get("pageSize"))

        jobs = jobService.get(pageSize, pageIdx)
        count = jobService.getTotalCount()
        jobList  = [ job.toDict() for job in jobs ]
        return json.dumps({
            "code": 0,
            "count": count,
            "data": jobList
        })
    else:
        return render_template("404.html", **{
            "msg": "您所请求方式错误!"
        })


@app.route("/spidy")
def get():
    cookies: dict[str, str]
    with open("./src/cookie.json", encoding="utf-8", mode="r") as file:
        cookies = json.loads(file.read())

    fiveOneConfig = FiveOneConfig("前程无忧")
    fiveOneConfig.cookies = cookies.get(fiveOneConfig.__class__.__name__)

    hookConfig = HookConfig("拉钩招聘")
    hookConfig.cookies = cookies.get(hookConfig.__class__.__name__)

    bossConfig = BossConfig("Boss直聘")
    bossConfig.cookies = cookies.get(bossConfig.__class__.__name__)

    zhiTongConfig = ZhiTongConfig("智通人才网")
    zhiTongConfig.cookies = cookies.get(zhiTongConfig.__class__.__name__)

    spilder = Spider(20, configs=[bossConfig])
    spilder.get(20)

    for config in spilder.configs:
        cookies.setdefault(config.__class__.__name__, config.getCookieString())

    with open("./src/cookie.json", encoding="utf-8", mode="w+") as file:
        file.write(json.dumps(cookies))
    return "ok"


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
