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

    current = requests.get('https://config.zscaler.com/api/private.zscaler.com/zpa/json', headers=headers)
    print('Current Status Code: '+str(current.status_code))

    if current.status_code == 200:

        f = open('/tmp/'+os.environ['SOURCE']+'.csv', 'w')
        f.write('A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z\n')

        for content in current.json()['content']:
            for ip in content['IPs']:
                if '/' not in ip and ':' not in ip:
                    ip += '/32'
            
                if ipaddress.ip_network(ip).version == 4:
                    netrange = ipaddress.IPv4Network(ip)
                    first, last = netrange[0], netrange[-1]
                    firstip = int(ipaddress.IPv4Address(first))
                    lastip = int(ipaddress.IPv4Address(last))
                    f.write(os.environ['SOURCE']+','+now+','+ip+','+str(firstip)+','+str(lastip)+',-,current,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')

                if ipaddress.ip_network(ip).version == 6:
                    netrange = ipaddress.IPv6Network(ip)
                    first, last = netrange[0], netrange[-1]
                    firstip = int(ipaddress.IPv6Address(first))
                    lastip = int(ipaddress.IPv6Address(last))
                    f.write(os.environ['SOURCE']+','+now+','+ip+','+str(firstip)+','+str(lastip)+',-,current,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')

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

        fname = f'{year}-{month}-{day}-{hour}-{os.environ["SOURCE"]}.csv.gz'
        fpath = f'/tmp/{fname}'
        print(fpath)

        with open('/tmp/'+os.environ['SOURCE']+'.csv', 'rb') as f_in:
            with gzip.open(fpath, 'wb') as f_out:
                f_out.writelines(f_in)

        s3.meta.client.upload_file(
            fpath,
            os.environ['S3_RESEARCH'],
            'v1/'+fname,
            ExtraArgs = {
                'ContentType': "application/gzip"
            }
        )

        os.system('ls -lh /tmp')

    else:
        print('Download Failed')

    return {
        'statusCode': 200,
        'body': json.dumps('Staging Completed')
    }