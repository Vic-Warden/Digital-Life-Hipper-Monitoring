# Database backend

`database.py` contains the code responsible for communicating with the `MySQL/MariaDB` database. 

Under the hood it uses the `mysql.connector` library, which provides simple but effective functions for communicating with a database.

`database.py` contains the following functions:

```python
__init__() # Responsible for initiating the object
connect()  # Gets called in the __init__ function and connects to the database.
do_query() # Runs a query on the database
check_valid_table() # Checks if the queried table is allowed to be queried
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

