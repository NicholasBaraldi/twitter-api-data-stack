FROM apache/airflow:2.4.1-python3.8

USER root

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository "deb http://security.debian.org/debian-security stretch/updates main" && \ 
    apt-get update && \
    apt-get install -y openjdk-8-jdk

RUN export JAVA_HOME

RUN export PYSPARK_SUBMIT_ARGS
USER airflow 
COPY ./requirements.txt /requirements.txt
RUN cd / && pip install -r requirements.txt
