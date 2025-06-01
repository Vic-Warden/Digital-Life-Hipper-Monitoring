# Flask Web Application Documentation

## Overview

This is a simple Flask web application that provides the user with simple paths to the dedicated files.

* `/`
* `/home`
* `/login`  
* `/logout` 
* `/profile`
* `/reset-password`

---

## How It Works

### 1. Redirect Root Route and define /home route

Description :

In this code, the redirect_to_home() function redirects users to the home page `/home` when they access the site root `/`
The `/home` route is protected and accessible only if a user is logged in

```python
# Route for the home page
@app.route('/')
def redirect_to_home():
    
    # Redirection to the home page by default
    return redirect('/home')

# Home's route
@app.route('/home')
def home():
    # if connected
    if 'user' in session:
        
        # Render the home.html
        return render_template('home.html', user=session['user'])
    else:
        # If user is not logged in, redirects to login page
        return redirect('/login')
```

### 2. Request the user & password and define /login route

Description :

This code defines a `/login` route that accepts both `GET` and `POST` methods.
When the method is `POST`, the email and password are retrieved, then the user is redirected to the home page.
If the method is `GET`, the login form login.html is displayed.

```python
# Request the user & the password with GET and POST methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve email and password 
        email = request.args['email']
        password = request.args['password']
        
        # Redirect to home after form submission
        return redirect('/home')
    else:     
        # Render the login.html
        return render_template('login.html')
```

### 2. End a User Session

Description :

The `/logout` route accepts only `POST` requests. It removes the user data from the session  then redirects them to the `login` page

```python
# Logout's route with POST methods
@app.route('/logout', methods=['POST'])
def logout():
    
    # ends the user's session
    session.pop('user', None)
    
    # Redirection to the login if logout
    return redirect('/login') 
```

### 3. Profile

Description :

The `/profile` route can be accessed to the user easily

```python
# Profile' route with GET & POST 
@app.route('/profile', methods=['GET', 'POST'])
def settings():
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
```

### 4. Reset-password

Description :

The `/Reset-password` route accepts only `POST` & `GET` requests. It displays a form allowing users to reset their password.

```python
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
            return render_template('reset_password.html', error="Error")
        
        # Verify that passwords
        if new_password != confirm_password:
            return render_template('reset_password.html', error="Password's Error")
        
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
```

It then gets ran on port 6001
```python
if __name__ == "__main__":
    app.run(debug=True, port=6001)
```