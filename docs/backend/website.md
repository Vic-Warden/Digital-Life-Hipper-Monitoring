
# Flask Web Application Documentation

## Overview

This is a Flask web application that provides routes for users and admin access, login/logout, profile management, password reset, and email change. It uses session and cookie-based authentication with a MySQL-backed custom database class.

### Available Routes:

* `/`
* `/home`
* `/login`  
* `/logout` 
* `/settings`
* `/reset-password`
* `/change-email`
* `/admin/home`
* `/admin/login`
* `/admin/patients`
* `/api/routine-disruption`
* `/api/add-patient`

---

## 1. App Initialization

The application is initialized using Flask and Werkzeug for password hashing. A custom `Database` class is used for database operations.

The database variables get loaded through a .env environment file. This enables a more secure way of storing passwords and endpoint addresses.

```python
import os  # Import os for .env centralized settings
# Import Flask
from flask import Flask, render_template, redirect, request, session, make_response
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
```

---

## 2. Root and Home Routes

Redirects the root `/` to `/home`. The `/home` route checks for a valid authentication cookie. 
Besides that the patient data is being exposed and made ready for use. Same for the calculated data which will be shown in the historical graphs on the home page.

```python
@app.route('/')
def redirect_to_home():
    return redirect('/home')

@app.route('/home')
def home():
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

            return render_template('home.html', patient=patient_data, calculated=calculated_data)
        else:
            return redirect('/login')
    else:
        return redirect('/login')

```

---

## 3. Login

Handles user login with secure cookie creation.

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if db.check_credentials(email, password):
            success, cookie_value = db.create_cookie(email)
            if not success:
                return "Failed to create cookie", 500

            response = make_response(redirect('/home'))
            response.set_cookie('auth_cookie', cookie_value, max_age=60*60*24*7, httponly=True, secure=True, samesite='Lax')
            return response

        return render_template('login.html', error="Invalid credentials. Please try again.")
    return render_template('login.html')
```

---

## 4. Logout

Removes the auth cookie and redirects to login.

```python
@app.route('/logout', methods=['POST'])
def logout():
    cookie = request.cookies.get('auth_cookie')
    db.remove_cookie(cookie)
    return redirect('/login')
```

---

## 5. Settings (Profile)

Displays and updates user profile information.

```python
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    cookie = request.cookies.get('auth_cookie')
    valid, user_data = db.verify_cookie(cookie)

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        therapist = request.form.get('therapist', '').strip()

        if not username or not email:
            message = "Names, e-mails and the therapist is required"
            return render_template('profile.html', user=session['user'], message=message)

        session['user']['username'] = username
        session['user']['email'] = email
        session['user']['therapist'] = therapist

        return render_template('profile.html', user=session['user'], message=message)
```

---

## 6. Reset Password

Allows users to reset their password securely.

```python
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not email or not new_password or not confirm_password:
            return render_template('reset_password.html', error="Please fill in all the fields.")
        if new_password != confirm_password:
            return render_template('reset_password.html', error="Passwords do not match.")
        if not db.check_user_exists(email):
            return render_template('reset_password.html', error="User not found.")

        hashed_password = generate_password_hash(new_password)
        db.update_user_password(email, hashed_password)
        return redirect('/login')

    return render_template('reset_password.html')
```

---

## 7. Change Email

Allows users to update their email address.

```python
@app.route('/change-email', methods=['POST'])
def change_email():
    cookie = request.cookies.get('auth_cookie')
    valid, user_data = db.verify_cookie(cookie)

    if not valid:
        return redirect('/login')

    new_email = request.form.get('new_email', '').strip()
    if not new_email:
        return render_template('profile.html', user=session['user'], message="Email cannot be empty.")

    db.change_user_email(cookie, new_email)
    session['user']['email'] = new_email

    return render_template('profile.html', user=session['user'], message="Email updated successfully.")
```

---

## 8. Admin Login

Admin users can access their own login on /admin/login.

```python
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if db.check_admin_credentials(email, password):
            success, cookie_value = db.create_cookie(email)
            if not success:
                return "Failed to create cookie", 500

            response = make_response(redirect('/admin/home'))
            response.set_cookie('auth_cookie', cookie_value, max_age=60*60*24*7, httponly=True, secure=True, samesite='Lax')
            return response

        return render_template('admin_login.html', error="Invalid credentials. Please try again.")
    return render_template('admin_login.html')
