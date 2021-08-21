from flask import Flask, request
import http
import json
import os
from SQLiteHelper import SQLiteHelper

debug = True
app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), "app.db")
db_helper = SQLiteHelper(db_path)


def make_json_response(data, code):
    if isinstance(data, str):
        response = app.response_class(response=data, status=code, mimetype="application/json")
    else:
        response = app.response_class(response=json.dumps(data), status=code, mimetype="application/json")
    return response


@app.route("/requests", methods=['GET'])
def process_request():
    hs_ids = db_helper.list_hs_ids()
    data = {
        "hs_ids": hs_ids,
    }
    response = make_json_response(data, http.HTTPStatus.OK)
    return response


@app.route("/requests/<guid>", methods=['GET'])
def get_results(guid):
    transactions_ids, transactions_data = db_helper.get_transactions_by_id(guid)
    data = [
        {"id": transaction_id, "data": transaction_data} for transaction_id, transaction_data in zip(transactions_ids, transactions_data)
    ]

    response = make_json_response(data, http.HTTPStatus.OK)
    return response


def create_app():
    return app


if __name__ == '__main__':
    if debug:
        app.debug = debug
        app.run(host='127.0.0.1', port=7777)
    else:
        app.run()
