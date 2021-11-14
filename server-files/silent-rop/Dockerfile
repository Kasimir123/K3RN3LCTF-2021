FROM ubuntu AS app
RUN apt-get update && apt-get install -y patchelf && rm -rf /var/lib/apt/lists/*
WORKDIR /home/ctf
COPY challenge/ld-2.31.so .
COPY challenge/libc.so.6 .
COPY challenge/chal .
COPY challenge/flag.txt . 
RUN patchelf --set-interpreter ./ld-2.31.so --set-rpath ./ ./chal


FROM redpwn/jail
COPY --from=app / /srv
COPY --from=app /home/ctf/flag.txt /srv/app/flag.txt
COPY --from=app /home/ctf/chal /srv/app/run
COPY --from=app /home/ctf/libc.so.6 /srv/app/libc.so.6
COPY --from=app /home/ctf/ld-2.31.so /srv/app/ld-2.31.so

ENV JAIL_TIME 120
ENV JAIL_CONNS_PER_IP 1
ENV JAIL_MEM 20M
