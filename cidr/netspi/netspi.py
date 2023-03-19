import boto3
import ipaddress
import json
import os
import requests
from boto3.dynamodb.conditions import Key

def handler(event, context):

    client = boto3.client('ssm')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    headers = {'User-Agent': 'Distillery Python Client/1.0'}
    ipv4 = requests.get('https://www.netspi.com/wp-content/uploads/2021/04/allowlist.txt', headers=headers)
    print('IPv4 Download Status Code: '+str(ipv4.status_code))

    if ipv4.status_code == 200:
        print('Checking NetSPI IPv4 Ranges')
        object = ipv4.text
        netspi = list(object.splitlines())
        for cidr in netspi:
            if(cidr) and 'Last' not in cidr:
                sortkey = 'NETSPI#'+cidr
                hostmask = cidr.split('/')
                iptype = ipaddress.ip_address(hostmask[0])
                nametype = 'IPv'+str(iptype.version)+'#'
                iprange = cidr
                response = table.query(
                    KeyConditionExpression = Key('pk').eq(nametype) & Key('sk').eq(sortkey)
                )
                if len(response['Items']) == 0:
                    print('NetSPI IP Ranges Updated')
                    netrange = ipaddress.IPv4Network(cidr)
                    first, last = netrange[0], netrange[-1]
                    firstip = int(ipaddress.IPv4Address(first))
                    lastip = int(ipaddress.IPv4Address(last))
                    table.put_item(
                        Item = {
                            'pk': nametype,
                            'sk': sortkey,
                            'cidr': iprange,
                            'created': '-',
                            'firstip': firstip,
                            'lastip': lastip
                        } 
                    )

    return {
        'statusCode': 200,
        'body': json.dumps('Download NetSPI IP Ranges')
    }