import socket
import threading

import requests
from dnslib import QTYPE, RR, DNSRecord


def handle(data, client):
    request = DNSRecord.parse(data)
    name = str(request.q.qname)
    qtype = QTYPE[request.q.qtype]

    reply = request.reply(aa=0)
    try:
        result = requests.get("https://dns.google/resolve", params={"name": name, "type": qtype}, timeout=3, verify=True).json()
        reply.header.rcode = result["Status"]
        for answer in result.get("Answer", []):
            line = f"{answer['name']} {answer['TTL']} IN {QTYPE[answer['type']]} {answer['data']}"
            reply.add_answer(*RR.fromZone(line))
    except Exception as error:
        print(f"error: {name}: {error}")
        reply.header.rcode = 2

    response = reply.pack()
    server.sendto(response, client)
    print(f"response: {name} {qtype}, {len(response)} bytes")


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1", 1053))
print("listening on 127.0.0.1:1053")

while True:
    data, client = server.recvfrom(4096)
    threading.Thread(target=handle, args=(data, client)).start()
