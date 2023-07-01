FROM python:3.9


WORKDIR /app

RUN apt-get update && \
    apt-get install -y git && \
    git clone https://github.com/mohammadjavad2001/sitehome.git && \
    cd repo &&\
    pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "repo.main:app", "--host", "127.0.0.1", "--port", "80"]
