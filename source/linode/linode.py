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
    r = requests.get('https://geoip.linode.com', headers=headers)
    print('Download Status Code: '+str(r.status_code))

    if r.status_code == 200:

        f = open('/tmp/'+os.environ['SOURCE']+'.csv', 'w')
        f.write('A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z\n')

        data = r.text
        output = list(data.splitlines())

        for cidr in output:
            if cidr.startswith('#'):
                continue
            else:
                parsed = cidr.split(',')
                hostmask = parsed[0].split('/')
                iptype = ipaddress.ip_address(hostmask[0])
                if iptype.version == 4:
                    netrange = ipaddress.IPv4Network(parsed[0])
                    first, last = netrange[0], netrange[-1]
                    firstip = int(ipaddress.IPv4Address(first))
                    lastip = int(ipaddress.IPv4Address(last))
                elif iptype.version == 6:
                    netrange = ipaddress.IPv6Network(parsed[0])
                    first, last = netrange[0], netrange[-1]
                    firstip = int(ipaddress.IPv6Address(first))
                    lastip = int(ipaddress.IPv6Address(last))            
                f.write(os.environ['SOURCE']+','+now+','+parsed[0]+','+str(firstip)+','+str(lastip)+','+parsed[2]+',-,'+parsed[3]+',-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')

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