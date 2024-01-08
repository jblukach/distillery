import boto3
import ipaddress
import json
import os
import requests

def handler(event, context):

    headers = {'User-Agent': 'Distillery (https://github.com/jblukach/distillery)'}

    r = requests.get('https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519', headers=headers)
    print('Link Status Code: '+str(r.status_code))

    staged = r.text
    parsed = staged.split('manually')
    front = parsed[1].split(' href="')
    back = front[1].split('" ')
    link = back[0]

    r = requests.get(link, headers=headers)
    print('Download Status Code: '+str(r.status_code))

    if r.status_code == 200:

        f = open('/tmp/'+os.environ['SOURCE']+'.csv', 'w')

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
                f.write(os.environ['SOURCE']+','+cidr['properties']['systemService']+','+region+','+ip+','+str(firstip)+','+str(lastip)+'\n')

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