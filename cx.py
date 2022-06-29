# query.py

import cx_Oracle

# Establish the database connection

cx_Oracle.init_oracle_client(
    lib_dir=r"C:\Program Files\PremiumSoft\Navicat Premium 16\instantclient_11_2")  # if used with navicat
connection = cx_Oracle.connect(
    user="system", password="oracle", dsn="localhost:49161/xe")


# Obtain a cursor
cursor = connection.cursor()

# Data for binding
manager_id = 145
first_name = "Peter"

# Execute the query
sql = """SELECT * FROM HR.employees WHERE manager_id = :mid"""
cursor.execute(sql, mid=manager_id)

# Loop over the result set
for row in cursor:
    print(row)
