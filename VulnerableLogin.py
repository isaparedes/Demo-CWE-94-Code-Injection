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
  <title>Login con eval() (VULNERABLE)</title>
  <style>
    body { font-family: monospace; background: #1a1a1a; color: #e0e0e0; padding: 2rem; }
    h1 { color: #ff5555; }
    input { padding: 0.5rem; width: 320px; display:block; margin-bottom: 0.5rem; }
    button { padding: 0.5rem 1rem; }
    pre { background: #000; padding: 1rem; border: 1px solid #444; white-space: pre-wrap; word-break: break-all; }
    .badge { background: #ff5555; color: #000; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; }
    .ok { color: #55ff88; }
    .fail { color: #ff5555; }
  </style>
</head>
<body>
  <h1>🔴 Login con eval() <span class="badge">VULNERABLE</span></h1>
  <form method="POST">
    <input name="username" placeholder="usuario" autofocus />
    <input name="password" placeholder="contraseña" type="text" />
    <button type="submit">Ingresar</button>
  </form>
  {% if result %}
    <p class="{{ 'ok' if success else 'fail' }}">{{ result }}</p>
  {% endif %}
  {% if condition %}
    <p>Expresión evaluada:</p>
    <pre>{{ condition }}</pre>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    success = False
    condition = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        #Esta es la vulnerabilidad, se arma una expresion de Python
        # concatenando el input del usuario y se evalua con eval()
        
        condition = f"users.get('{username}') == '{password}' "
        try:
            authenticated = eval(condition)
        except Exception as e:
            authenticated = False
            result = f"Error evaluando: {e}"

        if result is None:
            if authenticated:
                success = True
                result = f"Acceso concedido. Bienvenido, {username}"
            else:
                result = "Usuario o contraseña incorrectos"
        

    return render_template_string(TEMPLATE, result=result, success=success, condition=condition)

if __name__ == "__main__":
    app.run(debug=True, port=5000)