FROM python:3.6

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app

#COPY named_entity_recognition_mex_model(custom_flair_embeddings).pt /app/ner.pt
ADD https://cloud.dfki.de/owncloud/index.php/s/WWbnqJ6N8gQQWMD/download /app/ner.pt

#COPY part_of_speech_tagger_mex_model(Def_Word_Flair).pt /app/pos.pt
ADD https://cloud.dfki.de/owncloud/index.php/s/e7G9deea7eRksCY/download /app/pos.pt


CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
