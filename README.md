# Smart Home Flask

## Build Image

### Dockerfile

This repo will be built in stages

The docker file Dockerfile runs through the following steps:  

 - get debian bullseye-slim image.  
 - install the requirements for python and flask on debian  
 - copy over the `requirements.txt` file and run `pip install` on it  
 - This is copied separately so that the dependencies are cached and dont need to run
    everytime the image is rebuilt  
 - copy over the application config file for apache  
 - copy over the `.wsgi` file. This is the entrypoint for our application, the `run.py` file,
   and the application directory  
 - enable the new apache config file and headers   
 - disable the default apache config file
 - Enable the smart-home.conf apache config file
 - expose port 80  
 - point the container to the application directory  
 - the run command. 

### Build
The command to build the image:
```
docker build -t smart-home-flask .
```

## Run Image
The command to run the image is:
```
docker run -d -p 80:80 --name smart-home-flask smart-home-flask
```
Alternatively, you can use docker-compose to build and run the image with:
```
docker-compose up -d
```

## Deploy 
```
sudo mkdir /opt/docker
sudo cp  -rf smart-home-flask /opt/docker
```
Create systemd service file called start-home-flask.service and put it in /etc/systemd/system
smart-home-flask.service:
```
[Unit]
Description=Startup of the smart-home-flask docker container.  
After=smart-home-mqtt-tls-subd.service
Requires=smart-home-mqtt-tls-subd.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/bash -c "docker compose -f /opt/docker/smart-home-flask/docker-compose.yaml up --detach"
ExecStop=/bin/bash -c "docker compose -f /opt/docker/smart-home-flask/docker-compose.yaml stop"

[Install]
WantedBy=multi-user.target
```
