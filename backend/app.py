# backend/app.py

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Tender, Expenditure, Ministry, CivilServant, Project, Budget
from datetime import datetime

# create a Flask application instance 
app = Flask(__name__)

# configure the database connection to the local file app.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# configure flag to disable modification tracking and use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)

# create an API object to register resources
api = Api(app)

### Routes
@app.route("/")
def index():
    return "Welcome to the Citizens Portal API!"

# Tender Routes
class Tenders(Resource):
    def get(self):
        tenders = Tender.query.all()
        tender_list = [tender.to_dict() for tender in tenders]
        return make_response(jsonify(tender_list), 200)
    
    def post(self):
        data = request.get_json()
        new_tender = Tender(
            user_id=data['user_id'],
            expenditure_id=data['expenditure_id'],
            description=data['description'],
            cost=data['cost']
        )
        db.session.add(new_tender)
        db.session.commit()
        response = {
            'message': 'New tender created',
            'tender': new_tender.to_dict()
        }
        return make_response(jsonify(response), 201)

class TenderByID(Resource):
    def get(self, id):
        tender = Tender.query.get_or_404(id)
        response = {
            'message': 'Tender details',
            'tender': tender.to_dict()
        }
        return make_response(jsonify(response), 200)
    
    def put(self, id):
        tender = Tender.query.get_or_404(id)
        data = request.get_json()
        tender.description = data['description']
        tender.cost = data['cost']
        db.session.commit()
        response = {
            'message': 'Tender updated',
            'tender': tender.to_dict()
        }
        return make_response(jsonify(response), 200)
    
    def delete(self, id):
        tender = Tender.query.get_or_404(id)
        db.session.delete(tender)
        db.session.commit()
        return make_response('', 204)
    
# Expenditure Routes
class Expenditures(Resource):
    def get(self):
        expenditures = Expenditure.query.all()
        expenditure_list = [expenditure.to_dict() for expenditure in expenditures]
        return make_response(jsonify(expenditure_list), 200)
    
    def post(self):
        data = request.get_json()
        new_expenditure = Expenditure(
            budget_id=data['budget_id'],
            item=data['item'],
            amount=data['amount']
        )
        db.session.add(new_expenditure)
        db.session.commit()
        response = {
            'message': 'New expenditure created',
            'expenditure': new_expenditure.to_dict()
        }
        return make_response(jsonify(response), 201)

class ExpenditureByID(Resource):
    def get(self, id):
        expenditure = Expenditure.query.get_or_404(id)
        response = {
            'message': 'Expenditure details',
            'expenditure': expenditure.to_dict()
        }
        return make_response(jsonify(response), 200)
    
    def put(self, id):
        expenditure = Expenditure.query.get_or_404(id)
        data = request.get_json()
        expenditure.item = data['item']
        expenditure.amount = data['amount']
        db.session.commit()
        response = {
            'message': 'Expenditure updated',
            'expenditure': expenditure.to_dict()
        }
        return make_response(jsonify(response), 200)
    
    def delete(self, id):
        expenditure = Expenditure.query.get_or_404(id)
        db.session.delete(expenditure)
        db.session.commit()
        return make_response('', 204)

# Ministry Routes
class Ministries(Resource):
    def get(self):
        ministries = Ministry.query.all()
        result = [m.to_dict() for m in ministries]
        return make_response(jsonify(result), 200)

    def post(self):
        data = request.get_json()
        ministry = Ministry(name=data['name'])
        db.session.add(ministry)
        db.session.commit()
        return make_response(jsonify({'message': 'Ministry created successfully'}), 201)

