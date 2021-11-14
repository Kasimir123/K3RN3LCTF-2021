FROM python:slim AS app

RUN pip install --no-cache-dir pycryptodome 

FROM redpwn/jail
COPY --from=app / /srv
COPY flag.txt /srv/app/flag.txt
COPY mountaincipher.py /srv/app/mountaincipher.py

COPY server.py /srv/app/run


ENV JAIL_TIME 1200
ENV JAIL_CONNS_PER_IP 1
ENV JAIL_MEM 20M
