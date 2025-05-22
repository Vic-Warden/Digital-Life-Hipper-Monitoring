# Flask Web Application Documentation

## Overview

This is a simple Flask web application that provides the user with simple paths to the dedicated files.

* `/`
* `/home`
* `/login`  

---

## How It Works

### 1. Redirect Root Route and define /home route

Description :

In this code, the redirect_to_home() function redirects users to the home page `/home` when they access the site root `/`
The home() function displays the home.html page when a user accesses the `/home` URL.

```python
# Route for the home page
@app.route('/')
def redirect_to_home():
    # Redirection to the home page by default
    return redirect('/home')

# Home's route
@app.route('/home')
def home():
    # Render the home.html
    return render_template('home.html')
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
Description :

It then gets ran on port 6001
```python
if __name__ == "__main__":
    app.run(debug=True, port=6001)
```