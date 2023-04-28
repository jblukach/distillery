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

    r = requests.get('https://docs.tenable.com/ip-ranges/data.json')
    print('Download Status Code: '+str(r.status_code))

    if r.status_code == 200:
        output = r.json()
        if prevtoken != output['syncToken']:
            print('Updating Tenable IP Ranges')
            for cidr in output['prefixes']:
                sortkey = 'TENABLE#'+cidr['service']+'#'+cidr['region']+'#'+cidr['ip_prefix']
                hostmask = cidr['ip_prefix'].split('/')
                iptype = ipaddress.ip_address(hostmask[0])
                nametype = 'IPv'+str(iptype.version)+'#'
                iprange = cidr['ip_prefix']
                netrange = ipaddress.IPv4Network(cidr['ip_prefix'])
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv4Address(first))
                lastip = int(ipaddress.IPv4Address(last))
                table.put_item(
                    Item = {
                        'pk': nametype,
                        'sk': sortkey,
                        'service': cidr['service'],
                        'region': cidr['region'],
                        'cidr': iprange,
                        'edge': cidr['network_border_group'],
                        'created': output['createDate'],
                        'firstip': firstip,
                        'lastip': lastip
                    }
                )
            for cidr in output['ipv6_prefixes']:
                sortkey = 'TENABLE#'+cidr['service']+'#'+cidr['region']+'#'+cidr['ipv6_prefix']
                hostmask = cidr['ipv6_prefix'].split('/')
                iptype = ipaddress.ip_address(hostmask[0])
                nametype = 'IPv'+str(iptype.version)+'#'
                iprange = cidr['ipv6_prefix']
                netrange = ipaddress.IPv6Network(cidr['ipv6_prefix'])
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv6Address(first))
                lastip = int(ipaddress.IPv6Address(last))
                table.put_item( 
                    Item = {
                        'pk': nametype,
                        'sk': sortkey,
                        'service': cidr['service'],
                        'region': cidr['region'],
                        'cidr': iprange,
                        'edge': cidr['network_border_group'],
                        'created': output['createDate'],
                        'firstip': firstip,
                        'lastip': lastip
                    }
                )
            print('Tenable IP Ranges Updated')
            response = client.put_parameter(
                Name = os.environ['SSM_PARAMETER'],
                Value = output['syncToken'],
                Type = 'String',
                Overwrite = True
            )
        else:
            print('No Tenable IP Range Updates')

    return {
        'statusCode': 200,
        'body': json.dumps('Download Tenable IP Ranges')
    }