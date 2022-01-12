from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/employee_json'
db = SQLAlchemy(app)

class Employee(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    second_name = db.Column(db.String(20))
    hiring_date = db.Column(db.DateTime)
    specialization = db.Column(db.String(100))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, first_name, second_name, hiring_date, specialization):
        self.first_name = first_name
        self.second_name = second_name
        self.hiring_date = hiring_date
        self.specialization = specialization

    def __repr__(self):
        return f"{self.id}"

db.create_all()

class EmployeeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Employee
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        first_name = fields.String(required=True)
        second_name = fields.String(required=True)
        hiring_date = fields.DateTime(required=True)
        specialization = fields.String(required=True)

@app.route('/api/v2/employee', methods=['POST'])
def create_employee():
    data = request.get_json()
    employee_schema = EmployeeSchema()
    employee = employee_schema.load(data)
    result = employee_schema.dump(employee.create())
    return make_response(jsonify({"employee": result}), 200)

@app.route('/api/v2/employee', methods=['GET'])
def index():
    get_employees = Employee.query.all()
    employee_schema = EmployeeSchema(many=True)
    employees = employee_schema.dump(get_employees)
    return make_response(jsonify({"employees": employees}))

@app.route('/api/v2/employee/<id>', methods=['GET'])
def get_employee_by_id(id):
    get_employee = Employee.query.get(id)
    employee_schema = EmployeeSchema()
    employee = employee_schema.dump(get_employee)
    return make_response(jsonify({"employee": employee}))

@app.route('/api/v2/employee/<id>', methods=['DELETE'])
def delete_employee_by_id(id):
    get_employee = Employee.query.get(id)
    db.session.delete(get_employee)
    db.session.commit()
    return make_response("", 204)

@app.route('/api/v2/employee/<id>', methods=['PUT'])
def update_employee_by_id(id):
    data = request.get_json()
    get_employee = Employee.query.get(id)
    if data.get('first_name'):
        get_employee.first_name = data['first_name']
    if data.get('second_name'):
        get_employee.second_name = data['second_name']
    if data.get('hiring_date'):
        get_employee.hiring_date = data['hiring_date']
    if data.get('specialization'):
        get_employee.specialization = data['specialization']
    db.session.add(get_employee)
    db.session.commit()
    employee_schema = EmployeeSchema(only=['id', 'first_name', 'second_name', 'hiring_date', 'specialization'])
    employee = employee_schema.dump(get_employee)
    return make_response(jsonify({"employee": employee}))

if __name__ == "__main__":
    app.run(debug=True)





