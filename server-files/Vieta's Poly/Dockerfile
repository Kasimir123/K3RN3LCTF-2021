FROM python:slim AS app

FROM redpwn/jail
COPY --from=app / /srv

COPY main.py /srv/app/run


ENV JAIL_TIME 120
ENV JAIL_CONNS_PER_IP 1
ENV JAIL_MEM 20M
