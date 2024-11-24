import base64
import datetime
import string
from flask import Flask, render_template, redirect, url_for, request, session, flash
import jwt
import random
import sqlite3
import re
from functools import wraps

app = Flask(__name__)
app.secret_key = 'portal_a_secret_key'  # Replace with a secure key

# JWT Secret Key and Database Initialization
JWT_SECRET_KEY = "jwt_secret_key"
MFA_PASSWORD = "5wWJXCb..4-yIA!,DJ_pje|6Cmfu2'c"
INVITE_TOKEN = "invifnsjdfdsfjuisdnfdwfwrierj21309rjio2jfnwkjdfndskmnfkjdsfihweiofwi13rhj13ipdfdsvkmrfpiejfbndfbwefbwefbdsjfdofue20ofte"

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('portal_a_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT UNIQUE,
                            attempted INTEGER DEFAULT 0
                        )''')

# Decorator to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("You need to log in to access this page.")
            return redirect(url_for('login_email'))
        return f(*args, **kwargs)
    return decorated_function

# OTP generation function using (timestamp + email) XOR secret_key
def generate_otp(timestamp, email):
    combined_value = ''.join((str(ord(char)) for char in email))  # Combine timestamp and email
    print("Combined Value:", combined_value)
    combined_value = int(combined_value)  # Convert to integer
    print("Combined Value (int):", combined_value)
    otp = timestamp ^ combined_value  # XOR with secret key to get OTP
    print("Actual OTP:", otp)
    return otp  # Return OTP and timestamp for verification and clue display

@app.route('/')
def index():
    return redirect(url_for('login_email'))

# Function to validate email format
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

@app.route('/login_email', methods=['GET', 'POST'])
def login_email():
    if request.method == 'POST':
        email = request.form['email']
        # Validate email format
        if not is_valid_email(email):
            flash("Invalid email address. Please enter a valid email.")
            return redirect(url_for('login_email'))
        timestamp = datetime.datetime.now().strftime('%m%d%Y%H%M')
        email_in_ord = ''.join((str(ord(char)) for char in email))
        
        # Store OTP in the database for the user's email
        
        flash(f"Looks like the SMTP server is busy. OTP has not been sent to {email_in_ord} Perhaps you can guess the OTP instead or play this game xor[.]pw if you are bored.")
        session['email'] = email
        session['timestamp'] = timestamp
        return render_template('login_otp.html', email=email, timestamp=timestamp)
    return render_template('login_email.html')

@app.route('/login_otp', methods=['GET', 'POST'])
def login_otp():
    if request.method == 'POST':
        try:
            timestamp = int(request.form['timestamp'])
            print("Received Timestamp:", timestamp)
            email = request.form['email']
            email = email.lower()
            print("Received Email:", email)

            entered_otp = int(request.form['otp'])
            actual_otp = generate_otp(timestamp, email)
        except Exception as e:
            print(e)
            flash("Bad Request. Try again.")
            return redirect(url_for('login_email'))

        
        if entered_otp == actual_otp:

            session['logged_in'] = True
            session['email'] = email
            # Create entry in the 'users' table if not exists
            conn = get_db_connection()
            user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            if not user:
                conn.execute("INSERT INTO users (email) VALUES (?)", (email,))
                conn.commit()
            conn.close()
            
            # Redirect admin to MFA, regular users to treasure hunt
            if email == 'admin@journeytomars.com':  # Assuming admin's email
                return redirect(url_for('mfa_login'))
            else:
                return redirect(url_for('treasure_hunt'))
        else:
            flash("Invalid OTP. Please try again.")
            return redirect(url_for('login_email'))
    return redirect(url_for('login_email'))

@app.route('/mfa_login', methods=['GET', 'POST'])
def mfa_login():
    print("Session:", session)
    if request.method == 'POST':
            print("Session:", session)
            try:
                is_loggedin = session['logged_in']
                email = session['email']
            except KeyError as e:
                print(e)
                return redirect(url_for('login_email'))

            if session['logged_in'] and (str(session['email'])).lower() == 'admin@journeytomars.com':
                try:
                    mfa_password = request.form['mfa_password']
                except KeyError:
                    flash("Invalid MFA password.")
                    return redirect(url_for('mfa_login'))
                if mfa_password == MFA_PASSWORD:
                    session['mfa_logged_in'] = True
                    return redirect(url_for('generate_invite'))
                else:
                    flash("Invalid MFA password.")
                    return redirect(url_for('mfa_login'))
    try:
        is_loggedin = session['logged_in']
        email = session['email']
    except KeyError:
        return "Only Admins have to pass MFA to login.", 403
    
    return render_template('mfa_login.html')

@app.route('/treasure_hunt', methods=['GET', 'POST'])
@login_required
def treasure_hunt():
    # Check if the user has already attempted

    if request.method == 'POST':
        selected_token = request.form.get('token')
        try:
            # Connect to the database and check if the user has already attempted
            email = session.get('email')
            conn = get_db_connection()
            user = conn.execute("SELECT attempted FROM users WHERE email = ?", (email,)).fetchone()
            conn.close()
            # If the user has already attempted, redirect with a message
            if not user:
                redirect(url_for('login_email'))
            if user and user['attempted'] == 1:
                flash("You lost your golden chance. Everyone gets only one chance.")
                conn.close()
                return redirect(url_for('start_over'))
        except Exception as e:
            print(e)
            return "Internal Server Error.", 500
        
        # Decode token and check for admin role
        try:
            print("Selected Token:", selected_token)
            
            # First Base64 decode
            first_decoding = base64.b64decode(selected_token)
            # Second Base64 decode
            double_decoded_token = base64.b64decode(first_decoding).decode('utf-8')
            
            print("Double Decoded Token (JWT):", double_decoded_token)
            decoded_token = jwt.decode(double_decoded_token, JWT_SECRET_KEY, algorithms=["HS256"])
            print("Decoded Token:", decoded_token)
            
            # Check if the role is 'admin'
            if decoded_token.get('ext') == 'admin':
                flash(f"Woohoo, correct box! Use MFA password   {MFA_PASSWORD}   for admin login.")
                return render_template('treasure_hunt_disabled.html')
            else:
                # Mark the user as having attempted and failed
                conn = get_db_connection()
                # Mark the user as having attempted and failed in the database
                conn.execute("UPDATE users SET attempted = 1 WHERE email = ?", (email,))
                conn.commit()
                conn.close()
                flash("Invalid token. You lost your golden chance. Everyone gets only one chance.")
                return render_template('treasure_hunt_disabled.html')
        
        except Exception as e:
            print(e)
            return "Invalid token. Try again.", 400
            # Mark the user as having attempted and failed
            
    
    email = session['email']
    if email:
        email = email.lower()
    print("Email:", email)
    conn = get_db_connection()
    user = conn.execute("SELECT attempted FROM users WHERE email = ?", (email,)).fetchone()
    print("user:", user)
    conn.close()

    if user and user['attempted'] == 1:
        flash("You lost your golden chance. Everyone gets only one chance.")
        return render_template('treasure_hunt_disabled.html')
    tokens = generate_tokens()
    return render_template('treasure_hunt.html', tokens=tokens)


# Function to generate a random 4-character alphanumeric suffix
def generate_random_suffix(length=4):
    return ''.join(random.choices(string.ascii_letters, k=length))

# Generate tokens with one correct token for the 'admin' role and others with modified 'user' roles
def generate_tokens():
    tokens = []
    for i in range(10):
        role_with_suffix = generate_random_suffix().lower()
        if i == 7:
            # Generate the admin token without any modifications
            token = jwt.encode({'msg': 'this is a REAL token', 'ext': 'admin'}, JWT_SECRET_KEY, algorithm="HS256")
            print("Admin Token", token, i+1)
            token = base64.b64encode(base64.b64encode(token.encode())).decode()
            print("Admin Token Encoded", token)
        else:
            # Generate a user token with a random 4-character suffix appended to the role
            role_with_suffix = generate_random_suffix().lower()
            print("Role with Suffix:", role_with_suffix)
            token = jwt.encode({'msg': 'this is a FAKE token', 'ext': role_with_suffix}, JWT_SECRET_KEY, algorithm="HS256")
            print("User Token", token, i+1)

            # Double Base64 encode the token
            token = base64.b64encode(base64.b64encode(token.encode())).decode()
            print("User Token Encoded", token)

        tokens.append(token)
    return tokens

@app.route('/generate_invite')
def generate_invite():
    try:
        session['mfa_logged_in']
    except KeyError:
        return redirect(url_for('login_email'))

    if session['mfa_logged_in'] != True:
        return redirect(url_for('login_email'))
    
    # Generate invite token and send to Portal B
    invite_token = INVITE_TOKEN
    return render_template('generate_invite.html', invite_token=invite_token)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out. Please log in again.")
    return redirect(url_for('login_email'))

@app.route('/start_over')
def start_over():
    session.clear()
    return redirect(url_for('login_email'))

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5002)
