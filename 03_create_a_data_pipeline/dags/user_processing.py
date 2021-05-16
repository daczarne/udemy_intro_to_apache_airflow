from airflow.models import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from pandas import json_normalize
import json


#* Dictionary of default arguments. This arguments will apply to all tasks in the data pipeline.
default_arguments = {
	#* Data pipeline start date
	'start_date': datetime(2020, 1, 1)
}


#* This function processes the user information and it will be called in the pipeline by the PythonOperator. Its argument is a TaskInstance (ti). With it, we'll be able to access the X comes.
def _processing_user(ti):
	#* Assign the response JSON to a variable
	users = ti.xcom_pull(task_ids = ['extracting_user'])
	#* Make sure the variable is not empty
	if not len(users) or 'results' not in users[0]:
		raise ValueError('User is empty')
	#* Extract the user
	user = users[0]['results'][0]
	#* Extract the user information
	processed_user = {
		'first_name': user['name']['first'],
		'last_name': user['name']['last'],
		'country': user['location']['country'],
		'user_name': user['login']['username'],
		'password': user['login']['password'],
		'email': user['email']
	}
	#* Convert to a pandas dataframe and store it in tmp file
	processed_user.to_csv('/tmp/processed_user.csv', index = None, header = False)


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

	#! First task is to create the user table in the SQLite DB. Since we are going to interact with a SQLite DB, we need to use the SQLite Operator.
	creating_table = SqliteOperator(
		#* First we need to setup a task ID that is unique among the tasks in this data pipeline
		task_id = 'creating_table',
		#* Specify a DB connector. This needs to use one of the connectors specified on your Airflow console
		sqlite_conn_id = 'db_sqlite',
		#* Specify the SQL query to be run
		sql = """
			CREATE TABLE IF NOT EXISTS users (
				email TEXT NOT NULL PRIMARY KEY
				, first_name TEXT NOT NULL
				, last_name TEXT NOT NULL
				, country TEXT NOT NULL
				, user_name TEXT NOT NULL
				, password TEXT NOT NULL
			);
		"""
	)

	#! Second task is to check if the API is available using the HTTP sensor
	is_api_available = HttpSensor(
		task_id = 'is_api_available',
		#* Connection name. The connection in this case will be the url of the API to be checked for availability.
		http_conn_id = 'user_api',
		#* Specify the endpoint
		endpoint = 'api/'
	)

	#! Third task is to extracting the user from the API
	extracting_user = SimpleHttpOperator(
		#* Set the task id
		task_id = 'extracting_user',
		#* Connection name
		http_conn_id = 'user_api',
		#* Endpoint
		endpoint = 'api/',
		#* Specify the API method
		method = 'GET',
		#* Response filter
		response_filter = lambda response: json.loads(response.text),
		#* Log the API response so that we can check it in the logs in case of error
		log_response = True
	)

	#! Forth task is to process the user information. This means that we need to get only the information that we are looking for from the API response.
	processing_user = PythonOperator(
		#* Set the task id
		task_id = 'processing_user',
		#* Specify the python function that we want to call. This function needs to be defined.
		python_callable = _processing_user
	)

	#! Lastly, add the user to the users table. To do this we need to use the Bash operator to write to the SQLite DB
	storing_user = BashOperator(
		#* Set the task ID
		task_id = 'storing_user',
		#* Bash command to execute
		bash_command = 'echo -e ".separator ","\n. import /tmp/processed_user.csv users" | sqlite3 /home/airflow/airflow/airflow.db'
	)

	#! Now that all the tasks have been defined, we need to define the dependencies between them. To do so we'll list the tasks and include >> signs between them, going from first task to last.
	creating_table >> is_api_available >> extracting_user >> processing_user >> storing_user
