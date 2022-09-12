import boto3
import ipaddress
import json
import logging
import os
import requests
import time
import uuid
from datetime import datetime
from github import Github

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
client = boto3.client('ssm')

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

def downloader(instance, latest, parameter, link):
    
    r = requests.get(link)
    cidrs = r.json()
    
    if r.status_code == 200:
        for cidr in cidrs:
            try:
                if len(cidr['ips']) != 0:
                    for ip in cidr['ips']:
                        sortkey = 'O365#'+instance+'#'+cidr['serviceArea']+'#'+ip
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
                                'service': cidr['serviceArea'],
                                'cidr': ip,
                                'created': latest,
                                'endpoint': instance,
                                'firstip': firstip,
                                'lastip': lastip
                            }
                        )
            except:
                pass
            
        logger.info('o365 '+instance+' IP Ranges Updated')
        now = datetime.now()
        epoch = int(time.time())
        filename = '/tmp/'+str(now.strftime('%Y'))+'-'+str(now.strftime('%m'))+'-'+str(now.strftime('%d'))+'-o365-'+str(epoch)+'.md'
        with open(filename, 'w') as f:
            f.write('---\n')
            f.write('layout: post\n')
            f.write('title: o365 '+str(now)+'\n')
            f.write('author: "John Lukach"\n')
            f.write('tags: o365\n')
            f.write('---\n\n')
        f.close()
        upload(filename)
        response = client.put_parameter(
            Name = parameter,
            Value = str(latest),
            Type = 'String',
            Overwrite = True
        )   

def handler(event, context):
    
    r = requests.get('https://endpoints.office.com/version?clientrequestid='+str(uuid.uuid4()))
    logger.info('Link Status Code: '+str(r.status_code))
    
    if r.status_code == 200:
        versions = r.json()
        logger.info(versions)
        for version in versions:
            if version['instance'] == 'Worldwide':
                response = client.get_parameter(Name=os.environ['WORLD_PARAMETER'])
                prevtoken = response['Parameter']['Value']
                if prevtoken != str(version['latest']):
                    logger.info('Updating o365 Worldwide IP Ranges')
                    link = 'https://endpoints.office.com/endpoints/worldwide?clientrequestid='+str(uuid.uuid4())
                    downloader(version['instance'], version['latest'], os.environ['WORLD_PARAMETER'], link)
            elif version['instance'] == 'USGovDoD':
                response = client.get_parameter(Name=os.environ['DOD_PARAMETER'])
                prevtoken = response['Parameter']['Value']
                if prevtoken != str(version['latest']):
                    logger.info('Updating o365 USGovDoD IP Ranges')
                    link = 'https://endpoints.office.com/endpoints/USGOVDoD?clientrequestid='+str(uuid.uuid4())
                    downloader(version['instance'], version['latest'], os.environ['DOD_PARAMETER'], link)
            elif version['instance'] == 'USGovGCCHigh':
                response = client.get_parameter(Name=os.environ['HIGH_PARAMETER'])
                prevtoken = response['Parameter']['Value']
                if prevtoken != str(version['latest']):
                    logger.info('Updating o365 USGovGCCHigh IP Ranges')
                    link = 'https://endpoints.office.com/endpoints/USGOVGCCHigh?clientrequestid='+str(uuid.uuid4())
                    downloader(version['instance'], version['latest'], os.environ['HIGH_PARAMETER'], link)
            elif version['instance'] == 'China':
                response = client.get_parameter(Name=os.environ['CHINA_PARAMETER'])
                prevtoken = response['Parameter']['Value']
                if prevtoken != str(version['latest']):
                    logger.info('Updating o365 China IP Ranges')
                    link = 'https://endpoints.office.com/endpoints/China?clientrequestid='+str(uuid.uuid4())
                    downloader(version['instance'], version['latest'], os.environ['CHINA_PARAMETER'], link)
            elif version['instance'] == 'Germany':
                response = client.get_parameter(Name=os.environ['GERMANY_PARAMETER'])
                prevtoken = response['Parameter']['Value']
                if prevtoken != str(version['latest']):
                    logger.info('Updating o365 Germany IP Ranges')
                    link = 'https://endpoints.office.com/endpoints/Germany?clientrequestid='+str(uuid.uuid4())
                    downloader(version['instance'], version['latest'], os.environ['GERMANY_PARAMETER'], link)
    else:
        logger.info('No o365 IP Range Updates')

    return {
        'statusCode': 200,
        'body': json.dumps('Download o365 IP Ranges')
    }
