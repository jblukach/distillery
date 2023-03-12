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

    r = requests.get('https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json')
    print('Download Status Code: '+str(r.status_code))

    if r.status_code == 200:
        output = r.json()
        if prevtoken != output['last_updated_timestamp']:
            print('Updating Oracle IP Ranges')
            for region in output['regions']:
                for cidr in region['cidrs']:
                    sortkey = 'ORACLE#'+region['region']+'#'+cidr['cidr']
                    hostmask = cidr['cidr'].split('/')
                    iptype = ipaddress.ip_address(hostmask[0])
                    nametype = 'IPv'+str(iptype.version)+'#'
                    iprange = cidr['cidr']
                    netrange = ipaddress.IPv4Network(cidr['cidr'])
                    first, last = netrange[0], netrange[-1]
                    firstip = int(ipaddress.IPv4Address(first))
                    lastip = int(ipaddress.IPv4Address(last))
                    table.put_item(
                        Item = {
                            'pk': nametype,
                            'sk': sortkey,
                            'region': region['region'],
                            'cidr': iprange,
                            'created': output['last_updated_timestamp'],
                            'firstip': firstip,
                            'lastip': lastip
                        } 
                    )

            print('Oracle IP Ranges Updated')
            response = client.put_parameter(
                Name = os.environ['SSM_PARAMETER'],
                Value = output['last_updated_timestamp'],
                Type = 'String',
                Overwrite = True
            )
        else:
            print('No Oracle IP Range Updates')

    return {
        'statusCode': 200,
        'body': json.dumps('Download Oracle IP Ranges')
    }