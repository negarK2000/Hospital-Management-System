# Hospital Admission System API

from flask import Flask, jsonify, Response, request

BEDS_NUM: int = 0
beds: list = []

app = Flask(__name__)


@app.route('/beds-num', methods=['POST'])
def set_beds_num() -> Response:
    global BEDS_NUM, beds
    BEDS_NUM = request.json['beds']

    beds = [None] * BEDS_NUM

    return jsonify(True)


@app.route('/new-patient', methods=['POST'])
def add_new_patient() -> Response:
    global beds
    name: str = request.json['name']

    for i in range(BEDS_NUM):
        if not beds[i]:
            beds[i] = name
            return jsonify(True)

    return jsonify(False)


@app.route('/empty-beds', methods=['GET'])
def get_empty_beds() -> Response:
    emp: int = 0

    for i in range(BEDS_NUM):
        if not beds[i]:
            emp += 1

    return jsonify(emp)


@app.route('/discharge', methods=['DELETE'])
def discharge_patient() -> Response:
    global beds
    name: str = request.json['name']

    for i in range(BEDS_NUM):
        if beds[i] == name:
            beds[i] = None
            return jsonify(True)

    return jsonify(False)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
