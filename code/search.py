import ipaddress
import json
import sqlite3

def handler(event, context):

    print(event)

    try:
        iptype = ipaddress.ip_address(event['ip']) ### SLACK ###
        if iptype.version == 4 or iptype.version == 6:
            ip = event['ip']
    except:
        try:                      
            iptype = ipaddress.ip_address(event['rawPath'][1:]) ### URL ###
            if iptype.version == 4 or iptype.version == 6:
                ip = event['rawPath'][1:]
        except:
            iptype = ipaddress.ip_address(event['headers']['x-forwarded-for']) ### USER ###
            if iptype.version == 4 or iptype.version == 6:
                ip = event['headers']['x-forwarded-for']
            pass
        pass

    if iptype.version == 4:
        address = int(ipaddress.IPv4Address(ip))
    elif iptype.version == 6:
        address = int(ipaddress.IPv6Address(ip))

    conn = sqlite3.connect('distillery.sqlite3')
    c = conn.cursor()
    c.execute("SELECT source, service, region, cidr FROM distillery WHERE firstip <= ? AND lastip >= ?", (address, address))
    results = c.fetchall()
    conn.close()

    return {
        'statusCode': 200,
        'body': json.dumps(results, indent = 4)
    }