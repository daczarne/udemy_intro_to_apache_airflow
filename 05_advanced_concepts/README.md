# Advanced concepts

## SubDAGs

SubDAGs allow us to create a DAG inside another DAG so that we can group similar tasks together. To use SubDAGs we need the `SubDAG` operator. Then we need to create a function who's return value is the SubDAG and use that function as the value of the `subdag` argument of the operator. These SubDAGs should be placed on the `airflow/dags/subdags` directory.

The subdag function takes three arguments:

- `parent_dag_id`: the ID of the parent DAG
- `child_dag_id`: the ID of the child DAG
- `default_args`: the same dictionary of default arguments as the parent DAG. Especially important is that the SubDAG has the same `start_date` and the same schedule interval.

SubDAGs are not recommended to be used due to:

- can lead to deadlocks preventing other tasks from being run
- high complexity of implementation
- SubDAGs have their own Sequential Executor so parallelism can be leveraged

## TaskGroups


## XComs
