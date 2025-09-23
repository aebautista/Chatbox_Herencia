from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# Ruta  base ya creada
DATABASE = r"C:\Users\Arnold\Documents\Chatbox_Herencia\sisemasexp.db"
print("Base usada:", os.path.abspath(DATABASE))

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mision")
def mision():
    return render_template("mision.html")

@app.route("/vision")
def vision():
    return render_template("vision.html")

@app.route("/programas")
def programas():
    return render_template("programas.html")

# 🔎 Ruta de depuración para verificar tablas y cantidad de registros
@app.route("/debug_tablas")
def debug_tablas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = [t[0] for t in cursor.fetchall()]

    resultado = {}
    for t in tablas:
        cursor.execute(f"SELECT COUNT(*) FROM {t}")
        count = cursor.fetchone()[0]
        resultado[t] = count

    conn.close()
    return resultado

@app.route("/inscripcion/<programa>", methods=["GET", "POST"])
def inscripcion(programa):
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]

        # Mapeo seguro de programa a tabla de la base
        tabla_map = {
            "Ingeniería de Sistemas": "sistemas",
            "Derecho": "derecho",
            "Psicología": "psicologia",
            "Administración de Empresas": "administracion"
        }
        tabla = tabla_map.get(programa)

        if tabla is None:
            return "Programa no válido", 400

        # Guardar en la base
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO {tabla} (nombre, correo, telefono) VALUES (?, ?, ?)",
            (nombre, correo, telefono)
        )
        conn.commit()
        conn.close()

        return render_template("confirmacion.html", nombre=nombre, programa=programa)

    return render_template("inscripcion.html", programa=programa)

if __name__ == "__main__":
    app.run(debug=True)