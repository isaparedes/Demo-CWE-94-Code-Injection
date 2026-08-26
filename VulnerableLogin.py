from flask import Flask, request, render_template_string, g
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "sqlInjection_demo.db")

app = Flask(__name__)

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    if (os.path.exists(DB_PATH)):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, is_admin INTEGER)"
    )
    conn.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", 
        ("admin", "1234", 1),
    )
    conn.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", 
        ("juan", "juan123", 0),
    )
    conn.commit()
    conn.close()

TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Login (VULNERABLE)</title>
  <style>
    body { font-family: monospace; background: #1a1a1a; color: #e0e0e0; padding: 2rem; }
    h1 { color: #ff5555; }
    input { padding: 0.5rem; width: 250px; display:block; margin-bottom: 0.5rem; }
    button { padding: 0.5rem 1rem; }
    pre { background: #000; padding: 1rem; border: 1px solid #444; white-space: pre-wrap; }
    .badge { background: #ff5555; color: #000; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; }
    .ok { color: #55ff88; }
    .fail { color: #ff5555; }
  </style>
</head>
<body>
  <h1>🔴 Login <span class="badge">VULNERABLE</span></h1>
  <form method="POST">
    <input name="username" placeholder="usuario" autofocus />
    <input name="password" placeholder="contraseña" type="text" />
    <button type="submit">Ingresar</button>
  </form>
  {% if result %}
    <p class="{{ 'ok' if success else 'fail' }}">{{ result }}</p>
  {% endif %}
  {% if query %}
    <p>Query ejecutada:</p>
    <pre>{{ query }}</pre>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    success = False
    query = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        #Esta es la vulnerabilidad, el input del usuario se concatena directo
        #dentro del string SQL
        query = (
            f"SELECT * FROM users WHERE username = '{username}' "
            f"AND password = '{password}' "
        )
        cursor = get_db().execute(query)
        row = cursor.fetchone()

        if row:
            success = True
            result = f"Login exitoso. Bienvenido, {row[1]} (is_admin={row[3]})"
        else:
            result = "Usuario o contraseña incorrectos"

    return render_template_string(TEMPLATE, result=result, success=success, query=query)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)