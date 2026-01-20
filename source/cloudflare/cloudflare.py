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

    ipv4 = requests.get('https://www.cloudflare.com/ips-v4', headers=headers)
    print('Download Status Code: '+str(ipv4.status_code))

    ipv6 = requests.get('https://www.cloudflare.com/ips-v6', headers=headers)
    print('Download Status Code: '+str(ipv6.status_code))

    if ipv4.status_code == 200 and ipv6.status_code == 200:

        f = open('/tmp/'+os.environ['SOURCE']+'.csv', 'w')
        f.write('A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z\n')

        data = ipv4.text
        output = list(data.splitlines())

        for cidr in output:
            netrange = ipaddress.IPv4Network(cidr)
            first, last = netrange[0], netrange[-1]
            firstip = int(ipaddress.IPv4Address(first))
            lastip = int(ipaddress.IPv4Address(last))
            f.write(os.environ['SOURCE']+','+now+','+cidr+','+str(firstip)+','+str(lastip)+',-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')

        data = ipv6.text
        output = list(data.splitlines())

        for cidr in output:
            netrange = ipaddress.IPv6Network(cidr)
            first, last = netrange[0], netrange[-1]
            firstip = int(ipaddress.IPv6Address(first))
            lastip = int(ipaddress.IPv6Address(last))
            f.write(os.environ['SOURCE']+','+now+','+cidr+','+str(firstip)+','+str(lastip)+',-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')

        f.close()

        s3 = boto3.resource('s3')

        s3.meta.client.upload_file(
            '/tmp/'+os.environ['SOURCE']+'.csv',
            os.environ['S3_BUCKET'],
            'sources/'+os.environ['SOURCE']+'.csv',
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