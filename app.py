from flask import Flask, render_template, request, redirect, session
import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


@app.route("/")
def home():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name:
        return "Name is required", 400
    if not email:
        return "Email is required", 400
    if not password:
        return "Password is required", 400
    if not confirm_password:
        return "Confirm password is required", 400
    if password != confirm_password:
        return "Passwords do not match", 400

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",
            (email, name, password_hash)
        )
        db.commit()

        cursor.execute(
            "SELECT user_id, name FROM users WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()

        session["user_id"] = user[0]
        session["name"] = user[1]

        return redirect("/todos")

    except mysql.connector.IntegrityError:
        return "Email Already Exists", 409

    finally:
        cursor.close()
        db.close()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email:
        return "Email is required", 400
    if not password:
        return "Password is required", 400

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT user_id, name, password_hash FROM users WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()
    finally:
        cursor.close()
        db.close()

    if user is None or not bcrypt.checkpw(
        password.encode("utf-8"),
        user[2].encode("utf-8")
    ):
        return "Invalid email or password", 401

    session["user_id"] = user[0]
    session["name"] = user[1]

    return redirect("/todos")


@app.route("/todos")
def todo_list():
    if "user_id" not in session:
        return redirect("/login")

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            SELECT todo_id, title, is_done, created_at
            FROM todos
            WHERE user_id = %s
            ORDER BY todo_id DESC
            """,
            (session["user_id"],)
        )
        todos = cursor.fetchall()
    finally:
        cursor.close()
        db.close()

    return render_template("todos.html", todos=todos)


@app.route("/todos/add", methods=["POST"])
def add_todo():
    if "user_id" not in session:
        return redirect("/login")

    title = request.form.get("title", "").strip()

    if not title:
        return "Title is required", 400
    if len(title) > 200:
        return "Title is too long", 400

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO todos (user_id, title) VALUES (%s, %s)",
            (session["user_id"], title)
        )
        db.commit()
    finally:
        cursor.close()
        db.close()

    return redirect("/todos")


@app.route("/todos/edit/<int:todo_id>", methods=["POST"])
def edit_todo(todo_id):
    if "user_id" not in session:
        return redirect("/login")

    title = request.form.get("title", "").strip()

    if not title:
        return "Title is required", 400
    if len(title) > 200:
        return "Title is too long", 400

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            UPDATE todos
            SET title = %s
            WHERE todo_id = %s AND user_id = %s
            """,
            (title, todo_id, session["user_id"])
        )
        db.commit()
    finally:
        cursor.close()
        db.close()

    return redirect("/todos")


@app.route("/todos/toggle/<int:todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            UPDATE todos
            SET is_done = NOT is_done
            WHERE todo_id = %s AND user_id = %s
            """,
            (todo_id, session["user_id"])
        )
        db.commit()
    finally:
        cursor.close()
        db.close()

    return redirect("/todos")


@app.route("/todos/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM todos
            WHERE todo_id = %s AND user_id = %s
            """,
            (todo_id, session["user_id"])
        )
        db.commit()
    finally:
        cursor.close()
        db.close()

    return redirect("/todos")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)