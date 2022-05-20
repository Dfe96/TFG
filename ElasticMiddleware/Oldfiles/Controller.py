#pip install fastapi
#pip install uvicorn
#pip install pandas
#pip install aiofiles
#pip install matplotlib
#pip install python-multipart
#pip install pymongo
import http.client


import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import pandas as pd
import json
from pydantic import BaseModel
from typing import Optional,Any, Dict, AnyStr, List, Union
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import bson.json_util as json_util
#import matplotlib.pyplot as plt
#import requests
#from PIL import Image
#import io

#MONGO CLIENT CONFIG

try:
    # 27017 is the default port number for mongodb
    uri = 'mongodb://root:1234@127.28.0.2/admin'
    connect = MongoClient(uri)
    print("MongoDB cluster is reachable")

    db = connect.myDb
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
es = Elasticsearch("http://172.28.0.2:9200")#local ip 127.0.0.1 and resolved ip by docker 172.28.0.X for elasticnetwork













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

        collection.insert_one(credentials)
    except Exception as e:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(e)
        return str(e)

@app.get("/users")
def getUsers():
    cursor = collection.find()


    allusers={"Paper": 3}
    a = {"cars": 1, "houses": 2, "schools": 3, "stores": 4}
    b = {"Pens": 1, "Pencils": 2, "Paper": 3}
    for record in cursor:
        a.update(record),

        print (allusers)
    dict(allusers)
    print(allusers)





    a.update(b)
    print(a)
    return a
















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




