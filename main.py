import uvicorn
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile
import aiofiles
import pyexcel
import time
from datetime import datetime
import warnings
import cx_Oracle

# records = pyexcel.iget_records(file_name="real.xlsx")
# connection = cx_Oracle.connect(user="hr", password="welcome",
#                                dsn="localhost/orclpdb1")
# cursor = connection.cursor()


warnings.simplefilter("ignore")
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"emoji": "😆"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, limit: int, published: Optional[bool] = None):
    return {"item_id": item_id, "limit": limit, "published": published}


@app.post("/uploadxlsx/")
async def uploadxlsx(in_file: UploadFile):
    TITLE = in_file.filename
    NOW = datetime.now()
    date_now = str(NOW).replace(" ", "_")
    if not TITLE.endswith(".xlsx"):
        return
    Timestamp = time.time()
    async with aiofiles.open(f"files/{date_now}_{TITLE}", 'w+b') as out_file:
        content = await in_file.read()
        await out_file.write(content)
        records = pyexcel.iget_records(file_name=f"files/{date_now}_{TITLE}")
        for donnes in records:
            value = [str(value).replace(';', '')
                     for key, value in donnes.items()]
            keys = [str(key).replace(';', '') for key, value in donnes.items()]
            print((f"""
         INSERT INTO Customers ({', '.join(keys)})
 VALUES ({', '.join(value) });"""))
#             cursor.execute((f"""
#          INSERT INTO Customers ({', '.join(keys)})
#  VALUES ({', '.join(value) });"""))

    return {"Result": f"{date_now}_{TITLE}"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
