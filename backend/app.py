from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Tender, Expenditure, Project, Budget
from datetime import datetime

# create a Flask application instance
app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# create an API object to register resources
api = Api(app)

@app.route("/")
def index():
    return "Welcome to the Project Management API!"

# Tender Routes
@app.route('/tenders', methods=['GET', 'POST'])
def manage_tenders():
    if request.method == 'POST':
        data = request.get_json()
        new_tender = Tender(
            user_id=data['user_id'],
            budget_id=data['budget_id'],
            description=data['description'],
            cost=data['cost']
        )
        db.session.add(new_tender)
        db.session.commit()
        return jsonify(new_tender.to_dict()), 201
    else:
        tenders = Tender.query.all()
        return jsonify([tender.to_dict() for tender in tenders]), 200

@app.route('/tenders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_tender(id):
    tender = Tender.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(tender.to_dict()), 200
    elif request.method == 'PUT':
        data = request.get_json()
        tender.description = data['description']
        tender.cost = data['cost']
        db.session.commit()
        return jsonify(tender.to_dict()), 200
    elif request.method == 'DELETE':
        db.session.delete(tender)
        db.session.commit()
        return '', 204

# Expenditure Routes
@app.route('/expenditures', methods=['GET', 'POST'])
def manage_expenditures():
    if request.method == 'POST':
        data = request.get_json()
        new_expenditure = Expenditure(
            budget_id=data['budget_id'],
            item=data['item'],
            amount=data['amount']
        )
        db.session.add(new_expenditure)
        db.session.commit()
        return jsonify(new_expenditure.to_dict()), 201
    else:
        expenditures = Expenditure.query.all()
        return jsonify([expenditure.to_dict() for expenditure in expenditures]), 200

@app.route('/expenditures/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_expenditure(id):
    expenditure = Expenditure.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(expenditure.to_dict()), 200
    elif request.method == 'PUT':
        data = request.get_json()
        expenditure.item = data['item']
        expenditure.amount = data['amount']
        db.session.commit()
        return jsonify(expenditure.to_dict()), 200
    elif request.method == 'DELETE':
        db.session.delete(expenditure)
        db.session.commit()
        return '', 204

# Project Routes
class Projects(Resource):
    def get(self):
        projects = Project.query.all()
        result = [project.to_dict() for project in projects]
        return make_response(jsonify(result), 200)

    def post(self):
        data = request.get_json()
        project = Project(
            ministry_id=data['ministry_id'],
            name=data['name'],
            description=data['description'],
            date=datetime.fromisoformat(data['date']),
            status=data['status'],
            budget_id=data['budget_id']
        )
        db.session.add(project)
        db.session.commit()
        return make_response(jsonify(project.to_dict()), 201)

class ProjectByID(Resource):
    def get(self, project_id):
        project = Project.query.filter_by(project_id=project_id).first()
        if project:
            return make_response(jsonify(project.to_dict()), 200)
        else:
            return make_response(jsonify({'error': 'Project not found'}), 404)

    def patch(self, project_id):
        data = request.get_json()
        project = Project.query.filter_by(project_id=project_id).first()
        if project:
            project.ministry_id = data['ministry_id'] if 'ministry_id' in data else project.ministry_id
            project.name = data['name'] if 'name' in data else project.name
            project.description = data['description'] if 'description' in data else project.description
            project.date = datetime.fromisoformat(data['date']) if 'date' in data else project.date
            project.status = data['status'] if 'status' in data else project.status
            project.budget_id = data['budget_id'] if 'budget_id' in data else project.budget_id
            db.session.commit()
            return make_response(jsonify(project.to_dict()), 200)
        else:
            return make_response(jsonify({'error': 'Project not found'}), 404)

    def delete(self, project_id):
        project = Project.query.filter_by(project_id=project_id).first()
        if project:
            db.session.delete(project)
            db.session.commit()
            return make_response(jsonify({'message': 'Project deleted'}), 200)
        else:
            return make_response(jsonify({'error': 'Project not found'}), 404)

# Budget Routes
class Budgets(Resource):
    def get(self):
        budgets = Budget.query.all()
        result = [budget.to_dict() for budget in budgets]
        return make_response(jsonify(result), 200)

    def post(self):
        data = request.get_json()
        budget = Budget(amount=data['amount'])
        db.session.add(budget)
        db.session.commit()
        return make_response(jsonify(budget.to_dict()), 201)

class BudgetByID(Resource):
    def get(self, budget_id):
        budget = Budget.query.filter_by(budget_id=budget_id).first()
        if budget:
            return make_response(jsonify(budget.to_dict()), 200)
        else:
            return make_response(jsonify({'error': 'Budget not found'}), 404)

    def patch(self, budget_id):
        data = request.get_json()
        budget = Budget.query.filter_by(budget_id=budget_id).first()
        if budget:
            budget.amount = data['amount'] if 'amount' in data else budget.amount
            db.session.commit()
            return make_response(jsonify(budget.to_dict()), 200)
        else:
            return make_response(jsonify({'error': 'Budget not found'}), 404)

    def delete(self, budget_id):
        budget = Budget.query.filter_by(budget_id=budget_id).first()
        if budget:
            db.session.delete(budget)
            db.session.commit()
            return make_response(jsonify({'message': 'Budget deleted'}), 200)
        else:
            return make_response(jsonify({'error': 'Budget not found'}), 404)

# Add API resources
api.add_resource(Projects, '/projects')
api.add_resource(ProjectByID, '/projects/<int:project_id>')
api.add_resource(Budgets, '/budgets')
api.add_resource(BudgetByID, '/budgets/<int:budget_id>')

if _name_ == '_main_':
    app.run(port=5555, debug=True)