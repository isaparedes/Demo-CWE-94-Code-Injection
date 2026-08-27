from flask import Flask, request, render_template_string, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "clave-demo-cwe94"

users = {
    "admin": "1234",
    "juan": "juan1234",
}

TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Login (SEGURO)</title>
  <style>
    body {
      font-family: monospace;
      background: #1a1a1a;
      color: #e0e0e0;
      padding: 2rem;
    }

    h1 {
      color: #55ff88;
    }

    input {
      padding: 0.5rem;
      width: 320px;
      display: block;
      margin-bottom: 0.5rem;
    }

    button {
      padding: 0.5rem 1rem;
    }

    pre {
      background: #000;
      padding: 1rem;
      border: 1px solid #444;
      white-space: pre-wrap;
      word-break: break-all;
    }

    .badge {
      background: #55ff88;
      color: #000;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.8rem;
    }

    .ok {
      color: #55ff88;
    }

    .fail {
      color: #ff5555;
    }
  </style>
</head>

<body>

  <h1>🟢 Login <span class="badge">SEGURO</span></h1>

  <form method="POST">
    <input name="username" placeholder="usuario" autofocus />
    <input name="password" placeholder="contraseña" type="text" />
    <button type="submit">Ingresar</button>
  </form>

  {% if result %}
    <p class="{{ 'ok' if success else 'fail' }}">{{ result }}</p>
  {% endif %}

  <p>Comparación utilizada:</p>

  <pre>users.get(username) == password</pre>

</body>
</html>
"""


ADMIN_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Panel de administración</title>

  <style>
    body {
      font-family: monospace;
      background: #1a1a1a;
      color: #e0e0e0;
      padding: 2rem;
    }

    h1 {
      color: #55ff88;
    }

    .panel {
      background: #222;
      border: 1px solid #444;
      padding: 1.5rem;
      max-width: 600px;
    }

    .item {
      padding: 0.8rem;
      border-bottom: 1px solid #444;
    }

    a {
      color: #55aaff;
    }
  </style>
</head>

<body>

  <h1>Panel de administración</h1>

  <div class="panel">

    <p><strong>Bienvenido, administrador.</strong></p>

    <div class="item">
      Usuarios registrados: 2
    </div>

    <div class="item">
      Pedidos pendientes: 8
    </div>

    <div class="item">
      Productos disponibles: 24
    </div>

    <div class="item">
      Estado del sistema: Operativo
    </div>

  </div>

  <br>

  <a href="/">← Volver al login</a>

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

        # FIX CWE-94:
        # Los datos del usuario se utilizan directamente
        # como datos y nunca se convierten en código.

        authenticated = users.get(username) == password

        if authenticated:

            success = True
            session["username"] = username

            if username == "admin":
                return redirect(url_for("admin"))

            result = f"Acceso concedido. Bienvenido, {username}"

        else:
            result = "Usuario o contraseña incorrectos"

    return render_template_string(
        TEMPLATE,
        result=result,
        success=success
    )


@app.route("/admin")
def admin():

    if session.get("username") != "admin":

        return """
        <h1>403 - Acceso denegado</h1>
        <p>Esta página es solo para administradores.</p>
        <a href="/">← Volver al login</a>
        """, 403

    return render_template_string(ADMIN_TEMPLATE)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)