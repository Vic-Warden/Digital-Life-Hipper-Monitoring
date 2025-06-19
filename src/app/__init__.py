from flask import request, jsonify
import os  # Import os for .env centralized settings
# Import Flask
from flask import Flask, render_template, redirect, request, session, make_response, jsonify
from database import Database
import json
from dotenv import load_dotenv


# Import Werkzeug for have the possibility to hash a password
from werkzeug.security import generate_password_hash

from anomaly_detection import calculate_median, detect_anomalies

# Create the app Flask
app = Flask(__name__)

# Database instance

load_dotenv()  # This will look for a .env file in the current directory

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
        user_query = "SELECT id FROM User WHERE cookies = %s"
        result = db.do_query(user_query, (cookie,))

        if result:
            # Result returns a legitmate row containing the cookie
            device_id = result[0][0]  # result is a list of tuples
            data_query = "SELECT * FROM hipperdb.Data WHERE device_id = %s"
            patient_data = db.do_query(data_query, (device_id,))
            calculated_data = db.calculate_average_data(patient_data)

            return render_template('home.html', patient=patient_data, calculated=calculated_data, preferences=db.get_user_preferences(cookie))
        else:
            return redirect('/login')
    else:
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


@app.route('/admin/logout', methods=['GET'])
def admin_logout():
    # Clear the session
    cookie = request.cookies.get('auth_cookie')
    db.remove_cookie(cookie)

    # Redirection to the login if logout
    return redirect('/admin/login')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    cookie = request.cookies.get('auth_cookie')
    if not db.verify_cookie(cookie)[0]:
        return redirect('/login')

    if request.method == "POST":
        # Expecting JSON
        data = request.get_json()
        if not data:
            return jsonify({"error": "An error has occurred, please contact your administrator."}), 400

        # Extract values
        dark_mode = data.get('dark_mode', 0)
        large_font = data.get('large_font', 0)
        language = data.get('language', 'nl')

        # Validate language
        if language.lower() not in ["nl", "en"]:
            return jsonify({"error": "Language not supported."}), 400

        # Convert to boolean
        dark_mode = (dark_mode == 1)
        large_font = (large_font == 1)

        # Save preferences
        db.set_user_preferences(cookie, dark_mode, large_font, language)

        return jsonify({
            "msg": "Settings updated successfully.",
            "preferences": {
                "dark_mode": dark_mode,
                "large_font": large_font,
                "language": language
            }
        }), 200

    # If GET request, render the settings page
    return render_template("settings.html", preferences=db.get_user_preferences(cookie))

# Handle the admin settings


@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings():
    cookie = request.cookies.get('auth_cookie')
    if db.verify_cookie(cookie)[0]:

        if request.method == "POST":
            # Expecting JSON
            data = request.get_json()
            if not data:
                return jsonify({"error": "An error has occurred, please contact your administrator."}), 400

            # Extract values
            dark_mode = data.get('dark_mode', 0)
            large_font = data.get('large_font', 0)
            language = data.get('language', 'nl')

            # Validate language
            if language.lower() not in ["nl", "en"]:
                return jsonify({"error": "Language not supported."}), 400

            # Convert to boolean
            dark_mode = (dark_mode == 1)
            large_font = (large_font == 1)

            # Save preferences
            db.set_user_preferences(cookie, dark_mode, large_font, language)

            return jsonify({
                "msg": "Settings updated successfully.",
                "preferences": {
                    "dark_mode": dark_mode,
                    "large_font": large_font,
                    "language": language
                }
            }), 200

        return render_template("admin_settings.html", preferences=db.get_user_preferences(cookie))

    return redirect("/admin/login")


# Handle the admin login page


