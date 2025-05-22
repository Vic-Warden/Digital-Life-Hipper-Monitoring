# Database backend

`database.py` contains the code responsible for communicating with the `MySQL/MariaDB` database. 

Under the hood it uses the `mysql.connector` library, which provides simple but effective functions for communicating with a database.

`database.py` contains the following functions:

```python
__init__() # Responsible for initiating the object.
connect()  # Gets called in the __init__ function and connects to the database.
do_query() # Runs a query on the database
```

### How to execute queries

Queries can be executed using the `do_query()` function. In order to make a query and execute it the user should follow the following example.

```python
query = "SELECT * FROM users WHERE name = %s"
params = ("some_value",)
results = do_query(query, params)
```

The result from this action look like this:
```python

```


I can create new records in the database.
I can read or retrieve existing records from the database.
I can update existing records in the database.
I can delete records from the database.
Data integrity and security are maintained throughout all operations.