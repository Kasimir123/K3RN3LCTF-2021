# K3RN3LCTF-2021
Repository with the downloadable files and server files for the 2021 K3RN3LCTF.

## How to create the docker images

If you want to test a remote challenge after the ctf you can, on a linux machine with docker installed, go into the folder for the challenge and then run:

```
sudo docker-compose up
```

if you want to run the image in the background you can run:

```
sudo docker-compose up -d
```

This will create the docker image on whatever port is specified in docker-compose.yml. To double check what port a container is running on you can run:

```
sudo docker ps
```

When the image has been started you can connect to it with:

```
nc 0.0.0.0 port
```

All challenges can be started up from this repository except for wyze guy as it requires a 3 GB file that cannot be added to github.