@app.route('/admin/home', methods=['GET', 'POST'])
def admin_login():
    # if connected
    cookie = request.cookies.get('auth_cookie')
    if db.verify_cookie(cookie)[0]:
        # Render the home.html
        return render_template('admin_home.html', preferences=db.get_user_preferences(cookie))
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

    therapist_id = db.therapist_id_from_cookie(cookie)
    print(therapist_id)

    # list with patients
    patient_details = db.get_patients(therapist_id)
    print(patient_details)

    if not patient_details:
        return render_template('admin_patients.html', patients=[], message="No patients found.")

    return render_template('admin_patients.html', patients=patient_details)


@app.route('/api/add-patient', methods=['POST'])
def admin_add_patient():
    # Get data from form
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if user is authorized to add patient
    cookie = request.cookies.get('auth_cookie')
    valid, _ = db.verify_cookie(cookie)

    if not valid:
        return redirect('/admin/login')

    # Validate required data
    if not all([name, email, password, cookie]):
        return "Missing required fields", 400

    if not db.check_email(email):
        return "Email already exists", 400

    # Call DB logic to insert the patient
    success = db.add_patient(name, email, password, cookie)

    if not success:
        return "Failed to add patient", 400

    return redirect('/admin/patients')


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
    return render_template('admin_patient_details.html', patient=patient_details, preferences=db.get_user_preferences(cookie))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login_page():
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


@app.route('/change-email', methods=['POST'])
def change_email():
    cookie = request.cookies.get('auth_cookie')
    valid, user_data = db.verify_cookie(cookie)

    if not valid:
        return redirect('/login')

    # Retrieve the new email from the form
    new_email = request.form.get('new_email', '').strip()

    if not new_email:
        return render_template('profile.html', user=session['user'], message="Email cannot be empty.", preferences=db.get_user_preferences(cookie))

    # Update the user's email in the database
    db.change_user_email(cookie, new_email)

    # Update the session data
    session['user']['email'] = new_email

    return render_template('profile.html', user=session['user'], message="Email updated successfully.", preferences=db.get_user_preferences(cookie))


@app.route('/api/get-patients', methods=['GET'])
def get_patients():
    """
    API endpoint to retrieve all patients.
    Returns a JSON response with patient data and status code.
    """
    # TODO: Change this to auth_token
    # TODO: Change this to auth_token
    # TODO: Change this to auth_token
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
    # TODO: Change this to auth_token
    # TODO: Change this to auth_token
    # TODO: Change this to auth_token
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


