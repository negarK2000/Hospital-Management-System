# Hospital Blood Bank Management System API

import requests
import json
from flask import Flask, jsonify, Response, request, abort
from flask_restful import Api, Resource
import copy

class Patient:
    def __init__(self, name: str, blood_type: str, blood_per_day: int, days: int) -> None:
        self.name = name
        self.blood_type = blood_type
        self.blood_per_day = blood_per_day
        self.days = days

critical_mode: bool = False
patients: list[Patient] = []
blood_bank: dict = {
    "A": 0,
    "B": 0,
    "AB": 0,
    "O": 0
}

def set_critical_mode(patient) -> None:
    global critical_mode
    critical_mode = False

    total_blood: dict = copy.deepcopy(blood_bank)
    if(type(patient) == Patient):
        total_blood[patient.blood_type] -= patient.blood_per_day * patient.days

    for p in patients:
        total_blood[p.blood_type] -= p.blood_per_day * p.days

    if total_blood["O"] < 0 or total_blood["AB"] + total_blood["O"] + total_blood["B"] + total_blood["A"] < 0:
        critical_mode = True

    elif total_blood["A"] > 0:
        if total_blood["B"] < 0 and total_blood["B"] + total_blood["O"] < 0:
            critical_mode = True

    elif total_blood["A"] + total_blood["O"] < 0:
        critical_mode = True

    elif total_blood["B"] + total_blood["O"] + total_blood["A"] < 0:
        critical_mode = True

def is_blood_enough(patient: Patient) -> bool:
    first_day: dict = copy.deepcopy(blood_bank)
    first_day[patient.blood_type] -= patient.blood_per_day

    for p in patients:
        first_day[p.blood_type] -= p.blood_per_day

    if critical_mode:
        if first_day["O"] < 0 or first_day["AB"] + first_day["O"] + first_day["B"] + first_day["A"] < 0:
            return False

        elif first_day["A"] > 0:
            if first_day["B"] < 0 and first_day["B"] + first_day["O"] < 0:
                return False

        elif first_day["A"] + first_day["O"] < 0:
            return False

        elif first_day["B"] + first_day["O"] + first_day["A"] < 0:
            return False

    return True


app = Flask(__name__)


@app.route('/blood-bank', methods=['POST'])
def set_bank() -> Response:
    global blood_bank

    if request.json['type'] not in blood_bank:
        return abort(400, description="Wrong Blood Type")

    blood_bank[request.json['type']] = request.json['amount']
    return jsonify(True)


@app.route('/blood-bank', methods=['PUT'])
def add_to_bank() -> Response:
    global blood_bank

    if request.json['type'] not in blood_bank:
        return abort(400, description="Wrong Blood Type")

    blood_bank[request.json['type']] += request.json['diff']

    if len(patients) > 0:
        set_critical_mode(None)

    # debug purpose
    print(f"new: {request.json['type']} = {blood_bank[request.json['type']]}")

    return jsonify(True)


@app.route('/new-patient', methods=['POST'])
def add_patient() -> Response:
    global patients

    if request.json['blood-type'] not in blood_bank:
        return abort(400, description="Wrong Blood Type")

    patient = Patient(name=request.json['name'],
                      blood_type=request.json['blood-type'],
                      blood_per_day=request.json['blood_per_day'],
                      days=request.json['days'])

    set_critical_mode(patient)

    if is_blood_enough(patient):
        patients.append(patient)
        return jsonify(True)

    return jsonify(False)


@app.route('/critical-mode', methods=['GET'])
def is_critical_mode_on() -> Response:
    return jsonify(critical_mode)


if __name__ == '__main__':
    app.run(debug=True, port=5050)
