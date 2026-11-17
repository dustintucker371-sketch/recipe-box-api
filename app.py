from flask import Flask, g, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

DATABASE = "recipes.db"
app = Flask(__name__)

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@app.route("/recipes", methods=["GET"])
def get_recipes():
    db = get_db()
    cursor = db.execute("SELECT * FROM recipes")
    recipes = [dict(row) for row in cursor.fetchall()]
    return jsonify(recipes)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    password = (data.get("password") or "")

    if not username or not email or not password:
        return jsonify({"error": "username, email, and password are required"}), 400

    password_hash = generate_password_hash(password)

    db = get_db()
    try:
        db.execute(
            """
            INSERT INTO users (username, email, password_hash, created_at)
            VALUES (?, ?, ?, datetime('now'))
            """,
            (username, email, password_hash),
        )
        db.commit()
    except sqlite3.IntegrityError as e:
        message = str(e)
        if "users.username" in message:
            return jsonify({"error": "username already exists"}), 409
        if "users.email" in message:
            return jsonify({"error": "email already exists"}), 409
        return jsonify({"error": "account already exists"}), 409

    return jsonify({"username": username, "email": email}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "")

    if not username or not password:
        return jsonify({"error": "Invalid credentials"}), 401

    db = get_db()
    cursor = db.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user is None or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "id": user["id"],
        "username": user["username"]
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
