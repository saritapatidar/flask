from flask import Flask , jsonify ,redirect, url_for, Blueprint, render_template
from flask import request
from app.database import db
from app.models.employee_models import Employee
from app.forms.employee_forms import EmployeeForm
# from app.templete import employee_form_html

employee_bp = Blueprint('employee_bp', __name__)

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)
# migrate = Migrate(app, db) 

# @app.route("/user")
# def home():
#     return f"Hello, your age is {50}!"

# @app.route("/old_user/")
# def old_user():
#     return redirect(url_for("home"))

# @app.route("/data", methods=["GET","POST"])
# def data():
#     if request.method == "POST":
#         data = request.get_json()
#         return jsonify(data)
#     else:
#         return jsonify({"message": "Send a POST request with JSON data."})



# @app.route('/')
# def home():
#     x=Employee.query.all()
#     return x

@employee_bp.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json()
    if Employee.query.filter_by(name=data['name']).first():
        return jsonify({"message":"Employee with this name already exists."}),400
    new_employee = Employee(
        name=data['name'],
        age=data['age'],
        department=data['department']
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({"message":"Employee added successfully."}),201

@employee_bp.route("/get_all", methods=["GET"])
def get_employees():
    employees = Employee.query.all()
    result = []
    for emp in employees:
        emp_data = {
            'id': emp.id,
            'name': emp.name,
            'age': emp.age,
            'department': emp.department
        }
        result.append(emp_data)
    return jsonify(result),200

@employee_bp.route("/employee/<int:id>", methods=["PUT"])
def update_employee(id):
    data=request.get_json()
    emp=Employee.query.get(id)
    if not emp:
        return jsonify({"message":"Employee not found."}),404
    emp.name=data.get('name',emp.name)
    emp.age=data.get('age',emp.age)
    emp.department=data.get('department',emp.department)
    db.session.commit()
    return jsonify({"message":"Employee updated successfully."}),200

@employee_bp.route("/employees/<int:id>",methods=["DELETE"])
def delete_employee(id):
    emp = Employee.query.get(id)
    if not emp:
        return jsonify({"message":"Employee not found."}),404
    db.session.delete(emp)
    db.session.commit()
    return jsonify({"message":"Employee deleted successfully."}),200


@employee_bp.route("/emp/",methods=["GET","POST"])
def emp():
    form=EmployeeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            name=form.name.data
            age=form.age.data
            department=form.department.data
            new_emp=Employee(name=name,age=age,department=department)
            db.session.add(new_emp)
            db.session.commit()
            return redirect(url_for("employee_bp.emp"))
    else:
        return render_template("employee_form.html",form=form)
          
@employee_bp.route("/",methods=["GET"])
def emps():
    employees=Employee.query.all()
    return render_template("employee_list.html",employees=employees)

@employee_bp.route("/emp/<int:id>/delete",methods=["POST"])
def delete_emp(id):
    emp=Employee.query.get(id)
    if not emp:
        return "Employee not found",404
    db.session.delete(emp)
    db.session.commit()
    return redirect(url_for("employee_bp.emps"))

@employee_bp.route("/emp/<int:id>/update",methods=["GET","POST"])
def update_emp(id):
    emp=Employee.query.get(id)
    if not emp:
        return "Employee not found",404
    form=EmployeeForm(obj=emp)
    if request.method == "POST":
        if form.validate_on_submit():
            emp.name=form.name.data
            emp.age=form.age.data
            emp.department=form.department.data
            db.session.commit()
            return redirect(url_for("employee_bp.emps"))
    return render_template("employee_form.html",form=form)

if __name__ == "__main__":
    app.run(debug=True)




