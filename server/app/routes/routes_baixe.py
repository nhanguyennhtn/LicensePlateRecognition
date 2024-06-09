from flask import Blueprint, request, jsonify
from ..models import Baixe, db

baixe_bp = Blueprint('baixe', __name__)


@baixe_bp.route('/api/baixe/create', methods=['POST'])
def create_baixe():
    data = request.get_json()
    new_baixe = Baixe(
        ma_BX=data.get('ma_BX'),
        ten_BX=data.get('ten_BX'),
        vitri_BX=data.get('vitri_BX'),
        ma_ND=data.get('ma_ND')
    )

    if not ma_BX or not ten_BX or not vitri_BX:
        return jsonify({'error': 'Missing required fields'}), 400

    db.session.add(new_baixe)
    db.session.commit()
    return jsonify(new_baixe.to_dict()), 201


@baixe_bp.route('/api/baixe', methods=['GET'])
def get_all_baixe():
    baixe_list = Baixe.query.all()
    return jsonify([baixe.to_dict() for baixe in baixe_list]), 200


@baixe_bp.route('/api/baixe/<ma_BX>', methods=['GET'])
def get_baixe(ma_BX):
    baixe = Baixe.query.get(ma_BX)

    if baixe is None:
        return jsonify({'error': 'Baixe not found'}), 404

    return jsonify(baixe.to_dict()), 200


@baixe_bp.route('/api/baixe/<ma_BX>', methods=['PUT'])
def update_baixe(ma_BX):
    data = request.get_json()
    baixe = Baixe.query.get(ma_BX)
    if baixe is None:
        return jsonify({'error': 'Baixe not found'}), 404

    baixe.ten_BX = data.get('ten_BX', baixe.ten_BX)
    baixe.vitri_BX = data.get('vitri_BX', baixe.vitri_BX)
    baixe.ma_ND = data.get('ma_ND', baixe.ma_ND)

    db.session.commit()
    return jsonify(baixe.to_dict()), 200


@baixe_bp.route('/api/baixe/<ma_BX>', methods=['DELETE'])
def delete_baixe(ma_BX):
    baixe = Baixe.query.get(ma_BX)
    if baixe is None:
        return jsonify({'error': 'Baixe not found'}), 404

    db.session.delete(baixe)
    db.session.commit()
    return jsonify({'message': 'Baixe deleted successfully'}), 200
