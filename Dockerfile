FROM python:3.9

WORKDIR /project
COPY requirements.txt .
RUN pip install -r requirements.txt


#ENV WAIT_VERSION 2.7.2
#ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
#RUN chmod 777 /wait
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
