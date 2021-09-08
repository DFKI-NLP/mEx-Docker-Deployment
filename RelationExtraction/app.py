import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property

from flask import Flask, request
from flask_restplus import Api, Resource, fields
import json

import requests
from RelationExtraction import RelationExtractionModel


relex = RelationExtractionModel()

flask_app = Flask(__name__)
app = Api(app=flask_app,
          version="1.0",
          title="mEx Medical SequenceTagger API (Relation Extraction)",
          description="This API offers an interface to use RelEx models for text prediction",
          contact="Ammer Ayach",
          contact_email="amay01@dfki.de")

relex_space = app.namespace('relexx', description='RelEx API')


model = app.model('Taggers Input', {'list': fields.List(fields.List(fields.String()))})


@relex_space.route("/")
class RelEx(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'})
    @app.expect(model)
    def post(self):
        try:
            json_data = request.json
            print(json_data)
            tokens = json_data["tokens"]
            sent_start_index = json_data["sent_start_index"]
            tags = json_data["tags"]

            res = relex.predict(tokens, sent_start_index, tags)

            return {
                "ner_res": res["ner_res"],
                "rel_res": res["rel_res"]
            }

        except Exception as e:
            relex_space.abort(400, e.__doc__, status="Could not perform prediction", statusCode="400")




if __name__ == '__main__':
    flask_app.run(debug=False, port="5005")
