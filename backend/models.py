#backend/models.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime
from flask_bcrypt import bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

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

class Citizen(db.Model):
    __tablename__ = 'citizens'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    _password_hash = db.Column(db.String(100), nullable=False)

    civil_servants = db.relationship('CivilServant', backref='citizen', cascade='all, delete')
    tenders = db.relationship('Tender', backref='citizen', cascade='all, delete')

    def __repr__(self):
        return f'<Citizen {self.name}>'
    
    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    
    def to_dict(self):
        return {
            'user_id': self.id,
            'name': self.name,
            '_password_hash': self._password_hash,
        }

class Ministry(db.Model):
    __tablename__ = 'ministries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    amount = db.Column(db.Float)

    civil_servants = db.relationship('CivilServant', backref='ministry', cascade='all, delete')
    projects = db.relationship('Project', backref='ministry', cascade='all, delete')

    def __repr__(self):
        return f'<Ministry {self.name}>'
    
    def to_dict(self):
        return {
            'ministry_id': self.id,
            'name': self.name,
            'amount': f'Ksh {self.amount}'
        }
    
class CivilServant(db.Model):
    __tablename__ = 'civil_servants'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('citizens.id'), nullable=False)
    ministry_id = db.Column(db.Integer, db.ForeignKey('ministries.id'), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    allowance = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<CivilServant {self.role} | Ministry {self.ministry_id}>'
    
    def to_dict(self):
        return {
            'civil_id': self.id,
            'user_id': self.user_id,
            'ministry_id': self.ministry_id,
            'role': self.role,
            'salary': f'KSh {self.salary}',
            'allowance': f'Ksh {self.allowance}'
        }

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    ministry_id = db.Column(db.Integer, db.ForeignKey('ministries.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String(80), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String, nullable=False)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=False)

    def __repr__(self):
        return f'<Project {self.name} |Ministry {self.ministry_id}>'
    
    def to_dict(self):
        project_dict = {
            'project_id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'status': self.status,
            'budget_id': self.budget_id
        }

        if self.status != 'Complete':
            project_dict['end_date'] = None
        else:
            project_dict['end_date'] = self.end_date.isoformat()

        return project_dict

class Budget(db.Model):
    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    projects = db.relationship('Project', backref='budget', cascade='all')

    def __repr__(self):
        return f'<Ksh {self.amount}>'
    
    def to_dict(self):
        return {
            'budget_id': self.id,
            'amount': f'Ksh {self.amount}'
        }
    
class Expenditure(db.Model):
    __tablename__ = 'expenditures'

    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=False)
    item = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    tenders = db.relationship('Tender', backref='expenditure', cascade='all, delete')
    
    def __repr__(self):
        return f'<Expenditure {self.expenditure_id}>'

    def to_dict(self):
        return {
            'expenditure_id': self.id,
            'budget_id': self.budget_id,
            'item': self.item,
            'amount': f'Ksh {self.amount}'
        }

class Tender(db.Model):
    __tablename__ = 'tenders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('citizens.id'), nullable=False)
    expenditure_id = db.Column(db.Integer, db.ForeignKey('expenditures.id'), nullable=False)
    description = db.Column(db.String, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Tender {self.tender_id}>'

    def to_dict(self):
        return {
            'tender_id': self.id,
            'user_id': self.user_id,
            'expenditure_id': self.expenditure_id,
            'description': self.description,
            'cost': f'Ksh {self.cost}'
        }
