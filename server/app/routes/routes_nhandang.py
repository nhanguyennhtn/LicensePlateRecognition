from flask import Blueprint, request, jsonify
from ..models import Nhandang, db

nhandang_bp = Blueprint('nhandang', __name__)

@nhandang_bp.route('/api/nhandang', methods=['GET'])
def get_nhandangs():
    nhandangs = Nhandang.query.all()
    return jsonify([nhandang.to_dict() for nhandang in nhandangs])

@nhandang_bp.route('/api/nhandang/<int:ma_ND>', methods=['GET'])
def get_nhandang(ma_ND):
    nhandang = Nhandang.query.get_or_404(ma_ND)
    return jsonify(nhandang.to_dict())

@nhandang_bp.route('/api/nhandang/create', methods=['POST'])
def create_nhandang():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        bienso_ND = data.get('bienso_ND')
        anh_ND = data.get('anh_ND', '')  # Nếu không có anh_ND, đặt giá trị mặc định là chuỗi rỗng

        if not bienso_ND:
            return jsonify({'error': 'bienso_ND is required'}), 400

        new_nhandang = Nhandang(bienso_ND=bienso_ND, anh_ND=anh_ND)
        db.session.add(new_nhandang)
        db.session.commit()
        return jsonify(new_nhandang.to_dict()), 201

    except Exception as e:
        return jsonify({'error': 'Failed to decode JSON object', 'message': str(e)}), 400

@nhandang_bp.route('/nhandang/<int:ma_ND>', methods=['PUT'])
def update_nhandang(ma_ND):
    data = request.get_json()
    nhandang = Nhandang.query.get_or_404(ma_ND)
    
    nhandang.anh_ND = data.get('anh_ND', nhandang.anh_ND)
    nhandang.bienso_ND = data.get('bienso_ND', nhandang.bienso_ND)
    
    db.session.commit()
    return jsonify(nhandang.to_dict())

@nhandang_bp.route('/nhandang/<int:ma_ND>', methods=['DELETE'])
def delete_nhandang(ma_ND):
    nhandang = Nhandang.query.get_or_404(ma_ND)
    db.session.delete(nhandang)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200

