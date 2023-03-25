import boto3
import ipaddress
import json
import os
import requests
from boto3.dynamodb.conditions import Key

def handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    cfipv4 = requests.get('https://www.cloudflare.com/ips-v4')
    print('IPv4 Download Status Code: '+str(cfipv4.status_code))

    if cfipv4.status_code == 200:
        print('Checking Cloudflare IPv4 Ranges')
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
                print('Cloudflare IP Ranges Updated')
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

    cfipv6 = requests.get('https://www.cloudflare.com/ips-v6')
    print('IPv6 Download Status Code: '+str(cfipv6.status_code))

    if cfipv6.status_code == 200:
        print('Checking Cloudflare IPv6 Ranges')
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
                print('Cloudflare IP Ranges Updated')
                netrange = ipaddress.IPv6Network(cidr)
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv6Address(first))
                lastip = int(ipaddress.IPv6Address(last))
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
        'body': json.dumps('Download Cloudflare IP Ranges')
    }