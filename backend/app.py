from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Tender, Expenditure

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

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

if __name__ == '__main__':
    app.run(port=5555, debug=True)
