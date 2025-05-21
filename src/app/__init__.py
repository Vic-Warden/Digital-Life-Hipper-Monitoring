# Import Flask
from flask import Flask, render_template, redirect, request

# Create the app Flask
app = Flask(__name__)

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

# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True, port=6001)
