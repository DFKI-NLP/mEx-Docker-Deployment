FROM python:3.6

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app

#COPY ner.pt /app/ner.pt
ADD https://cloud.dfki.de/owncloud/index.php/s/WWbnqJ6N8gQQWMD/download /app/ner.pt

#COPY pos.pt /app/pos.pt
ADD https://cloud.dfki.de/owncloud/index.php/s/e7G9deea7eRksCY/download /app/pos.pt


CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
