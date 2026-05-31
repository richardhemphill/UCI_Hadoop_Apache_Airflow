# Airflow Docker Compose Kafka dbt Project

This folder starts Airflow and runs the dbt project stored in the sibling folder `../kafka_dbt_project`.

## Correct folder structure

```text
UCI_Hadoop_Apache_Airflow/
├── airflow_docker_compose_kafka_dbt/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── README.md
│   ├── .dbt/
│   │   └── profiles.yml
│   ├── dags/
│   │   └── kafka_dbt_pipeline_dag.py
│   ├── logs/
│   └── plugins/
│
└── kafka_dbt_project/
    ├── dbt_project.yml
    ├── models/
    └── ...
```

Important: do not keep an empty `kafka_dbt_project` folder inside `airflow_docker_compose_kafka_dbt`.

## Why the Docker volume uses `../kafka_dbt_project`

Docker commands are run from:

```bash
cd ~/projects//UCI_Hadoop_Apache_Airflow/airflow_docker_compose_kafka_dbt
```


The dbt project is one folder above, so the volume mapping is:

```yaml
- ../kafka_dbt_project:/opt/airflow/kafka_dbt_project
```

Inside the Airflow container, dbt sees the project at:

```text
/opt/airflow/kafka_dbt_project
```

## Start Airflow

```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/airflow_docker_compose_kafka_dbt
echo "AIRFLOW_UID=$(id -u)" > .env
docker compose build --no-cache
docker compose up -d
```
> **Note:** For non-Linux systems, [Airflow documentation states](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#setting-the-right-airflow-user) to use `50000` instead of `$(id -u)`.

## Check containers

```bash
docker compose ps
```

Expected:

```text
airflow-postgres     healthy
airflow-webserver    Up, port 8081->8080
airflow-scheduler    Up
```

## Open Airflow

```text
http://localhost:8081
```

Login:

```text
Username: admin
Password: admin
```

## Test dbt inside the Airflow container

> **Note:** If using Linux, add read/write permissions with `chmod -R o+rw ~/projects/UCI_Hadoop_Apache_Airflow/`

```bash
docker exec -it airflow_docker_compose_kafka_dbt-airflow-webserver-1 bash
cd /opt/airflow/kafka_dbt_project
dbt debug --profiles-dir .dbt
dbt run --profiles-dir .dbt
dbt test --profiles-dir .dbt
```
> **Note:** Upon finishing the test inside the container, use `exit` to depart from it.

## Trigger the DAG

In Airflow, search for:

```text
kafka_dbt_pipeline
```

Then click the trigger button.

## Stop Airflow

```bash
docker compose down
```
