import pandas as pd
import pyexcel

# import requests
# connection = cx_Oracle.connect(user="hr", password="welcome",
#                                dsn="localhost/orclpdb1")
# cursor = connection.cursor()


def toExcel(data, sheet_name='Sheet1'):
    df = pd.DataFrame(data)
    df.to_excel(f"files/{sheet_name}.xlsx", index=None)
    return f"files/{sheet_name}.xlsx"


# data = requests.get("https://olona-captcha.ew.r.appspot.com/api/skills")
# response = data.json()
# res = [elem["attributes"] for elem in response["data"]]
# toExcel(res)

def ReadAndWriteSql(file_name):
    records = pyexcel.iget_records(file_name=file_name)
    for donnes in records:
        value = [str(value).replace(';', '')
                 for key, value in donnes.items()]
        keys = [str(key).replace(';', '') for key, value in donnes.items()]
        # print to cursor.execute
        print((f"""
         INSERT INTO Customers ({', '.join(keys)})
 VALUES ({', '.join(value) });"""))
    return True


def ValueKeyToSql(keys, values):
    print(f"""
         INSERT INTO Customers ({', '.join(keys)})
 VALUES ({', '.join(values) });""")
    return f"""
         INSERT INTO Customers ({', '.join(keys)})
 VALUES ({', '.join(values) });"""
