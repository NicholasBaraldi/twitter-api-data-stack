FROM apache/airflow:2.4.0

RUN cd /twitter-api-data-stack && pip install .


WORKDIR /twitter-api-data-stack
CMD ["bash"]