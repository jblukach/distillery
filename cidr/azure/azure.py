import boto3
import ipaddress
import json
import logging
import os
import requests
import time
from datetime import datetime
from github import Github

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def upload(filename):
    
    ssm = boto3.client('ssm')
    token = ssm.get_parameter(Name=os.environ['GITHUB_TOKEN'], WithDecryption=True)
    
    with open(filename, 'r') as t:
        text = t.read()
    t.close()
    
    g = Github(token['Parameter']['Value'])
    repo = g.get_repo('4n6ir/cloudbot')
    
    parsed = filename.split('/')
    
    repo.create_file('_posts/'+parsed[2], parsed[2], text, branch='main')

def handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    client = boto3.client('ssm')
    response = client.get_parameter(Name=os.environ['SSM_PARAMETER'])
    prevtoken = response['Parameter']['Value']
    
    r = requests.get('https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519')
    logger.info('Link Status Code: '+str(r.status_code))
    
    staged = r.text
    parsed = staged.split('manually')
    front = parsed[1].split(' href="')
    back = front[1].split('" ')
    link = back[0]

    r = requests.get(link)
    logger.info('Download Status Code: '+str(r.status_code))

    if r.status_code == 200:
        output = r.json()
        if prevtoken != str(output['changeNumber']):
            logger.info('Updating Azure IP Ranges')
            for cidr in output['values']:
                for ip in cidr['properties']['addressPrefixes']:
                    sortkey = 'AZURE#'+cidr['name']+'#'+ip
                    hostmask = ip.split('/')
                    iptype = ipaddress.ip_address(hostmask[0])
                    nametype = 'IPv'+str(iptype.version)+'#'
                    if nametype == 'IPv4#':
                        netrange = ipaddress.IPv4Network(ip)
                        first, last = netrange[0], netrange[-1]
                        firstip = int(ipaddress.IPv4Address(first))
                        lastip = int(ipaddress.IPv4Address(last))
                    elif nametype == 'IPv6#':
                        netrange = ipaddress.IPv6Network(ip)
                        first, last = netrange[0], netrange[-1]
                        firstip = int(ipaddress.IPv6Address(first))
                        lastip = int(ipaddress.IPv6Address(last))
                    table.put_item(
                        Item= {  
                            'pk': nametype,
                            'sk': sortkey,
                            'service': cidr['name'],
                            'change': cidr['properties']['changeNumber'],
                            'cidr': ip,
                            'created': output['changeNumber'],
                            'firstip': firstip,
                            'lastip': lastip
                        }
                    )
            logger.info('Azure IP Ranges Updated')
            now = datetime.now()
            epoch = int(time.time())
            filename = '/tmp/'+str(now.strftime('%Y'))+'-'+str(now.strftime('%m'))+'-'+str(now.strftime('%d'))+'-azure-'+str(epoch)+'.md'
            with open(filename, 'w') as f:
                f.write('---\n')
                f.write('layout: post\n')
                f.write('title: Azure '+str(now)+'\n')
                f.write('author: "John Lukach"\n')
                f.write('tags: Azure\n')
                f.write('---\n\n')
            f.close()
            upload(filename)
            response = client.put_parameter(
                Name=os.environ['SSM_PARAMETER'],
                Value=str(output['changeNumber']),
                Type='String',
                Overwrite=True
            )
        else:
            logger.info('No Azure IP Range Updates')

    return {
        'statusCode': 200,
        'body': json.dumps('Download Azure IP Ranges')
    }