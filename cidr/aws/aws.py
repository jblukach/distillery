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
    
    r = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json')
    logger.info('Download Status Code: '+str(r.status_code))
    
    if r.status_code == 200:
        output = r.json()
        if prevtoken != output['syncToken']:
            logger.info('Updating AWS IP Ranges')
            for cidr in output['prefixes']:
                sortkey = 'AWS#'+cidr['service']+'#'+cidr['region']+'#'+cidr['ip_prefix']
                hostmask = cidr['ip_prefix'].split('/')
                iptype = ipaddress.ip_address(hostmask[0])
                nametype = 'IPv'+str(iptype.version)+'#'
                iprange = cidr['ip_prefix']
                netrange = ipaddress.IPv4Network(cidr['ip_prefix'])
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv4Address(first))
                lastip = int(ipaddress.IPv4Address(last))
                table.put_item(Item= {  'pk': nametype,
                                        'sk': sortkey,
                                        'service': cidr['service'],
                                        'region': cidr['region'],
                                        'cidr': iprange,
                                        'edge': cidr['network_border_group'],
                                        'created': output['createDate'],
                                        'firstip': firstip,
                                        'lastip': lastip
                                    } )
            for cidr in output['ipv6_prefixes']:
                sortkey = 'AWS#'+cidr['service']+'#'+cidr['region']+'#'+cidr['ipv6_prefix']
                hostmask = cidr['ipv6_prefix'].split('/')
                iptype = ipaddress.ip_address(hostmask[0])
                nametype = 'IPv'+str(iptype.version)+'#'
                iprange = cidr['ipv6_prefix']
                netrange = ipaddress.IPv6Network(cidr['ipv6_prefix'])
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv6Address(first))
                lastip = int(ipaddress.IPv6Address(last))
                table.put_item(Item= {  'pk': nametype,
                                        'sk': sortkey,
                                        'service': cidr['service'],
                                        'region': cidr['region'],
                                        'cidr': iprange,
                                        'edge': cidr['network_border_group'],
                                        'created': output['createDate'],
                                        'firstip': firstip,
                                        'lastip': lastip
                                    } )
            logger.info('AWS IP Ranges Updated')
            now = datetime.now()
            epoch = int(time.time())
            filename = '/tmp/'+str(now.strftime('%Y'))+'-'+str(now.strftime('%m'))+'-'+str(now.strftime('%d'))+'-aws-'+str(epoch)+'.md'
            with open(filename, 'w') as f:
                f.write('---\n')
                f.write('layout: post\n')
                f.write('title: AWS '+str(now)+'\n')
                f.write('author: "John Lukach"\n')
                f.write('tags: AWS\n')
                f.write('---\n\n')
            f.close()
            upload(filename)
            response = client.put_parameter(Name=os.environ['SSM_PARAMETER'],
                                            Value=output['syncToken'],
                                            Type='String',
                                            Overwrite=True)
        else:
            logger.info('No AWS IP Range Updates')

    return {
        'statusCode': 200,
        'body': json.dumps('Download AWS IP Ranges')
    }