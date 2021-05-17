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

As stated, the default executor is `SequentialExecutor`. To allow tasks in parallel, change it the `LocalExecutor`.
