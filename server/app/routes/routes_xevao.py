from flask import Blueprint, request, jsonify
from ..models import Xevao, db


xevao_bp = Blueprint('xevao', __name__)


@xevao_bp.route('/api/xevao/create', methods=['POST'])
def create_xevao():
    data = request.get_json()
    new_xevao = Xevao(
        bienso_XV=data['bienso_XV'],
        anh_XV=data['anh_XV'],
        thoigian_XV=data['thoigian_XV'],
        MSSV=data.get('MSSV'),
        ma_CC=data.get('ma_CC'),
        ma_BX=data.get('ma_BX')
    )
    if not Xevao.bienso_XV or not Xevao.anh_XV or not Xevao.thoigian_XV:
        return jsonify({'error': 'Missing required fields'}), 400

    db.session.add(new_xevao)
    db.session.commit()
    return jsonify(new_xevao.to_dict()), 201


@xevao_bp.route('/api/xevao', methods=['GET'])
def get_all_xevao():
    xevao_list = Xevao.query.all()
    return jsonify([xevao.to_dict() for xevao in xevao_list])


@xevao_bp.route('/api/xevao/<ma_XV>', methods=['GET'])
def get_xevao(ma_XV):
    xevao = Xevao.query.get_or_404(ma_XV)
    return jsonify(xevao.to_dict())


@xevao_bp.route('/api/xevao/<ma_XV>', methods=['PUT'])
def update_xevao(ma_XV):
    xevao = Xevao.query.get_or_404(ma_XV)
    data = request.get_json()

    xevao.anh_XV = data.get('anh_XV', xevao.anh_XV)
    xevao.bienso_XV = data.get('bienso_XV', xevao.bienso_XV)
    xevao.thoigian_XV = data.get('thoigian_XV', xevao.thoigian_XV)

    db.session.commit()
    return jsonify(xevao.to_dict())


@xevao_bp.route('/api/xevao/<ma_XV>', methods=['DELETE'])
def delete_xevao(ma_XV):
    xevao = Xevao.query.get_or_404(ma_XV)
    db.session.delete(xevao)
    db.session.commit()
    return '', 204
