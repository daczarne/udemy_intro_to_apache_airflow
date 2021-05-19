from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from datetime import datetime
from subdags.subdag_parallel_dag import subdag_parallel_dag

default_args = {
	'start_date': datetime(2020, 1, 1)
}

with DAG(
	'parallel_dag',
	schedule_interval = '@daily',
	default_args = default_args,
	catchup = False
) as dag:
	task_1 = BashOperator(
		task_id = 'task_1',
		bash_command = 'sleep 3'
	)
	#! SubDAG
	processing = SubDagOperator(
		task_id = 'processing_tasks',
		subdag = subdag_parallel_dag(
			parent_dag_id = 'parallel_dag',
			child_dag_id = 'processing_tasks',
			default_args = default_args
		)
	)
	task_4 = BashOperator(
		task_id = 'task_4',
		bash_command = 'sleep 3'
	)
	task_1 >> processing >> task_4
