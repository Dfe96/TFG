#pip install fastapi
#pip install uvicorn
#pip install pandas
#pip install aiofiles
#pip install matplotlib
#pip install python-multipart
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from datetime import datetime
from elasticsearch import Elasticsearch
import pandas as pd
import json
from typing import Any, Dict, AnyStr, List, Union

import matplotlib.pyplot as plt
import requests
from PIL import Image
import io

app = FastAPI()
es = Elasticsearch("http://localhost:9200")

#----------------------------simple type annotation structure to receive the arbitrary JSON data.-----------------------------------------
JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]
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


@app.get("/plot-iris")
def plot_iris():

    import pandas as pd
    import matplotlib.pyplot as plt

    url ='https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'
    iris = pd.read_csv(url)

    plt.scatter(iris['sepal_length'], iris['sepal_width'])
    plt.savefig('iris.png')
    file = open('iris.png', mode="rb")

    return StreamingResponse(file, media_type="image/png")
#-------------------------------------------------------------------------------------------#-------------------------------------------------------------------------------------------#-------------------------------------------------------------------------------------------

@app.post("/index", status_code=201)
async def postIndice(doc : Request ):
    resp = es.index(index="test-index", id=1, document=doc)

    return await resp.json()
@app.post("/testing",status_code=201)
async def root(request: Request):
    print(await request.body())
    print("adadaqad")
    print( "u know, for test")
    return {"received_request_body": await request.body()}

@app.get("/index")
def getIndice():
    resp = es.get(index="test-index", id=1)
    print(resp['_source'])
    jsonresp = json.dumps(resp['_source'], indent=4)
    print(jsonresp)
    return resp['_source']
@app.get("/Allindex")
def getIndice():
    schema = es.indices.get(index="*")## python dict with the map of the cluster

    #ust_indices = [index for index in indices_full_list if not index.startswith(".")] ## remove the objects created by marvel, e.g. ".marvel-date"
    # resp = es.indices.get_alias("*")
    # print(resp['_source'])
    # jsonresp = json.dumps(resp['_source'], indent=4)
    jsonresp = json.dumps(schema, indent=4)
    print(jsonresp)
    #print(schema)
    return schema

#---------------------------MAIN----------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)




