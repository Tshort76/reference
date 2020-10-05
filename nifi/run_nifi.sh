#!/bin/bash

docker rm nifi

docker run --name nifi -p 8080:8080 --mount source=share,destination=/mnt/data apache/nifi:latest