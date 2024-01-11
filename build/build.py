import boto3
import csv
import datetime
import hashlib
import json
import os
import sqlite3

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

    if os.path.exists('/tmp/distillery.sqlite3'):
        os.remove('/tmp/distillery.sqlite3')

    db = sqlite3.connect('/tmp/distillery.sqlite3')
    db.execute('CREATE TABLE IF NOT EXISTS distillery (pk INTEGER PRIMARY KEY, source TEXT, service TEXT, region TEXT, cidr  BLOB, firstip INTEGER, lastip INTEGER)')
    db.execute('CREATE INDEX firstip_index ON distillery (firstip)')
    db.execute('CREATE INDEX lastip_index ON distillery (lastip)')

    count = 0

    s3 = boto3.client('s3')
    files = s3.list_objects(Bucket=os.environ['S3_BUCKET'])['Contents']

    for file in files:
        print(file['Key'])
        s3.download_file(os.environ['S3_BUCKET'], file['Key'], '/tmp/'+file['Key'])

        with open('/tmp/'+file['Key']) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                db.execute('INSERT INTO distillery (source, service, region, cidr, firstip, lastip) VALUES (?, ?, ?, ?, ?, ?)', (row[0], row[1], row[2], row[3], row[4], row[5]))
                count += 1

        f.close()
        os.remove('/tmp/'+file['Key'])

    db.commit()
    db.close()

    f = open('/tmp/distillery.sha256','w')
    f.write(hasher('/tmp/distillery.sqlite3'))
    f.close()

    f = open('/tmp/distillery.updated','w')
    f.write(str(datetime.datetime.now()))
    f.close()

    f = open('/tmp/distillery.count','w')
    f.write(str(count))
    f.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/distillery.sqlite3',
        os.environ['UP_BUCKET'],
        'distillery.sqlite3',
        ExtraArgs = {
            'ContentType': "application/x-sqlite3"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/distillery.sha256',
        os.environ['UP_BUCKET'],
        'distillery.sha256',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/distillery.updated',
        os.environ['UP_BUCKET'],
        'distillery.updated',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/distillery.count',
        os.environ['UP_BUCKET'],
        'distillery.count',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Build Distillery')
    }