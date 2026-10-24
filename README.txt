DNS Proxy + DNS over HTTPS
==========================

Name: Adnan Alhabian   NetID: fpr1895

Setup: Install Python 3, then run pip install -r requirements.txt


Part 1 - UDP DNS proxy
----------------------
1. Start program (it uses 8.8.8.8 by default, or you can add your own upstream server like 1.1.1.1):
     python3 part1.py   or   python3 part1.py 1.1.1.1
2. In another terminal, run:
     dig @127.0.0.1 -p 1053 example.com A

Details:
  - It only listens on 127.0.0.1, so nobody outside your computer can get to it.
  - Every query gets its own thread, so a bunch of clients can use it at the same time.
  - It passes packets along without touching them, so the transaction ID comes back exactly the same.
  - If the upstream server doesn't answer within 2 seconds, it tries again, up to 3 times.
  - For every query, it prints the name and type, plus how big the response was.


Part 2 - DNS over HTTPS
-----------------------
1. Start program:
     python3 part2.py
2. In another terminal, run:
     dig @127.0.0.1 -p 1053 www.github.com A

Details:
  - Instead of 8.8.8.8, it asks Google's web API at https://dns.google/resolve, then turns
    Google's JSON answer back into a normal DNS reply for dig.
  - The ID, flags and question all come back the same as what dig sent.
  - A and CNAME both work (www.github.com shows you both), and so do other types like AAAA and MX.
  - verify=True makes sure it's really talking to Google by checking Google's HTTPS certificate.
  - If Google can't be reached, dig gets a SERVFAIL back instead of being left hanging.


Part 3 - Persistent session (extra credit)
------------------------------------------
1. Start program:
     python3 part3.py
2. In another terminal, send it 10 queries in a row:
     for i in $(seq 1 10); do dig @127.0.0.1 -p 1053 google.com A > /dev/null; done

Details:
  - It opens one HTTPS connection to Google (requests.Session()) and keeps reusing it for every query.
  - For each query, it prints how long it took, from the moment the question came in to when
    the answer went back out.

Measurements:
  First query:            86.8 ms
  Queries 2-10 average:   19.2 ms

The first query is the slow one because it has to open a connection to Google and do the
HTTPS handshake before it can even ask anything. After that, every query just reuses the
connection that's already open, so it skips all that setup and comes back about 4.5 times
faster. Part 2 doesn't keep a connection around, so it has to go through the handshake every
single time.
