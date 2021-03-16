import json
import boto3
from elasticsearch import Elasticsearch
#from requests_aws4auth import AWS4Auth

def lambda_handler(event, context):
    client = boto3.client('lex-runtime')
    print(event)
    query = event["q"]
    
    print("Query : ", query)
    
    response = client.post_text(
        botName='photoSearchBot',
        botAlias='search',
        userId='user',
        inputText=query
    )
    
    try:
        slots = response["slots"]
        
    except Exception as r:
        slots = {}
    
    relevant_keys = []
    if slots:
        print("slots : ", slots)
        
        search_labels = [val for val in slots.values() if val]
        
        print("search_labels : ", search_labels)
    
        es_auth = ("ESmaster", "Hw@2pass")
        es = Elasticsearch(hosts=["https://search-photos-pc56kr7gnw4icfiqn5y6eufsmu.us-east-1.es.amazonaws.com"], http_auth=es_auth)
        
        # res = es.search(
        #     index="photos", 
        #     body={
        #         "query": {
        #             "terms": {
        #                 "labels": search_labels,
        #                 "boost": 1.0
        #             }
        #         }
        #     }
        # )

        # print("Got {} Hits".format(res['hits']['total']))
        # for hit in res['hits']['hits']:
        #     relevant_keys.append(hit['_source']['objectKey'])

    return {
        'statusCode': 200,
        #'body': json.dumps({"images": relevant_keys})
        'body': json.dumps(slots)
    }
