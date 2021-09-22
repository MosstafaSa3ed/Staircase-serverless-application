import boto3
import os

def getLabels(event, context):
    
    info_id = event['queryStringParameters']['id']
    
    dynamo_client = boto3.resource('dynamodb')
    tabel_name = os.environ['TableName']
    table = dynamo_client.Table(tabel_name)
    
    res = table.get_item(Key={'PK': info_id})
    
    if 'Item' in res:

       return res['Item']

    else:

       return {
           'statusCode': '404',
           'body': 'Not found'
       }
    
    return res
    