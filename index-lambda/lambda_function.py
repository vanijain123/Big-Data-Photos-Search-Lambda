import json
import boto3
from elasticsearch import Elasticsearch
import time 
from datetime import datetime

def lambda_handler(event, context):
    
    # bucket = event['Records'][0]['s3']['bucket']['name'];
    bucket='photos-hw2'
    # file= event['Records'][0]['s3']['object']['key'];
    file='photos/mario.png'
    # TODO implement
    # s3 = boto3.resource('s3')
    # obj = s3.Object("photos-hw2", file)
    # body = obj.get()['Body'].read()  
    labels=[]
    #lambda modification

    try:
        rekognition_client = boto3.client('rekognition')
        response = rekognition_client.detect_labels(
            Image={'S3Object': {
                'Bucket': bucket,
                'Name': file
        }}, MaxLabels=10)
        print(response['Labels'])
        labels = [label['Name'] for label in response['Labels']]
    except e:
        print("exception",e)
    es = Elasticsearch(
        'https://search-photos-pc56kr7gnw4icfiqn5y6eufsmu.us-east-1.es.amazonaws.com',
        http_auth = ('ESmaster','HW2@pass')
    )
   
    # query ={
    #     "query":{
    #                 "match": {
    #                   "Cuisine"  :cuisine
    #                   }
    #     }
    # }
    now = datetime.now()
    body={"objectKey": file,"bucket": bucket,
    "createdTimestamp": now.strftime("%Y-%m-%dT%H:%M:%S"),
    "labels": labels}
    # print(body)
    # res=es.index(index="photos", id=file, body=body)
    # print(res['result'])
    result = es.search(index="photos", size=3)
    print(result)
    

        


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
