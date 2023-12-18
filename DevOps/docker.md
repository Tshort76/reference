# Overview
Containers are sandbox environments that run on the host OS, allowing for environment isolation without the overhead of virtual machines.  Isolation allows users to package an application with all of its dependencies into a standardized unit for software development and deployment. Unlike virtual machines (VMs), containers do not have high overhead and hence enable more efficient usage of the underlying system and resources.

## Advantages
- Rapid iteration of environment changes
- Reproducibility application across systems (since env is nearly constant)
- Low overhead, esp. when compared to VMs
- Portability of environment

## Components
<dl>
  <dt>Docker Hub</dt>
  <dd>Remote registry of docker images (~ pypi or NPM) </dd>
  <dt>Image</dt>
  <dd>The definition/specification/blueprint for an application environment (~ Class)</dd>
  <dt>Container</dt>
  <dd>The runnable instance of an Image (~ Object)</dd>
  <dt>Docker Daemon</dt>
  <dd>Background service running on the host that manages building, running, and distributing containers</dd>
  <dt>Docker Client</dt>
  <dd>Command line tool used to interact with Daemon</dd>
  <dt>Dockerfile</dt>
  <dd>text file that defines a Docker image (~ source code)</dd>
</dl>

# Core commands
## run
### Execution of 'docker run <image>'
1. The Docker client contacts the Docker daemon.
2. The Docker daemon pulls the image from the Docker Hub
3. The Docker daemon created a new container from that image which runs the executable, which produces some output
4. The Docker daemon streamed that output to the Docker client, which sends it to the terminal.
### arguments
<dl>
  <dt>-it</dt>
  <dd>Interactive mode to send multiple commands to the container</dd>
  <dt>--rm</dt>
  <dd>Remove the container when it exits</dd>
  <dt>-d</dt>
  <dd>Run in detached mode</dd>
  <dt>--name</dt>
  <dd>named the container</dd>
  <dt>-P</dt>
  <dd>publish all export ports to random ports</dd>
  <dt>-p <external_port>:<internal_port></dt>
  <dd>expose an container's internal port on a specific external port</dd>
  <dt>--help</dt>
  <dd>See a list of supported flags</dd>
</dl>

## port
`docker port <container-name>` View all mapped ports for a container
## stop
`docker stop <container-name/ID>` Stock a running container
## ps
- `docker ps` shows all containers that are currently running
### arguments
<dl>
  <dt>-a</dt>
  <dd>All ... show all containers that are on disk</dd>
  <dt>-q</dt>
  <dd>Return only the numeric ids</dd>
  <dt>-f</dt>
  <dd>filter output based on the conditions provided</dd>
</dl>

## images
`docker images` to list all locally available images

## rm
- `docker rm <container_id>` to remove a specific image
- ` docker rm $(docker ps -a -q -f status=exited)` to remove all containers with an exited status
  - `docker container prune` accomplishes the same thing

## rmi
`docker rmi` - removes images (vs containers)

## build
`docker build -t <tag_name> .` builds an image from the Dockerfile, taking an optional tag name with `-t` and a location of the directory containing the Dockerfile.

# Dockerfile
```dockerfile
FROM python:3.8

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files from client's cwd to the container's workdir
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# define the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python", "./app.py"]
```

# Multi-container environments
TODO 
https://docker-curriculum.com/#multi-container-environments

# Sources
- [https://docker-curriculum.com/](https://docker-curriculum.com/)
- 