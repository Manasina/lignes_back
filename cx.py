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

# Execute the query
# sql = """SELECT * FROM HR.employees WHERE manager_id = :mid"""
# cursor.execute(sql, mid=manager_id)

# Loop over the result set
# for row in cursor:
#     print(row)


# Insert
# sql = """SELECT * FROM HR.employees WHERE manager_id = :mid"""
sql = "INSERT INTO HR.COUNTRIES (COUNTRY_ID, COUNTRY_NAME, REGION_ID) VALUES ('MG','MADAGASCAR', 2)"
cursor.execute(sql)
connection.commit()
