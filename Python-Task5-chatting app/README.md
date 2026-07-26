# Oasis Infobyte Python Development Internship

## Task 5: Advanced Real-Time Chat Application

A Python-based multi-user web chat application built using Flask and Flask-SocketIO, featuring user authentication, multiple chat rooms, dynamic message history loading, and security transparency.

### Features & Functionality
- **Web-Based GUI:** Interactive chat client served locally via Flask with real-time socket communication.
- **User Authentication:** Registration and login system backed by an SQLite database (`chat_app.db`) with hashed passwords.
- **Multiple Chat Rooms:** Users can create or switch between named rooms dynamically.
- **Persistent Message History:** Past messages for each specific room are stored in SQLite and loaded instantly upon joining.
- **Security Transparency & End-to-End Awareness:**
  - *What is stored:* Usernames, hashed credentials, room names, timestamps, and message bodies are stored locally in plaintext within the `chat_app.db` SQLite database file.
  - *What is NOT encrypted:* Messages are transmitted and stored in plaintext. They are **not** end-to-end encrypted; server administrators or users with local filesystem access can read the message logs.

---

### Tech Stack
- **Language:** Python 3.x
- **Frameworks & Libraries:**
  - `Flask` (Web application framework)
  - `Flask-SocketIO` (Real-time bidirectional event-based communication)
  - `sqlite3` (Built-in Python database management for user records and chat history)
  - `werkzeug.security` (Password hashing utilities)

---

### Setup and Installation Instructions

1. **Navigate to the task directory:**
   ```bash
   cd "infobyte-python task5"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python chat_app.py
   ```

4. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:5000
   ```

---

### Usage Guide
1. **Register** a new account on the registration page.
2. **Login** with your credentials.
3. **Join or create a room** from the sidebar (e.g., "General", "Random", "Tech").
4. **Send messages** in real-time — all connected users in the same room will see them instantly.
5. **Switch rooms** by clicking any room name in the sidebar.
6. **Logout** using the button in the top navigation bar.

---

### Project Structure
```
infobyte-python task5/
├── chat_app.py          # Main Flask + SocketIO server
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── chat_app.db          # SQLite database (auto-created on first run)
├── templates/
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   └── chat.html        # Main chat interface
└── static/
    └── style.css        # Application stylesheet
```

---

### Author
**Hashir Shoaib**
Track: Python Programming | Task 5: Advanced Real-Time Chat Application
Oasis Infobyte Python Internship
