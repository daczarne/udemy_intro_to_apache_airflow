from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
	'start_date': datetime(2020, 1, 1)
}

with DAG(
	'parallel_dag',
	schedule_interval = '@daily',
	default_args = default_args,
	catchup = False
) as dag:
	#! Define four dummy tasks
	task_1 = BashOperator(
		task_id = 'task_1',
		bash_command = 'sleep 3'
	)
	task_2 = BashOperator(
		task_id = 'task_2',
		bash_command = 'sleep 3'
	)
	task_3 = BashOperator(
		task_id = 'task_3',
		bash_command = 'sleep 3'
	)
	task_4 = BashOperator(
		task_id = 'task_4',
		bash_command = 'sleep 3'
	)
	#! Define dependencies. To signal that task_2 and task_3 are the same level we group them in [] and pass them comma separated
	task_1 >> [task_2, task_3] >> task_4
