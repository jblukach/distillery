import boto3
import json
import os
import zipfile

def handler(event, context):
    
    s3 = boto3.client('s3')

    s3.download_file(
        os.environ['DEPLOY_BUCKET'],
        'search.py',
        '/tmp/search.py'
    )

    s3.download_file(
        os.environ['DOWN_BUCKET'],
        'distillery.sqlite3',
        '/tmp/distillery.sqlite3'
    )

    with zipfile.ZipFile('/tmp/distillery.zip', 'w') as zipf:

        zipf.write(
            '/tmp/search.py',
            'search.py'
        )

        zipf.write(
            '/tmp/distillery.sqlite3',
            'distillery.sqlite3'
        )

    s3.upload_file(
        '/tmp/distillery.zip',
        os.environ['DEPLOY_BUCKET'],
        'distillery.zip'
    )

    client = boto3.client('lambda')

    response = client.update_function_code(
        FunctionName = os.environ['LAMBDA_FUNCTION'],
        S3Bucket = os.environ['DEPLOY_BUCKET'],
        S3Key = 'distillery.zip'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Distillery Deployed')
    }