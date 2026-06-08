from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
app= Flask(__name__)
app.secret_key = "axis_secret_key"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "axis_db"

mysql = MySQL(app)
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "axis123":
            session["admin"] = True
            return redirect("/admin")

    if not session.get("admin"):
        return render_template("login.html")

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts")
    contatti = cur.fetchall()
    cur.close()

    return render_template("admin.html", contatti=contatti)


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/admin")
if __name__ == "__main__":
    app.run(debug=True, port=5001)