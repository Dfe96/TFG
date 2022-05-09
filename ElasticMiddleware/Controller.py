#pip install fastapi
#pip install uvicorn
#pip install pandas
#pip install aiofiles
#pip install matplotlib
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from datetime import datetime
from elasticsearch import Elasticsearch
import pandas as pd
import matplotlib.pyplot as plt
import requests
from PIL import Image
import io

app = FastAPI()
es = Elasticsearch("http://localhost:9200")


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

@app.post("/index/", status_code=201)
async def postIndice(doc : Request ):
    resp = es.index(index="test-index", id=1, document=doc)
    return await resp.json()


@app.get("/index")
def getIndice(doc ):
    resp = es.get(index="test-index", id=1)
    return resp

#---------------------------MAIN----------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)





#-------------------------------------------------------------------------------------------
# resp = requests.get('http://127.0.0.1:8000/plot-iris')
# file = io.BytesIO(resp.content)
# im = Image.open(file)
# im.show()