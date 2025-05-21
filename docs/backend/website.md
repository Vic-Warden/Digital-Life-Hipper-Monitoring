# Flask Web Application Documentation

## Overview

This is a simple Flask web application that provides the user with simple paths to the dedicated files.

`/` and `/home`

---

## How It Works

### 1. Redirect Root Route and define /home route
```python
@app.route('/')
def redirect_to_home():
    return redirect('/home')


@app.route('/home')
def home():
    return render_template('home.html')
```

It then gets ran on port 6001
```python
if __name__ == "__main__":
    app.run(debug=True, port=6001)
```