# app.py
from flask import Flask
from app.config import Config
from app.models import *
from app.routes.routes_taikhoan import taikhoan_bp
from app.routes.routes_sinhvien import sinhvien_bp
from app.routes.routes_congchuc import congchuc_bp
from app.routes.routes_xevao import xevao_bp
from app.routes.routes_xe import Thongtinxe_bp
from app.routes.routes_nhandang import nhandang_bp
from app.routes.routes_baixe import baixe_bp
from app.routes.routes_webcam import webcam_bp
from app.services.login import auth
from app.services.services_app import services_bp
from flask_cors import CORS


app = Flask(__name__)
app.config['SECRET_KEY'] = 'nhanguyen'
app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(taikhoan_bp)
app.register_blueprint(sinhvien_bp)
app.register_blueprint(congchuc_bp)
app.register_blueprint(xevao_bp)
app.register_blueprint(Thongtinxe_bp)
app.register_blueprint(nhandang_bp)
app.register_blueprint(baixe_bp)
app.register_blueprint(webcam_bp)
app.register_blueprint(auth)
app.register_blueprint(services_bp)
CORS(app)

# @app.route('/',methods=['GET'])
# def index():
#     return 'hiiii'

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)