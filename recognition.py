import json
import boto3
import os
import uuid



def get_labels(labels):
    """
    This fucntion:
    - takes the labels returned from the Rekognition service 
    - Get All the labels with its confidence and put them into dict
    
    return Dictionery of the labels and its confidience 
    example : label_dict['0'] = {'label' : 'car' , 'confidence' : '99.5415718' }
    
    """
    
    
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
