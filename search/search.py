import boto3
import ipaddress
import json
import logging
import os
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']
    
def get_slot(intent_request, slotName):
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        return slots[slotName]['value']['interpretedValue']
    else:
        return None    

def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']
    return {}

def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }

def handler(event, context):
    
    logger.info(event)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    session_attributes = get_session_attributes(event)
    slots = get_slots(event)
    ipaddr = get_slot(event, 'cidrip')

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
                firstdata.update(first['Items'])
            for item in firstdata:
                firstlist.append(item['sk']+'#'+item['created'])
               
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
                lastdata.update(last['Items'])
            for item in lastdata:
                lastlist.append(item['sk']+'#'+item['created'])
            
            matches = set(firstlist) & set(lastlist)
            theresults = {}
            theresults["cidrs"] = []
            for line in matches:
                parsed = line.split('#')
                linedict = {'cloud': parsed[0], 'service': parsed[1], 'region': parsed[2], 'cidr': parsed[3], 'lastseen': parsed[4]}
                theresults["cidrs"].append(linedict)
            
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
                firstdata.update(first['Items'])
            for item in firstdata:
                firstlist.append(item['sk']+'#'+item['created'])
               
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
                lastdata.update(last['Items'])
            for item in lastdata:
                lastlist.append(item['sk']+'#'+item['created'])
            
            matches = set(firstlist) & set(lastlist)
            theresults = {}
            theresults["cidrs"] = []
            for line in matches:
                parsed = line.split('#')
                linedict = {'cloud': parsed[0], 'service': parsed[1], 'region': parsed[2], 'cidr': parsed[3], 'lastseen': parsed[4]}
                theresults["cidrs"].append(linedict)
                
            msg = theresults
            
    except:
        
        msg = 'Invalid IP Address'
        pass

    message =  {
        'contentType': 'PlainText',
        'content': str(msg)
    }
    
    fulfillment_state = "Fulfilled"
    
    return close(event, session_attributes, fulfillment_state, message)