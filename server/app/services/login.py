from flask import Flask, request, jsonify, Blueprint,current_app
from ..models import Taikhoan
from ..config import Config
import jwt
import datetime

auth = Blueprint('auth', __name__)

@auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    TenDangNhap_TK = data.get('TenDangNhap_TK')
    MatKhau_TK = data.get('MatKhau_TK')

    taikhoan = Taikhoan.query.filter_by(TenDangNhap_TK=TenDangNhap_TK).first()

    if not taikhoan or taikhoan.MatKhau_TK != MatKhau_TK:
        return jsonify({'error': 'Invalid credentials'}), 401

    token = jwt.encode({
        'ma_TK': taikhoan.ma_TK,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token, 'status': True,'PhanQuyen_TK': taikhoan.PhanQuyen_TK })