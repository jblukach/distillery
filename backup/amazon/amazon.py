import boto3
import ipaddress
import json
import os
import requests

def handler(event, context):

    headers = {'User-Agent': 'Distillery (https://github.com/jblukach/distillery)'}
    r = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json', headers=headers)
    print('Download Status Code: '+str(r.status_code))

    if r.status_code == 200:

        f = open('/tmp/'+os.environ['SOURCE']+'.csv', 'w')

        output = r.json()

        for cidr in output['prefixes']:
            netrange = ipaddress.IPv4Network(cidr['ip_prefix'])
            first, last = netrange[0], netrange[-1]
            firstip = int(ipaddress.IPv4Address(first))
            lastip = int(ipaddress.IPv4Address(last))
            f.write(os.environ['SOURCE']+','+cidr['service']+','+cidr['region']+','+cidr['ip_prefix']+','+str(firstip)+','+str(lastip)+'\n')

        for cidr in output['ipv6_prefixes']:
            netrange = ipaddress.IPv6Network(cidr['ipv6_prefix'])
            first, last = netrange[0], netrange[-1]
            firstip = int(ipaddress.IPv6Address(first))
            lastip = int(ipaddress.IPv6Address(last))
            f.write(os.environ['SOURCE']+','+cidr['service']+','+cidr['region']+','+cidr['ipv6_prefix']+','+str(firstip)+','+str(lastip)+'\n')

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

    else:
        print('Download Failed')

    return {
        'statusCode': 200,
        'body': json.dumps('Staging Completed')
    }