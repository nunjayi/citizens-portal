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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///civil_servants.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

class CivilServant(db.Model):
    __tablename__ = 'civil_servant'
    civil_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    ministry_id = db.Column(db.Integer, db.ForeignKey('ministry.ministry_id'), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    allowance = db.Column(db.Float, nullable=False)

class Ministry(db.Model):
    __tablename__ = 'ministry'
    ministry_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    civil_servants = db.relationship('CivilServant', backref='ministry', lazy=True)

class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True)
    ministry_id = db.Column(db.Integer, db.ForeignKey('ministry.ministry_id'))
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
