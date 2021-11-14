FROM python:slim AS app

RUN pip install --no-cache-dir numpy


FROM redpwn/jail
COPY --from=app / /srv
COPY flag.txt /srv/app/flag.txt
COPY Private.py /srv/app/Private.py

COPY dangerouscommute.py /srv/app/run


ENV JAIL_TIME 1200
ENV JAIL_CONNS_PER_IP 1
ENV JAIL_MEM 40M
