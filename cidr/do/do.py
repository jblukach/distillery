import boto3
import ipaddress
import json
import logging
import os
import requests
import time
from boto3.dynamodb.conditions import Key
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
    
    client = boto3.client('ssm')
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    doips = requests.get('https://www.digitalocean.com/geo/google.csv')
    logger.info('IP Download Status Code: '+str(doips.status_code))

    if doips.status_code == 200:

        status = 'EMPTY'

        logger.info('Checking Digital Ocean IP Ranges')
        object = doips.text
        digitalocean = list(object.splitlines())

        for cidr in digitalocean:
            parsed = cidr.split(',')
            if parsed[1] == 'None':
                vartwo = 'None'
                varthree = 'None'
            else:
                vartwo = parsed[2]
                varthree = parsed[3]
            sortkey = 'DO#'+vartwo+'#'+parsed[0]
            hostmask = parsed[0].split('/')
            iptype = ipaddress.ip_address(hostmask[0])
            nametype = 'IPv'+str(iptype.version)+'#'
            iprange = parsed[0]
            if nametype == 'IPv4#':
                netrange = ipaddress.IPv4Network(parsed[0])
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv4Address(first))
                lastip = int(ipaddress.IPv4Address(last))
            if nametype == 'IPv6#':    
                netrange = ipaddress.IPv6Network(parsed[0])
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv6Address(first))
                lastip = int(ipaddress.IPv6Address(last))
            response = table.query(
                KeyConditionExpression = Key('pk').eq(nametype) & Key('sk').eq(sortkey)
            )
            if len(response['Items']) == 0:
                logger.info('Digital Ocean IP Ranges Updated')
                table.put_item(
                    Item= {
                        'pk': nametype,
                        'sk': sortkey,
                        'cidr': iprange,
                        'created': '-',
                        'firstip': firstip,
                        'lastip': lastip,
                        'country': parsed[1],
                        'city': varthree
                    } 
                )
                status = 'NEW'

    if status == 'NEW':
        now = datetime.now()
        epoch = int(time.time())
        filename = '/tmp/'+str(now.strftime('%Y'))+'-'+str(now.strftime('%m'))+'-'+str(now.strftime('%d'))+'-digitalocean-'+str(epoch)+'.md'
        with open(filename, 'w') as f:
            f.write('---\n')
            f.write('layout: post\n')
            f.write('title: Digital Ocean '+str(now)+'\n')
            f.write('author: "John Lukach"\n')
            f.write('tags: Digital Ocean\n')
            f.write('---\n\n')
        f.close()
        upload(filename)


    return {
        'statusCode': 200,
        'body': json.dumps('Download Digital Ocean IP Ranges')
    }