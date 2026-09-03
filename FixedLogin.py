from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "clave-demo-cwe94"

users = {
    "admin": {
        "password": "1234",
        "role": "admin"
    },
    "juan": {
        "password": "juan1234",
        "role": "user"
    },
}


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET" and "username" in session:
        if session["role"] == "admin":
            return redirect(url_for("admin"))

        return redirect(url_for("dashboard"))

    result = None
    success = False

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # SOLUCIÓN A CWE-94: Evitar el uso de eval() y realizar la comparación de manera segura.
        authenticated = (
            username in users
            and users[username]["password"] == password
        )

        if authenticated:

            success = True

            session["username"] = username
            session["role"] = users[username]["role"]

            if session["role"] == "admin":
                return redirect(url_for("admin"))

            return redirect(url_for("dashboard"))

        else:
            result = "Usuario o contraseña incorrectos"

    return render_template(
        "login.html",
        theme="fixed",
        result=result,
        success=success,
    )


@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("index"))

    # Los mismos datos ficticios que utiliza la versión vulnerable.

    projects = [
        {
            "name": "Sistema de Gestión",
            "status": "En progreso",
            "progress": 75
        },
        {
            "name": "Aplicación Web",
            "status": "En revisión",
            "progress": 45
        },
        {
            "name": "API Backend",
            "status": "Completado",
            "progress": 100
        }
    ]

    tasks = [
        "Revisar documentación del proyecto",
        "Actualizar requisitos",
        "Verificar cambios pendientes"
    ]

    return render_template(
        "dashboard.html",
        theme="fixed",
        username=session["username"],
        role=session["role"],
        projects=projects,
        tasks=tasks
    )


@app.route("/admin")
def admin():

    if "username" not in session:
        return redirect(url_for("index"))

    if session.get("role") != "admin":
        return render_template(
            "forbidden.html",
            theme="fixed"
        ), 403

    return render_template(
        "admin.html",
        theme="fixed"
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
        port=5001
    )