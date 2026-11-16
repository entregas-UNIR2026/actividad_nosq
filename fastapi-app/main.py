from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
import os, requests

app = FastAPI(title="API NoSQL (Segura)")

MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASS = os.getenv("MONGO_PASS", "admin123")
MONGO_HOST = os.getenv("MONGO_HOST", "mongo")

mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:27017/"
mongo = MongoClient(mongo_uri)
db = mongo[os.getenv("MONGO_DATABASE", "tienda")]

class Login(BaseModel): 
    username: str = Field(..., pattern="^[a-zA-Z0-9_]+$")
    password: str = Field(..., pattern="^[a-zA-Z0-9_]+$")

class Pedido(BaseModel): 
    producto: str; cantidad: int

@app.post("/login_mongo")
async def login(req: Login):
    user = db.usuarios.find_one({"username": req.username,
                                 "password": req.password}, {"_id":0})
    if user: return {"msg":"ok"}
    raise HTTPException(status_code=401, detail="Bad creds")

@app.get("/articulos")
def art_search(q: str=""):
    if "$" in q or "{" in q:
        raise HTTPException(status_code=422, detail="Caracteres inválidos")
    return requests.get("http://elasticsearch:9200/articulos/_search",
                        params={"q": q}).json()
