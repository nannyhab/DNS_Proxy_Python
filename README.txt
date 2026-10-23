DNS Proxy + DNS over HTTPS
==========================

Name: Adnan Alhabian   NetID: fpr1895

Setup: Install Python 3, then run pip install -r requirements.txt


Part 1 - UDP DNS proxy
----------------------
1. Start program (add an upstream server like 1.1.1.1 if you want, default is 8.8.8.8):
     python3 part1.py   or   python3 part1.py 1.1.1.1
2. In another terminal:
     dig @127.0.0.1 -p 1053 example.com A

Details:
  - Only listens on 127.0.0.1, so nothing outside your computer can reach it.
  - Each query gets its own thread, so many clients work at once.
  - Passes packets through unchanged, so the transaction ID stays the same.
  - Waits 2 seconds for the upstream, up to 3 tries.
  - Prints each query's name and type, and each response's size.


Part 2 - DNS over HTTPS
-----------------------
1. Start program:
     python3 part2.py
2. In another terminal:
     dig @127.0.0.1 -p 1053 www.github.com A

Details:
  - Asks Google at https://dns.google/resolve and turns its JSON answer into a normal DNS reply.
  - Keeps the same ID, flags and question.
  - Supports A and CNAME (www.github.com shows both), plus others like AAAA and MX.
  - verify=True checks Google's HTTPS certificate.
  - If Google can't be reached, dig gets SERVFAIL.


Part 3 - Persistent session (extra credit)
------------------------------------------
1. Start program:
     python3 part3.py
2. In another terminal, send 10 queries:
     for i in $(seq 1 10); do dig @127.0.0.1 -p 1053 google.com A > /dev/null; done

Details:
  - Reuses one HTTPS connection to Google (requests.Session()) for every query.
  - Prints each query's time, from receiving it to sending the answer.

Measurements:
  First query:            ____ ms
  Queries 2-10 average:   ____ ms

Why: the first query has to open the connection and do the HTTPS handshake.
The rest reuse that connection and skip it, so they're much faster.
Part 2 has no session, so it does the handshake on every query.
