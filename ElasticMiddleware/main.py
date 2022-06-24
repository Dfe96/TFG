#pip install fastapi
#pip install uvicorn
#pip install pandas
#pip install aiofiles
#pip install matplotlib
#pip install python-multipart
#pip install pymongo
#import http.client

from elasticsearch import Elasticsearch
import pandas as pd
import json
from fastapi import FastAPI, HTTPException, Depends, Request, status, File, UploadFile
from typing import Any, List

from fastapi.security import OAuth2PasswordRequestForm
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from fastapi.middleware.cors import CORSMiddleware
from src.models.user import *
from src.models.token import *

from src.services.jwttoken import create_access_token
from src.services.hashing import *
from src.services.oauth import get_current_user
import requests
import re
import time
from src.services.pdftojson import toJson
from datetime import datetime
from starlette.responses import JSONResponse
# import matplotlib.pyplot as plt
# import requests
# from PIL import Image
# import io
#MONGO CLIENT CONFIG





try:

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #Mongo CLIENT CONFIG
    uri = 'mongodb://root:1234@db/admin'# 27017 is the default port number for mongodb
    connect = MongoClient(uri)
    db=connect.myDb
    collection = db.demoCollection
    #ELASTIC CLIENT CONFIG
    #local ip 127.0.0.1 and resolved ip by docker 172.28.0.X for elasticnetwork
    es = Elasticsearch("http://es01:9200")
    #this url will be used in Request petitions, it is similar kind of request as Elasticsearch APIPython but atttacking directly to Elastic API
    urlelastic = 'http://es01:9200/'


except ConnectionFailure as e:
    print("[+] Database connection error!")
    raise e














# ----------------------------Here starts MAIN.py-----------------------------------------


# ----------------------------simple type annotation structure to receive the arbitrary JSON data.-----------------------------------------
class Item(BaseModel):
    requests: List[Any]



@app.get("/")
def read_root(current_user: User = Depends(get_current_user)):
    return {"data": "Hello OWrld"}

# -------------------------------------------------CRUD MONGODB ------------------------------------.-----------------------------------------
@app.post('/register')
def create_user(request: User):
    try:
        hashed_pass = Hash.bcrypt(request.password)
        user_object = dict(request)
        user_object["password"] = hashed_pass

        print(str(user_object["username"]))
        if collection.count_documents({"username": str(
                user_object["username"])}) != 0:  # if user exist we send error mesage and break operation

            return JSONResponse(status_code=400, content="username already exist.")
        else:

            user_id = collection.insert_one(user_object)
            print(request)
            return JSONResponse(status_code=201,
                                content={"res": "created"}
                                )
    except Exception as e:
        print("Error:")
        print(e)
        return str(e)


