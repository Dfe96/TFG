#pip install fastapi
#pip install uvicorn
#pip install pandas
#pip install aiofiles
#pip install matplotlib
#pip install python-multipart
#pip install pymongo
#import http.client


import uvicorn
from fastapi import FastAPI, Request

from elasticsearch import Elasticsearch, helpers
import pandas as pd
import json
from pydantic import BaseModel
from typing import Optional,Any, Dict, AnyStr, List, Union
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
#import matplotlib.pyplot as plt
#import requests
#from PIL import Image
#import io

#MONGO CLIENT CONFIG
from starlette.responses import JSONResponse

try:
    # 27017 is the default port number for mongodb
    uri = 'mongodb://root:1234@localhost/admin'
    connect = MongoClient(uri)
    print("MongoDB cluster is reachable")

    db=connect.myDb
    collection = db.demoCollection




    try:
        print("a")
    except Exception as e:
        raise e





except ConnectionFailure as e:
    print("[+] Database connection error!")
    raise e


#ELASTIC CLIENT CONFIG
app = FastAPI()
es = Elasticsearch("http://localhost:9200")#local ip 127.0.0.1 and resolved ip by docker 172.28.0.X for elasticnetwork













#----------------------------simple type annotation structure to receive the arbitrary JSON data.-----------------------------------------
class Item(BaseModel):
    requests: List[Any]

#-------------------------------------------------CRUD MONGODB ------------------------------------.-----------------------------------------
@app.post("/newUser",status_code=201)
async def createUser(user:str, password: str ):
    try:

        credentials = {
            "user":str(user),
            "password":str(password)

        }
        if collection.count_documents({"user": user}) != 0:#if user exist we send error mesage and break operation

            return JSONResponse (status_code=400, content="user already exist.")
        else:

            collection.insert_one(credentials)
            userfind=collection.find_one({"user": user}, {"_id":0})
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
async def deleteUSer(user:str):
    # collection.deleteOne({name:"Maki"})



    try:


        if collection.count_documents({"user": user}) != 0:#if user exist  send  mesage and performt operation
            userfind=collection.find_one({"user": user}, {"_id":0})
            collection.delete_one({'user': str(user)})
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
async def getUser(user:str):
    try:


        if collection.count_documents({"user": user}) != 0:#if user exist  send  mesage and performt operation
            userfind=collection.find_one({"user": user}, {"_id":0})
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
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(e)
        return str(e)


















@app.get("/testquery")
def getIndice():
    query= es.search(index="test-index",query=[])
    return query
#---------------------------MAIN----------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)




