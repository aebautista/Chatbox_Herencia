from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", page="home")

@app.route("/mision")
def mision():
    return render_template("mision.html", page="mision")

@app.route("/vision")
def vision():
    return render_template("vision.html", page="vision")

@app.route("/programas")
def programas():
    return render_template("programas.html", page="programas")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message", "").strip().lower()
    return jsonify({"response": responder_chatbot(user_message)})

def responder_chatbot(msg):
    if not msg:
        return "No entendí tu mensaje. ¿Podrías repetirlo?"
    if any(word in msg for word in ["hola", "buenas", "saludo"]):
        return "¡Hola! 👋 Bienvenido al chat de la Universitaria de Colombia."
    if "mision" in msg:
        return "Nuestra misión es formar profesionales integrales, comprometidos con el desarrollo social."
    if "vision" in msg:
        return "Nuestra visión es ser reconocidos como líderes en educación superior en Colombia."
    if "programa" in msg:
        return "Tenemos programas de Ingeniería, Ciencias Sociales y más. ¿Sobre cuál te gustaría saber?"
    if "gracias" in msg:
        return "¡Con gusto! 😊"
    return f"Interesante lo que dices: '{msg}'. ¿Quieres más información de Misión, Visión o Programas?"

if __name__ == "__main__":
    app.run(debug=True)