@app.route('/api/detect-anomalies', methods=['POST'])
def detect_anomalies_endpoint():
    token = request.cookies.get('auth_token')
    valid, reason = db.verify_auth_token(token)
    if not valid:
        return {"error": reason}, 401

    data = request.get_json()

    patient_id = data.get('patient_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    threshold_percent = data.get('threshold_percent', 20)

    if not patient_id or not start_date or not end_date:
        return {"error": "patient_id, start_date, and end_date are required"}, 400

    connection = db.get_connection()
    cursor = connection.cursor()

    query = f"""
        SELECT
            DATE(timestamp) AS date,
            steps
        FROM Data
        JOIN Device ON Data.device_id = Device.id
        WHERE Device.patient_id_device = {patient_id}
          AND DATE(timestamp) BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY date ASC;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    activity_data = [{"date": row[0], "steps": row[1]} for row in results]
    steps_list = [entry['steps'] for entry in activity_data]

    median = calculate_median(steps_list)
    anomalies = detect_anomalies(activity_data, median, threshold_percent)

    for anomaly in anomalies:
        anomaly['date'] = anomaly['date'].strftime('%Y-%m-%d')

    cursor.close()
    connection.close()

    return {
        'median_steps': median,
        'threshold_percent': threshold_percent,
        'anomalies': anomalies
    }, 200


@app.route('/anomaly-form')
def anomaly_form():
    return render_template('form.html')


@app.route('/api/upload-day-data', methods=['POST'])
def upload_day_data():
    """
    API endpoint to upload PAM day-level data.
    Expects POST form data including auth_token, patient_id, pam_data, and optionally device_mac_addr.
    """
    token = request.form.get('auth_token')
    valid, reason = db.verify_auth_token(token)
    if not valid:
        return jsonify({"error": reason}), 401

    mac_address = request.form.get('mac_address')
    pam_data = request.form.get('pam_data')

    if not mac_address or not pam_data:
        return jsonify({"error": "Mac Address and PAM data are required"}), 400

    try:
        pam_data = json.loads(pam_data)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in pam_data"}), 400

    success = db.upload_day_data(mac_address, pam_data)
    if not success:
        return jsonify({"error": "Failed to upload PAM data"}), 500

    return jsonify({"message": "PAM day data uploaded successfully"}), 200


@app.route('/api/upload-minute-data', methods=['POST'])
def upload_minute_data():
    """
    API endpoint to upload PAM minute-level data.
    Expects POST form data including auth_token, patient_id, pam_data, and optionally device_mac_addr.
    """
    token = request.form.get('auth_token')
    valid, reason = db.verify_auth_token(token)
    if not valid:
        return jsonify({"error": reason}), 401

    mac_address = request.form.get('mac_address')
    pam_data = request.form.get('pam_data')

    if not mac_address or not pam_data:
        return jsonify({"error": "Mac Address and PAM data are required"}), 400

    try:
        pam_data = json.loads(pam_data)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in pam_data"}), 400

    success = db.upload_minute_data(mac_address, pam_data)
    if not success:
        return jsonify({"error": "Failed to upload PAM data"}), 500

    return jsonify({"message": "PAM minute data uploaded successfully"}), 200


# @app.route('/api/last-update-period', methods=['GET'])
# def last_update_period():
#     """
#     API endpoint to get the last update period for a patient.
#     Returns a JSON response with the last update period and status code.
#     """
#     # TODO: Change this to auth_token
#     # TODO: Change this to auth_token
#     # TODO: Change this to auth_token
#     cookie = request.cookies.get('auth_cookie')
#     valid, user_data = db.verify_cookie(cookie)

#     if not valid:
#         return {"error": "Invalid or expired cookie"}, 401

#     device_mac_addr = request.args.get('device_mac_addr')
#     if not device_mac_addr:
#         return {"error": "Device MAC address is required"}, 400

#     last_update = db.get_last_update_period(device_mac_addr)
#     if not last_update:
#         return {"error": "No updates found for this patient"}, 404

#     return {"last_update": last_update}, 200

@app.route('/log/<mac_address>', methods=['GET'])
def get_log(mac_address):
    mac = mac_address.upper()
    log_entry = db.get_log_for_mac(mac)
    if not log_entry:
        return jsonify({}), 200
    return jsonify({
        "last_activity_pull": log_entry.get("last_activity_pull"),
        "last_day_data_pull": log_entry.get("last_day_data_pull")
    }), 200


@app.route('/log/<mac_address>', methods=['POST'])
def update_log(mac_address):
    mac = mac_address.upper()

    if not request.is_json:
        return {"error": "Expected JSON payload"}, 400
    data = request.get_json()

    activity = data.get("activity")
    day_data = data.get("day_data")

    if activity is None or day_data is None:
        return {"error": "Missing 'activity' or 'day_data' fields"}, 400

    success = db.update_log_timestamps(mac, activity, day_data)
    if not success:
        return {"error": "Failed to update log"}, 500

    return {"message": "Log updated"}, 200


@app.route('/routine-form', methods=['GET', 'POST'])
def routine_form():
    if request.method == 'POST':
        data = request.get_json()
        patient_id = data.get("patient_id")

        if not patient_id:
            return {"error": "Missing patient_id"}, 400

        patient_query = "SELECT name FROM User WHERE id = %s"
        patient_result = db.do_query(patient_query, (patient_id,))
        patient_name = patient_result[0][0] if patient_result else "Unknown"

        usual_slots = db.get_usual_active_slots(patient_id)

        disruptions = db.get_disruptions(patient_id, usual_slots)

        return {
            "patient_name": patient_name,
            "usual_slots": usual_slots,
            "disruptions": disruptions
        }, 200

    return render_template("routine_form.html")


# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=6001)
