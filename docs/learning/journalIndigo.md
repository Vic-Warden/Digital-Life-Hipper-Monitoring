# Learning Journal

### Learning story #203

I wanted to find out how I could containerize a `mysql/mariadb` database so that our team can work from their laptops without having to connect to a remote database.

In order to achieve this I used this source from [Medium](https://vijayasimhabr.medium.com/running-mysql-database-server-with-docker-ad10533473c7), they explained in a clear manner how this could be achieved.

They explained that  should have a  `docker-compose.yml`. I created that and also made a Dockerfile which contained the actual mysql installation, this way I could seperate the two and have more control over each part.

```yml
version: '3.8'

services:
  mysql:
    build: .
    ports:
      - "3306:3306"
    env_file:
      - .env
    # volumes:
    #   - ./init.sql:/docker-entrypoint-initdb.d/init.sql
```

I chose to expose port 3306 because it is the default MySQL database port. I also stored the sensitive information such as usernames and passwords inside a `.env` file, which gets passed down onto the container. This prevents users from accessing the password if they have breached the container.

I also chose not to use a volume as I wanted the environment to be purgable very quickly for testing purposes.

Here is the corresponding Dockerfile

```Dockerfile
FROM mariadb:latest

# Expose MySQL port
EXPOSE 3306

# Copy initialization SQL script
COPY ./init.sql /docker-entrypoint-initdb.d/
```

Here we are using the ltest version of the `mariadb` container. We are also copying the `init.sql` file into our `entrypointdb` for our container to run/use it when it gets initialized.

### Learning story #218

I want to know how to securely manage cookies in a database for a web application.

The importance of having secure cookies is to mitigate the risk of unauthorized access, session hijacking, and data leakage

I made use of this thread on [Stackoverflow](https://stackoverflow.com/questions/20314921/how-to-properly-and-securely-handle-cookies-and-sessions-in-pythons-flask)

It highlighted the different ways of managing cookies. And as we were aiming for persistance, we had to use a database for storing our cookies.

The though part is making sure your cookies are securely generated. For this, I made a script whih uses HMAC to securely sign a cookie. It also includes the email of the user and the expiration date in UNIX time.

```python
def create_cookie(self, value: str) -> tuple[bool, str]:
    """
    Create a signed cookie with value and expiration.

    The cookie format is: value|expires|signature

    Returns a tuple (True, cookie) if successful.
    """
    expires = int(time.time()) + WEEK  # Expires in one week
    payload = f"{value}|{expires}"

    signature = hmac.new(self.secret_key, payload.encode(),
                          hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode()

    cookie = f"{payload}|{signature_b64}"
    return (True, cookie)
```

 In order to verify the cookie we use this function.

 ```python
def verify_cookie(self, cookie: str) -> tuple[bool, str]:
    """
    Verify a signed cookie and return the value if valid.

    Raises ValueError if the cookie is invalid or expired.

    The cookie format is: value|expires|signature

    Returns boolean indicating whether the cookie is valid,
    """
    try:
        value, expires, signature_b64 = cookie.rsplit("|", 2)
        payload = f"{value}|{expires}"
        expected_signature = hmac.new(
            self.secret_key, payload.encode(), hashlib.sha256).digest()
        actual_signature = base64.urlsafe_b64decode(signature_b64.encode())

        if not hmac.compare_digest(expected_signature, actual_signature):
            return (False, "Invalid signature")

        if int(expires) < time.time():
            return (False, "Expired cookie")

        return (True, "")
    except Exception as e:
        return (False, f"Invalid cookie: {e}")
 ```

It makes use of the same HMAC package to create a new cookie which it then compares to the old one.

After the cookie is generated, it gets stored in the database for persistent storage. If the server ever goes down, all the sessions are still intact.

### Learning Story #241

For this learning story, I wanted to know how to safely implement an API so that we can performs actions using HTTP(S) using the API.

Its important that the API is protected against stuff like sql injection and other attacks.

I've read [this article](https://stackoverflow.blog/2021/10/06/best-practices-for-authentication-and-authorization-for-rest-apis/) and found a few interesting points to consider while making the API.

1) Always use authentication, for this we use our cookies which are tied to permissions.

2) Always use TLS, we will be using TLS when the final version of the app is ready.

3) Use input sanitization to mediate SQL injection attacks.

I have implemented these changes to make sure that our API is protected against common attacks.


```python
@app.route('/api/upload-pam-data', methods=['GET'])
def upload_pam_data():
    """
    API endpoint to upload PAM data.
    Returns a JSON response with success status and status code.
    """
    token = request.cookies.get('auth_token')
    valid, reason = db.verify_token(token)

    if not valid:
        return {"error": reason}, 401

    patient_id = request.args.get('patient_id')
    pam_data = request.args.get('pam_data')

    if not patient_id or not pam_data:
        return {"error": "Patient ID and PAM data are required"}, 400

    # Assuming pam_data is a JSON string, you might need to parse it
    pam_data = json.loads(pam_data)

    # TODO: Implement the actual upload logic
    # success = db.upload_pam_data(patient_id, pam_data)
    success = True
    if not success:
        return {"error": "Failed to upload PAM data"}, 500

    return {"message": "PAM data uploaded successfully"}, 200
```

## Learning Story #243

I want to know how I can send cookies using Flask to the Front-end (web browser) of the person who wants to login.

To achieve this, I read and followed [this article](https://www.naukri.com/code360/library/handling-cookies-in-flask) which explains it clearly.

I had to make sure to include the following to get it to work.

```python
# Create response and set cookie
response = make_response(redirect('/home'))
response.set_cookie(
    'auth_cookie',            # Cookie name
    cookie_value,             # Cookie value
)

# Redirect to home after form submission
return response
```

