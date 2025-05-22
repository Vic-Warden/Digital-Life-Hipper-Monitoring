# Database backend

`database.py` contains the code responsible for communicating with the `MySQL/MariaDB` database. 

Under the hood it uses the `mysql.connector` library, which provides simple but effective functions for communicating with a database.

`database.py` contains the following functions:

```python
__init__() # Responsible for initiating the object.
connect()  # Gets called in the __init__ function and connects to the database.
do_query() # Runs a query on the database
```

