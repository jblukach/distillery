import boto3
import ipaddress
import json
import logging
import os
import requests
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    
    client = boto3.client('ssm')
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    doips = requests.get('https://www.digitalocean.com/geo/google.csv')
    logger.info('IP Download Status Code: '+str(doips.status_code))

    if doips.status_code == 200:
        
        logger.info('Checking Digital Ocean IP Ranges')
        object = doips.text
        digitalocean = list(object.splitlines())

        for cidr in digitalocean:
            parsed = cidr.split(',')
            sortkey = 'DO#'+parsed[2]+'#'+parsed[0]
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
                        'city': parsed[3]
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
        'body': json.dumps('Download Digital Ocean IP Ranges')
    }