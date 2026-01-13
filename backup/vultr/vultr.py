import boto3
import ipaddress
import json
import os
import requests

def handler(event, context):

    headers = {'User-Agent': 'Distillery (https://github.com/jblukach/distillery)'}
    r = requests.get('https://geofeed.constant.com/?json', headers=headers)
    print('Download Status Code: '+str(r.status_code))

    if r.status_code == 200:

        output = r.json()

        f = open('/tmp/'+os.environ['SOURCE']+'.csv', 'w')

        for subnet in output['subnets']:
            hostmask = subnet['ip_prefix'].split('/')
            iptype = ipaddress.ip_address(hostmask[0])
            if iptype.version == 4:
                netrange = ipaddress.IPv4Network(subnet['ip_prefix'])
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv4Address(first))
                lastip = int(ipaddress.IPv4Address(last))
            elif iptype.version == 6:
                netrange = ipaddress.IPv6Network(subnet['ip_prefix'])
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv6Address(first))
                lastip = int(ipaddress.IPv6Address(last))
            f.write(os.environ['SOURCE']+','+subnet['city'].replace(',',' ')+','+subnet['region']+','+subnet['ip_prefix']+','+str(firstip)+','+str(lastip)+'\n')

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
        print('No Vultr IP Range Updates')

    return {
        'statusCode': 200,
        'body': json.dumps('Staging Completed')
    }