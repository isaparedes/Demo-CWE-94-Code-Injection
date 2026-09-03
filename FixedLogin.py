from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "clave-demo-cwe94"

users = {
    "admin": "1234",
    "juan": "juan1234",
}


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET" and "username" in session:
        if session["username"] == "admin":
            return redirect(url_for("admin"))
        return redirect(url_for("dashboard"))

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

    return render_template(
        "dashboard.html",
        theme="fixed",
        username=session["username"],
    )


@app.route("/admin")
def admin():

    if session.get("username") != "admin":
        return render_template("forbidden.html", theme="fixed"), 403

    return render_template("admin.html", theme="fixed")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
