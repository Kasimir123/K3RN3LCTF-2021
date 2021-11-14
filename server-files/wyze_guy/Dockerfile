FROM ubuntu:latest

RUN apt update -y
RUN apt install -y qemu-system curl

COPY . /ctf

RUN useradd ctf
RUN chown -R ctf /ctf
USER ctf

WORKDIR /ctf

CMD ["/ctf/start.sh"]


