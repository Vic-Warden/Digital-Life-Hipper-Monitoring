# Import Flask
from flask import Flask, render_template, redirect, request, session

# Create the app Flask
app = Flask(__name__)

# Required to use sessions
app.secret_key = 'your_secret_key_here'

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

# Logout's route with POST methods
@app.route('/logout', methods=['POST'])
def logout():
    
    # ends the user's session
    session.pop('user', None)
    
    # Redirection to the login if logout
    return redirect('/login') 

# Settings' route with GET & POST 
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user' not in session:
        return redirect('/login')
    
    # Retrieves sent data
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        
        if not username or not email:
                # If any field is empty
                message = "Names & e-mails required"
                return render_template('settings.html', user=session['user'], message=message)
        
        # Updates data in the session 
        session['user']['username'] = username
        session['user']['email'] = email
    
        # Render the settings.html
        return render_template('settings.html', user=session['user'], message=message)

# Render the settings.html if the method is GET
    return render_template('settings.html', user=session['user'])

        


# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True, port=6001)