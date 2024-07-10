from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Float

db = SQLAlchemy()

class Tender(db.Model):
    __tablename__ = 'tenders'

    tender_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    budget_id = Column(Integer, ForeignKey('budgets.id'), nullable=False)
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
    __tablename__ = 'expenditures'

    expenditure_id = Column(Integer, primary_key=True)
    budget_id = Column(Integer, ForeignKey('budgets.id'), nullable=False)
    item = Column(String, nullable=False)
    amount = Column(Float, nullable=False)

    def to_dict(self):
        return {
            'expenditure_id': self.expenditure_id,
            'budget_id': self.budget_id,
            'item': self.item,
            'amount': self.amount
        }
