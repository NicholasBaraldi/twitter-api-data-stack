FROM apache/airflow:2.4.0

COPY ./requirements.txt /requirements.txt
RUN cd / && pip install -r requirements.txt
