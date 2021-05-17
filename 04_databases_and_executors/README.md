# Databases and Executors

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
