import socket
import sys
import threading

UPSTREAM = sys.argv[1] if len(sys.argv) > 1 else "8.8.8.8"
TYPES = {1: "A", 2: "NS", 5: "CNAME", 15: "MX", 16: "TXT", 28: "AAAA"} #important for mapping the types, 


def get_question(query):
    labels = []
    i = 12
    while query[i] != 0:
        labels.append(query[i + 1:i + 1 + query[i]].decode())
        i += query[i] + 1
    qtype = int.from_bytes(query[i + 1:i + 3], "big")
    print(f'for debugging purposes {labels}')
    return ".".join(labels), TYPES.get(qtype, qtype)


def handle(query, client):
    name, qtype = get_question(query)
    print(f"query: {name} {qtype}")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as upstream:
        upstream.settimeout(2)
        for attempt in range(1, 4):
            upstream.sendto(query, (UPSTREAM, 53))
            try:
                response = upstream.recv(4096)
                server.sendto(response, client)
                print(f"response: {name}, {len(response)} bytes")
                return
            except socket.timeout:
                print(f"timeout {attempt}/3: {name}")


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1", 1053))
print(f"listening on 127.0.0.1:1053, upstream {UPSTREAM}")

while True:
    query, client = server.recvfrom(4096)
    threading.Thread(target=handle, args=(query, client)).start()
