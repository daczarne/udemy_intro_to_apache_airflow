# Creating data pipelines

A DAG is a data pipeline in Airflow. It is a graph that describes how the different tasks that make up the pipeline relate (depend on) to each other. There can be no loops in the graph as these would represent circular dependencies.

![](img/dag.png)

## DAG directory

The DAGs directory is not included out of the box. To create it, `cd` to the `airflow` directory, and run

``` zsh
mkdir dags
```

All the python files need to be placed in there. Each file will represent a DAG. In this example pipeline we'll create 5 tasks:

- `creating_table` will create the table where the users will be stored. To do this, we will use the `SQLite` operator.
- `is_api_available` will check if the API from where we are going to fetch the users is available. To do this, we'll use the `HTTP` sensor.
- `extracting_user` will fetch the user. This will be done with the `HTTP` operator.
- `processing_user` will run some python function to process the data that the API sent. This will be done using the `Python` operator.
- `storing_user` will store the processed user in the table that we created. To do this, we will use the `Bash` operator yo execute a bash command to store data into the SQLite DB.

We'll start with creating a `user_processing.py` file in which we will define the DAG.

## Operators

An operator is a task in the data pipeline. Always make sure to define one task per operator. This will ensure that if one task fails, only that task is retried.

![](img/operators.png)

There are three types of operators:

1. **Action** operators execute an action (for example, the `Python` operator, the `Batch` operator, etc)
2. **Transfer** operators transfer data from a source to a destination
3. **Sensor** operators are used to wait for a condition to be met before moving on to the next task

## Testing tasks

Each time we add a task to the data pipeline, we need to test it. To test a task run

``` zsh
airflow tasks test <dag_id> <task_id> <execution_date_in_yyyy-mm-dd_format>
```

This will test only the task. It will not check for dependencies, nor will it store any metadata.

## Triggering tasks

Once you've finished writing the DAG head on to the Airflow UI and turn it on to trigger its execution. Sometimes tasks might fail. For example, if one of the tasks is to create a table, then the task will only succeed the first time it runs since all other times the table will already exist. This is why it's important to make sure that tasks are idempotent.

## Scheduling DAGs

- `start_date` defines when the task will start being scheduled
- `schedule_interval` defines the frequency at which the data pipeline will be triggered

The DAG will be scheduled once the `start_date` + `schedule_interval` has elapsed. And you'll get an `execution_date` equal to the beginning of that date.

All dates in Airflow are in UTC timezone. This can be changed from the `airflow.cfg` file, under the `default_ui_timezone` and `default_timezone` parameters. Changing them is not advisable.

## Backfilling and catchup

If the `start_date` is in the past, you need to backfill your DAG run. Airflow will automatically run all non-triggered DAG runs in order to catch-up to the current date, starting from the last execution date. This behavior can be controlled by the `catchup` parameter in the DAG definition. By default this parameter is set to `True`.
