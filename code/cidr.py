import ipaddress
import json
import os
import sqlite3

def handler(event, context):

    try:
        ip = ipaddress.ip_address(event['rawQueryString'])
        ip = str(event['rawQueryString'])
    except ValueError:
        ip = ipaddress.ip_address(event['requestContext']['http']['sourceIp'])
        ip = str(event['requestContext']['http']['sourceIp'])

    address = str(int(ipaddress.ip_address(ip)))

    conn = sqlite3.connect('distillery.sqlite3')
    c = conn.cursor()
    c.execute("SELECT source, updated, cidr, firstip, lastip, region, service, border FROM distillery WHERE firstip <= ? AND lastip >= ?", (address, address))
    cidr = c.fetchall()
    conn.close()

    code = 200
    msg = {
        'ip': str(ip),
        'int': str(address),
        'cidr': cidr,
        'region': os.environ['AWS_REGION']
    }

    return {
        'statusCode': code,
        'body': json.dumps(msg, indent = 4)
    }