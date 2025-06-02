# Import Flask
from flask import Flask, render_template, redirect, request, session, make_response
from database import Database

# Import Werkzeug for have the possibility to hash a password
from werkzeug.security import generate_password_hash

# Create the app Flask
app = Flask(__name__)

# Required to use sessions
app.secret_key = 'your_secret_key_here'

# Database instance
db = Database(
    host="localhost",
    port=3306,
    user="root",
    password="superstronkrootpassword",
    database="hipperdb"
)

# Route for the home page


@app.route('/')
def redirect_to_home():

    # Redirection to the home page by default
    return redirect('/home')

# Home's route


@app.route('/home')
def home():
    # if connected
    cookie = request.cookies.get('auth_cookie')
    if db.verify_cookie(cookie)[0]:
        # Render the home.html
        return render_template('home.html')
    else:
        # If user is not logged in, redirects to login page
        return redirect('/login')

# Request the user & the password with GET and POST methods


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        # Retrieve email password & the therapist
        email = request.form.get('email')
        password = request.form.get('password')

        if db.check_credentials(email, password):
            # Create secure cookie
            success, cookie_value = db.create_cookie(email)

            print(f"Cookie created: {cookie_value}")

            if not success:
                return "Failed to create cookie", 500

            # Create response and set cookie
            response = make_response(redirect('/home'))
            response.set_cookie(
                'auth_cookie',            # Cookie name
                cookie_value,             # Cookie value
                max_age=60*60*24*7,       # 1 week
                httponly=True,            # Prevent JS access (XSS)
                secure=True,              # Only over HTTPS
                samesite='Lax'            # Protect from CSRF somewhat
            )

            # Redirect to home after form submission
            return response
        return render_template('login.html', error="Invalid credentials. Please try again.")
    else:
        # Render the login.html
        return render_template('login.html')

# Logout's route with POST methods


@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session
    cookie = request.cookies.get('auth_cookie')
    db.remove_cookie(cookie)

    # Redirection to the login if logout
    return redirect('/login')

# Profile' route with GET & POST


@app.route('/profile', methods=['GET', 'POST'])
def settings():
    cookie = request.cookies.get('auth_cookie')
    valid, user_data = db.verify_cookie(cookie)

    if 'user' not in session:
        return redirect('/login')

    # Retrieves sent data
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        therapist = request.form.get('therapist', '').strip()

        if not username or not email:
            # If any field is empty
            message = "Names, e-mails and the therapist is required"
            return render_template('profile.html', user=session['user'], message=message)

        # Updates data in the session
        session['user']['username'] = username
        session['user']['email'] = email
        session['user']['therapist'] = therapist

        # Render the settings.html
        return render_template('profile.html', user=session['user'], message=message)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # Retrieve admin credentials
        username = request.form.get('username')
        password = request.form.get('password')

        # Check admin credentials
        if username == 'admin' and password == 'admin123':
            # Set session variable for admin
            session['admin'] = True
            return redirect('/admin/dashboard')
        else:
            return render_template('admin_login.html', error="Invalid admin credentials.")

    # Render the admin login page
    return render_template('admin_login.html')

# Reset-password's route with GET & POST


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':

        # Retrieve form
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Every field is full
        if not email or not new_password or not confirm_password:
            return render_template('reset_password.html', error="Please fill in all the fields.")

        # Verify that passwords
        if new_password != confirm_password:
            return render_template('reset_password.html', error="Passwords do not match.")

        # Verify the user
        user_exists = db.check_user_exists(email)
        if not user_exists:
            return render_template('reset_password.html', error="User not found.")

        # Hash the new password
        hashed_password = generate_password_hash(new_password)

        # Update the new password
        db.update_user_password(email, hashed_password)

        return redirect('/login')

    # rentder the reset_password.html
    return render_template('reset_password.html')


# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True, port=6001)
