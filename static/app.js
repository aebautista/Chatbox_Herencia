function guardarHistorial() {
  localStorage.setItem("historial_chat", document.getElementById("chat").innerHTML);
}
function restaurarHistorial() {
  const data = localStorage.getItem("historial_chat");
  if (data) {
    document.getElementById("chat").innerHTML = data;
    document.getElementById("chat").scrollTop = document.getElementById("chat").scrollHeight;
  }
}
function limpiarHistorial() {
  localStorage.removeItem("historial_chat");
  document.getElementById("chat").innerHTML = "";
}

function sendMessage() {
  const input = document.getElementById("msg");
  const chat = document.getElementById("chat");
  const message = input.value.trim();
  if (!message) return;

  const userDiv = document.createElement("div");
  userDiv.className = "user";
  userDiv.innerText = "Tú: " + message;
  chat.appendChild(userDiv);
  guardarHistorial();

  input.value = "";
  chat.scrollTop = chat.scrollHeight;

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ message }),
  })
    .then((res) => res.json())
    .then((data) => {
      const botDiv = document.createElement("div");
      botDiv.className = "bot";
      botDiv.innerText = "Bot: " + data.response;
      chat.appendChild(botDiv);
      chat.scrollTop = chat.scrollHeight;
      guardarHistorial();
    })
    .catch(() => {
      const errorDiv = document.createElement("div");
      errorDiv.className = "bot";
      errorDiv.innerText = "Error de conexión con el servidor.";
      chat.appendChild(errorDiv);
      guardarHistorial();
    });
}

document.addEventListener("DOMContentLoaded", () => {
  restaurarHistorial();
  document.getElementById("msg").addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage();
    }
  });
});