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

The first section of the `docker-compose.yaml` is called `x-airflow-common:`. Here you can find the instructions that are going to be shared by all of the services.

- `image:` specifies the version of Airflow that is going to be used. In this case `2.1.0`.
- `environment:` lists all the environment variables used by Airflow in the container.
- `volumes:` allows you to bind folders from your local machine to the folders in the container. For example, `./dags:/opt/airflow/dags` says that the local folder `./dags` should be synchronized with the folder `/opt/airflow/dags` in the container.
- the `depends_on:` section allows us to define the order in which the dependencies need to be run, and the condition that needs to be met in order to consider the dependency as done. In this case, we are saying that `redis` needs to be run first, and only after the service is up and running (`service_healthy`), the `postgres` needs to run.

Then comes the section `services:`. Here is where each service is described. By default, we get the description of how the `postgres` and `redis` services need to be set-up. For these, we need to specify the `image` (version), environment variables, health checks, etc.

The we get a list of the Airflow services `airflow-webserver`, `airflow-scheduler`, and `airflow-worker`. Below their names we have the instruction `<<: *airflow-common`. This is telling the composer that it needs to use the instructions in the `x-airflow-common` section. Below this initial instruction we can add service-specific instructions.

`airflow-init` is a special service that only needs to be run once. It initializes the Airflow DB and creates the first Admin user. We can specify the username and password here. By default both are `airflow`.

The `flower` service is used to monitor the workers where the tasks are going to be executed.

Now, to run Airflow locally using this docker compose file we run:

``` zsh
docker-compose -f docker-compose.yaml up -d
```
