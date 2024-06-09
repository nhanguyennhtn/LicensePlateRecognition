from flask import Blueprint, request, jsonify
from ..models import Taikhoan, db, Sinhvien, Congchuc
# Tạo một blueprint cho routes
taikhoan_bp = Blueprint('taikhoan', __name__)

# API tạo tài khoản mới


@taikhoan_bp.route('/api/taikhoan/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    ma_TK = data.get('ma_TK')
    TenDangNhap_TK = data.get('TenDangNhap_TK')
    Email_TK = data.get('Email_TK')
    MatKhau_TK = data.get('MatKhau_TK')
    PhanQuyen_TK = data.get('PhanQuyen_TK', 'nhanvien')

    if not all([ma_TK, TenDangNhap_TK, Email_TK, MatKhau_TK]):
        return jsonify({'error': 'Missing required fields'}), 400

    if Taikhoan.query.filter_by(TenDangNhap_TK=TenDangNhap_TK).first():
        return jsonify({'error': 'Username already exists'}), 409

    if Taikhoan.query.filter_by(Email_TK=Email_TK).first():
        return jsonify({'error': 'Email already exists'}), 409

    new_user = Taikhoan(
        ma_TK=ma_TK,
        TenDangNhap_TK=TenDangNhap_TK,
        Email_TK=Email_TK,
        MatKhau_TK=MatKhau_TK,
        PhanQuyen_TK=PhanQuyen_TK
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# API lấy danh sách tất cả tài khoản


@taikhoan_bp.route('/api/taikhoan', methods=['GET'])
def get_all_taikhoan():
    taikhoans = Taikhoan.query.all()
    result = [{'ma_TK': taikhoan.ma_TK, 'TenDangNhap_TK': taikhoan.TenDangNhap_TK,
               'Email_TK': taikhoan.Email_TK, 'MatKhau_TK': taikhoan.MatKhau_TK,
               'PhanQuyen_TK': taikhoan.PhanQuyen_TK} for taikhoan in taikhoans]
    return jsonify(result), 200

# API lấy chi tiết tài khoản bằng ID


@taikhoan_bp.route('/api/taikhoan/<ma_TK>', methods=['GET'])
def get_taikhoan_by_id(ma_TK):
    taikhoan = Taikhoan.query.get(ma_TK)
    if taikhoan:
        return jsonify({'ma_TK': taikhoan.ma_TK, 'TenDangNhap_TK': taikhoan.TenDangNhap_TK,
                        'Email_TK': taikhoan.Email_TK, 'MatKhau_TK': taikhoan.MatKhau_TK,
                        'PhanQuyen_TK': taikhoan.PhanQuyen_TK}), 200
    else:
        return jsonify({'message': 'Không tìm thấy tài khoản'}), 404

# API cập nhật thông tin tài khoản


@taikhoan_bp.route('/api/taikhoan/update/<ma_TK>', methods=['PUT'])
def update_taikhoan(ma_TK):
    # data = request.json
    # taikhoan = Taikhoan.query.get(ma_TK)
    # if taikhoan:
    #     for key, value in data.items():
    #         setattr(taikhoan, key, value)
    #     db.session.commit()
    #     return jsonify({'message': 'Cập nhật thông tin tài khoản thành công'}), 200
    # else:
    #     return jsonify({'message': 'Không tìm thấy tài khoản'}), 404
    data = request.get_json()
    taikhoan = Taikhoan.query.filter_by(ma_TK=ma_TK).first()

    if not taikhoan:
        return jsonify({'error': 'Taikhoan not found'}), 404

    taikhoan.Email_TK = data.get('Email_TK', taikhoan.Email_TK)
    taikhoan.MatKhau_TK = data.get('MatKhau_TK', taikhoan.MatKhau_TK)
    taikhoan.PhanQuyen_TK = data.get('PhanQuyen_TK', taikhoan.PhanQuyen_TK)

    db.session.commit()
    return jsonify({'message': 'Taikhoan updated successfully'}), 200

# API xóa tài khoản


@taikhoan_bp.route('/api/taikhoan/<ma_TK>', methods=['DELETE'])
def delete_taikhoan(ma_TK):
    taikhoan = Taikhoan.query.filter_by(ma_TK=ma_TK).first()

    if not taikhoan:
        return jsonify({'error': 'Taikhoan not found'}), 404

    db.session.delete(taikhoan)
    db.session.commit()
    return jsonify({'message': 'Taikhoan deleted successfully'}), 200


@taikhoan_bp.route('/api/admin/list-info', methods=['GET'])
def get_info():
    # Lấy danh sách sinh viên
    sinhvien_list = Sinhvien.query.all()
    sinhvien_data = [sv.to_dict() for sv in sinhvien_list]

    # Lấy danh sách cong chuc
    congchuc_list = Congchuc.query.all()
    congchuc_data = [cc.to_dict() for cc in congchuc_list]

    return jsonify({
        'sinhvien': sinhvien_data,
        'congchuc': congchuc_data
    })


@taikhoan_bp.route('/api/admin/list-customers', methods=['GET'])
def get_list_customers():
    sinhvien_list = Sinhvien.query.all()
    conchuc_list = Congchuc.query.all()
    sinhvien_congchuc_list = db.session.query(Sinhvien.hoten_SV.label('ten'), Sinhvien.sdt_SV.label('sdt'), Sinhvien.bienso_xe)\
        .union_all(db.session.query(Congchuc.ten_CC.label('ten'), Congchuc.sdt_CC.label('sdt'), Congchuc.bienso_xe))\
        .all()

    info_list = [{'ten': info.ten, 'sdt': info.sdt, 'bienso_xe': info.bienso_xe}
                 for info in sinhvien_congchuc_list]

    return jsonify(info_list)
