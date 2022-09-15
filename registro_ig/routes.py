from registro_ig import app
from flask import render_template


@app.route("/")
def index():
    return render_template("index.html", pageTitle="Lista")


@app.route("/nuevo")
def alta():
    return render_template("new.html", pageTitle="Alta")   