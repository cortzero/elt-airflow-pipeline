This project is an ELT (Extract, Load, Transform) pipeline that extracts data from a source Postgres database, loads the data to a different Postgres database, and then performs transformations on the data. The data model is represented by the following ER diagram:


The only tranformation is to create a new films_rating table with the movie information and assign each one a rating category (**Excellent**, **Good**, **Average**, **Bad**, and **Trash**) based on its `user_rating` column.

## How to run the project
1. It is recommended to create a virtual environment for the project. In the root directory enter the following command:
```bash
python -m venv <virtual environment name>
```
2. Activate the virtual environment:
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. Run Docker Ccompose to create the container of the `init_airflow` first:
```bash
docker compose up init_airflow -d
```
5. Run the rest of the containers:
```bash
docker compose up
```
6. Go to the Airflow webserver GUI (`localhost:8080`) to trigger the DAG corresponding to the elt process named `elt_and_dbt`.
7. Check the `destination_postgres` container to see if the transformations were applied:
```bash
docker exec -it <container name of the destination postgres> psql -U postgres
```
