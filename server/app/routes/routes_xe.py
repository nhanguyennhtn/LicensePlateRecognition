from flask import Blueprint, request, jsonify
from ..models import Thongtinxe, db

Thongtinxe_bp = Blueprint('thongtinxe', __name__ )
# tất cả xe
@Thongtinxe_bp.route('/api/admin/thongtinxe', methods=['GET'])
def get_thongtinxe():
    thongtinxe = Thongtinxe.query.all()
    return jsonify([xe.to_dict() for xe in thongtinxe])
# xe theo bienso_xe
@Thongtinxe_bp.route('/api/admin/thongtinxe/<string:bienso_xe>', methods=['GET'])
def get_thongtinxe_by_bienso(bienso_xe):
    thongtinxe = Thongtinxe.query.get(bienso_xe)
    if not thongtinxe:
        return jsonify({'error': 'Xe không tồn tại'}), 404

    return jsonify(thongtinxe.to_dict())
#tạo thongtinxe mới
@Thongtinxe_bp.route('/api/admin/thongtinxe', methods=['POST'])
def add_thongtinxe():
    data = request.json()
    if not data or not data.get('bienso_xe') or not data.get('ten_xe'):
        return jsonify({'error': 'Thiếu thông tin biển số hoặc tên xe'}), 400
    
    if Thongtinxe.query.get(data['bienso_xe']):
        return jsonify({'error': 'Biển số xe đã tồn tại'}), 409

    new_thongtinxe = Thongtinxe(
        bienso_xe=data['bienso_xe'],
        ten_xe=data['ten_xe'],
        anh_xe=data.get('anh_xe', '')
    )
    db.session.add(new_thongtinxe)
    db.session.commit()
    return jsonify(new_thongtinxe.to_dict()), 201

#update xe:id
@Thongtinxe_bp.route('/api/admin/thongtinxe/<string:bienso_xe>', methods=['PUT'])
def update_thongtinxe(bienso_xe):
    thongtinxe = Thongtinxe.query.get(bienso_xe)
    if not thongtinxe:
        return jsonify({'error': 'Xe không tồn tại'}), 404

    data = request.json
    if not data or not data.get('ten_xe'):
        return jsonify({'error': 'Thiếu thông tin tên xe'}), 400

    thongtinxe.ten_xe = data['ten_xe']
    thongtinxe.anh_xe = data.get('anh_xe', thongtinxe.anh_xe)
    db.session.commit()
    return jsonify(thongtinxe.to_dict())

@Thongtinxe_bp.route('/api/admin/thongtinxe/<string:bienso_xe>', methods=['DELETE'])
def delete_thongtinxe(bienso_xe):
    thongtinxe = Thongtinxe.query.get(bienso_xe)
    if not thongtinxe:
        return jsonify({'error': 'Xe không tồn tại'}), 404
    
    db.session.delete(thongtinxe)
    db.session.commit()
    return '', 204