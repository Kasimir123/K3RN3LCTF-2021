FROM ubuntu AS app
RUN apt-get update && rm -rf /var/lib/apt/lists/*
WORKDIR /home/ctf
COPY challenge .


FROM redpwn/jail
COPY --from=app / /srv
COPY --from=app /home/ctf/flag.txt /srv/app/
COPY --from=app /home/ctf/chal /srv/app/run

ENV JAIL_TIME 120
ENV JAIL_CONNS_PER_IP 1
ENV JAIL_MEM 20M
