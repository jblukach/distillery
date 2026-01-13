import ipaddress
import json
import sqlite3

def handler(event, context):

    print(event)

    try:

        code = 200
        ip = event['rawPath'][1:]
        address = str(int(ipaddress.ip_address(ip)))

        conn = sqlite3.connect('distillery.sqlite3')
        c = conn.cursor()
        c.execute("SELECT source, service, region, cidr FROM distillery WHERE firstip <= ? AND lastip >= ?", (address, address))
        msg = c.fetchall()
        conn.close()

    except:

        msg = 'Where the Internet Ends'
        code = 404

    return {
        'statusCode': code,
        'body': json.dumps(msg, indent = 4)
    }