import boto3
import datetime
import hashlib
import json
import os
import requests
import zipfile

def hasher(filename):
    
    BLOCKSIZE = 65536
    sha256_hasher = hashlib.sha256()

    with open(filename,'rb') as h:
        buf = h.read(BLOCKSIZE)
        while len(buf) > 0:
            sha256_hasher.update(buf)
            buf = h.read(BLOCKSIZE)
    h.close()

    sha256 = sha256_hasher.hexdigest().upper()

    return sha256

def handler(event, context):
    
    s3 = boto3.client('s3')

    s3.download_file(
        os.environ['DEPLOY_BUCKET'],
        'search.py',
        '/tmp/search.py'
    )

    s3.download_file(
        os.environ['DEPLOY_BUCKET'],
        'distillery.sqlite3',
        '/tmp/distillery.sqlite3'
    )

    ssm = boto3.client('ssm')

    status = ssm.get_parameter(
        Name = os.environ['SSM_PARAMETER_STATUS'],
        WithDecryption = False
    )

    sha256 = hasher('/tmp/distillery.sqlite3')

    if status['Parameter']['Value'] != sha256:

        with zipfile.ZipFile('/tmp/distillery.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:

            zipf.write(
                '/tmp/search.py',
                'search.py'
            )

            zipf.write(
                '/tmp/distillery.sqlite3',
                'distillery.sqlite3'
            )

        zipf.close()

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

        ssm = boto3.client('ssm')

        token = ssm.get_parameter(
            Name = os.environ['SSM_PARAMETER_GIT'], 
            WithDecryption = True
        )

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer '+token['Parameter']['Value'],
            'X-GitHub-Api-Version': '2022-11-28'
        }

        year = datetime.datetime.now().strftime('%Y')
        month = datetime.datetime.now().strftime('%m')
        day = datetime.datetime.now().strftime('%d')
        epoch = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

        data = '''{
            "tag_name":"v'''+str(year)+'''.'''+str(month)+str(day)+'''.'''+str(epoch)+'''",
            "target_commitish":"main",
            "name":"distillery",
            "body":"The sha256 verification hash for the distillery.sqlite3 file is: '''+sha256+'''",
            "draft":false,
            "prerelease":false,
            "generate_release_notes":false
        }'''

        response = requests.post(
            'https://api.github.com/repos/jblukach/distillery/releases',
            headers=headers,
            data=data
        )

        print(response.json())

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer '+token['Parameter']['Value'],
            'X-GitHub-Api-Version': '2022-11-28',
            'Content-Type': 'application/octet-stream'
        }

        params = {
            "name":"distillery.zip"
        }

        url = 'https://uploads.github.com/repos/jblukach/distillery/releases/'+str(response.json()['id'])+'/assets'

        with open('/tmp/distillery.zip', 'rb') as f:
            data = f.read()
        f.close()

        response = requests.post(url, params=params, headers=headers, data=data)

        print(response.json())

        ssm.put_parameter(
            Name = os.environ['SSM_PARAMETER_STATUS'],
            Description = 'Distillery Status Change',
            Value = sha256,
            Type = 'String',
            Overwrite = True
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Distillery Deployed')
    }