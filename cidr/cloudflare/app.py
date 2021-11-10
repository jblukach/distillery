import boto3
import ipaddress
import json
import logging
import os
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambdaHandler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    client = boto3.client('ssm')
    response = client.get_parameter(Name=os.environ['SSM_PARAMETER'])
    prevtoken = response['Parameter']['Value']

    r1 = requests.get('https://www.cloudflare.com/ips-v4')
    r2 = requests.get('https://www.cloudflare.com/ips-v6')

    logger.info('Download Status Code: '+str(r.status_code))
    
    if r1.status_code and r2.status_code == 200:
        output = r1.text + r2.text
        cloudflare = list(output.splitlines())
        if prevtoken != output['syncToken']:
            logger.info('Updating Cloudflare IP Ranges')
            for cidr in cloudflare:
                try:
                    sortkey = 'Cloudflare#'+cidr
                    hostmask = cidr['ipv4Prefix'].split('/')
                    iptype = ipaddress.ip_address(hostmask[0])
                    nametype = 'IPv'+str(iptype.version)+'#'
                    iprange = cidr
                    netrange = ipaddress.IPv4Network(cidr)
                    first, last = netrange[0], netrange[-1]
                    firstip = int(ipaddress.IPv4Address(first))
                    lastip = int(ipaddress.IPv4Address(last))
                    table.put_item(
                        Item= {
                            'pk': nametype,
                            'sk': sortkey,
                            'cidr': iprange,
                            'created': output['creationTime'],
                            'firstip': firstip,
                            'lastip': lastip
                        } 
                    )
                except:
                    pass
                try:
                    sortkey = 'Cloudflare#'+cidr
                    hostmask = cidr.split('/')
                    iptype = ipaddress.ip_address(hostmask[0])
                    nametype = 'IPv'+str(iptype.version)+'#'
                    iprange = cidr
                    netrange = ipaddress.IPv6Network(cidr)
                    first, last = netrange[0], netrange[-1]
                    firstip = int(ipaddress.IPv6Address(first))
                    lastip = int(ipaddress.IPv6Address(last))
                    table.put_item(
                        Item= {
                            'pk': nametype,
                            'sk': sortkey,
                            'cidr': iprange,
                            'created': output['creationTime'],
                            'firstip': firstip,
                            'lastip': lastip
                        } 
                    )
                except:
                    pass            
            logger.info('Cloudflare IP Ranges Updated')
            response = client.put_parameter(Name=os.environ['SSM_PARAMETER'],
                                            Value=output['syncToken'],
                                            Type='String',
                                            Overwrite=True)
        else:
            logger.info('No Cloudflare IP Range Updates')

    return {
        'statusCode': 200,
        'body': json.dumps('Download Cloudflare IP Ranges')
    }