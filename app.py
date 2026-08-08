# ============================================
# SIGAT - Sistema de Gestión de Activos Tecnológicos
# Jeremy Rodríguez Bogantes
# app.py - Aplicación web (Flask)
# ============================================

from flask import Flask, render_template, request, redirect, session, url_for
from functools import wraps
from datetime import datetime, date
import os

import data

app = Flask(__name__)
# En producción, esta clave se debe definir como variable de entorno.
app.secret_key = os.environ.get("SECRET_KEY", "clave-secreta-para-pruebas-sigat")


# --------------------------------------------
# Decorador para proteger rutas que requieren sesión iniciada
# --------------------------------------------
def login_requerido(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("login"))
        return vista(*args, **kwargs)
    return envoltura


def autenticar(username, password):
    hash_ingresado = data.hash_password(password)
    for u in data.usuarios:
        if u["username"] == username and u["password"] == hash_ingresado:
            return u
    return None


# --------------------------------------------
# Login / Logout
# --------------------------------------------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if "usuario" in session:
        return redirect(url_for("dashboard"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        usuario = autenticar(username, password)
        if usuario:
            session["usuario"] = usuario["username"]
            session["nombre"] = usuario["nombre"]
            session["rol"] = usuario["rol"]
            return redirect(url_for("dashboard"))
        else:
            error = "Usuario o contraseña incorrectos."

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# --------------------------------------------
# Dashboard
# --------------------------------------------
@app.route("/dashboard")
@login_requerido
def dashboard():
    total_activos = len(data.activos)
    total_clientes = len(data.clientes)
    mantenimientos_pendientes = sum(
        1 for a in data.activos if a["estado"] == "En mantenimiento"
    )

    hoy = date.today()
    garantias_por_vencer = 0
    for a in data.activos:
        try:
            fecha_garantia = datetime.strptime(a["garantia"], "%Y-%m-%d").date()
            dias_restantes = (fecha_garantia - hoy).days
            if 0 <= dias_restantes <= 90:
                garantias_por_vencer += 1
        except ValueError:
            pass

    activos_recientes = sorted(
        data.activos, key=lambda a: a["fecha_adquisicion"], reverse=True
    )[:5]

    return render_template(
        "dashboard.html",
        total_activos=total_activos,
        total_clientes=total_clientes,
        mantenimientos_pendientes=mantenimientos_pendientes,
        garantias_por_vencer=garantias_por_vencer,
        activos_recientes=activos_recientes,
        nombre_cliente=data.nombre_cliente,
    )


# --------------------------------------------
# Clientes
# --------------------------------------------
@app.route("/clientes")
@login_requerido
def clientes():
    sedes_por_cliente = {}
    for c in data.clientes:
        sedes_por_cliente[c["id"]] = [s for s in data.sedes if s["cliente_id"] == c["id"]]
    return render_template("clientes.html", clientes=data.clientes, sedes_por_cliente=sedes_por_cliente)


@app.route("/clientes/nuevo", methods=["POST"])
@login_requerido
def nuevo_cliente():
    nuevo_id = max([c["id"] for c in data.clientes], default=0) + 1
    data.clientes.append({
        "id": nuevo_id,
        "nombre": request.form.get("nombre", "").strip(),
        "contacto": request.form.get("contacto", "").strip(),
        "telefono": request.form.get("telefono", "").strip(),
        "correo": request.form.get("correo", "").strip(),
    })
    return redirect(url_for("clientes"))


# --------------------------------------------
# Activos
# --------------------------------------------
@app.route("/activos")
@login_requerido
def activos():
    return render_template(
        "activos.html",
        activos=data.activos,
        clientes=data.clientes,
        sedes=data.sedes,
        nombre_cliente=data.nombre_cliente,
        nombre_sede=data.nombre_sede,
    )


@app.route("/activos/nuevo", methods=["POST"])
@login_requerido
def nuevo_activo():
    nuevo_id = max([a["id"] for a in data.activos], default=0) + 1
    data.activos.append({
        "id": nuevo_id,
        "serie": request.form.get("serie", "").strip(),
        "placa": request.form.get("placa", "").strip(),
        "cliente_id": int(request.form.get("cliente_id")),
        "sede_id": int(request.form.get("sede_id")),
        "usuario": request.form.get("usuario", "").strip(),
        "categoria": request.form.get("categoria", "").strip(),
        "marca": request.form.get("marca", "").strip(),
        "modelo": request.form.get("modelo", "").strip(),
        "fecha_adquisicion": request.form.get("fecha_adquisicion", ""),
        "estado": request.form.get("estado", "Operativo"),
        "garantia": request.form.get("garantia", ""),
    })
    return redirect(url_for("activos"))


# --------------------------------------------
# Mantenimientos
# --------------------------------------------
@app.route("/mantenimientos")
@login_requerido
def mantenimientos():
    lista = []
    for m in data.mantenimientos:
        activo = data.buscar_activo(m["activo_id"])
        lista.append({**m, "activo_serie": activo["serie"] if activo else "N/D"})
    return render_template("mantenimientos.html", mantenimientos=lista, activos=data.activos)


@app.route("/mantenimientos/nuevo", methods=["POST"])
@login_requerido
def nuevo_mantenimiento():
    nuevo_id = max([m["id"] for m in data.mantenimientos], default=0) + 1
    activo_id = int(request.form.get("activo_id"))
    data.mantenimientos.append({
        "id": nuevo_id,
        "activo_id": activo_id,
        "tipo": request.form.get("tipo", "Preventivo"),
        "fecha": request.form.get("fecha", ""),
        "tecnico": session.get("nombre", "N/D"),
        "descripcion": request.form.get("descripcion", "").strip(),
        "observaciones": request.form.get("observaciones", "").strip(),
    })
    # Si se marca como en mantenimiento, se refleja en el estado del activo
    activo = data.buscar_activo(activo_id)
    if activo and request.form.get("marcar_en_mantenimiento"):
        activo["estado"] = "En mantenimiento"
    return redirect(url_for("mantenimientos"))


# --------------------------------------------
# Garantías
# --------------------------------------------
@app.route("/garantias")
@login_requerido
def garantias():
    hoy = date.today()
    lista = []
    for a in data.activos:
        try:
            fecha_garantia = datetime.strptime(a["garantia"], "%Y-%m-%d").date()
            dias_restantes = (fecha_garantia - hoy).days
        except ValueError:
            dias_restantes = None

        if dias_restantes is None:
            estado_garantia = "Sin datos"
        elif dias_restantes < 0:
            estado_garantia = "Vencida"
        elif dias_restantes <= 90:
            estado_garantia = "Próxima a vencer"
        else:
            estado_garantia = "Vigente"

        lista.append({**a, "dias_restantes": dias_restantes, "estado_garantia": estado_garantia})

    return render_template("garantias.html", activos=lista, nombre_cliente=data.nombre_cliente)


# --------------------------------------------
# Consultas (búsqueda general)
# --------------------------------------------
@app.route("/consultas")
@login_requerido
def consultas():
    termino = request.args.get("q", "").strip().lower()
    resultados = []
    if termino:
        for a in data.activos:
            campos = [a["serie"], a["placa"], a["usuario"], a["marca"], a["modelo"],
                      data.nombre_cliente(a["cliente_id"]), data.nombre_sede(a["sede_id"])]
            if any(termino in str(campo).lower() for campo in campos):
                resultados.append(a)
    return render_template(
        "consultas.html",
        termino=termino,
        resultados=resultados,
        nombre_cliente=data.nombre_cliente,
        nombre_sede=data.nombre_sede,
    )


# --------------------------------------------
# Reportes
# --------------------------------------------
@app.route("/reportes")
@login_requerido
def reportes():
    tipo = request.args.get("tipo", "inventario")
    cliente_id = request.args.get("cliente_id", "todos")
    sede_id = request.args.get("sede_id", "todas")
    estado = request.args.get("estado", "todos")

    resultado = data.activos
    if cliente_id != "todos":
        resultado = [a for a in resultado if a["cliente_id"] == int(cliente_id)]
    if sede_id != "todas":
        resultado = [a for a in resultado if a["sede_id"] == int(sede_id)]
    if estado != "todos":
        resultado = [a for a in resultado if a["estado"] == estado]

    return render_template(
        "reportes.html",
        tipo=tipo,
        activos=resultado,
        clientes=data.clientes,
        sedes=data.sedes,
        cliente_id=cliente_id,
        sede_id=sede_id,
        estado=estado,
        nombre_cliente=data.nombre_cliente,
        nombre_sede=data.nombre_sede,
    )


# --------------------------------------------
# Configuración (marcador de espacio para futuras etapas)
# --------------------------------------------
@app.route("/configuracion")
@login_requerido
def configuracion():
    return render_template("configuracion.html")


if __name__ == "__main__":
    # debug=True solo debe usarse en desarrollo local
    app.run(debug=True)
