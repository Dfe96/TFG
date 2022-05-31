#pip install fastapi
#pip install uvicorn
#pip install pandas
#pip install aiofiles
#pip install matplotlib
#pip install python-multipart
#pip install pymongo
#import http.client


import uvicorn

from elasticsearch import Elasticsearch
import pandas as pd
import json
from fastapi import FastAPI, HTTPException, Depends, Request,status
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
#import matplotlib.pyplot as plt
#import requests
#from PIL import Image
#import io

#MONGO CLIENT CONFIG
from starlette.responses import JSONResponse

try:
    app = FastAPI()
    origins = [
        "http://localhost:9200",
        "http://localhost:27017",
        "http://localhost:4200"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #Mongo CLIENT CONFIG
    uri = 'mongodb://root:1234@172.18.0.2/admin'# 27017 is the default port number for mongodb
    connect = MongoClient(uri)
    db=connect.myDb
    collection = db.demoCollection
    # db = connect["User"]
    #ELASTIC CLIENT CONFIG

    es = Elasticsearch("http://localhost:9200")#local ip 127.0.0.1 and resolved ip by docker 172.28.0.X for elasticnetwork



except ConnectionFailure as e:
    print("[+] Database connection error!")
    raise e












#----------------------------Here starts MAIN.py-----------------------------------------


#----------------------------simple type annotation structure to receive the arbitrary JSON data.-----------------------------------------
class Item(BaseModel):
    requests: List[Any]

#-------------------------------------------------CRUD MONGODB ------------------------------------.-----------------------------------------
@app.get("/")
def read_root(current_user:User = Depends(get_current_user)):
    return {"data":"Hello OWrld"}

@app.post('/register')
def create_user(request:User):
    try:
        hashed_pass = Hash.bcrypt(request.password)
        user_object = dict(request)
        user_object["password"] = hashed_pass

        print(str(user_object["username"]))
        if collection.count_documents({"username": str(user_object["username"])}) != 0:#if user exist we send error mesage and break operation

            return JSONResponse (status_code=400, content="username already exist.")
        else:

            user_id = collection.insert_one(user_object)
            print(request)
            return JSONResponse (status_code=201,
                                 content={"res":"created"}
                                 )
    except Exception as e:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(e)
        return str(e)






@app.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends()):
    try:
        user = collection.find_one({"username":request.username})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with this {request.username} username')
        if not Hash.verify(user["password"],request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
        access_token = create_access_token(data={"sub": user["username"] })
        return JSONResponse(status_code=200,
                            content={"access_token": access_token, "token_type": "bearer"})

    except HTTPException as e:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        raise e


@app.post("/newUser",status_code=201)
async def createUser(username:str, password: str ):
    try:

        credentials = {
            "username":str(username),
            "password":str(password)

        }
        if collection.count_documents({"username": username}) != 0:#if user exist we send error mesage and break operation

            return JSONResponse (status_code=400, content="username already exist.")
        else:

            collection.insert_one(credentials)
            userfind=collection.find_one({"username": username}, {"_id":0})
            print("colis\n")
            print(userfind)
            return JSONResponse (status_code=201,
                                 content=userfind
                                 )
    except Exception as e:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(e)
        return str(e)

@app.get("/allusers")
def getUsers():
    allusers=[]
    list(allusers)
    col=collection.find({}, {"_id":0})
    for x in col :
        allusers.append(x)

        print(x)

    print(allusers)
    return allusers

@app.delete("/users")
async def deleteUSer(username:str):
    # collection.deleteOne({name:"Maki"})



    try:


        if collection.count_documents({"username": username}) != 0:#if user exist  send  mesage and performt operation
            userfind=collection.find_one({"username": username}, {"_id":0})
            collection.delete_one({'username': str(username)})
            # result.deleted_count


            print("colis\n")
            print(userfind)
            return JSONResponse (status_code=200,
                                 content=userfind
                                 )



        else:


            return JSONResponse (status_code=400, content="user doesnt exist.")
    except Exception as e:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(e)
        return str(e)



@app.get("/users")
async def getUser(username:str):
    try:


        if collection.count_documents({"username": username}) != 0:#if user exist  send  mesage and performt operation
            userfind=collection.find_one({"username": username}, {"_id":0})
            print("colis\n")
            print(userfind)
            return JSONResponse (status_code=200,
                                 content=userfind
                                 )



        else:


            return JSONResponse (status_code=400, content="username doesnt exist.")
    except Exception as e:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(e)
        return str(e)













#-------------------------------------------------REACHING MIDDLEWARE CALLS  ------------------------------------.-----------------------------------------
# /my-first-api call it is just a mock call to see if we can reach the middleware
@app.get("/my-first-api")
def hello(name = None):

    if name is None: #establecemos conciciones
        text = 'Hello!'

    else:
        text = 'Hello ' + name + '!'

    return text
@app.get("/get-iris")
def get_iris():



    url = "docs.json"
    df = pd.read_json("../archivosDePrueba/docs.json")
    print(df)
    return(df.to_json())



#----------------------------------------------------------CRUD Elasticsearch --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.post("/newIndex",status_code=201)
async def root(request: Request,index, id: Any = 1):
    try:
        print(await request.json())
        print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        print( "u know, for test")
        #return {"received_request_body": "skipIs : "+str(index) +" limit "+ str(id)+"    "+ str(await request.body())}
        j=await request.json()
        jsonresponse={str(index): j}#generamos un onjeto json que concatenamos con la request
        print(jsonresponse)
        resp = es.index(index=index, id=id, document=jsonresponse)
        return  jsonresponse

    except Exception as e:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(e)
        return str(e)


@app.get("/index")
def getIndice(index: str, id: Any):
    resp = es.get(index=index, id=id)
    print(resp['_source'])
    jsonresp = json.dumps(resp['_source'], indent=4)
    print(jsonresp)
    return resp

@app.get("/allindex")
def getIndice():

    schema = es.indices.get_alias().keys()

    allindexlist=[]
    for value in schema:
        print(value)
        allindexlist.append(value)
    print(allindexlist)

    return str(allindexlist)



@app.delete("/index")
def getIndice(index: str, id: Any):
    resp = es.delete(index=index, id=id)
    return resp

@app.put("/index")
async def root(request: Request,index, id: Any = 1):
    try:
        print(await request.json())
        print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        print( "u know, for test")
        #return {"received_request_body": "skipIs : "+str(index) +" limit "+ str(id)+"    "+ str(await request.body())}
        j=await request.json()
        jsonresponse={str(index): j}#generamos un onjeto json que concatenamos con la request
        print(jsonresponse)
        resp = es.update(index=index, id=id, doc=jsonresponse)


        return  resp

    except Exception as e:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(e)
        return str(e)


















@app.get("/testquery")
def getIndice():
    query= es.search(index="test-index",query=[])
    return query

#----------------------------Here ENDS MAIN.py-----------------------------------------

#---------------------------MAIN----------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)




