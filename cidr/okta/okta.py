import boto3
import ipaddress
import json
import os
import requests
from boto3.dynamodb.conditions import Key

def handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    ipv4 = requests.get('https://s3.amazonaws.com/okta-ip-ranges/ip_ranges.json')
    print('IPv4 Download Status Code: '+str(ipv4.status_code))

    if ipv4.status_code == 200:
        print('Checking Okta IPv4 Ranges')
        output = ipv4.json()
        for key in output:
            for cidr in output[key]['ip_ranges']:
                sortkey = 'OKTA#'+cidr
                hostmask = cidr.split('/')
                iptype = ipaddress.ip_address(hostmask[0])
                nametype = 'IPv'+str(iptype.version)+'#'
                iprange = cidr
                response = table.query(
                    KeyConditionExpression = Key('pk').eq(nametype) & Key('sk').eq(sortkey)
                )
                if len(response['Items']) == 0:
                    print('OKTA IP Ranges Updated')
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
        'body': json.dumps('Download Okta IP Ranges')
    }