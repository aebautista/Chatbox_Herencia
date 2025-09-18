from flask import Flask, render_template, request

app = Flask(__name__)

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

@app.route("/inscripcion/<programa>", methods=["GET", "POST"])
def inscripcion(programa):
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]
        # Aquí podrías guardar los datos en la base de datos si lo deseas
        return render_template("confirmacion.html", nombre=nombre, programa=programa)
    
    return render_template("inscripcion.html", programa=programa)

if __name__ == "__main__":
    app.run(debug=True)
