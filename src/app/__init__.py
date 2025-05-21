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
    if 'user' in session:
        # Render the home.html
        return render_template('home.html', user=session['user'])
    else:
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

# Logout's route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    # Redirection to the login 
    return redirect('/login') 

# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True, port=6001)
