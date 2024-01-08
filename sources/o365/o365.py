import boto3
import ipaddress
import json
import os
import requests
import uuid

def downloader(instance, link):

    headers = {'User-Agent': 'Distillery (https://github.com/jblukach/distillery)'}
    r = requests.get(link, headers=headers)
    print('Download Status Code: '+str(r.status_code))

    cidrs = r.json()

    f = open('/tmp/'+os.environ['SOURCE']+'.csv', 'a')

    if r.status_code == 200:
        for cidr in cidrs:
            try:
                if len(cidr['ips']) != 0:
                    for ip in cidr['ips']:
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
                        f.write(os.environ['SOURCE']+','+cidr['serviceArea']+','+instance+','+ip+','+str(firstip)+','+str(lastip)+'\n')
            except:
                pass 

    f.close()

def handler(event, context):

    headers = {'User-Agent': 'Distillery (https://github.com/jblukach/distillery)'}
    r = requests.get('https://endpoints.office.com/version?clientrequestid='+str(uuid.uuid4()), headers=headers)
    print('Link Status Code: '+str(r.status_code))

    if r.status_code == 200:
        versions = r.json()
        for version in versions:
            if version['instance'] == 'Worldwide':
                link = 'https://endpoints.office.com/endpoints/worldwide?clientrequestid='+str(uuid.uuid4())
                downloader(version['instance'], link)
            elif version['instance'] == 'USGovDoD':
                link = 'https://endpoints.office.com/endpoints/USGOVDoD?clientrequestid='+str(uuid.uuid4())
                downloader(version['instance'], link)
            elif version['instance'] == 'USGovGCCHigh':
                link = 'https://endpoints.office.com/endpoints/USGOVGCCHigh?clientrequestid='+str(uuid.uuid4())
                downloader(version['instance'], link)
            elif version['instance'] == 'China':
                link = 'https://endpoints.office.com/endpoints/China?clientrequestid='+str(uuid.uuid4())
                downloader(version['instance'], link)
            elif version['instance'] == 'Germany':
                link = 'https://endpoints.office.com/endpoints/Germany?clientrequestid='+str(uuid.uuid4())
                downloader(version['instance'], link)

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