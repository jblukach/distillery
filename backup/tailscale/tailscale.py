import boto3
import ipaddress
import json
import os
import requests

def handler(event, context):

    f = open('/tmp/'+os.environ['SOURCE']+'.csv', 'w')

    headers = {'User-Agent': 'Distillery (https://github.com/jblukach/distillery)'}
    r = requests.get('https://login.tailscale.com/derpmap/default', headers=headers)
    print('Download Status Code: '+str(r.status_code))

    if r.status_code == 200:

        for key, value in r.json()['Regions'].items():
            for node in value['Nodes']:

                netrange = ipaddress.IPv4Network(node['IPv4'])
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv4Address(first))
                lastip = int(ipaddress.IPv4Address(last))
                f.write(os.environ['SOURCE']+','+value['RegionName']+','+value['RegionCode']+','+node['IPv4']+','+str(firstip)+','+str(lastip)+'\n')

                netrange = ipaddress.IPv6Network(node['IPv6'])
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv6Address(first))
                lastip = int(ipaddress.IPv6Address(last))
                f.write(os.environ['SOURCE']+','+value['RegionName']+','+value['RegionCode']+','+node['IPv6']+','+str(firstip)+','+str(lastip)+'\n')

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