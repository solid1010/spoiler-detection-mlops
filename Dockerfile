FROM apache/airflow:2.7.2
USER root
RUN apt-get update && apt-get install -y gcc python3-dev # Wordcloud derleme için gerekebilir
USER airflow
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt