from flask import Flask, render_template
# from core.JobAnalysis import JobAnalysis
# from services.JobServices import JobService

app = Flask(__name__)


@app.route("/welcome")
def welcome():
    content = "hello World!"
    return render_template("welcome.html", **{"content": content})


@app.route("/")
def index():
    return render_template("index.html")


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
    # jobService = JobService()
    # jobs = jobService.getAll()

    # analysis = JobAnalysis()
    # analysis.statistic(jobs, "name")
