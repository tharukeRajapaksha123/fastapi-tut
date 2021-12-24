from fastapi import FastAPI
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File

app = FastAPI() 


@app.get("/")
def hello():
    return {"workstatys" : "fine"}


@app.post("/get-file") 
async def root(file:UploadFile = File(...)):
    return {"file_name" : file.filename}