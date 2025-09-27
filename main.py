from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import sqlite3
import os

app = Flask(__name__)

# Ruta base ya creada
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

# 🔎 Ruta de depuración
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

        tabla_map = {
            "Ingeniería de Sistemas": "sistemas",
            "Derecho": "derecho",
            "Psicología": "psicologia",
            "Administración de Empresas": "administracion"
        }
        tabla = tabla_map.get(programa)

        if tabla is None:
            return "Programa no válido", 400

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

# 📄 Página HTML inicial
@app.route("/listacarreras")
def listacarreras():
    conn = get_db_connection()
    cursor = conn.cursor()
    tablas = ["sistemas", "administracion", "derecho", "psicologia"]
    datos = {}
    for tabla in tablas:
        cursor.execute(f"SELECT id, nombre, correo, telefono FROM {tabla}")
        registros = cursor.fetchall()
        datos[tabla] = registros
    conn.close()
    return render_template("listacarreras.html", datos=datos)

# 🔥 API para datos en tiempo real
@app.route("/api/listacarreras")
def api_listacarreras():
    conn = get_db_connection()
    cursor = conn.cursor()
    tablas = ["sistemas", "administracion", "derecho", "psicologia"]
    datos = {}
    for tabla in tablas:
        cursor.execute(f"SELECT id, nombre, correo, telefono FROM {tabla}")
        registros = cursor.fetchall()
        datos[tabla] = [dict(r) for r in registros]
    conn.close()
    return jsonify(datos)

# ✏️ API para editar registro
@app.route("/api/editar_registro", methods=["POST"])
def editar_registro():
    data = request.get_json()
    tabla = data.get("tabla")
    registro_id = data.get("id")
    nombre = data.get("nombre")
    correo = data.get("correo")
    telefono = data.get("telefono")

    if not tabla or not registro_id:
        return jsonify({"status": "error", "msg": "Datos incompletos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE {tabla} SET nombre=?, correo=?, telefono=? WHERE id=?",
        (nombre, correo, telefono, registro_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


# 🗑 API para eliminar registro
@app.route("/api/eliminar_registro", methods=["POST"])
def eliminar_registro():
    data = request.get_json()
    tabla = data.get("tabla")
    registro_id = data.get("id")

    if not tabla or not registro_id:
        return jsonify({"status": "error", "msg": "Datos incompletos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {tabla} WHERE id=?", (registro_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

#chatbox
@app.route("/predict", methods=["GET", "POST"])
def predict():
    return render_template("chat.html")

if __name__ == "__main__":
    app.run(debug=True)
