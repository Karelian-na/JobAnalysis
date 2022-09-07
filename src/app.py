from flask import Flask, render_template
from core.JobAnalysis import JobAnalysis
from services.JobServices import JobService

app = Flask(__name__)

@app.route("/")
def index():
	content = "hello World!"
	return render_template("index.html", **{"content": content})

if __name__ == "__main__":
	# app.run("localhost", 5000, True)
	jobService = JobService()
	jobs = jobService.getAll()

	analysis = JobAnalysis()
	analysis.statistic(jobs, "name")