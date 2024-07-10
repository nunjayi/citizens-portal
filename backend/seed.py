from app import app
from models import db, Tender, Expenditure

with app.app_context():
    db.create_all()

    tender1 = Tender(user_id=1, budget_id=1, description='Office Supplies', cost=500.00)
    tender2 = Tender(user_id=2, budget_id=1, description='Construction Materials', cost=1500.00)

    expenditure1 = Expenditure(budget_id=1, item='Printer Paper', amount=50.00)
    expenditure2 = Expenditure(budget_id=1, item='Cement', amount=1000.00)

    db.session.add_all([tender1, tender2, expenditure1, expenditure2])
    db.session.commit()