class MinistryByID(Resource):
    def get(self, ministry_id):
        ministry = Ministry.query.filter_by(ministry_id=ministry_id).first()
        if ministry:
            return make_response(jsonify(ministry.to_dict()), 200)
        else:
            return make_response(jsonify({'error': 'Ministry not found'}), 404)

    def put(self, ministry_id):
        data = request.get_json()
        ministry = Ministry.query.filter_by(ministry_id=ministry_id).first()
        if not ministry:
            return make_response(jsonify({'message': 'Ministry not found'}), 404)

        ministry.name = data['name'] if 'name' in data else ministry.name
        db.session.commit()
        return make_response(jsonify({'message': 'Ministry updated successfully'}), 200)

    def delete(self, ministry_id):
        ministry = Ministry.query.filter_by(ministry_id=ministry_id).first()
        if not ministry:
            return make_response(jsonify({'message': 'Ministry not found'}), 404)

        db.session.delete(ministry)
        db.session.commit()
        return make_response(jsonify({'message': 'Ministry deleted successfully'}), 200)

# Civil Servant Routes
class CivilServants(Resource):
    def get(self):
        civil_servants = CivilServant.query.all()
        result = [cs.to_dict() for cs in civil_servants]
        return make_response(jsonify(result), 200)

    def post(self):
        data = request.get_json()
        civil_servant = CivilServant(
            user_id=data['user_id'],
            ministry_id=data['ministry_id'],
            role=data['role'],
            salary=data['salary'],
            allowance=data['allowance']
        )
        db.session.add(civil_servant)
        db.session.commit()
        return make_response(jsonify({'message': 'Civil Servant created successfully'}), 201)

class CivilServantByID(Resource):
    def get(self, civil_id):
        civil_servant = CivilServant.query.filter_by(civil_id=civil_id).first()
        if civil_servant:
            return make_response(jsonify(civil_servant.to_dict()), 200)
        else:
            return make_response(jsonify({'error': 'Civil Servant not found'}), 404)

    def put(self, civil_id):
        data = request.get_json()
        civil_servant = CivilServant.query.filter_by(civil_id=civil_id).first()
        if not civil_servant:
            return make_response(jsonify({'message': 'Civil Servant not found'}), 404)
        
        civil_servant.user_id = data['user_id'] if 'user_id' in data else civil_servant.user_id
        civil_servant.ministry_id = data['ministry_id'] if 'ministry_id' in data else civil_servant.ministry_id
        civil_servant.role = data['role'] if 'role' in data else civil_servant.role
        civil_servant.salary = data['salary'] if 'salary' in data else civil_servant.salary
        civil_servant.allowance = data['allowance'] if 'allowance' in data else civil_servant.allowance
        db.session.commit()
        return make_response(jsonify({'message': 'Civil Servant updated successfully'}), 200)

    def delete(self, civil_id):
        civil_servant = CivilServant.query.filter_by(civil_id=civil_id).first()
        if not civil_servant:
            return make_response(jsonify({'message': 'Civil Servant not found'}), 404)

        db.session.delete(civil_servant)
        db.session.commit()
        return make_response(jsonify({'message': 'Civil Servant deleted successfully'}), 200)

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
            project.ministry_id = data['ministry_id'] if'ministry_id' in data else project.ministry_id
            project.name = data['name'] if 'name' in data else project.name
            project.description = data['description'] if 'description' in data else project.description
            project.date = datetime.fromisoformat(data['date']) if 'date' in data else project.date
            project.status = data['status'] if'status' in data else project.status
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

api.add_resource(Tenders, '/tenders')
api.add_resource(TenderByID, '/tenders/<int:id>')
api.add_resource(Expenditures, '/expenditures')
api.add_resource(ExpenditureByID, '/expenditures/<int:id>')
api.add_resource(Ministries, '/ministries')
api.add_resource(MinistryByID, '/ministries/<int:ministry_id>')
api.add_resource(CivilServants, '/civil_servants')
api.add_resource(CivilServantByID, '/civil_servants/<int:civil_id>')
api.add_resource(Projects, '/projects')
api.add_resource(ProjectByID, '/projects/<int:project_id>')
api.add_resource(Budgets, '/budgets')
api.add_resource(BudgetByID, '/budgets/<int:budget_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)