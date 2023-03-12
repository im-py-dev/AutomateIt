from flask import Blueprint, render_template, redirect, url_for, request, flash, send_file, jsonify, abort
from flask_login import login_user, current_user, login_required, logout_user
from app import login_manager, db, bcrypt
from app.models import User, Applet
from app.forms import *
from sqlalchemy import or_
from flask_jwt_extended import jwt_required, get_jwt_identity


applet_bp = Blueprint('applet', __name__, url_prefix='/api/applet')


@applet_bp.route('/', methods=['GET'])
@jwt_required()
def read_applets():
    current_user_id = get_jwt_identity()
    applets = Applet.query.filter_by(user_id=current_user_id).all()
    applet_list = []
    for applet in applets:
        applet_list.append({
            'id': applet.id,
            'name': applet.name,
            'description': applet.description,
        })
    return jsonify(applet_list)


@applet_bp.route('/create', methods=['POST'])
@jwt_required()
def create_applet():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    if 'name' not in data:
        return jsonify({'message': 'Applet name is required'}), 400
    applet = Applet(user_id=current_user_id,
                    name=data['name'],
                    description=data.get('description', ''))
    db.session.add(applet)
    db.session.commit()
    return jsonify({'id': applet.id, 'name': applet.name}), 201


@applet_bp.route('/<int:applet_id>', methods=['GET'])
@jwt_required()
def read_applet(applet_id):
    current_user_id = get_jwt_identity()
    applet = Applet.query.filter_by(id=applet_id, user_id=current_user_id).first_or_404()
    applet_data = {
        'id': applet.id,
        'name': applet.name,
        'description': applet.description,
    }
    return jsonify(applet_data)


@applet_bp.route('/<int:applet_id>', methods=['PUT'])
@jwt_required()
def update_applet(applet_id):
    current_user_id = get_jwt_identity()
    applet = Applet.query.filter_by(id=applet_id, user_id=current_user_id).first_or_404()
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    applet.name = data.get('name', applet.name)
    applet.description = data.get('description', applet.description)
    db.session.commit()
    return jsonify({'id': applet.id, 'name': applet.name}), 200


@applet_bp.route('/<int:applet_id>', methods=['DELETE'])
@jwt_required()
def delete_applet(applet_id):
    current_user_id = get_jwt_identity()
    applet = Applet.query.filter_by(id=applet_id, user_id=current_user_id).first_or_404()
    db.session.delete(applet)
    db.session.commit()
    return jsonify({'message': 'Applet deleted successfully'}), 200
