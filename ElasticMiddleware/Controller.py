#pip install fastapi
#pip install uvicorn
#pip install pandas
#pip install aiofiles
#pip install matplotlib
#pip install python-multipart
import http.client

import fastapi
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import pandas as pd
import json
from pydantic import BaseModel
from typing import Optional,Any, Dict, AnyStr, List, Union

import matplotlib.pyplot as plt
import requests
from PIL import Image
import io

app = FastAPI()
es = Elasticsearch("http://localhost:9200")

#----------------------------simple type annotation structure to receive the arbitrary JSON data.-----------------------------------------
class Item(BaseModel):
    requests: List[Any]

#------------------------------------------------------------------------------------------------.-----------------------------------------
@app.get("/my-first-api")
def hello(name = None):

    if name is None: #establecemos conciciones
        text = 'Hello!'

    else:
        text = 'Hello ' + name + '!'

    return text
@app.get("/get-iris")
def get_iris():


    #url ='https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'
    url = "docs.json"
    df = pd.read_json("archivosDePrueba/docs.json")
    print(df)
    return(df.to_json())



#----------------------------------------------------------CRUD OPERATIONS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
    schema = es.indices.get_alias("*")
    #schema = es.indices.get(index="test-index")## python dict with the map of the cluster
    #schema = es.search(index='test-index', filter_path=['hits.hits._*'])
    #ust_indices = [index for index in indices_full_list if not index.startswith(".")] ## remove the objects created by marvel, e.g. ".marvel-date"
    # resp = es.indices.get_alias("*")
    # print(resp['_source'])
    # jsonresp = json.dumps(resp['_source'], indent=4)
    jsonresp = json.dumps(schema, indent=4)
    print(jsonresp)
    #print(schema)
    return schema



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
    uvicorn.run(app, host="0.0.0.0", port=8000)




