import os # Import os for .env centralized settings
# Import Flask
from flask import Flask, render_template, redirect, request, session, make_response
from database import Database

# Import Werkzeug for have the possibility to hash a password
from werkzeug.security import generate_password_hash

# Create the app Flask
app = Flask(__name__)

# Database instance

db = Database(
    host=os.getenv('MYSQL_HOST'),
    port=int(os.getenv('MYSQL_PORT')),
    user=os.getenv('MYSQL_ROOT_USER'),
    password=os.getenv('MYSQL_ROOT_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE')
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


@app.route('/logout', methods=['GET'])
def logout():
    # Clear the session
    cookie = request.cookies.get('auth_cookie')
    db.remove_cookie(cookie)

    # Redirection to the login if logout
    return redirect('/login')

# Profile' route with GET & POST


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    cookie = request.cookies.get('auth_cookie')
    if db.verify_cookie(cookie)[0]:

        if request.method == "POST":
            # TODO: Add logic for handling settings updates
            #  - Change email
            #  - Change password etc...
            pass

        return render_template("settings.html")

    return redirect("/login")

# Handle the admin login page


@app.route('/admin/home', methods=['GET', 'POST'])
def admin_login():
    # if connected
    cookie = request.cookies.get('auth_cookie')
    if db.verify_cookie(cookie)[0]:
        # Render the home.html
        return render_template('admin_home.html')
    else:
        # If user is not logged in, redirects to login page
        return redirect('/admin/login')


@app.route('/admin/patients', methods=['GET'])
def admin_patient_list():
    # Verify the cookie
    cookie = request.cookies.get('auth_cookie')
    valid, user_data = db.verify_cookie(cookie)

    if not valid:
        return redirect('/admin/login')

    # Fetch patient details from the database
    # TODO: Fix database
    # patient_details = db.get_patients()

    patient_details = {
        "name": "John Doe",
        "email": "john.doe@gmail.com",
    }

    if not patient_details:
        return "Patients not found", 404

    # Render the patient details page
    return render_template('admin_patients.html', patient=patient_details)


@app.route('/admin/patients/<patient_id>', methods=['GET'])
def admin_patient_details(patient_id):
    # Verify the cookie
    cookie = request.cookies.get('auth_cookie')
    valid, user_data = db.verify_cookie(cookie)

    if not valid:
        return redirect('/admin/login')

    # Fetch patient details from the database
    patient_details = db.get_patient_details(patient_id)

    if not patient_details:
        return "Patient not found", 404

    # Render the patient details page
    return render_template('admin_patient_details.html', patient=patient_details)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login_page():
    if request.method == 'POST':
        # Retrieve email password & the therapist
        email = request.form.get('email')
        password = request.form.get('password')

        if db.check_admin_credentials(email, password):
            # Create secure cookie
            success, cookie_value = db.create_cookie(email)

            print(f"Cookie created: {cookie_value}")

            if not success:
                return "Failed to create cookie", 500

            # Create response and set cookie
            response = make_response(redirect('/admin/home'))
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
        return render_template('admin_login.html', error="Invalid credentials. Please try again.")
    else:
        # Render the admin_login.html
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


@app.route('/change-email', methods=['POST'])
def change_email():
    cookie = request.cookies.get('auth_cookie')
    valid, user_data = db.verify_cookie(cookie)

    if not valid:
        return redirect('/login')

    # Retrieve the new email from the form
    new_email = request.form.get('new_email', '').strip()

    if not new_email:
        return render_template('profile.html', user=session['user'], message="Email cannot be empty.")

    # Update the user's email in the database
    db.change_user_email(cookie, new_email)

    # Update the session data
    session['user']['email'] = new_email

    return render_template('profile.html', user=session['user'], message="Email updated successfully.")


@app.route('/api/get-patients', methods=['GET'])
def get_patients():
    """
    API endpoint to retrieve all patients.
    Returns a JSON response with patient data and status code.
    """
    cookie = request.cookies.get('auth_cookie')
    valid, user_data = db.verify_cookie(cookie)

    if not valid:
        return {"error": "Invalid or expired cookie"}, 401

    patients = db.get_patients()
    if not patients:
        return {"error": "No patients found"}, 404

    return {"patients": patients}, 200


@app.route('/api/get-patient-data', methods=['GET'])
def get_patient_data():
    """
    API endpoint to retrieve patient data.
    Returns a JSON response with patient data and status code.
    """
    cookie = request.cookies.get('auth_cookie')
    valid, user_data = db.verify_cookie(cookie)

    if not valid:
        return {"error": "Invalid or expired cookie"}, 401

    patient = request.args.get('patient_id')
    if not patient:
        return {"error": "Patient ID is required"}, 400

    patient_data = db.get_patient_details(patient)
    if not patient_data:
        return {"error": "Patient not found"}, 404

    return patient_data, 200


# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True, port=6001)
