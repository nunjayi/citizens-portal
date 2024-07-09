# routes.py

from flask import request, jsonify
from models import db, CivilServant, Ministry, create_app

app = create_app()

@app.route('/ministries', methods=['POST'])
def create_ministry():
    name = request.json['name']
    ministry = Ministry(name=name)
    db.session.add(ministry)
    db.session.commit()
    return jsonify({'message': 'Ministry created successfully'}), 201

@app.route('/ministries', methods=['GET'])
def get_ministries():
    ministries = Ministry.query.all()
    return jsonify([{'ministry_id': m.ministry_id, 'name': m.name} for m in ministries])

@app.route('/civil_servants', methods=['POST'])
def create_civil_servant():
    data = request.json
    civil_servant = CivilServant(
        user_id=data['user_id'],
        ministry_id=data['ministry_id'],
        role=data['role'],
        salary=data['salary'],
        allowance=data['allowance']
    )
    db.session.add(civil_servant)
    db.session.commit()
    return jsonify({'message': 'Civil Servant created successfully'}), 201

@app.route('/civil_servants', methods=['GET'])
def get_civil_servants():
    civil_servants = CivilServant.query.all()
    return jsonify([{
        'civil_id': cs.civil_id,
        'user_id': cs.user_id,
        'ministry_id': cs.ministry_id,
        'role': cs.role,
        'salary': cs.salary,
        'allowance': cs.allowance
    } for cs in civil_servants])

@app.route('/civil_servants/<int:civil_id>', methods=['PUT'])
def update_civil_servant(civil_id):
    data = request.json
    civil_servant = CivilServant.query.get(civil_id)
    if not civil_servant:
        return jsonify({'message': 'Civil Servant not found'}), 404
    
    civil_servant.user_id = data['user_id']
    civil_servant.ministry_id = data['ministry_id']
    civil_servant.role = data['role']
    civil_servant.salary = data['salary']
    civil_servant.allowance = data['allowance']
    db.session.commit()
    return jsonify({'message': 'Civil Servant updated successfully'})

@app.route('/civil_servants/<int:civil_id>', methods=['DELETE'])
def delete_civil_servant(civil_id):
    civil_servant = CivilServant.query.get(civil_id)
    if not civil_servant:
        return jsonify({'message': 'Civil Servant not found'}), 404

    db.session.delete(civil_servant)
    db.session.commit()
    return jsonify({'message': 'Civil Servant deleted successfully'})
