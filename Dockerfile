FROM python:3.9

WORKDIR /project
COPY requirements.txt .
RUN pip install --ignore-installed -r requirements.txt
#RUN opentelemetry-bootstrap --action=install



#ENV WAIT_VERSION 2.7.2
#ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
#RUN chmod 777 /wait
CMD ["opentelemetry-instrument","uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080","--reload"]
