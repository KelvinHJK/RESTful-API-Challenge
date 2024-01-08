import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from app import app  # Assuming your Flask app is in a file named app.py
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime



# test on creating an employee
def test_create_employee():
    client = app.test_client()
    new_employee_data = {
        "name": "John",
        "dob": "2002-12-19",
        "date_joined": "2023-10-13",
        "date_left": "2023-11-13",
        "identity_no": "012345-67-8910",
        "department": "qc",
        "salary": 500,
        "remark": "excellent"
    }

    response = client.post("/employees", json=new_employee_data)
    data = json.loads(response.data.decode("utf-8"))

    assert response.status_code == 201

    assert "message" in data and "Employee added successfully" in data["message"]
    assert "id" in data and isinstance(ObjectId(data["id"]), ObjectId)
    assert "name" in data and data["name"] == new_employee_data["name"]


# test on created an employee with identity_no existed
def test_create_employee_existed_identity_no():
    client = app.test_client()

    # new employee data with identity_no existed in db
    dupp_employee_data = {
        "name": "Emily Hong",
        "dob": "2001-07-06",
        "date_joined": "2023-03-20",
        "date_left": None,
        "identity_no": "012345-67-8911",
        "department": "sales",
        "salary": 1000,
        "remark": "good"
    }

    response = client.post("/employees", json=dupp_employee_data)
    data = json.loads(response.data.decode("utf-8"))

    assert response.status_code == 400
    assert "message" in data and "Employee identity number existed" in data["message"]



# test on passing error data
def test_error_data():
    client = app.test_client()

    # employee data with errors
    error_employee_data = {
        "name": 12345,
        "dob": 2001,
        "date_joined": 2023,
        "date_left": "None",
        "identity_no": 12345678910,
        "department": "sales",
        "salary": 1000,
        "remark": ""
    }

    response = client.post("/employees", json=error_employee_data)
    data = json.loads(response.data.decode("utf-8"))

    assert response.status_code == 400
    assert "message" in data and "Validation error" in data["message"]


    # employee data for date_joined and date_left
    error_employee_date = {
        "name": "Emily Hong",
        "dob": "2001-07-06",
        "date_joined": "2023-03-20",
        "date_left": "2022-02-10",
        "identity_no": "012345-67-8911",
        "department": "sales",
        "salary": 1000,
        "remark": "good"
    }

    response2 = client.post("/employees", json=error_employee_date)
    data2 = json.loads(response2.data.decode("utf-8"))

    assert response2.status_code == 400
    assert "message" in data2 and "Validation error" in data2["message"]



# test on reading employee data
def test_read_employee():
    client = app.test_client()

    # make a request to the read endpoint
    response = client.get("/employees")
    data = json.loads(response.data.decode("utf-8"))

    # check if success
    assert response.status_code == 200
    assert "employees" in data
    assert isinstance(data["employees"], list)

    # check if the pre-added data is in the response
    existed_data = {
        "_id": '6595506d8afe15675bd19f96',
        "name": "Kelvin Ho Juin Ket",
        "dob": datetime.strptime("2002-12-08", '%Y-%m-%d').strftime('%Y-%m-%d'),
        "date_joined": datetime.strptime("2024-01-03", '%Y-%m-%d'),
        "date_left": datetime.strptime("2024-06-03", '%Y-%m-%d'),
        "identity_no": "021208-12-0267",
        "department": "engineering",
        "salary": 100.1,
        "remark": ""
    }
    assert any(emp["_id"] == existed_data["_id"] for emp in data["employees"])
    assert any(emp["name"] == existed_data["name"] for emp in data["employees"])
    assert any(emp["identity_no"] == existed_data["identity_no"] for emp in data["employees"])
    assert any(emp["department"] == existed_data["department"] for emp in data["employees"])


    existed_data2 = {
        "_id": '65956d80632275a7a1d2fe14',
        "name": "Jerad Liaw",
        "dob": datetime.strptime("2002-03-29", '%Y-%m-%d').strftime('%Y-%m-%d'),
        "date_joined": datetime.strptime("2021-01-02", '%Y-%m-%d'),
        "date_left": datetime.strptime("2022-05-12", '%Y-%m-%d'),
        "identity_no": "012345-67-8912",
        "department": "admin",
        "salary": 2000,
        "remark": "clever"
    }
    assert any(emp["_id"] == existed_data2["_id"] for emp in data["employees"])
    assert any(emp["name"] == existed_data2["name"] for emp in data["employees"])
    assert any(emp["identity_no"] == existed_data2["identity_no"] for emp in data["employees"])
    assert any(emp["department"] == existed_data2["department"] for emp in data["employees"])



