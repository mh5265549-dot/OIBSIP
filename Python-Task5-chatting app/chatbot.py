"""
Oasis Infobyte Python Internship — Task 5: Real-Time Chat Application
Author: Hashir Shoaib
Description: Multi-user real-time web chat with Flask, Flask-SocketIO, and SQLite.
             Supports user registration/login, multiple rooms, and persistent message history.
"""

import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO, join_room, leave_room, emit
from werkzeug.security import generate_password_hash, check_password_hash

# ─── App Configuration ────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "oasis_infobyte_chat_secret_key_2024"
socketio = SocketIO(app, cors_allowed_origins="*")

DB_NAME = "chat_app.db"

# ─── Database Initialization ──────────────────────────────────────────────────
def init_db():
    """Creates the SQLite database schema for users, rooms, and messages."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT    UNIQUE NOT NULL,
            password TEXT    NOT NULL,
            created_at TEXT  DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT    UNIQUE NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            room      TEXT    NOT NULL,
            username  TEXT    NOT NULL,
            message   TEXT    NOT NULL,
            timestamp TEXT    NOT NULL
        )
    """)

    # Seed default rooms
    default_rooms = ["General", "Random", "Tech", "Gaming", "Music"]
    for room in default_rooms:
        c.execute("INSERT OR IGNORE INTO rooms (name) VALUES (?)", (room,))

    conn.commit()
    conn.close()


def get_db():
    """Returns a new SQLite connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ─── Authentication Routes ────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def index():
    if "username" in session:
        return redirect(url_for("chat"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm  = request.form.get("confirm", "").strip()

        if not username or not password:
            flash("Username and password are required.", "error")
            return render_template("register.html")

        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("register.html")

        hashed = generate_password_hash(password)
        try:
            conn = get_db()
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
            conn.commit()
            conn.close()
            flash("Account created! Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists. Choose a different one.", "error")
            return render_template("register.html")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["username"] = username
            return redirect(url_for("chat"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ─── Chat Route ───────────────────────────────────────────────────────────────
@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    rooms = conn.execute("SELECT name FROM rooms ORDER BY name").fetchall()
    conn.close()

    return render_template("chat.html", username=session["username"], rooms=rooms)


# ─── SocketIO Events ──────────────────────────────────────────────────────────
@socketio.on("join")
def on_join(data):
    """Handles a user joining a chat room and loads message history."""
    username = session.get("username")
    room     = data.get("room", "General")

    join_room(room)

    # Load last 30 messages for this room
    conn = get_db()
    history = conn.execute(
        "SELECT username, message, timestamp FROM messages WHERE room = ? ORDER BY id DESC LIMIT 30",
        (room,)
    ).fetchall()
    conn.close()

    history_list = [{"username": r["username"], "message": r["message"], "timestamp": r["timestamp"]}
                    for r in reversed(history)]

    emit("room_history", {"room": room, "messages": history_list})
    emit("status_message", {"msg": f"{username} has joined {room}."}, to=room)


@socketio.on("leave")
def on_leave(data):
    """Handles a user leaving a chat room."""
    username = session.get("username")
    room     = data.get("room", "General")
    leave_room(room)
    emit("status_message", {"msg": f"{username} has left {room}."}, to=room)


@socketio.on("send_message")
def on_send_message(data):
    """Receives a message, saves to DB, and broadcasts to all in room."""
    username  = session.get("username", "Anonymous")
    room      = data.get("room", "General")
    message   = data.get("message", "").strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not message:
        return

    # Persist message in database
    conn = get_db()
    conn.execute(
        "INSERT INTO messages (room, username, message, timestamp) VALUES (?, ?, ?, ?)",
        (room, username, message, timestamp)
    )
    conn.commit()
    conn.close()

    emit("receive_message", {
        "username":  username,
        "message":   message,
        "timestamp": timestamp
    }, to=room)


@socketio.on("create_room")
def on_create_room(data):
    """Creates a new chat room if it does not already exist."""
    room_name = data.get("room_name", "").strip()
    if not room_name:
        return

    conn = get_db()
    try:
        conn.execute("INSERT INTO rooms (name) VALUES (?)", (room_name,))
        conn.commit()
        emit("room_created", {"room": room_name}, broadcast=True)
    except sqlite3.IntegrityError:
        emit("room_exists", {"room": room_name})
    finally:
        conn.close()


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print("=" * 55)
    print("  Oasis Infobyte — Task 5: Real-Time Chat Application")
    print("  Author  : Hashir Shoaib")
    print("  URL     : http://127.0.0.1:5000")
    print("=" * 55)
    socketio.run(app, debug=True, host="127.0.0.1", port=5000)
