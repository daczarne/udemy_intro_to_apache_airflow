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

Docker will start creating everything for you now. You'll know it's done when you see the following output:

``` shell
Creating airflow-local_postgres_1 ... done
Creating airflow-local_redis_1    ... done
Creating airflow-local_flower_1            ... done
Creating airflow-local_airflow-scheduler_1 ... done
Creating airflow-local_airflow-init_1      ... done
Creating airflow-local_airflow-webserver_1 ... done
Creating airflow-local_airflow-worker_1    ... done
```

To check what's running on the local Airflow instance, you can run the command:

``` zsh
docker ps
```

Your output should look something like this:

``` shell
CONTAINER ID   IMAGE                  COMMAND                  CREATED         STATUS                             PORTS                              NAMES
356ef38da7eb   apache/airflow:2.1.0   "/usr/bin/dumb-init …"   4 minutes ago   Up 3 minutes (healthy)             8080/tcp                           airflow-local_airflow-worker_1
330df0729306   apache/airflow:2.1.0   "/usr/bin/dumb-init …"   4 minutes ago   Up 25 seconds (health: starting)   0.0.0.0:8080->8080/tcp             airflow-local_airflow-webserver_1
d830875e346a   apache/airflow:2.1.0   "/usr/bin/dumb-init …"   4 minutes ago   Up 3 minutes (healthy)             8080/tcp                           airflow-local_airflow-scheduler_1
314115faf0ee   apache/airflow:2.1.0   "/usr/bin/dumb-init …"   4 minutes ago   Up 3 minutes (healthy)             0.0.0.0:5555->5555/tcp, 8080/tcp   airflow-local_flower_1
e5be6c8f9fe8   postgres:13            "docker-entrypoint.s…"   4 minutes ago   Up 4 minutes (healthy)             5432/tcp                           airflow-local_postgres_1
c4ca5b54cb81   redis:latest           "docker-entrypoint.s…"   4 minutes ago   Up 4 minutes (healthy)             0.0.0.0:6379->6379/tcp             airflow-local_redis_1
```

That's the list of containers that are running on the local instance, along with some information on them (like the image, how long ago they were created, etc.). If you now navigate to `localhost:8080` on your browser, you should be able to access the Airflow UI.

To stop docker compose run `docker-compose stop`. You should see an output that looks like the following:

``` shell
Stopping airflow-local_airflow-worker_1    ... done
Stopping airflow-local_airflow-webserver_1 ... done
Stopping airflow-local_airflow-scheduler_1 ... done
Stopping airflow-local_flower_1            ... done
Stopping airflow-local_postgres_1          ... done
Stopping airflow-local_redis_1             ... done
```

## Local executor

To use the `LocalExecutor` just change `AIRFLOW__CORE__EXECUTOR: CeleryExecutor` to `AIRFLOW__CORE__EXECUTOR: LocalExecutor`. Comment out the `AIRFLOW__CELERY__RESULT_BACKEND` and `AIRFLOW__CELERY__BROKER_URL` since they are not going to be used. Since we don't need `redis` either, you can comment out that as well. Same is true for the `airflow-worker` and `flower` services.
