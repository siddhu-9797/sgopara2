from flask import Flask, request, redirect, url_for, flash, make_response, render_template, session
from itsdangerous import URLSafeTimedSerializer, BadSignature
import sqlite3
from datetime import timedelta
import json
# Initialize the Flask app and the serializer with a simple secret key
app = Flask(__name__)
app.secret_key = 'iloveyou'  # Simple key to allow flask-unsign usage
serializer = URLSafeTimedSerializer(app.secret_key)
INVITE_TOKEN = "invifnsjdfdsfjuisdnfdwfwrierj21309rjio2jfnwkjdfndskmnfkjdsfihweiofwi13rhj13ipdfdsvkmrfpiejfbndfbwefbwefbdsjfdofue20ofte"


# Database connection function
def get_db_connection():
    conn = sqlite3.connect('portal_b_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database: create the invites table and insert a sample token if not present
def init_db():
    conn = get_db_connection()
    with conn:
        # Create the invites table if it doesn't exist
        conn.execute('''CREATE TABLE IF NOT EXISTS invites (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            token TEXT NOT NULL
                        )''')
        
        # Check if any tokens are already in the table
        existing_token = conn.execute("SELECT token FROM invites LIMIT 1").fetchone()
        
        # If no token exists, insert a sample 128-character token
        if not existing_token:
            sample_token = INVITE_TOKEN  # Replace with your 128-character token
            conn.execute("INSERT INTO invites (token) VALUES (?)", (sample_token,))
            print("Sample 128-character invite token has been inserted into the database.")

# Function to retrieve the 128-character invite token from the database
def get_stored_token():
    conn = get_db_connection()
    stored_token = conn.execute("SELECT token FROM invites ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    return stored_token['token'] if stored_token else None

@app.route('/')
def accept_invite():
    invite_token = request.args.get('token')
    if not invite_token:
        flash("This is an invite-only portal. Get your invitation from the other side.")
        return render_template("error.html", message="This is an invite-only portal. Get your invitation from the other side.")

    # Simulate invite token validation
    if invite_token == INVITE_TOKEN: # Replace with your 128-character token
        # Create session data with 'is_admin' and 'is_super_admin' flags
        session["admin"] = True
        session["super_admin"] = False
        
        # Set the session cookie
        resp = make_response(redirect(url_for('dashboard')))
        
        flash("You have successfully logged in!")
        return resp
    else:
        flash("Sorry, this is not the invite Elon has given you.")
        return render_template("error.html", message="Sorry, this is not the invite Elon has given you.")

@app.route('/dashboard')
def dashboard():
    # Retrieve and verify the session cookie
    session_cookie = request.cookies.get("session")
    admin = False
    super_admin = False
    if not session_cookie:
        return render_template("dashboard.html", message="Access restricted. You need to submit your invitation to the door keeper (/) to get access.")
    try:
        super_admin = session["super_admin"]
    except:
        super_admin = False
    try:
        admin = session["admin"]
    except:
        admin = False

    if admin and super_admin:
        return render_template("treasure_box.html", flag="FLAG{Super_Admin_Access_Granted}")
    if admin and not super_admin:
        return render_template("dashboard.html", message="Hi, Admin! I honor your status. There is a treasue box on Mars which has the flag. The treasue box opens only if you are a super admin.")
    else:
        return render_template("dashboard.html", message="Access restricted. You need to submit your invitation to the door keeper (/) to get access.")




# Error page route
@app.route('/error')
def error_page():
    message = request.args.get('message', "An error occurred.")
    return render_template("error.html", message=message)

if __name__ == '__main__':
    init_db()  # Initialize the database with the invites table and sample token
    app.run(host="0.0.0.0", port=5003)
