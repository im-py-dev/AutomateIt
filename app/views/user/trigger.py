from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Applet, Trigger
from app import db

trigger_bp = Blueprint('trigger', __name__, url_prefix='/api/trigger')


@trigger_bp.route('/', methods=['GET'])
@jwt_required()
def read_triggers():
    current_user_id = get_jwt_identity()
    applets = Applet.query.filter_by(user_id=current_user_id).all()
    trigger_list = []
    for applet in applets:
        for trigger in applet.triggers:
            trigger_list.append({
                'id': trigger.id,
                'name': trigger.name,
                'description': trigger.description,
                'applet_id': trigger.applet_id
            })
    return jsonify(trigger_list)


@trigger_bp.route('/<int:trigger_id>', methods=['GET'])
@jwt_required()
def read_trigger(trigger_id):
    current_user_id = get_jwt_identity()
    trigger = Trigger.query.join(Applet).filter(
        Trigger.id == trigger_id,
        Applet.user_id == current_user_id
    ).first_or_404()
    return jsonify({
        'id': trigger.id,
        'name': trigger.name,
        'description': trigger.description,
        'applet_id': trigger.applet_id
    })


@trigger_bp.route('/create', methods=['POST'])
@jwt_required()
def create_trigger():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    if 'name' not in data:
        return jsonify({'message': 'Trigger name is required'}), 400
    if 'applet_id' not in data:
        return jsonify({'message': 'Applet ID is required'}), 400
    applet = Applet.query.filter_by(id=data['applet_id'], user_id=current_user_id).first()
    if not applet:
        return jsonify({'message': 'Applet not found'}), 404
    trigger = Trigger(name=data['name'], description=data.get('description', ''), applet_id=applet.id)
    db.session.add(trigger)
    db.session.commit()
    return jsonify({'id': trigger.id, 'name': trigger.name}), 201


@trigger_bp.route('/<int:trigger_id>', methods=['PUT'])
@jwt_required()
def update_trigger(trigger_id):
    current_user_id = get_jwt_identity()
    trigger = Trigger.query.join(Applet).filter(
        Trigger.id == trigger_id,
        Applet.user_id == current_user_id
    ).first_or_404()
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    trigger.name = data.get('name', trigger.name)
    trigger.description = data.get('description', trigger.description)
    db.session.commit()
    return jsonify({'id': trigger.id, 'name': trigger.name}), 200


@trigger_bp.route('/<int:trigger_id>', methods=['DELETE'])
@jwt_required()
def delete_trigger(trigger_id):
    current_user_id = get_jwt_identity()
    trigger = Trigger.query.join(Applet).filter(
        Trigger.id == trigger_id,
        Applet.user_id == current_user_id
    ).first_or_404()
    db.session.delete(trigger)
    db.session.commit()
    return jsonify({'message': 'Trigger deleted successfully'}), 200
