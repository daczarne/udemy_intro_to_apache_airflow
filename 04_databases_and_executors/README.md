# Databases and Executors

[The default configuration](#the-default-configuration)  
[Installing PostgreSQL](#installing-postgresql)  
[Local executor](#local-executor)  
[Celery executor](#celery-executor)  
[Concurrency](#concurrency)  

## The default configuration

By default, Airflow uses the `SequentialExecutor` to run tasks. If two tasks have the same priority there's no way of knowing which one will be executed first (they should be parallelized). There are two parameters in Airflow that allow you to configure the executor: `sql_alchemy_conn` corresponds to the default Metastore path, and `executor`.

``` zsh
airflow config get-value core sql_alchemy_conn
```

SQLite does not allow multiple writes at the same time, this is why when using SQLite, only one task can be run at a time.

``` zsh
airflow config get-value core executor
```

As stated, the default executor is `SequentialExecutor`. To allow tasks in parallel, change the DB to PostgreSQL (which allows for multiple reads and writes to occur simultaneously), and the executor to the `LocalExecutor`.

## Installing PostgreSQL

In the command-line run

``` zsh
sudo apt update
```

to update all packages. Then install PostgreSQL by running

``` zsh
sudo apt install postgresql
```

To connect to PostgreSQL run

``` zsh
sudo -u postgres psql
```

Specify a password with the statement

``` sql
ALTER USER postgres PASSWORD '<new_password>';
```

Now open the `airflow.cfg` file and change

``` cfg
sql_alchemy_conn = sqlite:////home/airflow/airflow/airflow.db
```

for

``` cfg
sql_alchemy_conn = postgresql+psycopg2://postgres:postgres@localhost/postgres
```

Now make sure that you can reach the DB by running

``` zsh
airflow db check
```

## Local executor

The local executor will create sub-processes and execute each task in a sub-process. To change the executor open the `airflow.cfg` file and change

``` cfg
executor = SequentialExecutor
```

for

``` cfg
executor = LocalExecutor
```

Once changed make sure to kill all Airflow processes (like Web Server, or Scheduler) on your command line and re-initialize the DB by running

``` zsh
airflow db init
```

and create a new user. Then re-launch the Web Server and Scheduler.

## Celery Executor

The `LocalExecutor` is limited by the resources in the machine you are running it. To overcome this limitations you can use the `CeleryExecutor` or the `KubernetesExecutor`. All executors use the Queue to execute the tasks in the correct order. Every time a task needs to be executed it will be pushed inside the Queue. When the executor is ready to execute the task, it will pull it from the Queue. When using these executors, they are pulled by worker machines (not sub-processes).

The `CeleryExecutor` is a distributed task system. The more machines you use, the more tasks that can be run in tandem. With this executor the Queue is outside the executor and is third-party provided (in this case by Redis). This third-party tool needs to be installed and set-up.

![](airflow/img/celery_executor.png)

With Celery, each worker has a parameter called `worker_concurrency` that determines the number of tasks that can be run at the same time per worker machine. This needs to be defined in the `airflow.cfg` file.

Since multiple machines are going to be used as workers, each of them needs to be configured and have the necessary dependencies installed in order to be able to run the tasks.

To configure the executor make sure you've stopped the servers and install the Celery package by running

``` zsh
pipenv install 'apache-airflow[celery]'
```

Now we need to install Redis. First update the packages by running

``` zsh
sudo apt update
```

Then install Redis by running

``` zsh
sudo apt install redis-server
```

Now modify the Redis configuration to use it as a service. To open the configuration file run

``` zsh
sudo nano /etc/redis/redis.conf
```

Near the bottom of the file change the value of `supervised no` to `supervised systemd`. Exit the file with `Ctrl + x` and save it with `y`, and press `Enter`. Now restart Redis by running

``` zsh
sudo systemctl restart redis.service
```

To check if Redis is running use the command

``` zsh
sudo systemctl status redis.service
```

Now open the `airflow.cfg` file and change the `executor = CeleryExecutor` variable. Now make sure to set the following parameters:

- change `broker_url` from `redis://redis:6379/0` to `redis://localhost:6379/0` if you are running Airflow locally
- change `result_backend` from `db+postgresql://postgres:airflow@postgres/airflow` to `db+postgresql://postgres:postgres@localhost/postgres`

Lastly, install the Redis package.

``` zsh
pipenv install 'apache-airflow[redis]'
```

You can now use Flower to monitor the workers by running 

``` zsh
airflow celery flower
```

To add a new worker run

``` zsh
airflow celery worker
```

This command needs to be run on each machine that you want to add to your Celery cluster, since it will signal that that machine is an available worker.

## Concurrency

Some important parameters to control how tasks are executed are:

- `parallelism`: total number of tasks that can be executed in the entire Airflow instance. This is set in `airflow.cfg`. By default it's set to 32.
- `dag_concurrency`: total number of tasks to be executed in each specific DAG. This is set in `airflow.cfg`. By default it's set to 16. Should be greater or equal to `parallelism` to have any effect. This parameter affects all DAGs.
- `concurrency`: is a parameter that can be set at the DAG object level (i.e. in the python script) to set the maximum number of concurrent tasks for that DAG specifically. It's the same as `dag_concurrency` but for that DAG only.
- `max_active_runs_per_dag`: sets the maximum number of DAG runs that be run concurrently for the same DAG. Default is 16. This applies to all DAGs.
- `max_active_runs`: is a Python object parameter that can be set to determine the maximum number of DAG runs for that specific DAG.
