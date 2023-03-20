import boto3
import ipaddress
import json
import os
import requests

def handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    client = boto3.client('ssm')
    response = client.get_parameter(Name=os.environ['SSM_PARAMETER'])
    prevtoken = response['Parameter']['Value']

    r = requests.get('https://geofeed.constant.com/?json')
    print('Download Status Code: '+str(r.status_code))

    if r.status_code == 200:
        output = r.json()
        if prevtoken != output['updated']:
            print('Updating Vultr IP Ranges')
            for subnet in output['subnets']:
                sortkey = 'VULTR#'+subnet['region']+'#'+subnet['ip_prefix']
                hostmask = subnet['ip_prefix'].split('/')
                iptype = ipaddress.ip_address(hostmask[0])
                nametype = 'IPv'+str(iptype.version)+'#'
                iprange = subnet['ip_prefix']
                if nametype == 'IPv4#':
                    netrange = ipaddress.IPv4Network(subnet['ip_prefix'])
                    first, last = netrange[0], netrange[-1]
                    firstip = int(ipaddress.IPv4Address(first))
                    lastip = int(ipaddress.IPv4Address(last))
                elif nametype == 'IPv6#':
                    netrange = ipaddress.IPv6Network(subnet['ip_prefix'])
                    first, last = netrange[0], netrange[-1]
                    firstip = int(ipaddress.IPv6Address(first))
                    lastip = int(ipaddress.IPv6Address(last))
                table.put_item(
                    Item = {
                        'pk': nametype,
                        'sk': sortkey,
                        'region': subnet['region'],
                        'cidr': iprange,
                        'city': subnet['city'],
                        'country': subnet['alpha2code'],
                        'created': output['updated'],
                        'firstip': firstip,
                        'lastip': lastip
                    } 
                )

            print('Vultr IP Ranges Updated')
            response = client.put_parameter(
                Name = os.environ['SSM_PARAMETER'],
                Value = output['updated'],
                Type = 'String',
                Overwrite = True
            )
        else:
            print('No Vultr IP Range Updates')

    return {
        'statusCode': 200,
        'body': json.dumps('Download Vultr IP Ranges')
    }