from flask import Flask, request, render_template_string

app = Flask(__name__)

users = {
    "admin": "1234",
    "juan": "juan1234",
}

TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Login con eval() (SEGURO)</title>
  <style>
    body { font-family: monospace; background: #1a2e1a; color: #e0e0e0; padding: 2rem; }
    h1 { color: #55ff88; }
    input { padding: 0.5rem; width: 320px; display:block; margin-bottom: 0.5rem; }
    button { padding: 0.5rem 1rem; }
    pre { background: #000; padding: 1rem; border: 1px solid #444; white-space: pre-wrap; word-break: break-all; }
    .badge { background: #55ff88; color: #000; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; }
    .ok { color: #55ff88; }
    .fail { color: #ff5555; }
  </style>
</head>
<body>
  <h1>🟢 Login con eval() <span class="badge">SEGURO</span></h1>
  <form method="POST">
    <input name="username" placeholder="usuario" autofocus />
    <input name="password" placeholder="contraseña" type="text" />
    <button type="submit">Ingresar</button>
  </form>
  {% if result %}
    <p class="{{ 'ok' if success else 'fail' }}">{{ result }}</p>
  {% endif %}
  <p>Comparación usada (sin eval, sin código a partir de input):</p>
  <pre>users.get(username) == password</pre>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    success = False

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        #Este es el fix, se hace una comparacion directa sin construir
        #ni ejecutar codigo a partir del input del usuario
        authenticated = users.get(username) == password
        
        if authenticated:
            success = True
            result = f"Acceso concedido. Bienvenido, {username}"
        else:
            result = "Usuario o contraseña incorrectos"
        

    return render_template_string(TEMPLATE, result=result, success=success)

if __name__ == "__main__":
    app.run(debug=True, port=5001)