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

    current = requests.get('https://config.zscaler.com/api/'+os.environ['SOURCE']+'.net/cenr/json', headers=headers)
    print('Current Status Code: '+str(current.status_code))

    future = requests.get('https://config.zscaler.com/api/'+os.environ['SOURCE']+'.net/future/json', headers=headers)
    print('Future Status Code: '+str(future.status_code))

    recommended = requests.get('https://config.zscaler.com/api/'+os.environ['SOURCE']+'.net/hubs/cidr/json/recommended', headers=headers)
    print('Recommended Status Code: '+str(recommended.status_code))

    required = requests.get('https://config.zscaler.com/api/'+os.environ['SOURCE']+'.net/hubs/cidr/json/required', headers=headers)
    print('Required Status Code: '+str(required.status_code))

    if current.status_code == 200 and future.status_code == 200 and recommended.status_code == 200 and required.status_code == 200:

        f = open('/tmp/'+os.environ['SOURCE']+'.csv', 'w')
        f.write('A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z\n')

        key = os.environ['SOURCE']+'.net'

        for continent in current.json()[key].keys():
            for city in current.json()[key][continent]:
                location = city.split(':')[1].strip()
                for cidr in current.json()[key][continent][city]:

                    if ipaddress.ip_network(cidr['range']).version == 4:
                        netrange = ipaddress.IPv4Network(cidr['range'])
                        first, last = netrange[0], netrange[-1]
                        firstip = int(ipaddress.IPv4Address(first))
                        lastip = int(ipaddress.IPv4Address(last))
                        f.write(os.environ['SOURCE']+','+now+','+cidr['range']+','+str(firstip)+','+str(lastip)+','+location+',current,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')

                    if ipaddress.ip_network(cidr['range']).version == 6:
                        netrange = ipaddress.IPv6Network(cidr['range'])
                        first, last = netrange[0], netrange[-1]
                        firstip = int(ipaddress.IPv6Address(first))
                        lastip = int(ipaddress.IPv6Address(last))
                        f.write(os.environ['SOURCE']+','+now+','+cidr['range']+','+str(firstip)+','+str(lastip)+','+location+',current,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')

        for cidr in future.json()['prefixes']:

            cidr = cidr.strip()

            if ipaddress.ip_network(cidr).version == 4:
                netrange = ipaddress.IPv4Network(cidr)
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv4Address(first))
                lastip = int(ipaddress.IPv4Address(last))
                f.write(os.environ['SOURCE']+','+now+','+cidr+','+str(firstip)+','+str(lastip)+',-,future,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')

            if ipaddress.ip_network(cidr).version == 6:
                netrange = ipaddress.IPv6Network(cidr)
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv6Address(first))
                lastip = int(ipaddress.IPv6Address(last))
                f.write(os.environ['SOURCE']+','+now+','+cidr+','+str(firstip)+','+str(lastip)+',-,future,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')

        for cidr in recommended.json()['hubPrefixes']:

            cidr = cidr.strip()

            if ipaddress.ip_network(cidr).version == 4:
                netrange = ipaddress.IPv4Network(cidr)
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv4Address(first))
                lastip = int(ipaddress.IPv4Address(last))
                f.write(os.environ['SOURCE']+','+now+','+cidr+','+str(firstip)+','+str(lastip)+',-,recommended,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')

            if ipaddress.ip_network(cidr).version == 6:
                netrange = ipaddress.IPv6Network(cidr)
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv6Address(first))
                lastip = int(ipaddress.IPv6Address(last))
                f.write(os.environ['SOURCE']+','+now+','+cidr+','+str(firstip)+','+str(lastip)+',-,recommended,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')

        for cidr in required.json()['hubPrefixes']:

            cidr = cidr.strip()

            if ipaddress.ip_network(cidr).version == 4:
                netrange = ipaddress.IPv4Network(cidr)
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv4Address(first))
                lastip = int(ipaddress.IPv4Address(last))
                f.write(os.environ['SOURCE']+','+now+','+cidr+','+str(firstip)+','+str(lastip)+',-,required,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')

            if ipaddress.ip_network(cidr).version == 6:
                netrange = ipaddress.IPv6Network(cidr)
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv6Address(first))
                lastip = int(ipaddress.IPv6Address(last))
                f.write(os.environ['SOURCE']+','+now+','+cidr+','+str(firstip)+','+str(lastip)+',-,required,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-\n')

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