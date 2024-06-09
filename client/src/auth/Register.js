import { Link } from "react-router-dom";
import '../assets/scss/register.scss';
import FileBase64 from 'react-file-base64'
import React, { useState } from 'react';
import axios from 'axios';


export default function Register() {
    const [form, setForm] = useState({})
    const [error, setError] = useState('')
    const [select, setSelect] = useState('sinhvien')
    const [image, setImage] = useState(null)


    const handleChange = (e) => {
        const { name, value } = e.target;
        form.anh_xe = image
        if (name === 'ngayketthuc') {
            const today = new Date().toISOString().split('T')[0]
            if (value < today) {
                return setError('Ngày kết thúc phải lớn hơn hoặc bằng ngày hiện tại.')
            }
        }
        setForm({ ...form, [name]: value });
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        axios.post('http://localhost:5000/api/taikhoan/create', form)
            .then(response => {
                console.log('Xevao added successfully:', response.data)
            })
            .catch(error => {
                console.error('Error adding Xevao:', error);
            });

    }
    // console.log(image);
    return (
        <div className="wrapper">
            <div className="container main">
                <div className="row " style={{ width: 500 + 'px' }}>
                    <div className="card">
                        <div className="">
                            <div className="card-block align-items-center">
                                <h2 className=" card-header border-0 text-center mb-3 bg-white ">Đăng ký!</h2>
                                <div className="card-body border-0 pt-0">
                                    <div className="row justify-content-center">
                                        <div class="form-group p-1 ms-4">
                                            <select value={select} onChange={(e) => setSelect(e.target.value)}>
                                                <option value={'sinhvien'}>Sinh viên</option>
                                                <option value={'congchuc'}>Cán bộ</option>
                                            </select>
                                        </div>

                                        {select === "sinhvien" ?
                                            <form className='mt-3 form-login' onSubmit={handleSubmit}>
                                                <div class="form-group p-1">
                                                    <input className='p-2 w-100' type="text" name="TenDangNhap_TK" value={form.TenDangNhap_TK} onChange={handleChange} placeholder="Tên đăng nhập" required />
                                                </div>
                                                <div class="form-group p-1">
                                                    <input className='p-2 w-100' type="email" name="Email_TK" value={form.Email_TK} onChange={handleChange} placeholder="Địa chỉ Email" required />
                                                </div>
                                                <div class="form-group p-1">
                                                    <input className='p-2 w-100 mb-1' type="password" name="MatKhau_TK" value={form.MatKhau_TK} onChange={handleChange} placeholder="Mật khẩu" required />
                                                </div>
                                                <div class="form-group p-1 d-flex gap-2">
                                                    <input className='p-2 w-100 mb-1' type="text" name="hoten_SV" value={form.hoten_SV} onChange={handleChange} placeholder="Họ tên sinh viên" required />
                                                    <input className='p-2 w-100 mb-1' type="text" name="MSSV" value={form.MSSV} onChange={handleChange} placeholder="Mã số sinh viên" required />
                                                </div>
                                                <div class="form-group p-1">
                                                    <input className='p-2 w-100 mb-1' type="text" name="sdt_SV" value={form.sdt_SV} onChange={handleChange} placeholder="Số điện thoại" required />
                                                </div>
                                                <div class="form-group p-1 d-flex gap-2">
                                                    <input className='p-2 w-100 mb-1' type="date" name="ngaydangky" value={form.ngaydangky} onChange={handleChange} placeholder="Đăng ký ngày" required />
                                                    <input className='p-2 w-100 mb-1' type="date" name="ngayketthuc" value={form.ngayketthuc} onChange={handleChange} placeholder="Kết thúc ngày" required />
                                                </div>
                                                <div class="form-group p-1 d-flex gap-2">
                                                    <input className='p-2 w-100 mb-1' type="text" name="bienso_xe" value={form.bienso_xe} onChange={handleChange} placeholder="Biển số xe" required />
                                                    <input className='p-2 w-100 mb-1' type="text" name="ten_xe" value={form.ten_xe} onChange={handleChange} placeholder="Tên xe" required />
                                                </div>
                                                <div class="form-group p-1 ">
                                                    <FileBase64
                                                        multiple={false}
                                                        onDone={({ base64 }) => {
                                                            setImage(base64)
                                                        }}
                                                    />
                                                    {/* <input className='p-2 w-100 mb-1' type="file" accept="image/*" name="anh_xe" value={form.anh_xe} onChange={handleChange} placeholder="ảnh xe" required /> */}
                                                    {image && <img src={image} alt="Preview" style={{ width: '200px' }} />}
                                                </div>
                                                <div class="form-group pb-0 mt-1">
                                                    <span className="ps-2">Bạn chưa có tài khoản? <Link to={'/login'}>Đăng nhập</Link></span>
                                                </div>
                                                <div className="row mt-1 px-3">
                                                    <button type="submit" className="btn btn-primary btn-block mt-3"> Đăng ký</button>
                                                </div>
                                                <div class="form-group pb-0 mt-1">
                                                    <div className='ps-2 text-center'> {error && <p style={{ color: 'red' }}>{error}</p>}</div>
                                                </div>
                                            </form>
                                            :
                                            <form className='mt-3 form-login' onSubmit={handleSubmit}>
                                                <div class="form-group p-1">
                                                    <input className='p-2 w-100' type="text" name="ten_CC" value={form.ten_CC} onChange={(e) => e.target} placeholder="Tên cán bộ" required />
                                                </div>
                                                <div class="form-group p-1">
                                                    <input className='p-2 w-100 mb-1' type="password" name="MatKhau_TK" value={form.MatKhau_TK} onChange={handleChange} placeholder="Mật khẩu" required />
                                                </div>
                                                <div class="form-group p-1 d-flex gap-2">
                                                    <input className='p-2 w-100 mb-1' type="text" name="ten_CC" value={form.MSSV} onChange={handleChange} placeholder="Họ tên cán bộ" required />
                                                    <input className='p-2 w-100 mb-1' type="text" name="ma_CC" value={form.MSSV} onChange={handleChange} placeholder="Mã số cán bộ" required />
                                                </div>
                                                <div class="form-group p-1">
                                                    <input className='p-2 w-100 mb-1 ' type="text" name="sdt_CC" value={form.sdt_CC} onChange={handleChange} placeholder="số điện thoại" required />
                                                </div>
                                                <div class="form-group pb-0 mt-1">
                                                    <span className="ps-2">Bạn chưa có tài khoản? <Link to={'/login'}>Đăng nhập</Link></span>
                                                </div>
                                                <div className="row mt-1 px-3">
                                                    <button type="submit" className="btn btn-primary btn-block mt-3"> Đăng ký</button>
                                                </div>
                                                <div class="form-group pb-0 mt-1">
                                                    <div className='ps-2 text-center'> {error && <p style={{ color: 'red' }}>{error}</p>}</div>
                                                </div>
                                            </form>
                                        }

                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    )
}