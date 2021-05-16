from airflow.models import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from datetime import datetime

#* Dictionary of default arguments. This arguments will apply to all tasks in the data pipeline.
default_arguments = {
	#* Data pipeline start date
	'start_date': datetime(2020, 1, 1)
}

#* Instantiate the DAG. To do so provide the following arguments to the DAG class
#*		DAG ID: a string with the name of the DAG. Must be unique among all DAGs.
#*		Scheduling interval. This controls the frequency at which the data pipeline will be triggered.
#*		The default_args argument imports all default arguments and applies them to all tasks.
#*		catchup 
with DAG(
	'user_processing',
	schedule_interval = '@daily',
	default_args = default_arguments,
	catchup = False
) as dag:
	#* First task is to create the user table in the SQLite DB. Since we are going to interact with a SQLite DB, we need to use the SQLite Operator.
	creating_table = SqliteOperator(
		#* First we need to setup a task ID that is unique among the tasks in this data pipeline
		task_id = 'creating_table',
		#* Specify a DB connector. This needs to use one of the connectors specified on your Airflow console
		sqlite_conn_id = 'db_sqlite',
		#* Specify the SQL query to be run
		sql = """
			CREATE TABLE users (
				email TEXT NOT NULL PRIMARY KEY
				, first_name TEXT NOT NULL
				, last_name TEXT NOT NULL
				, country TEXT NOT NULL
				, user_name TEXT NOT NULL
				, password TEXT NOT NULL
			);
		"""
	)

