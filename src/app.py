from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
	content = "hello World!"
	return render_template("index.html", **{"content": content})

if __name__ == "__main__":
	app.run("localhost", 5000, True)