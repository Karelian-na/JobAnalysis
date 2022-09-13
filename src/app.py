import json
from flask import Flask, render_template, request
from core.JobAnalysis import JobAnalysis
from services.JobServices import JobService
from core.Spider import Spider
from core.SpiderConfig import FiveOneConfig, BossConfig, ZhiTongConfig, HookConfig

app = Flask(__name__)

@app.route("/welcome")
def welcome():
    content = "hello World!"
    return render_template("welcome.html", **{"content": content})


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
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

@app.route("/totalAnalysis.html")
def totalAnalysis():
    return render_template("totalAnalysis.html")


@app.route("/singleCareerAnalysis.html")
def singleCareerAnalysis():
    return render_template("singleCareerAnalysis.html")


@app.route("/singleVocationAnalysis.html")
def singleVocationAnalysis():
    return render_template("singleVocationAnalysis.html")


@app.route("/allJobDetails.html")
def allJobDetails():
    return render_template("allJobDetails.html")

if __name__ == "__main__":
    app.run("localhost", 5000, True)
