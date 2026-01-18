import boto3
import datetime
import gzip
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
    r = requests.get('https://azureipranges.azurewebsites.net/Data/China.json', headers=headers)
    print('Download Status Code: '+str(r.status_code))

    if r.status_code == 200:

        f = open('/tmp/'+os.environ['SOURCE']+'.csv', 'w')
        f.write('A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z\n')

        output = r.json()

        for cidr in output['values']:
            for ip in cidr['properties']['addressPrefixes']:
                hostmask = ip.split('/')
                iptype = ipaddress.ip_address(hostmask[0])
                if iptype.version == 4:
                    netrange = ipaddress.IPv4Network(ip)
                    first, last = netrange[0], netrange[-1]
                    firstip = int(ipaddress.IPv4Address(first))
                    lastip = int(ipaddress.IPv4Address(last))
                elif iptype.version == 6:
                    netrange = ipaddress.IPv6Network(ip)
                    first, last = netrange[0], netrange[-1]
                    firstip = int(ipaddress.IPv6Address(first))
                    lastip = int(ipaddress.IPv6Address(last))
                if len(cidr['properties']['region']) == 0:
                    region = 'global'
                else:
                    region = cidr['properties']['region']
                f.write(os.environ['SOURCE']+','+now+','+ip+','+str(firstip)+','+str(lastip)+','+region+','+cidr['properties']['systemService']+',-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')

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