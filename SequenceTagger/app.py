import requests
import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property

from flask import Flask, request
from flask_restplus import Api, Resource, fields
from flair.data import Sentence
from flair.models import SequenceTagger

NERTagger: SequenceTagger = SequenceTagger.load(model="ner.pt")
POSTagger: SequenceTagger = SequenceTagger.load(model="pos.pt")

flask_app = Flask(__name__)
app = Api(app=flask_app,
          version="1.0",
          title="mEx Medical SequenceTagger API (NER & POS)",
          description="This API offers an interface to use NER & POS models for text prediction",
          contact="Ammer Ayach",
          contact_email="amay01@dfki.de")

pos_space = app.namespace('pos', description='POS-Tagger API')
ner_space = app.namespace('ner', description='NER-Tagger API')
ner_space_for_rel = app.namespace('nerrelex', description='NER-Tagger API for Relation Extraction')
relex_space = app.namespace('relex', description='RelEx API')


model = app.model('Taggers Input', {'list': fields.List(fields.List(fields.String()))})
model_single = app.model('Single Tagger Input', {'sentence': fields.List(fields.String())})


@pos_space.route("/")
class POS(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'})
    @app.expect(model)
    def post(self):
        try:
            json_data = request.json
            sent_list = json_data["list"]

            res = []
            id = 1
            for i in range(len(sent_list)):
                text = sent_list[i]

                sentence = Sentence(text=text, use_tokenizer=False)
                POSTagger.predict(sentence)


                for j in range(len(sentence.tokens)):
                    res.append(["T" + str(id), "Sent-" + str(i), "Tok-" + str(j), "Tok-" + str(j),
                                sentence.tokens[j].get_tag('pos').value])
                    id += 1

            return {
                "pos_tags": res
            }
        except Exception as e:
            pos_space.abort(400, e.__doc__, status="Could not perform prediction", statusCode="400")


def merge_ner_tags(id, in_res, res):
    k = 0
    org_k = 0
    while k < len(in_res):
        if in_res[k][3] == "O":
            in_res[k].insert(0, "T" + str(id))
            #res.append(in_res[k])
            #id += 1
            k += 1
        elif in_res[k][3].split("-")[0] == "B":
            tmp = [in_res[k]]
            for l in range(len(in_res[k + 1:])):
                if in_res[k + 1:][l][3] == "O":
                    k += l + 1
                    break
                elif in_res[k + 1:][l][3].split("-")[0] == "B":
                    k += l + 1
                    break
                else:
                    tmp.append(in_res[k + 1:][l])

            res.append(["T" + str(id), tmp[0][0], tmp[0][1], tmp[-1][2], tmp[0][-1].split("-")[1]])
            id += 1

        if org_k == k:
            k += 1
            org_k += 1
        else:
            org_k = k


@ner_space.route("/")
class NER(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'})
    @app.expect(model)
    def post(self):
        try:

            json_data = request.json
            sent_list = json_data["list"]

            res = []
            id = 1
            for i in range(len(sent_list)):
                text = sent_list[i]
                sentence = Sentence(text=text, use_tokenizer=False)
                NERTagger.predict(sentence)

                in_res = []
                for j in range(len(sentence.tokens)):
                    in_res.append(["Sent-" + str(i), "Tok-" + str(j), "Tok-" + str(j),
                                   sentence.tokens[j].get_tag('ner').value])

                merge_ner_tags(id, in_res, res)

            return {
                "ner_tags": res
            }
        except Exception as e:
            ner_space.abort(400, e.__doc__, status="Could not perform prediction", statusCode="400")


@relex_space.route("/")
class RelEx(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'})
    @app.expect(model)
    def post(self):
        try:
            json_data = request.json
            sent_list = json_data["list"]

            sent_start_index = [0]
            all_tags = []
            all_sents = []
            for i in range(len(sent_list)):
                sentence = Sentence(text=sent_list[i], use_tokenizer=False)
                NERTagger.predict(sentence)
                ner_res = [token.get_tag('ner').value for token in sentence.tokens]

                all_tags.extend(ner_res)
                all_sents.extend(sent_list[i])
                sent_start_index.append(sent_start_index[-1]+len(sent_list[i]))

            sent_start_index = sent_start_index[:-1][1:]
            r = requests.post("http://mex2:5005/relexx/", json={"tokens": all_sents, "tags": all_tags, "sent_start_index": sent_start_index})
            #r = requests.post("http://localhost:5005/relexx/", json={"tokens": all_sents, "tags": all_tags, "sent_start_index": sent_start_index})
            rel_res = r.json()

            return {
                "ner_tags": rel_res["ner_res"],
                "relations": rel_res["rel_res"],
            }

        except Exception as e:
            relex_space.abort(400, e.__doc__, status="Could not perform prediction", statusCode="400")


if __name__ == '__main__':
    flask_app.run(debug=True, port="5000")
