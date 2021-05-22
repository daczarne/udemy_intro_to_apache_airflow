from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from datetime import datetime
from airflow.utils.task_group import TaskGroup


default_args = {
	'start_date': datetime(2020, 1, 1)
}

with DAG(
	'parallel_dag',
	schedule_interval = '@daily',
	default_args = default_args,
	catchup = False
) as dag:
	#! Task 1
	task_1 = BashOperator(
		task_id = 'task_1',
		bash_command = 'sleep 3'
	)
	#! Task Group
	with TaskGroup('processing_tasks') as processing_tasks:
		task_2 = BashOperator(
			task_id = 'task_2',
			bash_command = 'sleep 3'
		)
		task_3 = BashOperator(
			task_id = 'task_3',
			bash_command = 'sleep 3'
		)
	#! Task 4
	task_4 = BashOperator(
		task_id = 'task_4',
		bash_command = 'sleep 3'
	)
	#! Dependencies
	task_1 >> processing_tasks >> task_4