```

---

## 9. Admin Home

Admin users (therapists) can access their home page and view patient details on /admin/home

```python
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
```

## 10. Admin Patients

Admin users (therapists) can see there patient a list of their patients.

```python
@app.route('/admin/patients', methods=['GET'])
def admin_patient_list():
    # Verify the cookie
    cookie = request.cookies.get('auth_cookie')
    valid, user_data = db.verify_cookie(cookie)

    if not valid:
        return redirect('/admin/login')
    
    therapist_id = db.therapist_id_from_cookie(cookie)
    print(therapist_id)

    # Extended list with 6 patients
    patient_details = db.get_patients(therapist_id)
    print(patient_details)

    if not patient_details:
        return "Patients not found", 404

    return render_template('admin_patients.html', patients=patient_details)
```

## 11. Patients

`get_patients(therapist_id: int)` returns a list of all the patients connected to a therapist.

```python
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
```

## 12. Patient Data

`get_patient_details(patient_id: int)` returns the details from a single patient.

```python
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
```

## 13. Upload PAM Data

`upload_pam_data()` is an API endpoint reserved for uploading movement data in JSON format to the server.

It checks the cookies to make sure the user is authenticated and then uses the request.args.get() function to receive the patient_id and the pam_data.

The upload pam data route also uses an authentication token (otherwise known as an api token) and can only communicate if that token is provided with the request.

```python
@app.route('/api/upload-pam-data', methods=['GET'])
def upload_pam_data():
    """
    API endpoint to upload PAM data.
    Returns a JSON response with success status and status code.
    """a
    token = request.cookies.get('auth_token')
    valid, reason = db.verify_auth_token(token)
    if not valid:
        return {"error": reason}, 401

    patient_id = request.args.get('patient_id')
    pam_data = request.args.get('pam_data')
    device_mac_addr = request.args.get('device_mac_addr')

    if not patient_id or not pam_data:
        return {"error": "Patient ID and PAM data are required"}, 400

    # Assuming pam_data is a JSON string, you might need to parse it
    pam_data = json.loads(pam_data)

    # TODO: Implement the actual upload logic
    success = db.upload_pam_data(patient_id, pam_data)
    success = True
    if not success:
        return {"error": "Failed to upload PAM data"}, 500

    return {"message": "PAM data uploaded successfully"}, 200
```

## 14. Get the last update period

## 📄 Device Update Period Functions

### 🔍 `get_last_update_period`

Gets the last time at which the data was updated.

```python
def get_last_update_period(self, device_mac_addr: str):
    """
    ### Get the last update period for a device based on its MAC address.

    Returns the last update period as a string.
    """
    query = "SELECT last_update_period FROM Device WHERE device_mac_addr = %s;"
    params = (device_mac_addr,)
    result = self.do_query(query, params, fetch=True)

    if result and len(result) > 0:
        return result[0][0]
    return None
```

## 15. Admin logout

Removes the auth cookie and redirects to admin login.

```python
@app.route('/admin/logout', methods=['POST'])
def logout():
    cookie = request.cookies.get('auth_cookie')
    db.remove_cookie(cookie)
    return redirect('/admin/login')
```

## 16. Token Authentication

Checks the authentication token of the base station for communication with the api.

```python
token = request.cookies.get('auth_token')
valid, reason = db.verify_auth_token(token)
if not valid:
    return {"error": reason}, 401
```

## 16. Log date time
update and get last date and time when data was pulled form sensor by looking at the mac address
### Get date time
```python
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
```

### 17. Update date time
```python
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
```

Find functions used for implementation under [database.py](database.py.md).

## 18. Routine Analysis & Anomaly Detection

Detects if a patient has not been active in his usual time slots for a certain number of consecutive days

**Méthode :** `POST`
**Payload :**

```json
{
  "patient_id": 12
}
```

**Réponse :**

```json
{
  "disruptions": [
    {
      "hour_slot": 10,
      "inactive_days": ["2025-06-10", "2025-06-11", "2025-06-12"]
    }
  ]
}
```

## 18. Add Patient

This route adds a new patient into the database.

```python
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

    # Call DB logic to insert the patient
    success = db.add_patient(name, email, password, cookie)

    if not success:
        return "Failed to add patient", 400

    return redirect('/admin/patients')
```

## 19. Running the App

```python
if __name__ == "__main__":
    app.run(debug=True, port=6001)
```