from flask import Flask, render_template, redirect


app = Flask(__name__)


@app.route('/')
def redirect_to_home():
    return redirect('/home')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True, port=6001)
