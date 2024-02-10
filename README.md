# Introduction

    This service will act as kafka producer downloads 837/835 claims ans sends it to kafka broker.

## Required pip packages

- pymongo
- flask_cors
- flask
- pyx12

## Required Python Scripts

- block_update.py
- wsgi_upload.py
  
## Other Required  Files

- Nil

## Script Execution Command

    gunicorn -w 1 -b  0.0.0.0:4000 wsgi_upload:app

## Changeable Urls

- **Pymongo Database URL** in **upload_Service.py**
- **Kakfa Broker URL(bootstrap.servers)** in **block_update.py**

## Local Docker Execution Command

Docker Command to Run: docker run --rm -it -p 8080:8080 -v my_shared_volume:/app/files upload-service

## Ecs Service Configurations

- Volume Required: Yes
- Type of Volume: EFS(Elastic File System)
- Volume Mount: **/app/files/**
- Network Mode: Bridge Network
- LoadBalancer Required: Yes