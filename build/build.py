import boto3
import datetime
import csv
import gzip
import json
import os
import sqlite3

def handler(event, context):

    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    day = datetime.datetime.now().strftime('%d')
    hour = datetime.datetime.now().strftime('%H')

    if os.path.exists('/tmp/distillery.sqlite3'):
        os.remove('/tmp/distillery.sqlite3')

    db = sqlite3.connect('/tmp/distillery.sqlite3')
    db.execute('CREATE TABLE IF NOT EXISTS distillery (pk INTEGER PRIMARY KEY, source TEXT, updated TEXT, cidr  BLOB, firstip INTEGER, lastip INTEGER, region TEXT, service TEXT, border TEXT, I TEXT, J TEXT, K TEXT, L TEXT, M TEXT, N TEXT, O TEXT, P TEXT, Q TEXT, R TEXT, S TEXT, T TEXT, U TEXT, V TEXT, W TEXT, X TEXT, Y TEXT, Z TEXT)')
    db.execute('CREATE INDEX firstip_index ON distillery (firstip)')
    db.execute('CREATE INDEX lastip_index ON distillery (lastip)')

    s3 = boto3.client('s3')
    files = s3.list_objects(Bucket=os.environ['S3_BUCKET'],Prefix='sources/')['Contents']

    for file in files:
        print(file['Key'])
        fname = file['Key'].split('/')[-1]
        s3.download_file(os.environ['S3_BUCKET'], file['Key'], '/tmp/'+fname)

        with open('/tmp/'+fname) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                db.execute('INSERT INTO distillery (source, updated, cidr, firstip, lastip, region, service, border, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25]))

        f.close()
        os.remove('/tmp/'+fname)

    db.commit()
    db.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/distillery.sqlite3',
        os.environ['S3_BUCKET'],
        'distillery.sqlite3',
        ExtraArgs = {
            'ContentType': "application/x-sqlite3"
        }
    )

    with open('/tmp/distillery.sqlite3', 'rb') as f_in:
        with gzip.open('/tmp/distillery.sqlite3.gz', 'wb') as f_out:
            f_out.writelines(f_in)

    s3.meta.client.upload_file(
        '/tmp/distillery.sqlite3.gz',
        os.environ['S3_RESEARCH'],
        year+'/'+month+'/'+day+'/'+hour+'/distillery.sqlite3.gz',
        ExtraArgs = {
            'ContentType': "application/gzip"
        }
    )

    os.system('ls -lh /tmp')

    return {
        'statusCode': 200,
        'body': json.dumps('Build Distillery')
    }