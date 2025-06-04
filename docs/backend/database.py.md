# Database backend

`database.py` contains the code responsible for communicating with the `MySQL/MariaDB` database. 

Under the hood it uses the `mysql.connector` library, which provides simple but effective functions for communicating with a database.

`database.py` contains the following functions:

```python
__init__()             # Initializes connection and configuration
connect()              # Establishes the MySQL connection
do_query()            # Executes parameterized queries on the database
check_valid_table()   # Checks if a table name is allowed to be queried
check_email()         # Checks if an email is already registered
check_credentials()   # Verifies email and password combination
add_patient()         # Registers a new patient in the system
remove_patient()      # Removes a patient based on their email
create_cookie()       # Creates a new login cookie for a user
verify_cookie()       # Verifies a cookie's validity and retrieves the associated user
remove_cookie()       # Deletes a cookie from the database
change_user_email()   # Changes the users email based on session token
```

### How to execute queries

Queries can be executed using the `do_query()` function. In order to make a query and execute it the user should follow the following example.

```python
db = Database(
    host="host",
    port=port,
    user="user",
    password="password",
    database="database"
)

query = "SELECT * FROM users WHERE name = %s"
params = ("some_value",)
results = db.do_query(query, params)
```

The result from this action look like this:
```python
list[tuple] | None
```

* A list of tuples containing the result set.
* None if the query fails or if there is no connection to the database.

### Data integrity and security

In order to make sure that the integrity and security of the database is enforced, multiple best practices have been applied to the code.

**Uses parameterized queries**
```python
cursor.execute(query, params)
```

* This prevents SQL injection, ensuring that values in params are properly escaped and interpreted as data, not SQL commands.
* Supports integrity by preventing malformed or malicious queries that could harm your data.

**Query execution is wrapped in a try/except/finally block**

```python
try:
    ...
except Error as e:
    ...
finally:
    cursor.close()
```

* Prevents unhandled exceptions from leaving the connection or cursor in an undefined state.
* Helps maintain transactional safety in multi-query operations.

**Connection health check**

```python
if not self._connection:
    print("No connection to the database.")
    return None
```

* Prevents trying to query a disconnected or invalid database, which avoids corruption or inconsistent reads/writes.

### Cookie Management

The class integrates a Cookie handler from a separate module to manage login sessions.

```python
self.cookie = Cookie()
```

**Cookie Functions**

`create_cookie(email: str):` Creates and stores a cookie for a given email.

`verify_cookie(cookie: str):` Validates a cookie and returns associated user info.

`remove_cookie(cookie: str):` Deletes the cookie from the database.

These functions enable session handling for users while maintaining secure authentication flows.

### Account Management

**Account Functions**

`change_user_email(token: str, new_email: str):` Changes the users email based on the session token.


### Patient Data Access

`get_patient_details(patient_id: int) -> dict | None`

Gets a full summary of a patient’s:

- PAM data records (`data` table)
- Linked devices (`device` table)
- Personal goals (`goal` table)

Returns `None` if no information is found.

`get_patients(therapeut_id: int) -> list[dict] | None`

Returns a list of patients linked to a therapist:

```python
[
  { "id": 1, "name": "John Doe", "email": "john@example.com" },
  ...
]
```