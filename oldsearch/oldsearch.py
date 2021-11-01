import boto3
import ipaddress
import json
import logging
import os
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    return response

def handler(event, context):
    
    logger.info(event)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    session_attributes = event['sessionAttributes'] if event['sessionAttributes'] is not None else {}
    slots = event['currentIntent']['slots']
    ipaddr = slots['cidrip']

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
                IndexName='firstip',KeyConditionExpression=Key('pk').eq('IPv4#') & Key('firstip').lte(intip)
            )
            firstdata = first['Items']
            while 'LastEvaluatedKey' in first:
                first = table.query(
                    IndexName='firstip',KeyConditionExpression=Key('pk').eq('IPv4#') & Key('firstip').lte(intip),
                    ExclusiveStartKey=first['LastEvaluatedKey']
                )
                try:
                    firstdata.update(first['Items'])
                except:
                    pass
            for item in firstdata:
                firstlist.append(item['sk']+'#'+str(item['created']))
               
            lastlist = []
            last = table.query(
                IndexName='lastip',KeyConditionExpression=Key('pk').eq('IPv4#') & Key('lastip').gte(intip)
            )
            lastdata = last['Items']
            while 'LastEvaluatedKey' in last:
                last = table.query(
                    IndexName='lastip',KeyConditionExpression=Key('pk').eq('IPv4#') & Key('lastip').gte(intip),
                    ExclusiveStartKey=last['LastEvaluatedKey']
                )
                try:
                    lastdata.update(last['Items'])
                except:
                    pass
            for item in lastdata:
                lastlist.append(item['sk']+'#'+str(item['created']))
            
            matches = set(firstlist) & set(lastlist)
            theresults = {}
            theresults["cidrs"] = []
            for line in matches:
                parsed = line.split('#')
                theresults["cidrs"].append(parsed)
            
            msg = theresults
            
        elif iptype.version == 6:
            
            intip = int(ipaddress.IPv6Address(ipaddr))
            
            firstlist = []
            first = table.query(
                IndexName='firstip',KeyConditionExpression=Key('pk').eq('IPv6#') & Key('firstip').lte(intip)
            )
            firstdata = first['Items']
            while 'LastEvaluatedKey' in first:
                first = table.query(
                    IndexName='firstip',KeyConditionExpression=Key('pk').eq('IPv6#') & Key('firstip').lte(intip),
                    ExclusiveStartKey=first['LastEvaluatedKey']
                )
                try:
                    firstdata.update(first['Items'])
                except:
                    pass
            for item in firstdata:
                firstlist.append(item['sk']+'#'+str(item['created']))
               
            lastlist = []
            last = table.query(
                IndexName='lastip',KeyConditionExpression=Key('pk').eq('IPv6#') & Key('lastip').gte(intip)
            )
            lastdata = last['Items']
            while 'LastEvaluatedKey' in last:
                last = table.query(
                    IndexName='lastip',KeyConditionExpression=Key('pk').eq('IPv6#') & Key('lastip').gte(intip),
                    ExclusiveStartKey=last['LastEvaluatedKey']
                )
                try:
                    lastdata.update(last['Items'])
                except:
                    pass
            for item in lastdata:
                lastlist.append(item['sk']+'#'+str(item['created']))
            
            matches = set(firstlist) & set(lastlist)
            theresults = {}
            theresults["cidrs"] = []
            for line in matches:
                parsed = line.split('#')
                theresults["cidrs"].append(parsed)
                
            msg = theresults
            
    except:
        
        msg = 'Invalid IP Address'
        pass

    return close(
		session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': str(msg)
        }
	)
