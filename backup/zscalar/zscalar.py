import boto3
import ipaddress
import json
import os
import requests

def handler(event, context):

    f = open('/tmp/'+os.environ['SOURCE']+'.csv', 'w')

    headers = {'User-Agent': 'Distillery (https://github.com/jblukach/distillery)'}
    r = requests.get('https://config.zscaler.com/api/zscaler.net/hubs/cidr/json/required', headers=headers)
    print('Download Status Code: '+str(r.status_code))

    if r.status_code == 200:

        for cidr in r.json()['hubPrefixes']:

            cidr = cidr.strip()

            if ipaddress.ip_network(cidr).version == 4:
                netrange = ipaddress.IPv4Network(cidr)
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv4Address(first))
                lastip = int(ipaddress.IPv4Address(last))
                f.write(os.environ['SOURCE']+','+os.environ['SOURCE']+','+r.json()['type']+','+cidr+','+str(firstip)+','+str(lastip)+'\n')

            if ipaddress.ip_network(cidr).version == 6:
                netrange = ipaddress.IPv6Network(cidr)
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv6Address(first))
                lastip = int(ipaddress.IPv6Address(last))
                f.write(os.environ['SOURCE']+','+os.environ['SOURCE']+','+r.json()['type']+','+cidr+','+str(firstip)+','+str(lastip)+'\n')

    else:
        print('Download Failed')

    r = requests.get('https://config.zscaler.com/api/zscaler.net/hubs/cidr/json/recommended', headers=headers)
    print('Download Status Code: '+str(r.status_code))

    if r.status_code == 200:

        for cidr in r.json()['hubPrefixes']:

            cidr = cidr.strip()

            if ipaddress.ip_network(cidr).version == 4:
                netrange = ipaddress.IPv4Network(cidr)
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv4Address(first))
                lastip = int(ipaddress.IPv4Address(last))
                f.write(os.environ['SOURCE']+','+os.environ['SOURCE']+','+r.json()['type']+','+cidr+','+str(firstip)+','+str(lastip)+'\n')

            if ipaddress.ip_network(cidr).version == 6:
                netrange = ipaddress.IPv6Network(cidr)
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv6Address(first))
                lastip = int(ipaddress.IPv6Address(last))
                f.write(os.environ['SOURCE']+','+os.environ['SOURCE']+','+r.json()['type']+','+cidr+','+str(firstip)+','+str(lastip)+'\n')

    else:
        print('Download Failed')

    f.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/'+os.environ['SOURCE']+'.csv',
        os.environ['S3_BUCKET'],
        os.environ['SOURCE']+'.csv',
        ExtraArgs = {
            'ContentType': "text/csv"
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Staging Completed')
    }