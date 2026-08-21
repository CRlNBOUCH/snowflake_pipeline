FROM apache/airflow:3.3.1

USER root

RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

USER airflow
RUN pip install --no-cache-dir \
    apache-airflow-providers-snowflake \
    snowflake-connector-python \
    dbt-snowflake