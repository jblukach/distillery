import boto3
import ipaddress
import json
import logging
import os
import requests
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambdaHandler(event, context):
    
    client = boto3.client('ssm')
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    cfipv4 = requests.get('https://www.cloudflare.com/ips-v4')
    logger.info('IPv4 Download Status Code: '+str(cfipv4.status_code))
    
    if cfipv4.status_code == 200:
        logger.info('Checking Cloudflare IPv4 Ranges')
        object = cfipv4.text
        cloudflare = list(object.splitlines())
        for cidr in cloudflare:
            sortkey = 'CLOUDFLARE#'+cidr
            hostmask = cidr.split('/')
            iptype = ipaddress.ip_address(hostmask[0])
            nametype = 'IPv'+str(iptype.version)+'#'
            iprange = cidr
            response = table.query(
                KeyConditionExpression = Key('pk').eq(nametype) & Key('sk').eq(sortkey)
            )
            if len(response['Items']) == 0:
                logger.info('Cloudflare IP Ranges Updated')
                netrange = ipaddress.IPv4Network(cidr)
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv4Address(first))
                lastip = int(ipaddress.IPv4Address(last))
                table.put_item(
                    Item= {
                        'pk': nametype,
                        'sk': sortkey,
                        'cidr': iprange,
                        'created': '-',
                        'firstip': firstip,
                        'lastip': lastip
                    } 
                )
                client.put_parameter(
                    Name = os.environ['SSM_PARAMETER'],
                    Value = 'NEW',
                    Type = 'String',
                    Overwrite = True
                )

    cfipv6 = requests.get('https://www.cloudflare.com/ips-v6')
    logger.info('IPv6 Download Status Code: '+str(cfipv6.status_code))

    if cfipv6.status_code == 200:
        logger.info('Checking Cloudflare IPv6 Ranges')
        object = cfipv6.text
        cloudflare = list(object.splitlines())
        for cidr in cloudflare:
            sortkey = 'CLOUDFLARE#'+cidr
            hostmask = cidr.split('/')
            iptype = ipaddress.ip_address(hostmask[0])
            nametype = 'IPv'+str(iptype.version)+'#'
            iprange = cidr
            response = table.query(
                KeyConditionExpression = Key('pk').eq(nametype) & Key('sk').eq(sortkey)
            )
            if len(response['Items']) == 0:
                logger.info('Cloudflare IP Ranges Updated')
                netrange = ipaddress.IPv6Network(cidr)
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv6Address(first))
                lastip = int(ipaddress.IPv6Address(last))
                table.put_item(
                    Item= {
                        'pk': nametype,
                        'sk': sortkey,
                        'cidr': iprange,
                        'created': '-',
                        'firstip': firstip,
                        'lastip': lastip
                    } 
                )
                client.put_parameter(
                    Name = os.environ['SSM_PARAMETER'],
                    Value = 'NEW',
                    Type = 'String',
                    Overwrite = True
                )

    return {
        'statusCode': 200,
        'body': json.dumps('Download Cloudflare IP Ranges')
    }