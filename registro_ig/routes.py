from registro_ig import app
from flask import render_template, request, redirect
import csv


@app.route("/")
def index():
    fichero = open("data/movimientos.txt", "r")
    csvReader = csv.reader(fichero, delimiter=',', quotechar='"')
    movimientos = []
    for movimiento in csvReader:
        movimientos.append(movimiento)

#movimientos = [movimiento for movimiento in csvReader] #list comprehension
    fichero.close()
    return render_template("index.html", pageTitle="Lista", movements=movimientos)


@app.route("/nuevo", methods=["GET", "POST"])
def alta():
    if request.method == "GET":
        return render_template("new.html", pageTitle="Alta")
    else:
        fichero =open("data/movimientos.txt", "a", newline="")
        csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')

        

        csvWriter.writerow([request.form['date'], request.form['concept'], request.form['quantity']])
        fichero.close()
        return redirect("/")


@app.route("/delete")
def baja():
    return render_template("delete.html", pageTitle="Baja")


@app.route("/modification")
def modificacion():
    return render_template("modification.html", pageTitle="Modificacion")         