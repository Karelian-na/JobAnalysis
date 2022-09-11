import json
from flask import Flask, render_template
from core.JobAnalysis import JobAnalysis
from services.JobServices import JobService
from core.Spider import Spider
from core.SpiderConfig import FiveOneConfig, BossConfig
#import requests

app = Flask(__name__)


@app.route("/")
def index():
    content = "hello World!"
    return render_template("index.html", **{"content": content})

@app.route("/totalAnalysis.html")
def totalAnalysis():
    return render_template("totalAnalysis.html")


@app.route("/singleAnalysis.html")
def singleAnalysis():
    return render_template("singleAnalysis.html")


@app.route("/allJobDetails.html")
def allJobDetails():
    return render_template("allJobDetails.html")

if __name__ == "__main__":
    # app.run("localhost", 5000, True)
    cookies: dict[str, str]
    with open("./src/cookie.json", encoding="utf-8", mode="r") as file:
        cookies = json.loads(file.read())

    fiveOneConfig = FiveOneConfig(100)
    fiveOneConfig.cookies = cookies.get(fiveOneConfig.__class__.__name__)
    
    bossConfig = BossConfig(10)
    bossConfig.cookies = cookies.get(bossConfig.__class__.__name__)
    
    
    spilder = Spider(20, configs=[fiveOneConfig])
    jobs = spilder.get(30)

    cookies: dict[str, str] = {}
    for config in spilder.configs:
        cookies.setdefault(config.__class__.__name__, config.getCookieString())
    
    with open("./src/cookie.json", encoding="utf-8", mode="w+") as file:
        file.write(json.dumps(cookies))


    #jobs = []
    #config = FiveOneConfig(10)
    #data = json.load(open("./src/core/51data.json", encoding="utf-8"))
    #items = config.getRawJobsList(data)
    #for item in items:
    #    job = config.createRawJobInstance(item).toLocalJob()
    #    if job:
    #        jobs.append(job)