FROM python:3.6

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app

COPY named_entity_recognition_mex_model.pt /app/ner.pt

COPY part_of_speech_tagger_mex_model.pt /app/pos.pt


CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
