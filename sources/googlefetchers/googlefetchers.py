import boto3
import ipaddress
import json
import os
import requests

def handler(event, context):

    headers = {'User-Agent': 'Distillery (https://github.com/jblukach/distillery)'}
    r = requests.get('https://developers.google.com/search/apis/ipranges/user-triggered-fetchers.json', headers=headers)
    print('Download Status Code: '+str(r.status_code))

    if r.status_code == 200:

        output = r.json()

        f = open('/tmp/'+os.environ['SOURCE']+'.csv', 'w')

        for cidr in output['prefixes']:

            try:
                netrange = ipaddress.IPv4Network(cidr['ipv4Prefix'])
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv4Address(first))
                lastip = int(ipaddress.IPv4Address(last))
                f.write(os.environ['SOURCE']+','+os.environ['SOURCE']+','+os.environ['SOURCE']+','+cidr['ipv4Prefix']+','+str(firstip)+','+str(lastip)+'\n')
            except:
                pass

            try:
                netrange = ipaddress.IPv6Network(cidr['ipv6Prefix'])
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv6Address(first))
                lastip = int(ipaddress.IPv6Address(last))
                f.write(os.environ['SOURCE']+','+os.environ['SOURCE']+','+os.environ['SOURCE']+','+cidr['ipv6Prefix']+','+str(firstip)+','+str(lastip)+'\n')
            except:
                pass

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