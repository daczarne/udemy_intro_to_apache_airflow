from airflow import DAG
from airflow.operators.bash import BashOperator


def subdag_parallel_dag(parent_dag_id, child_dag_id, default_args):
	with DAG(
		dag_id = f'{parent_dag_id}.{child_dag_id}',
		default_args = default_args
	) as dag:
	#! List the tasks that will be encapsulated in the SubDAG 
		task_2 = BashOperator(
			task_id = 'task_2',
			bash_command = 'sleep 3'
		)
		task_3 = BashOperator(
			task_id = 'task_3',
			bash_command = 'sleep 3'
		)
	#! Return the DAG object
	return dag

