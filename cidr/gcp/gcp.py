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
    
    r = requests.get('https://www.gstatic.com/ipranges/cloud.json')
    logger.info('Download Status Code: '+str(r.status_code))
    
    if r.status_code == 200:
        output = r.json()
        if prevtoken != output['syncToken']:
            logger.info('Updating GCP IP Ranges')
            for cidr in output['prefixes']:
                try:
                    sortkey = 'GCP#'+cidr['scope']+'#'+cidr['ipv4Prefix']
                    hostmask = cidr['ipv4Prefix'].split('/')
                    iptype = ipaddress.ip_address(hostmask[0])
                    nametype = 'IPv'+str(iptype.version)+'#'
                    iprange = cidr['ipv4Prefix']
                    netrange = ipaddress.IPv4Network(cidr['ipv4Prefix'])
                    first, last = netrange[0], netrange[-1]
                    firstip = int(ipaddress.IPv4Address(first))
                    lastip = int(ipaddress.IPv4Address(last))
                    service = cidr['service']
                    scope = cidr['scope']
                    table.put_item(
                        Item= {
                            'pk': nametype,
                            'sk': sortkey,
                            'service': service,
                            'scope': scope,
                            'cidr': iprange,
                            'created': output['creationTime'],
                            'firstip': firstip,
                            'lastip': lastip
                        }
                    )
                except:
                    pass
                try:
                    sortkey = 'GCP#'+cidr['scope']+'#'+cidr['ipv6Prefix']
                    hostmask = cidr['ipv6Prefix'].split('/')
                    iptype = ipaddress.ip_address(hostmask[0])
                    nametype = 'IPv'+str(iptype.version)+'#'
                    iprange = cidr['ipv6Prefix']
                    netrange = ipaddress.IPv6Network(cidr['ipv6Prefix'])
                    first, last = netrange[0], netrange[-1]
                    firstip = int(ipaddress.IPv6Address(first))
                    lastip = int(ipaddress.IPv6Address(last))
                    service = cidr['service']
                    scope = cidr['scope']
                    table.put_item(
                        Item= {
                            'pk': nametype,
                            'sk': sortkey,
                            'service': service,
                            'scope': scope,
                            'cidr': iprange,
                            'created': output['creationTime'],
                            'firstip': firstip,
                            'lastip': lastip
                        }
                    )
                except:
                    pass
            logger.info('GCP IP Ranges Updated')
            now = datetime.now()
            epoch = int(time.time())
            filename = '/tmp/'+str(now.strftime('%Y'))+'-'+str(now.strftime('%m'))+'-'+str(now.strftime('%d'))+'-gcp-'+str(epoch)+'.md'
            with open(filename, 'w') as f:
                f.write('---\n')
                f.write('layout: post\n')
                f.write('title: GCP '+str(now)+'\n')
                f.write('author: "John Lukach"\n')
                f.write('tags: GCP\n')
                f.write('---\n\n')
            f.close()
            #upload(filename)
            response = client.put_parameter(Name=os.environ['SSM_PARAMETER'],
                                            Value=output['syncToken'],
                                            Type='String',
                                            Overwrite=True)
        else:
            logger.info('No GCP IP Range Updates')

    return {
        'statusCode': 200,
        'body': json.dumps('Download GCP IP Ranges')
    }