@app.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends()):
    try:
        user = collection.find_one({"username": request.username})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No user found with this {request.username} username')
        if not Hash.verify(user["password"], request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Wrong Username or password')
        access_token = create_access_token(data={"sub": user["username"]})
        return JSONResponse(status_code=200,
                            content={"access_token": access_token, "token_type": "bearer"})

    except HTTPException as e:
        print("Error:")

        raise e

@app.get("/allusers")
def get_users():
    allusers = []
    list(allusers)
    col = collection.find({}, {"_id": 0})
    for x in col:
        allusers.append(x)

        print(x)

    print(allusers)
    return allusers


@app.delete("/users")
async def delete_user(username: str):
    # collection.deleteOne({name:"Maki"})

    try:

        if collection.count_documents(
                {"username": username}) != 0:  # if user exist  send  mesage and performt operation
            userfind = collection.find_one({"username": username}, {"_id": 0})
            collection.delete_one({'username': str(username)})
            # result.deleted_count

            print("colis\n")
            print(userfind)
            return JSONResponse(status_code=200,
                                content=userfind
                                )



        else:

            return JSONResponse(status_code=400, content="user doesnt exist.")
    except Exception as e:
        print("Error")
        print(e)
        return str(e)


@app.get("/users")
async def getUser(username: str):
    try:

        if collection.count_documents(
                {"username": username}) != 0:  # if user exist  send  mesage and performt operation
            userfind = collection.find_one({"username": username}, {"_id": 0})
            print("colis\n")
            print(userfind)
            return JSONResponse(status_code=200,
                                content=userfind
                                )



        else:

            return JSONResponse(status_code=400, content="username doesnt exist.")
    except Exception as e:
        print("Error")
        print(e)
        return str(e)


# ----------------------------------------------------------CRUD Elasticsearch --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.post("/newIndex", status_code=201)
async def post_index(index: Any, request: Request, id: Any = 1):
    try:
        print(await request.json())
        print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("u know, for test")
        j = await request.json()
        print("index is", index)
        print("request is", j)
        print("id is", id)
        resp = es.index(index=str(index), id=str(id), document=j)
        return index

    except Exception as e:
        print("Error")
        print(e)
        raise e


@app.post("/pdftoJson", status_code=201)
async def post_indexpdf(index: Any,author: str = "ElBarto", id: str =" 1", file: bytes = File(), ):
    try:
        request = toJson(file)#llamamos a toJson que usa la libreria FLITZ para extraer la información del pdf
        timestamp=time.time()
        dt_object = datetime.fromtimestamp(timestamp)

        #llamamos a re.(regresion library) con objeto de eliminar caracteres especiales.EX:Recuperaci\´on\\nde Informaci\´on -->Recuperacion\nde Informacion
        my_new_string = re.sub('[^a-zA-Z0-9 \n\.]', '', request)
        jsonresponse = {
                        "date":dt_object,
                        "author":author,
                        "text": my_new_string}
        print("index is", index)
        print("id is", id)
        print("jsonresponse is", jsonresponse)
        print(
            "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        print("u know, for test")
        resp = es.index(index=index, id=id, document=jsonresponse)
        return JSONResponse(status_code=201,
                            content=request
                            )

    except Exception as e:
        print("Error")
        print(e)
        raise e


@app.get("/index")
def get_Index(index: str, id: str):
    resp = es.get(index=index, id=id)
    print(resp['_source'])
    jsonresp = json.dumps(resp['_source'], indent=4)
    print(jsonresp)
    return resp


@app.get("/allindex")
def get_Indexes():
    schema = es.indices.get_alias().keys()

    allindexlist = []
    for value in schema:
        print(value)
        allindexlist.append(value)
    print(allindexlist)

    return allindexlist


@app.get("/mapping")
def get_Mapp(index: str):
    path = urlelastic + index + '/_mapping'

    r = requests.get(path)
    return (json.loads(r.text))
@app.get("/search")
def search(index: str):
    try:
        path = urlelastic + index + '/_search'

        r = requests.get(path)

        response=json.loads(r.text)
        responsecode=r.status_code

        if(responsecode!=200):
            return (json.loads(r.text))
        #
        # for x in response['hits']['hits'] :
        #     print(x['_id'])
        # print(response)
        return (json.loads(r.text))
    except Exception as e:
        print("Error")
        print(e)
        raise e
@app.get("/searchMatch")
def get_match(index: str,matchRequested: str):
    try:
        path = urlelastic + index + '/_search'
        body={"query": { "match": {"text": matchRequested}}}
        r = requests.post(path,json=body)
        responsecode=r.status_code
        if(responsecode!=200):
            return JSONResponse(status_code=responsecode,
                                content=json.loads(r.text)
                                )
        return (json.loads(r.text))
    except Exception as e:
        print("Error")
        print(e)
        raise e


@app.delete("/deleteindex",status_code=200)
def delete_Index(index: str):
    try:
        path = urlelastic +index
        r = requests.delete(path)

        txtresponse=(json.loads(r.text))
        return JSONResponse(status_code=200,
                            content=txtresponse
                            )
    except Exception as e:
        print("Error")
        print(e)
        raise e


@app.delete("/indexbyid")
def delete_IndexById(index: str, id: str):
    resp = es.delete(index=index, id=id)
    return resp
@app.post("/searchinIndex")
def search_inIndex(index: str,body:Any):
    path=urlelastic+index+"/_search"
    #-----------------------------------------------------------------------------REVISAR
    return

@app.put("/index")
async def root(request: Request, index, id: Any = 1):
    try:
        print(await request.json())
        print(
            "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        print("u know, for test")
        # return {"received_request_body": "skipIs : "+str(index) +" limit "+ str(id)+"    "+ str(await request.body())}
        j = await request.json()
        jsonresponse = {str(index): j}  # generamos un onjeto json que concatenamos con la request
        print(jsonresponse)
        resp = es.update(index=index, id=id, doc=jsonresponse)

        return resp

    except Exception as e:
        print("Error")
        print(e)
        return str(e)


@app.get("/testquery")
def getIndice():
    query = es.search(index="test-index", query=[])
    return query


# ----------------------------Here ENDS MAIN.py-----------------------------------------