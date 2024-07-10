from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Float, MetaData
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
    app = Flask(_name_)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

class Tender(db.Model):
    _tablename_ = 'tenders'

    tender_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    budget_id = Column(Integer, ForeignKey('budgets.budget_id'), nullable=False)
    description = Column(String, nullable=False)
    cost = Column(Float, nullable=False)

    def to_dict(self):
        return {
            'tender_id': self.tender_id,
            'user_id': self.user_id,
            'budget_id': self.budget_id,
            'description': self.description,
            'cost': self.cost
        }

class Expenditure(db.Model):
    _tablename_ = 'expenditures'

    expenditure_id = Column(Integer, primary_key=True)
    budget_id = Column(Integer, ForeignKey('budgets.budget_id'), nullable=False)
    item = Column(String, nullable=False)
    amount = Column(Float, nullable=False)

    def to_dict(self):
        return {
            'expenditure_id': self.expenditure_id,
            'budget_id': self.budget_id,
            'item': self.item,
            'amount': self.amount
        }

class CivilServant(db.Model):
    _tablename_ = 'civil_servant'
    civil_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    ministry_id = db.Column(db.Integer, db.ForeignKey('ministry.ministry_id'), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    allowance = db.Column(db.Float, nullable=False)

class Ministry(db.Model):
    _tablename_ = 'ministry'
    ministry_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    civil_servants = db.relationship('CivilServant', backref='ministry', lazy=True)

class Project(db.Model):
    _tablename_ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True)
    ministry_id = db.Column(db.Integer, db.ForeignKey('ministry.ministry_id'))
    name = db.Column(db.String)
    description = db.Column(db.String(80))
    date = db.Column(db.DateTime)
    status = db.Column(db.String)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.budget_id'))

    budget = db.relationship('Budget', backref='projects', cascade='all')

    def _repr_(self):
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
    _tablename_ = 'budgets'

    budget_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)

    def _repr_(self):
        return f'<Ksh {self.amount}>'
    
    def to_dict(self):
        return {
            'budget_id': self.budget_id,
            'amount': f'Ksh {self.amount}'
        }