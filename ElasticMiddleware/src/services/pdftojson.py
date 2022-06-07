#PDF to JSON using Python 3+

# package to install
# pip install Fitz
# pip install pymupdf
import fitz
import json

document  = fitz.open('/home/diego/Documentos/git/TFG/ElasticMiddleware/archivosDePrueba/paper339.pdf')

def toJson(document:any):


    text = ''

    with fitz.open(stream=document) as doc:
        for page in doc:
            text+= page.get_text()
    # print(text)


    #json_object = json.dumps(text)

    #print(json_object)
    return text



if __name__ == "__main__":
    a=toJson(document)
    print(a)