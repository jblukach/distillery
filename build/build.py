import boto3
import csv
import json
import os
import sqlite3

def handler(event, context):

    if os.path.exists('/tmp/distillery.sqlite3'):
        os.remove('/tmp/distillery.sqlite3')

    db = sqlite3.connect('/tmp/distillery.sqlite3')
    db.execute('CREATE TABLE IF NOT EXISTS distillery (pk INTEGER PRIMARY KEY, source TEXT, service TEXT, region TEXT, cidr  BLOB, firstip INTEGER, lastip INTEGER)')
    db.execute('CREATE INDEX firstip_index ON distillery (firstip)')
    db.execute('CREATE INDEX lastip_index ON distillery (lastip)')

    s3 = boto3.client('s3')
    files = s3.list_objects(Bucket=os.environ['S3_BUCKET'])['Contents']

    for file in files:
        print(file['Key'])
        s3.download_file(os.environ['S3_BUCKET'], file['Key'], '/tmp/'+file['Key'])

        with open('/tmp/'+file['Key']) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                db.execute('INSERT INTO distillery (source, service, region, cidr, firstip, lastip) VALUES (?, ?, ?, ?, ?, ?)', (row[0], row[1], row[2], row[3], row[4], row[5]))

        f.close()
        os.remove('/tmp/'+file['Key'])

    db.commit()
    db.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/distillery.sqlite3',
        os.environ['UP_BUCKET'],
        'distillery.sqlite3',
        ExtraArgs = {
            'ContentType': "application/x-sqlite3"
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Build Distillery')
    }