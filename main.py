import cx_Oracle
from datetime import datetime
import aiofiles
from fastapi import UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from typing import Optional
import uvicorn
from tasks import ReadAndWriteSql
import warnings


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


@app.get("/")
async def read_root():
    return {"emoji": "😆"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, limit: int, published: Optional[bool] = None):
    return {"item_id": item_id, "limit": limit, "published": published}


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


@app.get("/listes")
async def get_listes():
    return


@app.get("/listes/{download_id}")
async def get_listes():
    return


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
