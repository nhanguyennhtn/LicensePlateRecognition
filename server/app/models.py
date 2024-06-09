from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

db = SQLAlchemy()


class Taikhoan(db.Model):
    ma_TK = db.Column(db.String(10), unique=True, primary_key=True)
    TenDangNhap_TK = db.Column(db.String(80), unique=True, nullable=False)
    Email_TK = db.Column(db.String(80), unique=True, nullable=False)
    MatKhau_TK = db.Column(db.String(120), unique=True, nullable=False)
    PhanQuyen_TK = db.Column(
        Enum('admin', 'nhanvien', name='phanquyen_tk'), nullable=False)

    def __repr__(self):
        return f'<taikhoan {self.TenDangNhap_TK}>'


class Thongtinxe(db.Model):
    __tablename__ = 'thongtinxe'
    bienso_xe = db.Column(db.String(20), primary_key=True)
    ten_xe = db.Column(db.String(100), nullable=False)
    anh_xe = db.Column(db.TEXT)

    def __repr__(self):
        return f'<Thongtinxe {self.bienso_xe}>'

    def to_dict(self):
        return {
            'bienso_xe': self.bienso_xe,
            'ten_xe': self.ten_xe,
            'anh_xe': self.anh_xe,
        }


class Sinhvien(db.Model):
    MSSV = db.Column(db.String(10), unique=True, primary_key=True)
    hoten_SV = db.Column(db.String(100))
    sdt_SV = db.Column(db.String(50))
    ngaydangky = db.Column(db.String(80))
    ngayketthuc = db.Column(db.String(80))
    trangthai_SV = db.Column( Enum('choxacnhan','xacnhan', 'tuchoi', name='trangthai_SV'), nullable=False)

    bienso_xe = db.Column(db.String(80), db.ForeignKey('thongtinxe.bienso_xe'))

    def __repr__(self):
        return f'<sinhvien {self.hoten_SV}>'

    def to_dict(self):
        return {
            'MSSV': self.MSSV,
            'hoten_SV': self.hoten_SV,
            'sdt_SV': self.sdt_SV,
            'ngaydangky': self.ngaydangky,
            'ngayketthuc': self.ngayketthuc,
            'bienso_xe': self.bienso_xe,
        }


class Congchuc(db.Model):
    __tablename__ = 'congchuc'
    ma_CC = db.Column(db.String(10), primary_key=True)
    ten_CC = db.Column(db.String(100), nullable=False)
    sdt_CC = db.Column(db.String(20), nullable=False)
    chucvu_CC = db.Column(db.String(100))
    ngayBD_CC = db.Column(db.Date)

    bienso_xe = db.Column(db.String(20), db.ForeignKey('thongtinxe.bienso_xe'))

    def __repr__(self):
        return f'<congchuc {self.ten_CC}>'

    def to_dict(self):
        return {
            'ma_CC': self.ma_CC,
            'ten_CC': self.ten_CC,
            'sdt_CC': self.sdt_CC,
            'chucvu_CC': self.chucvu_CC,
            'ngayBD_CC': self.ngayBD_CC,
            'bienso_xe': self.bienso_xe,
        }


class Nguoidung(db.Model):
    ma_ND = db.Column(db.String(10), unique=True, primary_key=True)
    hoten_ND = db.Column(db.String(100), nullable=False)
    sdt_ND = db.Column(db.String(15))
    ma_TK = db.Column(db.String(10), db.ForeignKey(
        'taikhoan.ma_TK'), nullable=False)

    def __repr__(self):
        return f'<nguoidung {self.hoten_ND}>'

    def to_dict(self):
        return {
            'ma_ND': self.ma_ND,
            'hoten_ND': self.hoten_ND,
            'sdt_ND': self.sdt_ND,
            'ma_TK': self.ma_TK,
        }


class Baixe(db.Model):
    __tablename__ = 'baixe'

    ma_BX = db.Column(db.String(10), primary_key=True)
    ten_BX = db.Column(db.String(100), nullable=False, unique=True)
    vitri_BX = db.Column(db.String(100), nullable=False)
    ma_ND = db.Column(db.String(10), db.ForeignKey('nguoidung.ma_ND'))

    def __repr__(self):
        return f'<Baixe {self.ma_BX}>'

    def to_dict(self):
        return {
            'ma_BX': self.ma_BX,
            'ten_BX': self.ten_BX,
            'vitri_BX': self.vitri_BX,
            'ma_ND': self.ma_ND
        }


class Xevao(db.Model):
    __tablename__ = 'xevao'

    bienso_XV = db.Column(db.String(20), primary_key=True)
    anh_XV = db.Column(db.TEXT, nullable=False)
    thoigian_XV = db.Column(db.DateTime)
    MSSV = db.Column(db.String(10), db.ForeignKey('sinhvien.MSSV'))
    ma_CC = db.Column(db.String(10), db.ForeignKey('congchuc.ma_CC'))
    ma_BX = db.Column(db.String(10), db.ForeignKey('baixe.ma_BX'))

    def __repr__(self):
        return f'<Xevao {self.bienso_XV}>'

    def to_dict(self):
        return {
            'bienso_XV': self.bienso_XV,
            'anh_XV': self.anh_XV,
            'thoigian_XV': self.thoigian_XV.strftime('%Y-%m-%d %H:%M:%S') if self.thoigian_XV else None,
            'MSSV': self.MSSV if self.MSSV else None,
            'ma_CC': self.ma_CC if self.ma_CC else None,
            'ma_BX': self.ma_BX,
        }


class Nhandang(db.Model):
    bienso_ND = db.Column(db.String(20), primary_key=True)
    anh_ND = db.Column(db.TEXT)

    def __repr__(self):
        return f'<nhandang {self.ma_ND}>'

    def to_dict(self):
        return ({
            'bienso_ND': self.bienso_ND,
            'anh_ND': self.anh_ND,
        })
