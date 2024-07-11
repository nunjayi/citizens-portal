from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime

# Contains definitions of tables and associated schema constructs
metadata = MetaData(
    naming_convention={
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s'
    }
)

# Create the Flask SQLAlchemy extension
db = SQLAlchemy(metadata=metadata)

def create_app():
    # Initialize the Flask application
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

class Ministry(db.Model):
    __tablename__ = 'ministries'
    ministry_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Ministry {self.name}>'
    
    def to_dict(self):
        return {
            'ministry_id': self.ministry_id,
            'name': self.name
        }
    
class CivilServant(db.Model):
    __tablename__ = 'civil_servants'
    civil_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    ministry_id = db.Column(db.Integer, db.ForeignKey('ministries.ministry_id'), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    allowance = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<CivilServant {self.role} | Ministry {self.ministry_id}>'
    
    def to_dict(self):
        return {
            'civil_id': self.civil_id,
            'user_id': self.user_id,
            'ministry_id': self.ministry_id,
            'role': self.role,
            'salary': f'KSh {self.salary}',
            'allowance': f'Ksh {self.allowance}'
        }

class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True)
    ministry_id = db.Column(db.Integer, db.ForeignKey('ministries.ministry_id'))
    name = db.Column(db.String)
    description = db.Column(db.String(80))
    date = db.Column(db.DateTime)
    status = db.Column(db.String)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.budget_id'))

    budget = db.relationship('Budget', backref='projects', cascade='all')

    def __repr__(self):
        return f'<Project {self.name} |Ministry {self.ministry_id}>'
    
    def to_dict(self):
        return {
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'date': self.date.isoformat(),
            'status': self.status,
            'budget_id': self.budget_id
        }

class Budget(db.Model):
    __tablename__ = 'budgets'

    budget_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)

    def __repr__(self):
        return f'<Ksh {self.amount}>'
    
    def to_dict(self):
        return {
            'budget_id': self.budget_id,
            'amount': f'Ksh {self.amount}'
        }
    
class Expenditure(db.Model):
    __tablename__ = 'expenditures'

    expenditure_id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.budget_id'), nullable=False)
    item = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<Expenditure {self.expenditure_id}>'

    def to_dict(self):
        return {
            'expenditure_id': self.expenditure_id,
            'budget_id': self.budget_id,
            'item': self.item,
            'amount': f'Ksh {self.amount}'
        }

class Tender(db.Model):
    __tablename__ = 'tenders'

    tender_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('civil_servants.user_id'), nullable=False)
    expenditure_id = db.Column(db.Integer, db.ForeignKey('expenditures.expenditure_id'), nullable=False)
    description = db.Column(db.String, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Tender {self.tender_id}>'

    def to_dict(self):
        return {
            'tender_id': self.tender_id,
            'user_id': self.user_id,
            'expenditure_id': self.expenditure_id,
            'description': self.description,
            'cost': f'Ksh {self.cost}'
        }
