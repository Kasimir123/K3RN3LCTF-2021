FROM ubuntu:20.04 AS app
RUN apt-get update && apt-get install -y patchelf && rm -rf /var/lib/apt/lists/*
WORKDIR /home/ctf
COPY deploy/ .
RUN patchelf --set-interpreter /home/ctf/ld-linux-x86-64.so.2 --set-rpath /home/ctf ./gradebook

FROM redpwn/jail

COPY --from=app / /srv
COPY --from=app /home/ctf/gradebook /srv/app/
COPY --from=app /home/ctf/ld-linux-x86-64.so.2 /srv/app/
COPY --from=app /home/ctf/libc.so.6 /srv/app/
COPY --from=app /home/ctf/flag.txt /srv/app/
RUN cp /srv/app/gradebook /srv/app/run

ENV JAIL_TIME 120
ENV JAIL_CONNS_PER_IP 1
ENV JAIL_MEM 20M
