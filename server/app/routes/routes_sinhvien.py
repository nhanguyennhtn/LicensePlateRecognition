from flask import Blueprint, request, jsonify
from ..models import Sinhvien, db

sinhvien_bp = Blueprint('sinhvien', __name__)


@sinhvien_bp.route('/api/admin/sinhvien', methods=['GET'])
def get_sinhvien():
    sinhviens = Sinhvien.query.all()
    return jsonify([sv.to_dict() for sv in sinhviens] )

# @sinhvien_bp.route('/api/admin/sinhvien/id', methods=['GET'])