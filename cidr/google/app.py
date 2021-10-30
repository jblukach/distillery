import boto3
import ipaddress
import json
import logging
import os
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambdaHandler(event, context):
    
    logger.info(event)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    client = boto3.client('ssm')
    response = client.get_parameter(Name=os.environ['SSM_PARAMETER'])
    prevtoken = response['Parameter']['Value']
    
    r = requests.get('https://www.gstatic.com/ipranges/goog.json')
    logger.info('Download Status Code: '+str(r.status_code))
    
    if r.status_code == 200:
        output = r.json()
        if prevtoken != output['syncToken']:
            logger.info('Updating Google IP Ranges')
            for cidr in output['prefixes']:
                try:
                    sortkey = 'GOOGLE#'+cidr['ipv4Prefix']
                    hostmask = cidr['ipv4Prefix'].split('/')
                    iptype = ipaddress.ip_address(hostmask[0])
                    nametype = 'IPv'+str(iptype.version)+'#'
                    iprange = cidr['ipv4Prefix']
                    netrange = ipaddress.IPv4Network(cidr['ipv4Prefix'])
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
                    sortkey = 'GOOGLE#'+cidr['ipv6Prefix']
                    hostmask = cidr['ipv6Prefix'].split('/')
                    iptype = ipaddress.ip_address(hostmask[0])
                    nametype = 'IPv'+str(iptype.version)+'#'
                    iprange = cidr['ipv6Prefix']
                    netrange = ipaddress.IPv6Network(cidr['ipv6Prefix'])
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

            response = client.put_parameter(Name=os.environ['SSM_PARAMETER'],
                                            Value=output['syncToken'],
                                            Type='String',
                                            Overwrite=True)
        else:
            logger.info('No Google IP Range Updates')

    return {
        'statusCode': 200,
        'body': json.dumps('Download Google IP Ranges')
    }