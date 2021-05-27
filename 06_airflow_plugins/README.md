# Airflow plugins

Airflow can be customized with new Operators and new views in the UI.

## The plugin system

In Airflow we can customize:

- **Operators**: build new operators that better suit your needs (new operators or operators that extend the functionality of existing ones).
- **Views**: customize the Airflow UI.
- **Hooks**: create new hooks to interact with external sources.

By default, Airflow will monitor three folders: `config`, `dags`, and `plugins`. To create new plugins, first create the `plugins` folder in the `airflow` directory (it is not automatically created). Inside this folder you can create new plugins using regular Python modules. So, create a new folder inside the `plugins` folder. The name of this sub-folder should be the same as the name of your plugin. Then put all the files related to the new plugin inside of it. Each new operator, sensor, etc. should have its own Python script.

By default, plugins are lazy loaded, so you'll need to re-start Airflow every time a new plugin is added. Once added, it can be modified without restarting.
