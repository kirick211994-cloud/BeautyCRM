import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        date = request.form["date"]
        comment = request.form["comment"]

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO clients (name, phone, date, comment)
        VALUES (?, ?, ?, ?)
        """, (name, phone, date, comment))

        connection.commit()
        connection.close()

        return f"""
        <h1>Спасибо за запись!</h1>
        <p>Имя: {name}</p>
        <p>Телефон: {phone}</p>
        <p>Дата: {date}</p>
        <p>Комментарий: {comment}</p>
        """

    return render_template("index.html")
@app.route("/admin")
def admin():

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM clients")

    clients = cursor.fetchall()

    connection.close()

    return render_template("admin.html", clients=clients)
@app.route("/delete/<int:id>")
def delete(id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM clients WHERE id = ?", (id,))

    connection.commit()
    connection.close()

    return redirect("/admin")
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        date = request.form["date"]
        comment = request.form["comment"]
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("""
        UPDATE clients
        SET name = ?, phone = ?, date = ?, comment = ?
        WHERE id = ?
        """, (name, phone, date, comment, id))

        connection.commit()
        connection.close()

        return redirect("/admin")

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM clients WHERE id = ?", (id,))

    client = cursor.fetchone()

    connection.close()

    return render_template("edit.html", client=client)
if __name__ == "__main__":
    app.run(debug=True)
