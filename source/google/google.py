import boto3
import datetime
import ipaddress
import json
import os
import requests

def handler(event, context):

    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    day = datetime.datetime.now().strftime('%d')
    hour = datetime.datetime.now().strftime('%H')
    minute = datetime.datetime.now().strftime('%M')
    now = f'{year}-{month}-{day}T{hour}:{minute}Z'

    headers = {'User-Agent': 'Distillery (https://github.com/jblukach/distillery)'}
    r = requests.get('https://www.gstatic.com/ipranges/goog.json', headers=headers)
    print('Download Status Code: '+str(r.status_code))

    if r.status_code == 200:

        output = r.json()

        f = open('/tmp/google.csv', 'w')

        for cidr in output['prefixes']:

            try:
                netrange = ipaddress.IPv4Network(cidr['ipv4Prefix'])
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv4Address(first))
                lastip = int(ipaddress.IPv4Address(last))
                f.write('google,'+now+','+cidr['ipv4Prefix']+','+str(firstip)+','+str(lastip)+',-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')
            except:
                pass

            try:
                netrange = ipaddress.IPv6Network(cidr['ipv6Prefix'])
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv6Address(first))
                lastip = int(ipaddress.IPv6Address(last))
                f.write('google,'+now+','+cidr['ipv6Prefix']+','+str(firstip)+','+str(lastip)+',-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')
            except:
                pass

        f.close()

        s3 = boto3.resource('s3')

        s3.meta.client.upload_file(
            '/tmp/google.csv',
            os.environ['S3_BUCKET'],
            'sources/google.csv',
            ExtraArgs = {
                'ContentType': "text/csv"
            }
        )

    else:
        print('Download Failed')

    return {
        'statusCode': 200,
        'body': json.dumps('Staging Completed')
    }