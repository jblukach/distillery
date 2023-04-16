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

    headers = {'User-Agent': 'Distillery Python Client/1.0'}
    r = requests.get('https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519', headers=headers)
    print('Link Status Code: '+str(r.status_code))

    staged = r.text
    parsed = staged.split('manually')
    front = parsed[1].split(' href="')
    back = front[1].split('" ')
    link = back[0]

    r = requests.get(link)
    print('Download Status Code: '+str(r.status_code))

    if r.status_code == 200:
        output = r.json()
        if prevtoken != str(output['changeNumber']):
            print('Updating Azure IP Ranges')
            for cidr in output['values']:
                for ip in cidr['properties']['addressPrefixes']:
                    sortkey = 'AZURE#'+cidr['name']+'#'+ip
                    hostmask = ip.split('/')
                    iptype = ipaddress.ip_address(hostmask[0])
                    nametype = 'IPv'+str(iptype.version)+'#'
                    if nametype == 'IPv4#':
                        netrange = ipaddress.IPv4Network(ip)
                        first, last = netrange[0], netrange[-1]
                        firstip = int(ipaddress.IPv4Address(first))
                        lastip = int(ipaddress.IPv4Address(last))
                    elif nametype == 'IPv6#':
                        netrange = ipaddress.IPv6Network(ip)
                        first, last = netrange[0], netrange[-1]
                        firstip = int(ipaddress.IPv6Address(first))
                        lastip = int(ipaddress.IPv6Address(last))
                    table.put_item(
                        Item = {  
                            'pk': nametype,
                            'sk': sortkey,
                            'service': cidr['name'],
                            'change': cidr['properties']['changeNumber'],
                            'cidr': ip,
                            'created': output['changeNumber'],
                            'firstip': firstip,
                            'lastip': lastip
                        }
                    )
            print('Azure IP Ranges Updated')
            response = client.put_parameter(
                Name = os.environ['SSM_PARAMETER'],
                Value = str(output['changeNumber']),
                Type = 'String',
                Overwrite = True
            )
        else:
            print('No Azure IP Range Updates')

    return {
        'statusCode': 200,
        'body': json.dumps('Download Azure IP Ranges')
    }