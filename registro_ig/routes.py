from config import LAST_ID_FILE, MOVIMIENTOS_FILE, NEW_FILE
from registro_ig import app
from flask import render_template, request, redirect, url_for
import csv
from datetime import date
import os
from registro_ig.models import delete_by, insert, select_all, select_by, insert, update_by


@app.route("/")
def index():
    movimientos = select_all()
    return render_template("index.html", pageTitle="Lista", movements=movimientos)

@app.route("/nuevo", methods=["GET", "POST"])
def alta():
    if request.method == "GET":
        return render_template("new.html", pageTitle="Alta", dataForm={})
    else:
        """
        1. Validar el formulario
            Fecha valida y <= hoy
        2. Concepto no sea vacio
        3. Cantidad no sea 0
        """
        errores = validaFormulario(request.form)
        
        if not errores:
            insert([request.form["date"],
                    request.form["concept"],
                    request.form["quantity"]
            ])

            return redirect("/")
        else:
            return render_template("new.html", pageTitle="Alta", msgErrors=errores, dataForm=dict(request.form))

def form_to_list(id, form):
    return [str(id), form["date"], form["concept"], form["quantity"]]


def validaFormulario(camposFormulario):
    errores = []
    hoy = date.today().isoformat()
    if camposFormulario["date"] > hoy:
        errores.append("La fecha introducida es el futuro.")

    if camposFormulario["concept"] == "":
        errores.append("Introduce un concepto para la transacción.")

    #La primera condicion es para que el numero sea distinto a 0
    #La segunda condicion es para que el campo no este vacio
    if camposFormulario["quantity"] == "" or float(camposFormulario["quantity"]) == 0.0:
        errores.append("Introduce una cantidad positiva o negativa")

    return errores


@app.route("/modificar/<int:id>", methods=["GET", "POST"])
def modifica(id):
    if request.method == "GET":
        """
        1. Consultar en movimientos.tx y recuperar el registro con id al de la peticion
        2. Devolver el formulario html con los datos de mi registro
        """
        register = select_by(id)
        return render_template("update.html", registro=register, pageTitle = "Modificar")
    else:
        """
        1. Validar registro de entrada
        2. Si el registro es correcto lo sustituyo en movimientos.txt. La mejor manera es copiar registro a registro el fichero nuevo y dar el cambiazo
        3. redirect
        4. Si el registro es incorrecto la gestion de errores que conocemos
        """
        errores = validaFormulario(request.form)
        
        if not errores:
            update_by(id, form_to_list(id, request.form))
            return redirect(url_for("index"))
        else:
            return render_template("update.html", registro=form_to_list(id, request.form), pageTitle = "Modificar", msgErrors=errores)


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def borrar(id):
    if request.method == "GET":
        registro_definitivo = select_by(id)
        if registro_definitivo:
            return render_template("delete.html", registro=registro_definitivo)
        else:
            return redirect(url_for("index"))
    else:
        """
        1. abrir fichero movimientos.txt en lectura
        2. abrir fichero moviemientos.txt en escritura
        3. copiar todos los registros uno a uno en su orden exceptuadno el que queremos borrar
        4. borrar movimientos.txt
        5. renombrar movimientos.txt a movimientos.txt
        """
        delete_by(id)
        return redirect(url_for("index"))

                