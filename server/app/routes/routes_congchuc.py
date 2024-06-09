from flask import Blueprint, request, jsonify
from ..models import Congchuc, db


congchuc_bp = Blueprint('congchuc', __name__)

@congchuc_bp.route('/api/admin/congchuc', methods=['GET'])
def get_congchuc():
    congchuc_list = Congchuc.query.all()
    return jsonify([congchuc.to_dict() for congchuc in congchuc_list]), 200

@congchuc_bp.route('/api/admin/congchuc/<ma_CC>', methods=['GET'])
def get_congchuc_detail(ma_CC):
    congchuc = Congchuc.query.get_or_404(ma_CC)
    return jsonify(congchuc.to_dict()), 200

@congchuc_bp.route('/api/admin/congchuc/<ma_CC>', methods=['PUT'])
def update_congchuc(ma_CC):
    data = request.get_json()
    congchuc = Congchuc.query.get_or_404(ma_CC)

    congchuc.ten_CC = data.get('ten_CC', congchuc.ten_CC)
    congchuc.sdt_CC = data.get('sdt_CC', congchuc.sdt_CC)
    congchuc.chucvu_CC = data.get('chucvu_CC', congchuc.chucvu_CC)
    if data.get('ngayBD_CC'):
        congchuc.ngayBD_CC = datetime.datetime.strptime(data['ngayBD_CC'], '%Y-%m-%d').date()
    congchuc.bienso_xe = data.get('bienso_xe', congchuc.bienso_xe)

    db.session.commit()
    return jsonify(congchuc.to_dict()), 200

@congchuc_bp.route('/api/admin/congchuc/<ma_CC>', methods=['DELETE'])
def delete_congchuc(ma_CC):
    congchuc = Congchuc.query.get_or_404(ma_CC)
    db.session.delete(congchuc)
    db.session.commit()
    return '', 204