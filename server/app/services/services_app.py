from flask import Blueprint, jsonify, request
from datetime import datetime
from ..models import Nhandang, Sinhvien, Congchuc, db, Thongtinxe

services_bp = Blueprint('services', __name__)

@services_bp.route('/api/search_by_plate', methods=['GET'])
def search_by_plate():
    bienso_ND = request.args.get('bienso_ND')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 

    sinhvien = Sinhvien.query.filter_by(bienso_xe=bienso_ND).first()
    if sinhvien:
        thongtinxe = Thongtinxe.query.filter_by(bienso_xe=sinhvien.bienso_xe).first()
        return jsonify({
            'chucvu': 'sinhvien',
            'biensoxe': sinhvien.bienso_xe,
            'MSSV': sinhvien.MSSV if sinhvien else None,
            'congchuc': None,
            'ten': sinhvien.hoten_SV,
            'anh_xe': thongtinxe.anh_xe if thongtinxe else None,
            'thoigian': current_time,
        })

    congchuc = Congchuc.query.filter_by(bienso_xe=bienso_ND).first()
    if congchuc:
        thongtinxe = Thongtinxe.query.filter_by(bienso_xe=congchuc.bienso_xe).first()
        return jsonify({
            'chucvu': congchuc.chucvu_CC,
            'biensoxe': congchuc.bienso_xe,
            'MSSV': None,
            'congchuc': congchuc.ma_CC if congchuc else None,
            'ten': congchuc.ten_CC,
            'anh_xe': thongtinxe.anh_xe if thongtinxe else None,
            'thoigian': current_time,
        })

    nhandang = Nhandang.query.filter_by(bienso_ND=bienso_ND).first()
    if nhandang:
        return jsonify({
            'chucvu': 'khach',
            'biensoxe': nhandang.bienso_ND,
            'MSSV': None,
            'congchuc': None,
            'anh_xe': None,
            'thoigian': current_time,
            # **nhandang.to_dict()
        })

    return jsonify({
            'chucvu': 'khach',
            'biensoxe': None,
            'MSSV': None,
            'congchuc': None,
            'anh_xe': None,
            'thoigian': current_time,
        })