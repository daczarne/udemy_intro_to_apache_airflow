# Docker

## Introduction to Docker

Docker is a container system for isolating environments. All configurations go in the `Dockerfile`. From it we build a **Docker Image**. We run the container with:

``` zsh
docker run <image_name>
```

The application runs inside the container. The container is like a Virtual Machine, but with no OS included (and thus lighter than a VM).

To define and run multiple container applications we use **Docker Compose**. Airflow is one of such applications since we need to run the MetaDB, the web-server, and the scheduler. Each one will run in a separate container, but they need to work together. To orchestrate all this we need a `docker-compose.yaml` file that describes the services that we want to run for the application. Each component of Airflow is a service. All containers in this orchestration will be able to communicate with the others since they share the same *network*.

## Run Airflow in a local Docker container

First let's create a directory and `cd` into it_

``` zsh
mkdir airflow-local && cd airflow-local
```

Now we need to download the `docker-compose.yaml` file by running:

``` zsh
wget https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml
```
