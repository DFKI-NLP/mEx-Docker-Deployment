FROM python:3.6

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install spacy==3.0.7
RUN pip install https://github.com/explosion/spacy-models/releases/download/de_core_news_sm-3.0.0/de_core_news_sm-3.0.0.tar.gz
ADD . /app

COPY relation_extraction_mex_model.pt /app/relex.pt


CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5005"]
