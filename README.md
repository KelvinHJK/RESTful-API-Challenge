# RESTful-API-Challenge
Develop a RESTful API using Python that interfaces with a MongoDB database to perform CRUD (Create, Read, Update, Delete) operations.


## Step 1: Setup Python Environment
Create a Virtual Environment with Python 3.11:
```
python3.11 -m venv venv
```
Activate Virtual Environment:
```
.\venv\Scripts\activate
```

## Step 2: Clone the repository and install Dependencies
Clone the repository: 
```
git clone https://github.com/KelvinHJK/RESTful-API-Challenge.git
```
Install dependencies: 
```
pip install -r requirements.txt
```

## Step 3: Setting up MongoDB
1. Install MongoDB on the local machine
2. Connect to the default new connection URI, which should be "mongodb://localhost:27017"
3. Create a new database named "employeedb" with the collection name "employees"

(Employees)

4. Add dummy data to the database, by pressing "ADD DATA" > "Import JSON or CSV file" > select "dbdummy_employees.json"
5. (optional) Db validation, press on the Validation tab, copy the text in "dbval_employees.txt", and click update

(Logging)

6. (optional) Create a new collection named "logs" under "employeedb".
7. (optional) Add db validation. Press on the Validation tab, copy the text in "dbval_logs.txt", and click update


## Step 4: Running the API
Start the Flask Server
```
python app.py
```

**Endpoints**

1. List all employees: 
```
GET /employees
```
2. Create a new employee:
```
POST /employees
```
3. Get details of specific employee:
```
GET /employees/{identity_no}
```
4. Update details of a specific employee:
```
PUT /employees/{identity_no}
```
5. Delete specific employee:
```
DELETE /employees/{identity_no}
```


## Documentation
Look into documentation.docx for detailed API specifications and database schemas.



