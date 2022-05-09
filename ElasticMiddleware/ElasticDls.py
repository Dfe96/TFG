#pip install elasticsearch-dsl


from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch()

s = Search(using=client)

s = Search().using(client).query("match", any="data")
response = s.execute()
print(response.hits.total)
for h in response:
    print(h.title, h.body)


