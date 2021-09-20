import json
import boto3
import os
import uuid

def generate_presigned_url(s3_client, client_method, method_parameters, expires_in):
    """
    Generate a presigned Amazon S3 URL that can be used to perform an action.

    :param s3_client: A Boto3 Amazon S3 client.
    :param client_method: The name of the client method that the URL performs.
    :param method_parameters: The parameters of the specified client method.
    :param expires_in: The number of seconds the presigned URL is valid for.
    :return: The presigned URL.
    """
    url = s3_client.generate_presigned_url(
        ClientMethod=client_method,
        Params=method_parameters,
        ExpiresIn=expires_in
    )
        
    return url

def generateUrl(event, context):
    
    s3_client = boto3.client('s3')
    ClientMethod= 'put_object'
    method_parameters = {'Bucket': 'staircase-tem-imgs-bucket-v1', 'Key': 'unrecognized-img'}
    expires_in = 3600
    
    url = generate_presigned_url(s3_client, ClientMethod, method_parameters, expires_in)
    
    return url
    
    
    
def get_labels(labels):
    
    label_dict = {}
    cnt = 0
    for label in labels['Labels']:
        tem = {'label': label['Name'], 'confidence': str(label['Confidence'])}
        label_dict[str(cnt)] = tem
        cnt+=1
        
    return label_dict

def imgRecognition(event, context):
    
    bucketName= os.environ['BUCKET_NAME'] #'staircase-tem-imgs-bucket-v1'
    key = 'unrecognized-img'
    rek_client = boto3.client('rekognition')
    s3_client = boto3.client('s3')
    dynamo_client = boto3.resource('dynamodb')
    
    tabel_name = os.environ['TableName']
    table = dynamo_client.Table(tabel_name)
    
    try:
        labels = rek_client.detect_labels(
            Image={
            'S3Object': {
                'Bucket': bucketName,
                'Name': key
                }
            }
            )
    except:
        raise Exception ("File format must to be an image")
      
    labels = get_labels(labels)
    id = str(uuid.uuid4())
    labels['PK'] = id
    
    table.put_item(
        Item=labels
    )      
    
    return id
    
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
    
    