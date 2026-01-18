import boto3
import json
import os
import zipfile

def handler(event, context):
    
    s3 = boto3.client('s3')

    print("Downloading cidr.py and distillery.sqlite3")

    s3.download_file(os.environ['S3_BUCKET'], 'cidr.py', '/tmp/cidr.py')
    s3.download_file(os.environ['S3_BUCKET'], 'distillery.sqlite3', '/tmp/distillery.sqlite3')

    print("Packaging cidr.zip")

    with zipfile.ZipFile('/tmp/cidr.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        zipf.write('/tmp/cidr.py','cidr.py')
        zipf.write('/tmp/distillery.sqlite3','distillery.sqlite3')
    zipf.close()

    print("Uploading cidr.zip")

    s3.upload_file('/tmp/cidr.zip',os.environ['S3_BUCKET'],'cidr.zip')
    s3.upload_file('/tmp/cidr.zip',os.environ['S3_USE1'],'cidr.zip')
    s3.upload_file('/tmp/cidr.zip',os.environ['S3_USW2'],'cidr.zip')

    client = boto3.client('lambda', region_name = 'us-east-1')

    print("Updating "+os.environ['LAMBDA_FUNCTION_USE1'])

    response = client.update_function_code(
        FunctionName = os.environ['LAMBDA_FUNCTION_USE1'],
        S3Bucket = os.environ['S3_USE1'],
        S3Key = 'cidr.zip'
    )

    client = boto3.client('lambda', region_name = 'us-west-2')

    print("Updating "+os.environ['LAMBDA_FUNCTION_USW2'])

    response = client.update_function_code(
        FunctionName = os.environ['LAMBDA_FUNCTION_USW2'],
        S3Bucket = os.environ['S3_USW2'],
        S3Key = 'cidr.zip'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Deploy Distillery')
    }