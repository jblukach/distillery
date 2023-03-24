import boto3
import ipaddress
import json
import os
from boto3.dynamodb.conditions import Key

def handler(event, context):

    print(event)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    try:
        ipaddr = event['ip']            ### SLACK ###
    except:
        pass

    try:
        ipaddr = event['rawPath'][1:]   ### URL ###
    except:
        pass

    try:

        iptype = ipaddress.ip_address(ipaddr)

        if iptype.is_multicast == True:
            msg = 'Multicast IP Address - RFC 3171 (IPv4) or RFC 2373 (IPv6)'
        elif iptype.is_private == True:
            msg = 'Private IP Address - IANA IPv4/IPv6 Special Registry'
        elif iptype.is_unspecified == True:
            msg = 'Unspecified IP Address - RFC 5735 (IPv4) or RFC 2373 (IPv6)'
        elif iptype.is_reserved == True:
            msg = 'Reserved IP Address - IETF Requirment'
        elif iptype.is_loopback == True:
            msg = 'Loopback IP Address - RFC 3330 (IPv4) or RFC 2373 (IPv6)'
        elif iptype.is_link_local == True:
            msg = 'Link Local IP Address - RFC 3927'

        elif iptype.version == 4:

            intip = int(ipaddress.IPv4Address(ipaddr))

            firstlist = []
            first = table.query(
                IndexName = 'firstip',
                KeyConditionExpression = Key('pk').eq('IPv4#') & Key('firstip').lte(intip)
            )
            firstdata = first['Items']
            while 'LastEvaluatedKey' in first:
                first = table.query(
                    IndexName = 'firstip',
                    KeyConditionExpression = Key('pk').eq('IPv4#') & Key('firstip').lte(intip),
                    ExclusiveStartKey = first['LastEvaluatedKey']
                )
                firstdata.extend(first['Items'])
            for item in firstdata:
                firstlist.append(item['sk']+'#'+str(item['created']))

            lastlist = []
            last = table.query(
                IndexName = 'lastip',
                KeyConditionExpression = Key('pk').eq('IPv4#') & Key('lastip').gte(intip)
            )
            lastdata = last['Items']
            while 'LastEvaluatedKey' in last:
                last = table.query(
                    IndexName = 'lastip',
                    KeyConditionExpression = Key('pk').eq('IPv4#') & Key('lastip').gte(intip),
                    ExclusiveStartKey = last['LastEvaluatedKey']
                )
                lastdata.extend(last['Items'])
            for item in lastdata:
                lastlist.append(item['sk']+'#'+str(item['created']))

            matches = set(firstlist) & set(lastlist)
            theresults = {}
            theresults["cidrs"] = []
            for line in matches:
                parsed = line.split('#')
                theresults["cidrs"].append(parsed)

            code = 200
            msg = theresults

        elif iptype.version == 6:

            intip = int(ipaddress.IPv6Address(ipaddr))

            firstlist = []
            first = table.query(
                IndexName = 'firstip',
                KeyConditionExpression = Key('pk').eq('IPv6#') & Key('firstip').lte(intip)
            )
            firstdata = first['Items']
            while 'LastEvaluatedKey' in first:
                first = table.query(
                    IndexName = 'firstip',
                    KeyConditionExpression = Key('pk').eq('IPv6#') & Key('firstip').lte(intip),
                    ExclusiveStartKey = first['LastEvaluatedKey']
                )
                firstdata.extend(first['Items'])
            for item in firstdata:
                firstlist.append(item['sk']+'#'+str(item['created']))

            lastlist = []
            last = table.query(
                IndexName = 'lastip',
                KeyConditionExpression = Key('pk').eq('IPv6#') & Key('lastip').gte(intip)
            )
            lastdata = last['Items']
            while 'LastEvaluatedKey' in last:
                last = table.query(
                    IndexName = 'lastip',
                    KeyConditionExpression = Key('pk').eq('IPv6#') & Key('lastip').gte(intip),
                    ExclusiveStartKey = last['LastEvaluatedKey']
                )
                lastdata.extend(last['Items'])
            for item in lastdata:
                lastlist.append(item['sk']+'#'+str(item['created']))

            matches = set(firstlist) & set(lastlist)
            theresults = {}
            theresults["cidrs"] = []
            for line in matches:
                parsed = line.split('#')
                theresults["cidrs"].append(parsed)

            code = 200
            msg = theresults

    except:

        code = 404
        msg = 'Where the Internet Ends'

        pass

    return {
        'statusCode': code,
        'body': json.dumps(msg, indent = 4)
    }