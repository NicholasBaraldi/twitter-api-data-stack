FROM apache/airflow:2.4.0

USER root

RUN apt update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant && \
    apt-get clean;

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME
USER airflow 
COPY ./requirements.txt /requirements.txt
RUN cd / && pip install -r requirements.txt