# test on reading specific employee data
def test_read_one_employee():
    client = app.test_client()

    # existing employee identity_no
    test_identity_no = '021208-12-0267'
    response = client.get(f"/employees/{test_identity_no}")
    data = json.loads(response.data.decode("utf-8"))

    # check if success
    assert response.status_code == 200

    # check the data returned for correctness
    expected_data = {
        "name": "Kelvin Ho Juin Ket",
        "dob": datetime.strptime("2002-12-08", '%Y-%m-%d').strftime('%a, %d %b %Y %H:%M:%S GMT'),
        "date_joined": datetime.strptime("2024-01-03", '%Y-%m-%d').strftime('%a, %d %b %Y %H:%M:%S GMT'),
        "date_left": datetime.strptime("2024-06-03", '%Y-%m-%d').strftime('%a, %d %b %Y %H:%M:%S GMT'),
        "identity_no": "021208-12-0267",
        "department": "engineering",
        "salary": 100.1,
        "remark": ""
    }

    # exclude _id from comparison
    assert {k: v for k, v in data.items() if k != '_id'} == expected_data


# test on updating employee data
def test_update_employee():
    client = app.test_client()

    # existing employee identity_no
    test_identity_no = '021105-12-0635'

    response = client.get(f"/employees/{test_identity_no}")
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert data["name"] == "Marco Lee"
    assert data["name"] != "Marco Lee Yung Han"

    # new data to update the employee
    updated_data = {
        "name": "Marco Lee Yung Han",
        "dob": "2002-11-05",
        "date_joined": "2021-10-10",
        "date_left": "2022-11-20",
        "identity_no": test_identity_no,
        "department": "sales",
        "salary": 150,
        "remark": "good comm"
    }

    # make a request to the update endpoint
    response = client.put(f"/employees/{test_identity_no}", json=updated_data)
    data = json.loads(response.data.decode("utf-8"))

    # check if success
    assert response.status_code == 200
    assert "message" in data and data["message"] == "Employee updated successfully"

    # get the updated employee from the database
    new_response = client.get(f"/employees/{test_identity_no}")
    new_data = json.loads(new_response.data.decode("utf-8"))

    # Check if the data in the database matches the updated data
    assert new_data["name"] == updated_data["name"]
    assert datetime.strptime(new_data["dob"], '%a, %d %b %Y %H:%M:%S GMT') == datetime.strptime(updated_data["dob"], '%Y-%m-%d')
    assert datetime.strptime(new_data["date_joined"], '%a, %d %b %Y %H:%M:%S GMT') == datetime.strptime(updated_data["date_joined"], '%Y-%m-%d')
    assert datetime.strptime(new_data["date_left"], '%a, %d %b %Y %H:%M:%S GMT') == datetime.strptime(updated_data["date_left"], '%Y-%m-%d')
    assert new_data["department"] == updated_data["department"]
    assert new_data["salary"] == updated_data["salary"]
    assert new_data["remark"] == updated_data["remark"]

    # update the data back to the initial data
    initial_data = {
        "name": "Marco Lee",
        "dob": "2002-11-05",
        "date_joined": "2022-10-10",
        "date_left": "2023-01-20",
        "identity_no": test_identity_no,
        "department": "sales",
        "salary": 600,
        "remark": ""
    }

    response = client.put(f"/employees/{test_identity_no}", json=initial_data)
    assert response.status_code == 200


# test on deleting employee data
def test_delete_employee():
    client = app.test_client()

    test_identity_no = "012345-67-8910"

    # check if the employee exists before deletion
    response_before = client.get(f"/employees/{test_identity_no}")
    assert response_before.status_code == 200

    # delete the employee
    response = client.delete(f"/employees/{test_identity_no}")
    
    assert response.status_code == 200
    assert response.json["message"] == "Employee deleted successfully"

    # check if the employee is not found after deletion
    response_after = client.get(f"/employees/{test_identity_no}")
    assert response_after.status_code == 404

