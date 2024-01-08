import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
from flask_cors import CORS

from validation import validate_employee

app = Flask(__name__)
CORS(app)


# mongodb connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/employeedb"
db = PyMongo(app)

# logging destructive methods such as CREATE, UPDATE and DELETE
def log_action(action, employee_id, details):
    log_entry = {
        "timestamp": datetime.utcnow(),
        "action": action,
        "employee_id": employee_id,
        "details": details
    }

    # Insert log entry into the logging collection
    db.db.logs.insert_one(log_entry)


# API endpoints
# CREATE
@app.route("/employees", methods=['POST'])
def create_employee():
    data = request.json

    # data validation
    validation_error = validate_employee(data)
    if validation_error:
        return jsonify({"message": "Validation error", "error": validation_error}), 400

    # convert date to datetime object
    data['dob'] = datetime.strptime(data['dob'], '%Y-%m-%d')
    data['date_joined'] = datetime.strptime(data['date_joined'], '%Y-%m-%d')
    data['date_left'] = datetime.strptime(data['date_left'], '%Y-%m-%d') if data.get('date_left') is not None else None

    # check if identity_no existed
    existing_employee = db.db.employees.find_one({"identity_no": data["identity_no"]})
    if existing_employee and existing_employee["_id"] != ObjectId(data.get("_id")):
        return jsonify({"message": "Employee identity number existed"}), 400


    # insert to db
    result = db.db.employees.insert_one(data)
    log_action("create", data.get("identity_no"), "Employee created successfully")

    return jsonify({"message": "Employee added successfully", "id": str(result.inserted_id), "name": data["name"]}), 201


# READ
@app.route('/employees', methods=['GET'])
def read_employee():
    employees = list(db.db.employees.find())

    # Convert ObjectId to string for JSON serialization
    for employee in employees:
        employee['_id'] = str(employee['_id'])

    return jsonify({"employees": employees})

# READ (specific identity_no)
@app.route('/employees/<identity_no>', methods=['GET'])
def get_employee(identity_no):
    employee = db.db.employees.find_one({"identity_no": identity_no})

    if employee:
        # Convert ObjectId to string for JSON serialization
        employee['_id'] = str(employee['_id'])
        return jsonify(employee), 200
    else:
        return jsonify({"message": "Employee not found"}), 404


# UPDATE
@app.route('/employees/<identity_no>', methods=['PUT'])
def update_employee(identity_no):
    data = request.json

    # data validation
    validation_error = validate_employee(data)
    if validation_error:
        return jsonify({"message": "Validation error", "error": validation_error}), 400

    # convert date to datetime object
    data['dob'] = datetime.strptime(data['dob'], '%Y-%m-%d')
    data['date_joined'] = datetime.strptime(data['date_joined'], '%Y-%m-%d')
    data['date_left'] = datetime.strptime(data['date_left'], '%Y-%m-%d') if data.get('date_left') is not None else None

    result = db.db.employees.update_one({"identity_no": identity_no}, {"$set": data})
    
    if result.modified_count > 0:
        log_action("update", data.get("identity_no"), "Employee updated successfully")
        return jsonify({"message": "Employee updated successfully"})
    else:
        return jsonify({"message": "Employee not found"}), 404


# DELETE
@app.route('/employees/<identity_no>', methods=['DELETE'])
def delete_employee(identity_no):
    result = db.db.employees.delete_one({"identity_no": identity_no})

    if result.deleted_count > 0:
        log_action("delete", identity_no, "Employee updated successfully")
        return jsonify({"message": "Employee deleted successfully"})
    else:
        return jsonify({"message": "Employee not found"}), 404



# READ logs
@app.route('/logs', methods=['GET'])
def get_logs():
    # Implement logic to retrieve logs from the MongoDB table
    # You might want to support query parameters for filtering, pagination, etc.


    logs = db.db.logs.find({}, {"_id": 0})  # Exclude _id field from the response
    return jsonify({"logs": list(logs)})




if __name__ == '__main__':
    app.run(debug=True)
