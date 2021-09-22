import json
import boto3

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
    
    

    