import cx_Oracle
from datetime import datetime
import aiofiles
from fastapi import UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from typing import Optional
import uvicorn
from tasks import ReadAndWriteSql, ValueKeyToSql
import warnings
import requests
from pydantic import BaseModel
from typing import Union

warnings.simplefilter("ignore")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LinesTypes(BaseModel):
    keys: list
    values: list


@app.get("/")
async def read_root():
    return {"emoji": "😆"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, limit: int, published: Optional[bool] = None):
    return {"item_id": item_id, "limit": limit, "published": published}


@app.get("/listes")
async def get_listes(pagination: int = 1):
    data = requests.get(
        f"https://api.disneyapi.dev/characters?page={pagination}")
    response = data.json()
    return response["data"]


@app.post("/uploadxlsx/{type}")
async def uploadxlsx(in_file: UploadFile, type):
    new_file = f"files/{str(datetime.now()).replace(' ', '_')}_{in_file.filename}"
    if not new_file.endswith(".xlsx"):
        return
    async with aiofiles.open(new_file, 'w+b') as out_file:
        content = await in_file.read()
        await out_file.write(content)
        response = ReadAndWriteSql(new_file)
    return {"Result": new_file}


@app.post("/uploadlignes")
async def upload_lignes(line:  LinesTypes):
    readResponse = ValueKeyToSql(line.keys, line.values)
    return readResponse


@app.get("/listes/{download_id}")
async def get_listes(download_id):
    data = requests.get(f"https://api.disneyapi.dev/characters/{download_id}")
    response = data.json()
    return response


@app.get("/keys/{concerned}")
async def get__keys(concerned: str = "LFR"):
    # some async function
    return [
        {
            "number": 1,
            "name": "ID LIGNE",
            "db_column": "ID_LIGNE",
            "type": "int",
            "required": False,
        },
        {
            "number": 2,
            "name": "SOA",
            "db_column": "CODE_SOA",
            "type": "str",
            "required": True,
        },
        {
            "number": 3,
            "name": "Code Ministere",
            "db_column": "CODE_MIN",
            "type": "int",
            "required": False,
        },
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
